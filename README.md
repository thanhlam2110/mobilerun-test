# MobileRun Test Suite

🌐 **Language / Ngôn ngữ:** English | [Tiếng Việt](README.vi.md)

📦 **Official MobileRun repository:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

This repository provides a compact test suite for experimenting with **MobileRun**, an LLM-based framework for controlling Android devices and emulators.

The project is organized around three usage modes:

1. **CLI mode** — test MobileRun directly from the command line.
2. **Cloud LLM mode** — run MobileRun from Python using OpenAI API.
3. **Local LLM mode** — run MobileRun from Python using a local Ollama model.

The main purpose of this repository is to evaluate MobileRun for Android UI automation before integrating it into larger mobile-analysis, dynamic-testing, or agentic-AI workflows.

---

## Repository structure

```text
.
├── asset/
├── mobilerun-cli/
├── mobilerun-cloud-llm/
├── mobilerun-local-llm/
├── .gitignore
├── command.txt
└── requirements.txt
```

| Path | Description |
|---|---|
| `asset/` | Stores supporting files such as MobileRun APKs, screenshots, or other assets. |
| `mobilerun-cli/` | Contains the CLI-first setup and usage notes. |
| `mobilerun-cloud-llm/` | Contains the Python SDK example for running MobileRun with OpenAI API. |
| `mobilerun-local-llm/` | Contains the Python SDK example for running MobileRun with a local Ollama model. |
| `.gitignore` | Prevents secrets, virtual environments, logs, and generated files from being committed. |
| `command.txt` | Optional notes for frequently used commands. |
| `requirements.txt` | Optional top-level dependency snapshot. |

---

## Modules

### `mobilerun-cli`

This module is intended for quick validation of the MobileRun CLI workflow.  
It is useful when you want to check whether the Android device, ADB, MobileRun Portal, and LLM provider are correctly configured.

Use this module first when setting up MobileRun on a new machine or device.

---

### `mobilerun-cloud-llm`

This module demonstrates how to use MobileRun through the Python SDK with a cloud LLM provider.

The current example targets OpenAI through the `OpenAIResponses` provider.  
This mode is recommended for UI-heavy or dynamic Android apps because stronger cloud models usually provide better reasoning, action selection, and recovery behavior.

---

### `mobilerun-local-llm`

This module demonstrates how to use MobileRun through the Python SDK with a local Ollama model.

The default local model used in this repository is:

```text
qwen3.5:4b
```

This mode is useful for private, low-cost, and offline-friendly experiments.  
However, smaller local models may be weaker than cloud models on complex UI reasoning tasks.

---

## Recommended usage flow

For a new Android device or development environment, the recommended order is:

1. Start with `mobilerun-cli` to validate the basic device setup.
2. Use `mobilerun-cloud-llm` to test stronger LLM-based automation.
3. Use `mobilerun-local-llm` to compare local/private execution with Ollama.

This separation helps identify whether a failure is caused by the Android setup, the MobileRun configuration, the cloud model, or the local model.

---

## Documentation

Each submodule contains its own README with detailed setup instructions:

| Module | README |
|---|---|
| CLI mode | `mobilerun-cli/README.md` |
| Cloud LLM mode | `mobilerun-cloud-llm/README.md` |
| Local LLM mode | `mobilerun-local-llm/README.md` |

The root README only provides a high-level overview. Refer to the module-specific README files for concrete setup commands and configuration details.
