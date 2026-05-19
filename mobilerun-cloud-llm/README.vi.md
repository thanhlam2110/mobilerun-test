# mobilerun-cloud-llm

🌐 **Language / Ngôn ngữ:** [English](README.md) | Tiếng Việt

📦 **Repository chính thức:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

Ví dụ Python SDK để chạy MobileRun với OpenAI API thông qua provider `OpenAIResponses`.

Project này dùng để test MobileRun như một Python SDK trước khi tích hợp vào pipeline automation lớn hơn.

---

## 1. Cài đặt

Tạo và activate môi trường Python ảo:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Chuẩn bị thiết bị Android:

```powershell
adb devices
mobilerun setup
mobilerun ping
```

Set OpenAI API key:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

Tùy chọn: lưu key permanent cho Windows user hiện tại:

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY", "User")
```

Sau đó đóng và mở lại PowerShell.

---

## 2. Chạy

Test Android Settings cơ bản:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

Lệnh MobileRun CLI tương đương đã test thành công:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

Test post status trên Facebook:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana and post a new status that says 'This is automation test by mobilerun'" --steps 20 --debug
```

Test post status trên Facebook, có yêu cầu verify và lưu trajectory:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', then verify the posted text appears before finishing." --steps 30 --debug --save-trajectory action
```

---

## 3. Các option hữu ích

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --steps 30 --reasoning --debug

python app.py --goal "Open Settings and tell me the Android version" --steps 30 --vision --debug

python app.py --goal "Open Settings and tell me the Android version" --device YOUR_DEVICE_SERIAL --steps 20 --debug

python app.py --goal "Open the Facebook app with the package name com.facebook.katana and post a new status that says 'This is automation test by mobilerun'" --steps 20 --debug

python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', then verify the posted text appears before finishing." --steps 30 --debug --save-trajectory action
```

---

## 4. Kiểm tra runtime configuration

File `app.py` hiện tại in ra cấu hình runtime cuối cùng sau khi load `config.openai.yaml` và sau khi apply các CLI override như `--steps`, `--debug`, `--vision`, `--no-vision`, `--reasoning`, hoặc `--no-reasoning`.

Ví dụ:

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

Phần này hữu ích vì cấu hình runtime thực tế có thể khác file YAML nếu có CLI flag override.

---

## 5. Ví dụ `config.openai.yaml`

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

# 6. Giải thích các trường trong `config.openai.yaml`

## 6.1 `agent`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.name` | `mobilerun` | Tên của MobileRun agent. | Chủ yếu dùng cho định danh/logging. |
| `agent.max_steps` | `20` | Số step tối đa của agent. | Tương đương `--steps 20`. Tăng lên nếu task dài. |
| `agent.reasoning` | `true` | Bật reasoning mode. | `true` dùng Manager + Executor; `false` dùng FastAgent/direct execution. |
| `agent.streaming` | `true` | Bật streaming output từ LLM. | Giúp xem phản hồi trung gian. |
| `agent.after_sleep_action` | `1.0` | Thời gian chờ sau mỗi action. | Giúp UI cập nhật trước khi quan sát bước tiếp theo. |
| `agent.wait_for_stable_ui` | `0.3` | Thời gian chờ UI ổn định. | Tăng nếu app có animation hoặc chuyển màn hình chậm. |
| `agent.use_normalized_coordinates` | `false` | Có dùng tọa độ chuẩn hóa hay không. | `false` nghĩa là dùng tọa độ màn hình thật nếu tool tọa độ được bật. |

## 6.2 `agent.fast_agent`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.fast_agent.vision` | `true` | Bật screenshot vision cho FastAgent. | Chủ yếu dùng khi `reasoning: false`. |
| `agent.fast_agent.parallel_tools` | `true` | Cho phép gọi nhiều tool trong một step. | Nhanh hơn, nhưng có thể kém thận trọng hơn one-action-per-step. |

## 6.3 `agent.manager`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.manager.vision` | `true` | Bật screenshot vision cho Manager. | Quan trọng khi `reasoning: true`. |
| `agent.manager.stateless` | `false` | Quy định Manager có giữ trạng thái hội thoại hay không. | `false` thường tốt hơn cho task nhiều bước. |

## 6.4 `agent.executor`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.executor.vision` | `true` | Bật screenshot vision cho Executor. | Quan trọng khi `reasoning: true` vì Executor thực hiện action cụ thể trên UI. |

## 6.5 `agent.app_cards`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.app_cards.enabled` | `true` | Bật app-card support. | Giúp MobileRun dùng metadata bổ sung về app khi có. |
| `agent.app_cards.mode` | `local` | Nguồn app-card. | `local` nghĩa là đọc app cards từ thư mục local. |
| `agent.app_cards.app_cards_dir` | `config/app_cards` | Thư mục chứa app cards local. | Có thể dùng để cung cấp metadata riêng cho app. |
| `agent.app_cards.server_url` | `null` | URL của app-card server từ xa. | `null` nghĩa là không dùng remote server. |
| `agent.app_cards.server_timeout` | `2.0` | Timeout khi gọi remote app-card server. | Chỉ liên quan khi có server từ xa. |
| `agent.app_cards.server_max_retries` | `2` | Số lần retry tối đa khi gọi remote app-card server. | Chỉ liên quan khi có server từ xa. |

## 6.6 `llm_profiles`

MobileRun có thể dùng các LLM profile khác nhau cho từng vai trò.

| Profile | Khi nào dùng | Vai trò |
|---|---|---|
| `manager` | `reasoning: true` | Lập kế hoạch cấp cao. |
| `executor` | `reasoning: true` | Chuyển kế hoạch của Manager thành action UI cụ thể. |
| `fast_agent` | `reasoning: false` | Quan sát UI và chọn action trực tiếp. |
| `app_opener` | Khi cần mở app | Resolve app name/package name. |
| `structured_output` | Khi cần format kết quả có cấu trúc | Sinh output có cấu trúc nếu được yêu cầu. |

Các field phổ biến trong từng profile:

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `provider` | `OpenAIResponses` | Provider LLM mà MobileRun sử dụng. | Với OpenAI API hiện tại, dùng `OpenAIResponses`, không dùng `OpenAI`. |
| `model` | `gpt-4o` | Tên model. | Nên dùng model mạnh hơn cho task UI phức tạp. |
| `temperature` | `0.2` | Mức độ ngẫu nhiên của model. | Giá trị thấp phù hợp hơn cho automation ổn định. |
| `kwargs.max_tokens` | `4096` | Số output token tối đa. | Tăng nếu output bị cắt; giảm để kiểm soát chi phí. |

Gợi ý cấu hình profile:

| Profile | Model khuyến nghị | Temperature khuyến nghị | Lý do |
|---|---|---:|---|
| `manager` | `gpt-4o` | `0.2` | Cần năng lực lập kế hoạch. |
| `executor` | `gpt-4o` | `0.1` | Cần sinh action UI chính xác. |
| `fast_agent` | `gpt-4o` | `0.2` | Xử lý tương tác UI trực tiếp. |
| `app_opener` | `gpt-4o-mini` | `0.0` | Resolve app/package khá đơn giản. |
| `structured_output` | `gpt-4o-mini` | `0.0` | Cần format ổn định, deterministic. |

## 6.7 `device`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `device.serial` | `null` | ADB device serial. | `null` để auto-detect; nếu có nhiều device thì nên set serial cụ thể. |
| `device.platform` | `android` | Nền tảng target. | Use case hiện tại là Android. |
| `device.use_tcp` | `false` | Có dùng ADB over TCP/IP hay không. | Giữ `false` nếu dùng USB/emulator; dùng `true` nếu dùng wireless ADB. |
| `device.auto_setup` | `true` | Cho phép setup tự động. | Hữu ích cho Portal/device preparation. |

Ví dụ chỉ định thiết bị cụ thể:

```yaml
device:
  serial: R58Nxxxxxxx
  platform: android
  use_tcp: false
  auto_setup: true
```

## 6.8 `tools`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---|---|---|
| `tools.disabled_tools` | `click_at`, `click_area`, `long_press_at` | Các tool bị tắt cho agent. | Tắt tool tọa độ để khuyến khích agent click theo element index an toàn hơn. |
| `tools.stealth` | `false` | Cờ stealth mode. | Giữ `false` cho test bình thường. |

Vì sao tắt coordinate tools?

| Tool bị tắt | Ý nghĩa | Vì sao tắt? |
|---|---|---|
| `click_at` | Click tại tọa độ thô. | Ít ổn định giữa các thiết bị/kích thước màn hình. |
| `click_area` | Click trong một vùng màn hình. | Kém chính xác hơn click theo element index. |
| `long_press_at` | Long press tại tọa độ thô. | Rủi ro nếu layout UI thay đổi. |

## 6.9 `telemetry`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `telemetry.enabled` | `false` | Bật/tắt telemetry. | `false` tránh gửi telemetry ẩn danh từ config này. |

## 6.10 `tracing`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `tracing.enabled` | `false` | Bật tracing integration. | Chỉ bật nếu cần trace nâng cao. |
| `tracing.provider` | `phoenix` | Backend tracing. | Chỉ liên quan khi tracing được bật. |
| `tracing.langfuse_screenshots` | `false` | Có gửi screenshot lên Langfuse hay không. | Giữ `false` nếu không cần. |
| `tracing.langfuse_secret_key` | `""` | Langfuse secret key. | Không commit secret thật. |
| `tracing.langfuse_public_key` | `""` | Langfuse public key. | Không commit key thật. |
| `tracing.langfuse_host` | `""` | Langfuse host URL. | Chỉ cần nếu dùng Langfuse. |
| `tracing.langfuse_user_id` | `anonymous` | User ID cho Langfuse trace. | Có thể đổi cho thí nghiệm. |
| `tracing.langfuse_session_id` | `""` | Session ID cho trace. | Hữu ích để gom nhóm các run. |

## 6.11 `logging`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `logging.debug` | `false` | Bật debug logs. | CLI `--debug` sẽ override thành `true`. |
| `logging.save_trajectory` | `none` | Điều khiển lưu trajectory. | Dùng `action` để lưu trace theo từng action. |
| `logging.trajectory_path` | `trajectories` | Thư mục lưu trajectory. | Hữu ích cho debug và evaluation. |
| `logging.rich_text` | `false` | Bật định dạng terminal rich text. | Giữ `false` để log dạng plain. |
| `logging.trajectory_gifs` | `true` | Tạo GIF từ trajectory nếu được hỗ trợ. | Hữu ích để review trực quan. |

Ví dụ lưu trajectory:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug --save-trajectory action
```

## 6.12 `credentials`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `credentials.enabled` | `false` | Bật sử dụng credentials đã lưu. | Giữ `false` cho test đơn giản. |
| `credentials.file_path` | `config/credentials.yaml` | Đường dẫn file credentials. | Không commit credentials thật. |

---

## 7. Cấu hình gợi ý

### 7.1 Fast direct mode

Phù hợp với task đơn giản:

```yaml
agent:
  reasoning: false

  fast_agent:
    vision: false
    parallel_tools: true
```

Ví dụ:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

### 7.2 Reasoning + vision mode

Phù hợp với app dynamic như Facebook:

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

Ví dụ:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', then verify the posted text appears before finishing." --steps 30 --debug --save-trajectory action
```

---

## 8. Ghi chú

### `OpenAI` vs `OpenAIResponses`

Trong version MobileRun đã test, runtime provider nên dùng là:

```text
OpenAIResponses
```

không phải:

```text
OpenAI
```

Nếu chạy thủ công:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAI --model gpt-4o
```

có thể gặp:

```text
Unsupported provider 'OpenAI'
```

Hãy dùng:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

### Usage warning

Bạn có thể thấy:

```text
Could not get usage: Unsupported provider: openai_responses_llm
```

Warning này thường không làm task dừng. Nó có vẻ liên quan đến token/cost usage tracking, không phải lỗi điều khiển thiết bị.

### Verification

Với task yêu cầu verification, nên viết goal thật rõ:

```powershell
python app.py --goal "Open the Facebook app with the package name com.facebook.katana, post a new status that says 'This is automation test by mobilerun', wait until posting finishes, then explicitly check the visible feed or profile timeline for the exact text 'This is automation test by mobilerun'. Only finish if the exact text is visible on screen." --steps 40 --debug --save-trajectory action
```
