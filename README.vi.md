# Hướng dẫn cài đặt MobileRun CLI

🌐 **Language / Ngôn ngữ:** English | [Tiếng Việt](README.vi.md)

📦 **Official repository:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

---

`MobileRun` là công cụ CLI bằng Python dùng để điều khiển thiết bị Android hoặc emulator thông qua LLM agent.  
Tài liệu này tập trung vào cách setup theo hướng **CLI trước**, sử dụng môi trường Python cô lập `.venv`, ADB, MobileRun Portal và OpenAI API.

---

## 1. Yêu cầu

Môi trường khuyến nghị:

- Windows PowerShell
- Python 3.11, 3.12 hoặc 3.13
- Android Platform Tools / ADB
- Điện thoại Android hoặc emulator với:
  - Đã bật Developer Options
  - Đã bật USB Debugging
  - Đã chấp nhận ADB authorization
- OpenAI API key hoặc API key của provider khác được MobileRun hỗ trợ

Kiểm tra Python:

```powershell
python --version
```

Kiểm tra ADB:

```powershell
adb version
adb devices
```

---

## 2. Tạo môi trường Python cô lập

Tạo thư mục test:

```powershell
mkdir C:\Users\ASUS\anaconda3-project-code\EBPS\mobilerun-test
cd C:\Users\ASUS\anaconda3-project-code\EBPS\mobilerun-test
```

Tạo và activate `.venv`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nâng cấp `pip` và cài MobileRun:

```powershell
python -m pip install --upgrade pip
pip install mobilerun
```

Kiểm tra MobileRun đã được cài trong `.venv`:

```powershell
mobilerun --version
mobilerun --help
```

Output có dạng:

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

## 3. Kết nối thiết bị Android

Kết nối điện thoại Android hoặc emulator, sau đó chạy:

```powershell
adb devices
```

Kết quả mong muốn:

```text
List of devices attached
DEVICE_SERIAL    device
```

Nếu thiết bị hiện `unauthorized`, hãy kiểm tra màn hình điện thoại và bấm cho phép USB debugging.

---

## 4. Cài và kiểm tra MobileRun Portal

Cài và bật MobileRun Portal:

```powershell
mobilerun setup
```

Kiểm tra thiết bị đã sẵn sàng chưa:

```powershell
mobilerun ping
```

Nếu `ping` thành công, thiết bị đã sẵn sàng để chạy tự động hóa bằng CLI.

---

## 5. Cấu hình LLM provider

Bạn có thể cấu hình provider bằng wizard:

```powershell
mobilerun configure
```

Ví dụ cấu hình thành công:

```text
Provider: OpenAI (OpenAIResponses)
Model: gpt-5.4-mini
Advanced settings changed: No
```

Set OpenAI API key cho PowerShell session hiện tại:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

Để lưu permanent cho Windows user hiện tại:

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY", "User")
```

Sau đó đóng và mở lại PowerShell.

---

## 6. Chạy MobileRun từ CLI

### Cách A — Dùng cấu hình đã lưu

Sau khi chạy `mobilerun configure`, bạn có thể chạy task mà không cần truyền thủ công provider và model:

```powershell
mobilerun run "Open Settings and tell me the Android version" --steps 20 --debug
```

### Cách B — Override provider và model thủ công

Lệnh sau đã được test và chạy được:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

Dùng dạng này khi bạn muốn chỉ định rõ runtime provider và model của OpenAI.

---

## 7. Giới hạn số step

Dùng option `--steps`:

```powershell
mobilerun run "Open Settings and tell me the Android version" --steps 20 --debug
```

Ví dụ giới hạn 10 step:

```powershell
mobilerun run "Open Settings and tell me the Android version" --steps 10 --debug
```

Nếu không truyền `--steps`, MobileRun sẽ dùng giới hạn mặc định. Trong log đã quan sát, default là:

```text
Step 1/15
```

Tức là số step mặc định là `15`.

Để xem toàn bộ option của lệnh `run`:

```powershell
mobilerun run --help
```

---

## 8. Các lệnh hữu ích

Liệt kê thiết bị đang kết nối:

```powershell
mobilerun devices
```

Kiểm tra sức khỏe hệ thống:

```powershell
mobilerun doctor
```

Kiểm tra thiết bị đã sẵn sàng chưa:

```powershell
mobilerun ping
```

Mở giao diện terminal UI:

```powershell
mobilerun tui
```

Xem help cấp cao:

```powershell
mobilerun --help
```

Xem help riêng cho lệnh `run`:

```powershell
mobilerun run --help
```

---

## 9. Điều khiển thiết bị trực tiếp

MobileRun cũng hỗ trợ thao tác trực tiếp với thiết bị mà không cần LLM reasoning.

Ví dụ:

```powershell
mobilerun device screenshot
mobilerun device ui
mobilerun device press home
```

Nên dùng các lệnh này để kiểm tra ADB và MobileRun Portal trước khi chạy task bằng LLM.

---

## 10. Xuất danh sách thư viện Python đã cài

Liệt kê package đã cài:

```powershell
python -m pip list
```

Xuất dependency chính xác ra `requirements.txt`:

```powershell
python -m pip freeze > requirements.txt
```

Lưu danh sách package dễ đọc:

```powershell
python -m pip list > pip-list.txt
```

Hiển thị package theo format giống `requirements.txt` nhưng không lưu file:

```powershell
python -m pip list --format=freeze
```

---

## 11. Lỗi thường gặp

### Unsupported provider `OpenAI`

Nếu chạy:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAI --model gpt-4o
```

có thể gặp lỗi:

```text
Unsupported provider 'OpenAI'
Supported: ['Anthropic', 'DeepSeek', 'GoogleGenAI', 'MiniMax', 'Ollama', 'OpenAILike', 'OpenAIResponses', 'OpenRouter']
```

Hãy dùng `OpenAIResponses`:

```powershell
mobilerun run "Open Settings and tell me the Android version" --provider OpenAIResponses --model gpt-4o --steps 20 --debug
```

Hoặc dùng cấu hình đã lưu:

```powershell
mobilerun configure
mobilerun run "Open Settings and tell me the Android version" --steps 20 --debug
```

### Could not get usage: Unsupported provider: openai_responses_llm

Thông báo đã quan sát:

```text
Could not get usage: Unsupported provider: openai_responses_llm
```

Thông báo này thường không làm task dừng. Trong lần chạy đã quan sát, MobileRun vẫn hoàn thành thành công:

```text
Goal achieved: Found the Android version in Settings > About phone > Software information: Android version 13.
```

Có vẻ thông báo này liên quan đến phần báo cáo token/cost usage, không phải lỗi điều khiển thiết bị.
