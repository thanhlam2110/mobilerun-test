# mobilerun-local-llm

🌐 **Language / Ngôn ngữ:** [English](README.md) | Tiếng Việt

📦 **Repository chính thức:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

Ví dụ Python SDK để chạy MobileRun với model local thông qua Ollama.

Model mặc định:

```text
qwen3.5:4b
```

Project này dùng để test MobileRun local trước khi tích hợp vào pipeline automation lớn hơn. So với bản cloud/OpenAI, bản local Ollama rẻ hơn và riêng tư hơn, nhưng model local nhỏ có thể yếu hơn trong các tác vụ UI reasoning phức tạp.

---

## 1. Cài đặt

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Kiểm tra MobileRun:

```powershell
where mobilerun
mobilerun --help
```

---

## 2. Chuẩn bị Ollama

Kiểm tra các model đã cài:

```powershell
ollama list
```

Tải model mặc định nếu chưa có:

```powershell
ollama pull qwen3.5:4b
```

Chạy Ollama API server trong một terminal riêng:

```powershell
ollama serve
```

Lưu ý: lệnh sau là sai vì `ollama serve` không nhận tên model:

```powershell
ollama serve qwen3.5:4b
```

Test trực tiếp model:

```powershell
ollama run qwen3.5:4b "Say hello in one sentence."
```

Kiểm tra model nào đang được load:

```powershell
ollama ps
```

| Lệnh | Mục đích |
|---|---|
| `ollama list` | Liệt kê các model đã cài local. |
| `ollama pull qwen3.5:4b` | Tải model nếu chưa có. |
| `ollama serve` | Chạy Ollama API server tại `http://localhost:11434`. |
| `ollama run qwen3.5:4b` | Chạy/chat trực tiếp với model. |
| `ollama ps` | Hiển thị các model đang được load/chạy. |

---

## 3. Chuẩn bị thiết bị Android

```powershell
adb devices
mobilerun setup
mobilerun ping
```

Nếu `mobilerun ping` thành công, thiết bị Android đã sẵn sàng để chạy MobileRun automation.

---

## 4. Chạy

Test Android Settings cơ bản:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

Nếu Ollama chạy trên máy khác:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --base-url http://192.168.1.10:11434 --steps 20 --debug
```

Lệnh MobileRun CLI tương đương:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider Ollama --model qwen3.5:4b --base_url http://localhost:11434 --steps 20 --debug
```

Nếu MobileRun CLI của bạn không nhận `--base_url`, hãy dùng lệnh Python SDK ở trên hoặc cấu hình Ollama thông qua `config.ollama.yaml`.

---

## 5. Các option hữu ích

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --steps 30 --debug --save-trajectory action

python app.py --goal "Open Settings and tell me the Android version" --base-url http://localhost:11434 --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --model qwen3.5:4b --steps 20 --debug

python app.py --goal "Open Settings and tell me the Android version" --device YOUR_DEVICE_SERIAL --steps 20 --debug
```

Với model local text nhỏ, nên test đầu tiên bằng:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug --no-vision --no-reasoning
```

---

## 6. Kiểm tra runtime configuration

File `app.py` có thể in ra cấu hình runtime cuối cùng sau khi load `config.ollama.yaml` và sau khi apply CLI overrides như `--steps`, `--debug`, `--vision`, `--no-vision`, `--reasoning`, `--no-reasoning`, `--base-url`, hoặc `--model`.

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

## 7. Ví dụ `config.ollama.yaml`

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

# 8. Giải thích các trường trong `config.ollama.yaml`

## 8.1 `agent`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.name` | `mobilerun` | Tên của MobileRun agent. | Chủ yếu dùng cho định danh/logging. |
| `agent.max_steps` | `20` | Số step tối đa của agent. | Tương đương `--steps 20`. Tăng lên nếu task dài. |
| `agent.reasoning` | `false` | Bật hoặc tắt reasoning mode. | `false` dùng FastAgent/direct execution; khuyến nghị đầu tiên cho model local nhỏ. |
| `agent.streaming` | `true` | Bật streaming output từ LLM. | Giúp xem phản hồi trung gian. |
| `agent.after_sleep_action` | `1.0` | Thời gian chờ sau mỗi action. | Giúp UI cập nhật trước khi quan sát bước tiếp theo. |
| `agent.wait_for_stable_ui` | `0.5` | Thời gian chờ UI ổn định. | Cao hơn cloud config một chút vì local inference/UI timing có thể chậm hơn. |
| `agent.use_normalized_coordinates` | `false` | Có dùng tọa độ chuẩn hóa hay không. | `false` nghĩa là dùng tọa độ màn hình thật nếu tool tọa độ được bật. |

## 8.2 `agent.fast_agent`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.fast_agent.vision` | `false` | Bật screenshot vision cho FastAgent. | Giữ `false` cho model local text-only nhỏ. |
| `agent.fast_agent.parallel_tools` | `false` | Cho phép gọi nhiều tool trong một step. | `false` an toàn hơn cho model local yếu vì bắt agent hành động thận trọng hơn. |

## 8.3 `agent.manager`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.manager.vision` | `false` | Bật screenshot vision cho Manager. | Giữ `false` cho `qwen3.5:4b` trừ khi dùng model hỗ trợ vision. |
| `agent.manager.stateless` | `false` | Quy định Manager có giữ trạng thái hội thoại hay không. | `false` thường tốt hơn cho task nhiều bước nếu bật reasoning mode. |

## 8.4 `agent.executor`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.executor.vision` | `false` | Bật screenshot vision cho Executor. | Giữ `false` cho model local text-only nhỏ. |

## 8.5 `agent.app_cards`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `agent.app_cards.enabled` | `true` | Bật app-card support. | Giúp MobileRun dùng metadata bổ sung về app khi có. |
| `agent.app_cards.mode` | `local` | Nguồn app-card. | `local` nghĩa là đọc app cards từ thư mục local. |
| `agent.app_cards.app_cards_dir` | `config/app_cards` | Thư mục chứa app cards local. | Có thể dùng để cung cấp metadata riêng cho app. |
| `agent.app_cards.server_url` | `null` | URL app-card server từ xa. | `null` nghĩa là không dùng remote server. |
| `agent.app_cards.server_timeout` | `2.0` | Timeout khi gọi remote app-card server. | Chỉ liên quan khi có server từ xa. |
| `agent.app_cards.server_max_retries` | `2` | Số lần retry tối đa khi gọi remote app-card server. | Chỉ liên quan khi có server từ xa. |

## 8.6 `llm_profiles`

| Profile | Khi nào dùng | Vai trò |
|---|---|---|
| `manager` | `reasoning: true` | Lập kế hoạch cấp cao. |
| `executor` | `reasoning: true` | Chuyển kế hoạch của Manager thành action UI cụ thể. |
| `fast_agent` | `reasoning: false` | Quan sát UI và chọn action trực tiếp. |
| `app_opener` | Khi cần mở app | Resolve app name/package name. |
| `structured_output` | Khi cần format kết quả có cấu trúc | Sinh output có cấu trúc nếu được yêu cầu. |

Các field phổ biến trong từng Ollama profile:

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `provider` | `Ollama` | Provider LLM mà MobileRun sử dụng. | Dùng `Ollama` cho model local được serve bởi Ollama. |
| `model` | `qwen3.5:4b` | Tên model Ollama. | Phải khớp với tên hiển thị bởi `ollama list`. |
| `temperature` | `0.2` | Mức độ ngẫu nhiên của model. | Giá trị thấp phù hợp hơn cho automation ổn định. |
| `kwargs.base_url` | `http://localhost:11434` | URL Ollama server. | Dùng IP khác nếu Ollama chạy trên remote host. |
| `kwargs.request_timeout` | `180.0` | Timeout request tính bằng giây. | Local inference có thể chậm, nên để cao hơn cloud timeout thông thường. |

Gợi ý cấu hình local profile:

| Profile | Model khuyến nghị | Temperature khuyến nghị | Lý do |
|---|---|---:|---|
| `manager` | `qwen3.5:4b` | `0.2` | Chỉ dùng nếu bật reasoning mode. |
| `executor` | `qwen3.5:4b` | `0.1` | Cần action UI deterministic hơn. |
| `fast_agent` | `qwen3.5:4b` | `0.2` | Model chính khi `reasoning: false`. |
| `app_opener` | `qwen3.5:4b` | `0.0` | Resolve app/package đơn giản. |
| `structured_output` | `qwen3.5:4b` | `0.0` | Format ổn định, deterministic. |

## 8.7 `device`

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

## 8.8 `tools`

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

## 8.9 `telemetry`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `telemetry.enabled` | `false` | Bật/tắt telemetry. | `false` tránh gửi telemetry ẩn danh từ config này. |

## 8.10 `tracing`

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

## 8.11 `logging`

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

## 8.12 `credentials`

| Trường | Ví dụ | Ý nghĩa | Ghi chú thực tế |
|---|---:|---|---|
| `credentials.enabled` | `false` | Bật sử dụng credentials đã lưu. | Giữ `false` cho test đơn giản. |
| `credentials.file_path` | `config/credentials.yaml` | Đường dẫn file credentials. | Không commit credentials thật. |

---

## 9. Cấu hình local gợi ý

### 9.1 Safe local direct mode

Khuyến nghị đầu tiên cho `qwen3.5:4b`:

```yaml
agent:
  reasoning: false

  fast_agent:
    vision: false
    parallel_tools: false
```

Ví dụ:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 20 --debug
```

### 9.2 Local reasoning mode

Chỉ dùng nếu model local có thể follow multi-step planning tốt:

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

Ví dụ:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --steps 30 --debug --reasoning
```

### 9.3 Remote Ollama server

Nếu Ollama chạy trên máy khác:

```powershell
python app.py --goal "Open Settings and tell me the Android version" --base-url http://192.168.1.10:11434 --steps 20 --debug
```

YAML tương đương:

```yaml
kwargs:
  base_url: http://192.168.1.10:11434
  request_timeout: 180.0
```

---

## 10. Ghi chú

### Giới hạn của local model

`qwen3.5:4b` là model nhỏ và có thể fail với app dynamic phức tạp. Nếu nó loop hoặc chọn sai UI element:

1. Giảm độ phức tạp của task.
2. Giữ `reasoning: false`.
3. Giữ `vision: false`.
4. Giữ `parallel_tools: false`.
5. Tăng `max_steps`.
6. Test cùng task với bản cloud/OpenAI để xác nhận device setup đúng.

### Vision mode

Nên tắt vision cho setup mặc định:

```yaml
vision: false
```

Lý do: `qwen3.5:4b` được xem như model local text nhỏ trong setup này. Chỉ nên bật vision nếu model local được chọn và provider path của MobileRun hỗ trợ image input.

### Ollama server vs model

Đây là hai lệnh khác nhau:

```powershell
ollama serve
```

chạy Ollama server.

```powershell
ollama run qwen3.5:4b
```

chạy model tương tác.

MobileRun chỉ cần Ollama server đang chạy. Nó sẽ gọi model qua Ollama API bằng cấu hình:

```yaml
provider: Ollama
model: qwen3.5:4b
kwargs:
  base_url: http://localhost:11434
```

### Kiểm tra MobileRun có gọi Ollama hay không

Khi MobileRun local chạy đúng, terminal `ollama serve` nên xuất hiện inference API requests như:

```text
POST /api/chat
```

hoặc:

```text
POST /api/generate
```

Các request như:

```text
GET /api/tags
GET /api/ps
```

chỉ cho thấy server/model status đã được kiểm tra.
