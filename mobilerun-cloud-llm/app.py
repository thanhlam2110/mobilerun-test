"""
mobilerun-cloud-llm/app.py

Run MobileRun from Python SDK using OpenAI API through the OpenAIResponses provider.

Example:
    python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug

Prerequisites:
    1. pip install -r requirements.txt
    2. mobilerun setup
    3. mobilerun ping
    4. Set OPENAI_API_KEY
"""

from __future__ import annotations

import argparse
import asyncio
import os
import shutil
import subprocess
import sys
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


def precheck_environment() -> None:
    """Run lightweight checks before starting the MobileRun SDK."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. In PowerShell, run:\n"
            '$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"'
        )

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

    return config


async def run_goal(args: argparse.Namespace) -> int:
    load_dotenv()

    if not args.skip_precheck:
        precheck_environment()

    MobileAgent, MobileConfig = import_mobilerun()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = MobileConfig.from_yaml(str(config_path))
    config = patch_config(config, args)
    print("\n========== Runtime MobileRun Config ==========")
    print("max_steps:", config.agent.max_steps)
    print("reasoning:", config.agent.reasoning)
    print("manager vision:", config.agent.manager.vision)
    print("executor vision:", config.agent.executor.vision)
    print("fast_agent vision:", config.agent.fast_agent.vision)
    print("debug:", config.logging.debug)
    print("save_trajectory:", config.logging.save_trajectory)
    print("=============================================\n")

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
        description="Run MobileRun Python SDK with OpenAI API / OpenAIResponses."
    )
    parser.add_argument(
        "--goal",
        default="Open Settings and tell me the Android version",
        help="Natural-language goal for the mobile agent.",
    )
    parser.add_argument(
        "--config",
        default="config.openai.yaml",
        help="Path to MobileRun YAML config.",
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
        help="Enable screenshot vision for all agents.",
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
        help="Skip adb/mobilerun ping checks.",
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
