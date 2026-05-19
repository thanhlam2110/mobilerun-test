# MobileRun CLI Setup

🌐 **Language / Ngôn ngữ:** English | [Tiếng Việt](README.vi.md)

📦 **Official repository:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

---

`MobileRun` is a Python-based CLI tool for controlling an Android device or emulator through LLM agents.  
This guide focuses on a **CLI-first setup** using an isolated Python `.venv`, ADB, MobileRun Portal, and OpenAI API.

---

## 1. Requirements

Recommended environment:

- Windows PowerShell
- Python 3.11, 3.12, or 3.13
- Android Platform Tools / ADB
- Android phone or emulator with:
  - Developer Options enabled
  - USB Debugging enabled
  - ADB authorization accepted
- OpenAI API key or another supported provider key

Check Python:

```powershell
python --version
```

Check ADB:

```powershell
adb version
adb devices
```

---

## 2. Create an isolated Python environment

Create a test folder:

```powershell
mkdir C:\Users\ASUS\anaconda3-project-code\EBPS\mobilerun-test
cd C:\Users\ASUS\anaconda3-project-code\EBPS\mobilerun-test
```

Create and activate `.venv`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Upgrade `pip` and install MobileRun:

```powershell
python -m pip install --upgrade pip
pip install mobilerun
```

Check that MobileRun is installed inside `.venv`:

```powershell
mobilerun --version
mobilerun --help
```

Expected output:

```text
v0.6.0rc3
Usage: mobilerun [OPTIONS] COMMAND [ARGS]...

  Mobilerun - Control your Android device through LLM agents.

Options:
  --version  Show mobilerun version and exit
  --help     Show this message and exit.

Commands:
  anthropic    Anthropic authentication commands.
  configure    Configure LLM provider, auth mode, and model.
  connect      Connect to a device over TCP/IP.
  device       Direct device actions (screenshot, tap, swipe, etc.).
  devices      List connected Android devices.
  disconnect   Disconnect from a device.
  doctor       Check system health and diagnose issues.
  gemini       Gemini OAuth commands.
  macro        Replay recorded automation sequences.
  openai       OpenAI OAuth commands.
  ping         Ping a device to check if it is ready and accessible.
  run          Run a command on your mobile device using natural language.
  setup        Install and enable the Mobilerun Portal on a device.
  setup-token  Create a long-lived Anthropic setup token using...
  tui          Launch the Mobilerun Terminal User Interface.
```

---

## 3. Connect Android device

Connect the Android phone or emulator, then run:

```powershell
adb devices
```

Expected result:

```text
List of devices attached
DEVICE_SERIAL    device
```

If the device is shown as `unauthorized`, check the phone screen and allow USB debugging.

---

## 4. Install and check MobileRun Portal

Install and enable MobileRun Portal:

```powershell
mobilerun setup
```

Check whether the device is ready:

```powershell
mobilerun ping
```

If `ping` succeeds, the device is ready for CLI automation.

---

## 5. Configure LLM provider

You can configure the LLM provider interactively:

```powershell
mobilerun configure
```

Example configuration:

```text
Provider: OpenAI (OpenAIResponses)
Model: gpt-5.4-mini
Advanced settings changed: No
```

Set OpenAI API key for the current PowerShell session:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

To save it permanently for the current Windows user:

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY", "User")
```

Then close and reopen PowerShell.

---

## 6. Run MobileRun from CLI

### Option A — Use saved configuration

After running `mobilerun configure`, you can run a task without passing provider and model manually:

```powershell
mobilerun run "Open Settings and tell me the Android version" --steps 20 --debug
```

### Option B — Override provider and model manually

This command has been tested and works:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

Use this form when you want to explicitly specify the OpenAI runtime provider and model.

---

## 7. Limit the number of steps

Use the `--steps` option:

```powershell
mobilerun run "Open Settings and tell me the Android version" --steps 20 --debug
```

Example with 10 steps:

```powershell
mobilerun run "Open Settings and tell me the Android version" --steps 10 --debug
```

If `--steps` is not provided, MobileRun uses its default limit. In the observed run, the default was:

```text
Step 1/15
```

So the default step limit was `15`.

To see all options for the `run` command:

```powershell
mobilerun run --help
```

---

## 8. Useful commands

List connected devices:

```powershell
mobilerun devices
```

Check system health:

```powershell
mobilerun doctor
```

Check device readiness:

```powershell
mobilerun ping
```

Launch terminal UI:

```powershell
mobilerun tui
```

Show top-level help:

```powershell
mobilerun --help
```

Show help for `run`:

```powershell
mobilerun run --help
```

---

## 9. Direct device actions

MobileRun can also execute direct device actions without LLM reasoning.

Examples:

```powershell
mobilerun device screenshot
mobilerun device ui
mobilerun device press home
```

Use these commands to verify that ADB and MobileRun Portal are working before running LLM-based tasks.

---

## 10. Export installed Python packages

List installed packages:

```powershell
python -m pip list
```

Export exact dependencies to `requirements.txt`:

```powershell
python -m pip freeze > requirements.txt
```

Save a readable package list:

```powershell
python -m pip list > pip-list.txt
```

Show packages in `requirements.txt` format without saving:

```powershell
python -m pip list --format=freeze
```

---

## 11. Troubleshooting

### Unsupported provider `OpenAI`

If you run:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAI --model gpt-4o
```

you may get:

```text
Unsupported provider 'OpenAI'
Supported: ['Anthropic', 'DeepSeek', 'GoogleGenAI', 'MiniMax', 'Ollama', 'OpenAILike', 'OpenAIResponses', 'OpenRouter']
```

Use `OpenAIResponses` instead:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

Or use the saved configuration:

```powershell
mobilerun configure
mobilerun run "Open Settings and tell me the Android version" --steps 20 --debug
```

### Could not get usage: Unsupported provider: openai_responses_llm

Observed message:

```text
Could not get usage: Unsupported provider: openai_responses_llm
```

This usually does not stop the task. In the observed run, MobileRun still completed successfully:

```text
Goal achieved: Found the Android version in Settings > About phone > Software information: Android version 13.
```

This appears related to token/cost usage reporting, not device control itself.
