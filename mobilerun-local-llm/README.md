# mobilerun-local-llm

🌐 **Language / Ngôn ngữ:** English | [Tiếng Việt](README.vi.md)

📦 **Official repository:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

Python SDK example for running MobileRun with a local Ollama model.

Default model:

```text
qwen3.5:4b
```

This project is intended for testing MobileRun locally before integrating it into a larger automation pipeline. Compared with the cloud/OpenAI version, the local Ollama version is cheaper and private, but small local models can be weaker at complex UI reasoning.

---

## 1. Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Check MobileRun:

```powershell
where mobilerun
mobilerun --help
```

---

## 2. Prepare Ollama

Check installed models:

```powershell
ollama list
```

Pull the default model if it is missing:

```powershell
ollama pull qwen3.5:4b
```

Start the Ollama API server in a dedicated terminal:

```powershell
ollama serve
```

Important: this is incorrect because `ollama serve` accepts no model argument:

```powershell
ollama serve qwen3.5:4b
```

To test the model directly:

```powershell
ollama run qwen3.5:4b "Say hello in one sentence."
```

To check which model is currently loaded:

```powershell
ollama ps
```

| Command | Purpose |
|---|---|
| `ollama list` | Lists locally installed models. |
| `ollama pull qwen3.5:4b` | Downloads the model if missing. |
| `ollama serve` | Starts the Ollama API server at `http://localhost:11434`. |
| `ollama run qwen3.5:4b` | Runs or chats with the model directly. |
| `ollama ps` | Shows currently loaded/running models. |

---

## 3. Prepare the Android device

```powershell
adb devices
mobilerun setup
mobilerun ping
```

If `mobilerun ping` succeeds, the Android device is ready for MobileRun automation.

---

## 4. Run

Basic Android Settings test:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

If Ollama runs on another host:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --base-url http://192.168.1.10:11434 --steps 20 --debug
```

Equivalent explicit MobileRun CLI command:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider Ollama --model qwen3.5:4b --base_url http://localhost:11434 --steps 20 --debug
```

If your MobileRun CLI does not accept `--base_url`, use the Python SDK command above or configure Ollama through `config.ollama.yaml`.

---

## 5. Useful options

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --steps 30 --debug --save-trajectory action

python app.py --goal "Open Settings and tell me the Android version" --base-url http://localhost:11434 --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --model qwen3.5:4b --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --device YOUR_DEVICE_SERIAL --steps 20 --debug
```

Recommended first test for small local text models:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug --no-vision --no-reasoning
```

---

## 6. Runtime configuration check

The current `app.py` can print the final runtime configuration after loading `config.ollama.yaml` and applying CLI overrides such as `--steps`, `--debug`, `--vision`, `--no-vision`, `--reasoning`, `--no-reasoning`, `--base-url`, or `--model`.

Example:

```text
========== Runtime MobileRun Config ==========
max_steps: 20
reasoning: False
manager vision: False
executor vision: False
fast_agent vision: False
debug: True
save_trajectory: none
=============================================
```

---

## 7. `config.ollama.yaml` example

```yaml
agent:
  name: mobilerun
  max_steps: 20
  reasoning: false
  streaming: true
  after_sleep_action: 1.0
  wait_for_stable_ui: 0.5
  use_normalized_coordinates: false

  fast_agent:
    vision: false
    parallel_tools: false

  manager:
    vision: false
    stateless: false

  executor:
    vision: false

  app_cards:
    enabled: true
    mode: local
    app_cards_dir: config/app_cards
    server_url: null
    server_timeout: 2.0
    server_max_retries: 2

llm_profiles:
  manager:
    provider: Ollama
    model: qwen3.5:4b
    temperature: 0.2
    kwargs:
      base_url: http://localhost:11434
      request_timeout: 180.0

  executor:
    provider: Ollama
    model: qwen3.5:4b
    temperature: 0.1
    kwargs:
      base_url: http://localhost:11434
      request_timeout: 180.0

  fast_agent:
    provider: Ollama
    model: qwen3.5:4b
    temperature: 0.2
    kwargs:
      base_url: http://localhost:11434
      request_timeout: 180.0

  app_opener:
    provider: Ollama
    model: qwen3.5:4b
    temperature: 0.0
    kwargs:
      base_url: http://localhost:11434
      request_timeout: 180.0

  structured_output:
    provider: Ollama
    model: qwen3.5:4b
    temperature: 0.0
    kwargs:
      base_url: http://localhost:11434
      request_timeout: 180.0

device:
  serial: null
  platform: android
  use_tcp: false
  auto_setup: true

tools:
  disabled_tools:
    - click_at
    - click_area
    - long_press_at
  stealth: false

telemetry:
  enabled: false

tracing:
  enabled: false
  provider: phoenix
  langfuse_screenshots: false
  langfuse_secret_key: ""
  langfuse_public_key: ""
  langfuse_host: ""
  langfuse_user_id: anonymous
  langfuse_session_id: ""

logging:
  debug: false
  save_trajectory: none
  trajectory_path: trajectories
  rich_text: false
  trajectory_gifs: true

credentials:
  enabled: false
  file_path: config/credentials.yaml
```

---

# 8. `config.ollama.yaml` field reference

## 8.1 `agent`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.name` | `mobilerun` | Name of the MobileRun agent. | Mainly used for identification/logging. |
| `agent.max_steps` | `20` | Maximum number of agent steps. | Equivalent to `--steps 20`. Increase for long tasks. |
| `agent.reasoning` | `false` | Enables or disables reasoning mode. | `false` uses FastAgent/direct execution; recommended first for small local models. |
| `agent.streaming` | `true` | Enables streaming output from the LLM. | Useful for seeing intermediate responses. |
| `agent.after_sleep_action` | `1.0` | Delay after each action. | Helps the UI update before the next observation. |
| `agent.wait_for_stable_ui` | `0.5` | Wait time for UI stabilization. | Slightly higher than cloud config because local inference/UI timing can be slower. |
| `agent.use_normalized_coordinates` | `false` | Whether to use normalized coordinates. | `false` means real screen coordinates if coordinate tools are enabled. |

## 8.2 `agent.fast_agent`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.fast_agent.vision` | `false` | Enables screenshot vision for FastAgent. | Keep `false` for small text-only local models. |
| `agent.fast_agent.parallel_tools` | `false` | Allows multiple tool calls in one step. | `false` is safer for weaker local models because it forces more conservative actions. |

## 8.3 `agent.manager`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.manager.vision` | `false` | Enables screenshot vision for Manager. | Keep `false` for `qwen3.5:4b` unless using a vision-capable model. |
| `agent.manager.stateless` | `false` | Controls whether the Manager keeps conversation state. | `false` usually helps multi-step tasks if reasoning mode is enabled. |

## 8.4 `agent.executor`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.executor.vision` | `false` | Enables screenshot vision for Executor. | Keep `false` for small text-only local models. |

## 8.5 `agent.app_cards`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.app_cards.enabled` | `true` | Enables app-card support. | Helps MobileRun use additional app metadata when available. |
| `agent.app_cards.mode` | `local` | App-card source mode. | `local` means reading app cards from a local directory. |
| `agent.app_cards.app_cards_dir` | `config/app_cards` | Directory containing local app cards. | Can be used to provide app-specific metadata. |
| `agent.app_cards.server_url` | `null` | Remote app-card server URL. | `null` means no remote server is used. |
| `agent.app_cards.server_timeout` | `2.0` | Timeout for remote app-card requests. | Only relevant if a remote server is configured. |
| `agent.app_cards.server_max_retries` | `2` | Maximum retries for remote app-card requests. | Only relevant if a remote server is configured. |

## 8.6 `llm_profiles`

| Profile | Used when | Role |
|---|---|---|
| `manager` | `reasoning: true` | Plans high-level steps. |
| `executor` | `reasoning: true` | Converts the Manager plan into concrete UI actions. |
| `fast_agent` | `reasoning: false` | Directly observes the UI and chooses actions. |
| `app_opener` | When opening apps | Resolves app names/package names. |
| `structured_output` | When structured result formatting is needed | Produces structured outputs when requested. |

Common fields inside each Ollama profile:

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `provider` | `Ollama` | LLM provider used by MobileRun. | Use `Ollama` for local models served by Ollama. |
| `model` | `qwen3.5:4b` | Ollama model name. | Must match the name shown by `ollama list`. |
| `temperature` | `0.2` | Randomness of the model. | Lower values are better for deterministic automation. |
| `kwargs.base_url` | `http://localhost:11434` | Ollama server URL. | Use another IP if Ollama runs on a remote host. |
| `kwargs.request_timeout` | `180.0` | Request timeout in seconds. | Local inference can be slow, so keep this higher than typical cloud timeout. |

Recommended local profile usage:

| Profile | Recommended model | Recommended temperature | Reason |
|---|---|---:|---|
| `manager` | `qwen3.5:4b` | `0.2` | Used only if reasoning mode is enabled. |
| `executor` | `qwen3.5:4b` | `0.1` | Needs more deterministic UI actions. |
| `fast_agent` | `qwen3.5:4b` | `0.2` | Main model when `reasoning: false`. |
| `app_opener` | `qwen3.5:4b` | `0.0` | Simple app/package resolution. |
| `structured_output` | `qwen3.5:4b` | `0.0` | Stable deterministic formatting. |

## 8.7 `device`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `device.serial` | `null` | ADB device serial. | Use `null` for auto-detect; set a serial if multiple devices are connected. |
| `device.platform` | `android` | Target platform. | Current use case is Android. |
| `device.use_tcp` | `false` | Whether to use ADB over TCP/IP. | Keep `false` for USB/emulator; use `true` for wireless ADB. |
| `device.auto_setup` | `true` | Allows automatic setup behavior. | Useful for Portal/device preparation. |

Example with a specific device:

```yaml
device:
  serial: R58Nxxxxxxx
  platform: android
  use_tcp: false
  auto_setup: true
```

## 8.8 `tools`

| Field | Example | Meaning | Practical note |
|---|---|---|---|
| `tools.disabled_tools` | `click_at`, `click_area`, `long_press_at` | Tools disabled for the agent. | Disabling coordinate-based tools encourages safer element-index actions. |
| `tools.stealth` | `false` | Stealth mode flag. | Keep `false` for normal testing. |

Why disable coordinate tools?

| Disabled tool | Meaning | Why disable it? |
|---|---|---|
| `click_at` | Click at a raw coordinate. | Less robust across devices and screen sizes. |
| `click_area` | Click inside a screen area. | Less precise than element-index clicking. |
| `long_press_at` | Long press at a raw coordinate. | Risky if the UI layout changes. |

## 8.9 `telemetry`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `telemetry.enabled` | `false` | Enables/disables telemetry. | `false` avoids sending anonymized telemetry from this config. |

## 8.10 `tracing`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `tracing.enabled` | `false` | Enables tracing integration. | Enable only if you need advanced traces. |
| `tracing.provider` | `phoenix` | Tracing backend. | Only relevant when tracing is enabled. |
| `tracing.langfuse_screenshots` | `false` | Whether to send screenshots to Langfuse. | Keep `false` unless needed. |
| `tracing.langfuse_secret_key` | `""` | Langfuse secret key. | Do not commit real secrets. |
| `tracing.langfuse_public_key` | `""` | Langfuse public key. | Do not commit real secrets. |
| `tracing.langfuse_host` | `""` | Langfuse host URL. | Required only if using Langfuse. |
| `tracing.langfuse_user_id` | `anonymous` | User ID for Langfuse traces. | Can be changed for experiments. |
| `tracing.langfuse_session_id` | `""` | Session ID for traces. | Useful for grouping runs. |

## 8.11 `logging`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `logging.debug` | `false` | Enables debug logs. | CLI `--debug` overrides this to `true`. |
| `logging.save_trajectory` | `none` | Controls trajectory saving. | Use `action` to save action-level traces. |
| `logging.trajectory_path` | `trajectories` | Folder for saved trajectories. | Useful for debugging and evaluation. |
| `logging.rich_text` | `false` | Enables rich terminal formatting. | Keep `false` for plain logs. |
| `logging.trajectory_gifs` | `true` | Enables GIF generation from trajectories when supported. | Useful for visual review. |

Trajectory example:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug --save-trajectory action
```

## 8.12 `credentials`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `credentials.enabled` | `false` | Enables use of stored credentials. | Keep `false` for simple tests. |
| `credentials.file_path` | `config/credentials.yaml` | Path to credentials file. | Never commit real credentials. |

---

## 9. Suggested local configurations

### 9.1 Safe local direct mode

Recommended first for `qwen3.5:4b`:

```yaml
agent:
  reasoning: false

  fast_agent:
    vision: false
    parallel_tools: false
```

Example:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

### 9.2 Local reasoning mode

Use only if the local model can follow multi-step planning well:

```yaml
agent:
  reasoning: true

  fast_agent:
    vision: false

  manager:
    vision: false

  executor:
    vision: false
```

Example:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 30 --debug --reasoning
```

### 9.3 Remote Ollama server

If Ollama runs on another machine:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --base-url http://192.168.1.10:11434 --steps 20 --debug
```

Equivalent YAML change:

```yaml
kwargs:
  base_url: http://192.168.1.10:11434
  request_timeout: 180.0
```

---

## 10. Notes

### Local model limitations

`qwen3.5:4b` is small and may fail on complex dynamic apps. If it loops or selects wrong UI elements:

1. Reduce task complexity.
2. Keep `reasoning: false`.
3. Keep `vision: false`.
4. Keep `parallel_tools: false`.
5. Increase `max_steps`.
6. Test the same task with the cloud/OpenAI version to verify that the device setup is correct.

### Vision mode

Keep vision disabled for this default setup:

```yaml
vision: false
```

Reason: `qwen3.5:4b` is treated here as a small local text model. Vision should only be enabled if the selected local model and MobileRun provider path support image input.

### Ollama server vs model

These are different commands:

```powershell
ollama serve
```

starts the Ollama server.

```powershell
ollama run qwen3.5:4b
```

runs the model interactively.

MobileRun only needs the Ollama server to be running. It requests the model through the Ollama API using:

```yaml
provider: Ollama
model: qwen3.5:4b
kwargs:
  base_url: http://localhost:11434
```

### Checking whether MobileRun is calling Ollama

When MobileRun local runs correctly, the `ollama serve` terminal should show inference API requests such as:

```text
POST /api/chat
```

or:

```text
POST /api/generate
```

Requests such as:

```text
GET /api/tags
GET /api/ps
```

only indicate that the server/model status was checked.
