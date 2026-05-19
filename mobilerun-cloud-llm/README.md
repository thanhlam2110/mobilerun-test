# mobilerun-cloud-llm

🌐 **Language / Ngôn ngữ:** English | [Tiếng Việt](README.vi.md)

📦 **Official repository:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

Python SDK example for running MobileRun with OpenAI API through the `OpenAIResponses` provider.

This project is intended for testing MobileRun as a Python SDK before integrating it into a larger automation pipeline.

---

## 1. Setup

Create and activate a Python virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Prepare the Android device:

```powershell
adb devices
mobilerun setup
mobilerun ping
```

Set OpenAI API key:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

Optional: save the key permanently for the current Windows user:

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY", "User")
```

Then close and reopen PowerShell.

---

## 2. Run

Basic Android Settings test:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

Equivalent explicit MobileRun CLI command that was tested:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

Facebook posting test:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana and post a new status that says 'This is automation test by mobilerun'" --steps 20 --debug
```

Facebook posting test with verification and trajectory saving:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', then verify the posted text appears before finishing." --steps 30 --debug --save-trajectory action
```

---

## 3. Useful options

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --steps 30 --reasoning --debug

python app.py --goal "Open Settings and tell me the Android version" --steps 30 --vision --debug

python app.py --goal "Open Settings and tell me the Android version" --device YOUR_DEVICE_SERIAL --steps 20 --debug

python app.py --goal "Open the Facebook app with the package name com.facebook.katana and post a new status that says 'This is automation test by mobilerun'" --steps 20 --debug

python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', then verify the posted text appears before finishing." --steps 30 --debug --save-trajectory action
```

---

## 4. Runtime configuration check

The current `app.py` prints the final runtime configuration after loading `config.openai.yaml` and after applying CLI overrides such as `--steps`, `--debug`, `--vision`, `--no-vision`, `--reasoning`, or `--no-reasoning`.

Example:

```text
========== Runtime MobileRun Config ==========
max_steps: 30
reasoning: True
manager vision: True
executor vision: True
fast_agent vision: True
debug: True
save_trajectory: action
=============================================
```

This is useful because the actual runtime config may differ from the YAML file if CLI flags override it.

---

## 5. `config.openai.yaml` example

```yaml
agent:
  name: mobilerun
  max_steps: 20
  reasoning: true
  streaming: true
  after_sleep_action: 1.0
  wait_for_stable_ui: 0.3
  use_normalized_coordinates: false

  fast_agent:
    vision: true
    parallel_tools: true

  manager:
    vision: true
    stateless: false

  executor:
    vision: true

  app_cards:
    enabled: true
    mode: local
    app_cards_dir: config/app_cards
    server_url: null
    server_timeout: 2.0
    server_max_retries: 2

llm_profiles:
  manager:
    provider: OpenAIResponses
    model: gpt-4o
    temperature: 0.2
    kwargs:
      max_tokens: 4096

  executor:
    provider: OpenAIResponses
    model: gpt-4o
    temperature: 0.1
    kwargs:
      max_tokens: 4096

  fast_agent:
    provider: OpenAIResponses
    model: gpt-4o
    temperature: 0.2
    kwargs:
      max_tokens: 4096

  app_opener:
    provider: OpenAIResponses
    model: gpt-4o-mini
    temperature: 0.0
    kwargs:
      max_tokens: 2048

  structured_output:
    provider: OpenAIResponses
    model: gpt-4o-mini
    temperature: 0.0
    kwargs:
      max_tokens: 2048

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

# 6. `config.openai.yaml` field reference

## 6.1 `agent`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.name` | `mobilerun` | Name of the MobileRun agent. | Mainly used for identification/logging. |
| `agent.max_steps` | `20` | Maximum number of agent steps. | Equivalent to `--steps 20`. Increase for long tasks. |
| `agent.reasoning` | `true` | Enables reasoning mode. | `true` uses Manager + Executor; `false` uses FastAgent/direct execution. |
| `agent.streaming` | `true` | Enables streaming output from the LLM. | Useful for seeing intermediate responses. |
| `agent.after_sleep_action` | `1.0` | Delay after each action. | Helps the UI update before the next observation. |
| `agent.wait_for_stable_ui` | `0.3` | Wait time for UI stabilization. | Increase if the app has animations or slow transitions. |
| `agent.use_normalized_coordinates` | `false` | Whether to use normalized coordinates. | `false` means using real screen coordinates if coordinate tools are enabled. |

## 6.2 `agent.fast_agent`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.fast_agent.vision` | `true` | Enables screenshot vision for FastAgent. | Used mainly when `reasoning: false`. |
| `agent.fast_agent.parallel_tools` | `true` | Allows multiple tool calls in one step. | Faster, but may be less conservative than one-action-per-step. |

## 6.3 `agent.manager`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.manager.vision` | `true` | Enables screenshot vision for the Manager. | Important when `reasoning: true`. |
| `agent.manager.stateless` | `false` | Controls whether the Manager keeps conversation state. | `false` usually helps multi-step tasks. |

## 6.4 `agent.executor`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.executor.vision` | `true` | Enables screenshot vision for the Executor. | Important when `reasoning: true` because the Executor performs concrete UI actions. |

## 6.5 `agent.app_cards`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `agent.app_cards.enabled` | `true` | Enables app-card support. | Helps MobileRun use additional app metadata when available. |
| `agent.app_cards.mode` | `local` | App-card source mode. | `local` means reading app cards from a local directory. |
| `agent.app_cards.app_cards_dir` | `config/app_cards` | Directory containing local app cards. | Can be used to provide app-specific metadata. |
| `agent.app_cards.server_url` | `null` | Remote app-card server URL. | `null` means no remote server is used. |
| `agent.app_cards.server_timeout` | `2.0` | Timeout for remote app-card requests. | Only relevant if a remote server is configured. |
| `agent.app_cards.server_max_retries` | `2` | Maximum retries for remote app-card requests. | Only relevant if a remote server is configured. |

## 6.6 `llm_profiles`

MobileRun can use different LLM profiles for different roles.

| Profile | Used when | Role |
|---|---|---|
| `manager` | `reasoning: true` | Plans high-level steps. |
| `executor` | `reasoning: true` | Converts the Manager plan into concrete UI actions. |
| `fast_agent` | `reasoning: false` | Directly observes the UI and chooses actions. |
| `app_opener` | When opening apps | Resolves app names/package names. |
| `structured_output` | When structured result formatting is needed | Produces structured outputs when requested. |

Common fields inside each profile:

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `provider` | `OpenAIResponses` | LLM provider used by MobileRun. | For current OpenAI API usage, use `OpenAIResponses`, not `OpenAI`. |
| `model` | `gpt-4o` | Model name. | Use stronger models for UI-heavy tasks. |
| `temperature` | `0.2` | Randomness of the model. | Lower values are better for deterministic automation. |
| `kwargs.max_tokens` | `4096` | Maximum output tokens. | Increase if outputs are truncated; reduce to control cost. |

Recommended profile usage:

| Profile | Recommended model | Recommended temperature | Reason |
|---|---|---:|---|
| `manager` | `gpt-4o` | `0.2` | Needs planning ability. |
| `executor` | `gpt-4o` | `0.1` | Needs precise UI action generation. |
| `fast_agent` | `gpt-4o` | `0.2` | Handles direct UI interaction. |
| `app_opener` | `gpt-4o-mini` | `0.0` | Simple package/app resolution. |
| `structured_output` | `gpt-4o-mini` | `0.0` | Stable deterministic formatting. |

## 6.7 `device`

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

## 6.8 `tools`

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

## 6.9 `telemetry`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `telemetry.enabled` | `false` | Enables/disables telemetry. | `false` avoids sending anonymized telemetry from this config. |

## 6.10 `tracing`

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

## 6.11 `logging`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `logging.debug` | `false` | Enables debug logs. | CLI `--debug` overrides this to `true`. |
| `logging.save_trajectory` | `none` | Controls trajectory saving. | Use `action` to save action-level traces. |
| `logging.trajectory_path` | `trajectories` | Folder for saved trajectories. | Useful for debugging and evaluation. |
| `logging.rich_text` | `false` | Enables rich terminal formatting. | Keep `false` for plain logs. |
| `logging.trajectory_gifs` | `true` | Enables GIF generation from trajectories when supported. | Useful for visual review. |

Trajectory examples:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug --save-trajectory action
```

## 6.12 `credentials`

| Field | Example | Meaning | Practical note |
|---|---:|---|---|
| `credentials.enabled` | `false` | Enables use of stored credentials. | Keep `false` for simple tests. |
| `credentials.file_path` | `config/credentials.yaml` | Path to credentials file. | Never commit real credentials. |

---

## 7. Suggested configurations

### 7.1 Fast direct mode

Good for simple tasks:

```yaml
agent:
  reasoning: false

  fast_agent:
    vision: false
    parallel_tools: true
```

Example:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

### 7.2 Reasoning + vision mode

Good for dynamic apps such as Facebook:

```yaml
agent:
  reasoning: true

  fast_agent:
    vision: true

  manager:
    vision: true

  executor:
    vision: true
```

Example:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', then verify the posted text appears before finishing." --steps 30 --debug --save-trajectory action
```

---

## 8. Notes

### `OpenAI` vs `OpenAIResponses`

In the current tested MobileRun version, the runtime provider should be:

```text
OpenAIResponses
```

not:

```text
OpenAI
```

If you manually run:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAI --model gpt-4o
```

you may see:

```text
Unsupported provider 'OpenAI'
```

Use:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

### Usage warning

You may see:

```text
Could not get usage: Unsupported provider: openai_responses_llm
```

This warning usually does not stop the task. It appears related to token/cost usage tracking, not device control.

### Verification

For tasks that require verification, make the goal explicit:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', wait until posting finishes, then explicitly check the visible feed or profile timeline for the exact text 'This is automation test by mobilerun'. Only finish if the exact text is visible on screen." --steps 40 --debug --save-trajectory action
```
