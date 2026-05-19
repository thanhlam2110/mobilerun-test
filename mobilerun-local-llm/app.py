"""
mobilerun-local-llm/app.py

Run MobileRun from Python SDK using a local Ollama model.

Default model:
    qwen3.5:4b

Example:
    python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug

Prerequisites:
    1. pip install -r requirements.txt
    2. ollama serve
    3. ollama pull qwen3.5:4b
    4. mobilerun setup
    5. mobilerun ping
"""

from __future__ import annotations

import argparse
import asyncio
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def import_mobilerun() -> tuple[Any, Any]:
    """Import MobileRun classes with fallback paths across versions."""
    try:
        from mobilerun import MobileAgent, MobileConfig  # type: ignore
        return MobileAgent, MobileConfig
    except Exception:
        from mobilerun import MobileAgent  # type: ignore
        from mobilerun.config_manager import MobileConfig  # type: ignore
        return MobileAgent, MobileConfig


def run_shell(command: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    """Run a shell command and capture stdout/stderr."""
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def check_ollama(base_url: str, model: str) -> None:
    """Check that Ollama is reachable. Warn if the model is not listed."""
    tags_url = base_url.rstrip("/") + "/api/tags"

    try:
        with urllib.request.urlopen(tags_url, timeout=5) as response:
            payload = response.read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {base_url}.\n"
            "Start Ollama first, for example:\n"
            "  ollama serve\n\n"
            f"Original error: {exc}"
        ) from exc

    if model not in payload:
        print(
            f"WARNING: Ollama is running, but model `{model}` was not found in /api/tags.\n"
            f"Run this first:\n  ollama pull {model}\n",
            file=sys.stderr,
        )


def precheck_environment(base_url: str, model: str) -> None:
    """Run lightweight checks before starting the MobileRun SDK."""
    check_ollama(base_url=base_url, model=model)

    if shutil.which("adb") is None:
        raise RuntimeError("adb was not found in PATH. Install Android Platform Tools first.")

    adb = run_shell(["adb", "devices"])
    if adb.returncode != 0:
        raise RuntimeError(f"adb devices failed:\n{adb.stderr}")

    if "\tdevice" not in adb.stdout:
        raise RuntimeError(
            "No authorized Android device found.\n"
            "Run `adb devices`, then allow USB debugging on the phone."
        )

    # Optional but useful: if mobilerun CLI exists, verify Portal readiness.
    if shutil.which("mobilerun"):
        ping = run_shell(["mobilerun", "ping"], timeout=60)
        if ping.returncode != 0:
            raise RuntimeError(
                "mobilerun ping failed. Run `mobilerun setup` first.\n\n"
                f"STDOUT:\n{ping.stdout}\n\nSTDERR:\n{ping.stderr}"
            )


def patch_profile_base_url(config: Any, base_url: str) -> None:
    """
    Best-effort update of Ollama base_url in MobileConfig.llm_profiles.

    This handles both dict-based and object-based profile representations.
    """
    profiles = getattr(config, "llm_profiles", None)
    if not profiles:
        return

    profile_names = ("manager", "executor", "fast_agent", "app_opener", "structured_output")

    for name in profile_names:
        profile = None
        if isinstance(profiles, dict):
            profile = profiles.get(name)
        else:
            profile = getattr(profiles, name, None)

        if profile is None:
            continue

        if isinstance(profile, dict):
            kwargs = profile.setdefault("kwargs", {})
            kwargs["base_url"] = base_url
        elif hasattr(profile, "kwargs"):
            if profile.kwargs is None:
                profile.kwargs = {}
            profile.kwargs["base_url"] = base_url


def patch_config(config: Any, args: argparse.Namespace) -> Any:
    """Apply CLI overrides to MobileConfig loaded from YAML."""
    if getattr(config, "agent", None) is not None:
        if args.steps is not None:
            config.agent.max_steps = args.steps
        if args.reasoning is not None:
            config.agent.reasoning = args.reasoning
        if args.vision is not None:
            for sub_name in ("fast_agent", "manager", "executor"):
                sub_cfg = getattr(config.agent, sub_name, None)
                if sub_cfg is not None and hasattr(sub_cfg, "vision"):
                    sub_cfg.vision = args.vision

    if getattr(config, "device", None) is not None:
        if args.device:
            config.device.serial = args.device
        if args.tcp:
            config.device.use_tcp = True

    if getattr(config, "logging", None) is not None:
        if args.debug:
            config.logging.debug = True
        if args.save_trajectory:
            config.logging.save_trajectory = args.save_trajectory

    patch_profile_base_url(config, args.base_url)

    return config


async def run_goal(args: argparse.Namespace) -> int:
    load_dotenv()

    if not args.skip_precheck:
        precheck_environment(base_url=args.base_url, model=args.model)

    MobileAgent, MobileConfig = import_mobilerun()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = MobileConfig.from_yaml(str(config_path))
    config = patch_config(config, args)

    agent = MobileAgent(
        goal=args.goal,
        config=config,
        timeout=args.timeout,
    )

    result = await agent.run()

    print("\n========== MobileRun Result ==========")
    print(f"Success: {getattr(result, 'success', None)}")
    print(f"Reason : {getattr(result, 'reason', None)}")
    print(f"Steps  : {getattr(result, 'steps', None)}")

    structured_output = getattr(result, "structured_output", None)
    if structured_output is not None:
        print(f"Structured output: {structured_output}")

    return 0 if getattr(result, "success", False) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run MobileRun Python SDK with local Ollama."
    )
    parser.add_argument(
        "--goal",
        default="Open Settings and tell me the Android version",
        help="Natural-language goal for the mobile agent.",
    )
    parser.add_argument(
        "--config",
        default="config.ollama.yaml",
        help="Path to MobileRun YAML config.",
    )
    parser.add_argument(
        "--model",
        default="qwen3.5:4b",
        help="Ollama model name. Default: qwen3.5:4b",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        help="Ollama base URL.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=20,
        help="Maximum number of MobileRun steps.",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="ADB device serial. Leave empty to auto-detect.",
    )
    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Use TCP device communication if configured.",
    )
    parser.add_argument(
        "--reasoning",
        action="store_true",
        default=None,
        help="Enable reasoning mode: ManagerAgent + ExecutorAgent.",
    )
    parser.add_argument(
        "--no-reasoning",
        dest="reasoning",
        action="store_false",
        help="Disable reasoning mode: use FastAgent direct execution.",
    )
    parser.add_argument(
        "--vision",
        action="store_true",
        default=None,
        help="Enable screenshot vision for all agents. Not recommended for small non-vision local models.",
    )
    parser.add_argument(
        "--no-vision",
        dest="vision",
        action="store_false",
        help="Disable screenshot vision for all agents.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging.",
    )
    parser.add_argument(
        "--save-trajectory",
        choices=["none", "step", "action"],
        default=None,
        help="Save trajectory level.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1000,
        help="Workflow timeout in seconds.",
    )
    parser.add_argument(
        "--skip-precheck",
        action="store_true",
        help="Skip Ollama/adb/mobilerun ping checks.",
    )
    return parser.parse_args()


def main() -> None:
    try:
        exit_code = asyncio.run(run_goal(parse_args()))
        raise SystemExit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        raise SystemExit(130)
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
