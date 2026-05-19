# mobilerun-local-llm

Python SDK example for running MobileRun with a local Ollama model.

Default model:

```text
qwen3.5:4b
```

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Prepare Ollama:

```powershell
ollama serve
ollama pull qwen3.5:4b
```

Prepare the Android device:

```powershell
adb devices
mobilerun setup
mobilerun ping
```

## Run

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

If Ollama runs on another host:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --base-url http://192.168.1.10:11434 --steps 20 --debug
```

Equivalent explicit CLI command:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider Ollama --model qwen3.5:4b --base_url http://localhost:11434 --steps 20 --debug
```

## Notes

- Keep `vision: false` for small local text-only models.
- Start with `reasoning: false` because direct FastAgent mode is cheaper and faster for small local models.
- If the local model loops or fails to follow the UI, test first with the cloud/OpenAI version to verify that the device setup is correct.
