# MobileRun Test Suite

🌐 **Language / Ngôn ngữ:** [English](README.md) | Tiếng Việt

📦 **Repository MobileRun chính thức:** [droidrun/mobilerun](https://github.com/droidrun/mobilerun)

Repository này cung cấp một bộ test nhỏ gọn để thử nghiệm **MobileRun**, một framework dựa trên LLM dùng để điều khiển thiết bị Android hoặc emulator.

Project được tổ chức theo ba chế độ sử dụng:

1. **CLI mode** — test MobileRun trực tiếp từ command line.
2. **Cloud LLM mode** — chạy MobileRun từ Python bằng OpenAI API.
3. **Local LLM mode** — chạy MobileRun từ Python bằng model Ollama local.

Mục tiêu chính của repository là đánh giá MobileRun cho Android UI automation trước khi tích hợp vào các workflow lớn hơn như mobile analysis, dynamic testing hoặc agentic AI.

---

## Cấu trúc repository

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

| Đường dẫn | Mô tả |
|---|---|
| `asset/` | Lưu các file hỗ trợ như MobileRun APK, screenshot hoặc asset khác. |
| `mobilerun-cli/` | Chứa hướng dẫn setup và sử dụng theo hướng CLI-first. |
| `mobilerun-cloud-llm/` | Chứa ví dụ Python SDK để chạy MobileRun với OpenAI API. |
| `mobilerun-local-llm/` | Chứa ví dụ Python SDK để chạy MobileRun với model Ollama local. |
| `.gitignore` | Tránh commit secret, virtual environment, log và file sinh tự động. |
| `command.txt` | Ghi chú tùy chọn cho các command thường dùng. |
| `requirements.txt` | Snapshot dependency cấp repository nếu cần. |

---

## Các module

### `mobilerun-cli`

Module này dùng để kiểm tra nhanh workflow MobileRun bằng CLI.  
Nó hữu ích khi cần xác nhận thiết bị Android, ADB, MobileRun Portal và LLM provider đã được cấu hình đúng.

Nên dùng module này đầu tiên khi setup MobileRun trên máy hoặc thiết bị mới.

---

### `mobilerun-cloud-llm`

Module này minh họa cách dùng MobileRun thông qua Python SDK với cloud LLM provider.

Ví dụ hiện tại dùng OpenAI thông qua provider `OpenAIResponses`.  
Chế độ này phù hợp với các app Android có UI phức tạp hoặc dynamic, vì cloud model mạnh thường có khả năng reasoning, chọn action và phục hồi lỗi tốt hơn.

---

### `mobilerun-local-llm`

Module này minh họa cách dùng MobileRun thông qua Python SDK với model Ollama local.

Model local mặc định trong repository này là:

```text
qwen3.5:4b
```

Chế độ này phù hợp cho các thử nghiệm riêng tư, chi phí thấp và gần với offline execution.  
Tuy nhiên, model local nhỏ có thể yếu hơn cloud model trong các task UI reasoning phức tạp.

---

## Luồng sử dụng khuyến nghị

Với một thiết bị Android hoặc môi trường phát triển mới, nên test theo thứ tự:

1. Bắt đầu với `mobilerun-cli` để kiểm tra setup thiết bị cơ bản.
2. Dùng `mobilerun-cloud-llm` để test automation với LLM mạnh hơn.
3. Dùng `mobilerun-local-llm` để so sánh khả năng chạy local/private bằng Ollama.

Cách tách module như vậy giúp xác định lỗi đến từ Android setup, cấu hình MobileRun, cloud model hay local model.

---

## Lưu ý bảo mật

Không commit API key thật, token, credentials hoặc file cấu hình riêng tư.

Trong file ví dụ, chỉ dùng placeholder, ví dụ:

```env
OPENAI_API_KEY=REPLACE_WITH_YOUR_OPENAI_API_KEY
```

Các file và thư mục nên ignore:

```gitignore
.env
*.env
!.env.example
.venv/
__pycache__/
trajectories/
*.log
```

Nếu lỡ commit API key thật, hãy revoke hoặc rotate key ngay lập tức trước khi push repository.

---

## Tài liệu

Mỗi submodule có README riêng với hướng dẫn setup chi tiết:

| Module | README |
|---|---|
| CLI mode | `mobilerun-cli/README.md` |
| Cloud LLM mode | `mobilerun-cloud-llm/README.md` |
| Local LLM mode | `mobilerun-local-llm/README.md` |

README ở cấp root chỉ cung cấp tổng quan. Hãy xem README riêng của từng module để biết command setup và chi tiết cấu hình.
