# K4-Day03-B5-3-E403 - Chatbot Định Hướng Sự Nghiệp

Repo này là bài Lab 03: Chatbot vs ReAct Agent, được tuỳ biến theo đề tài **Chatbot Định Hướng Sự Nghiệp**. Mục tiêu là so sánh chatbot baseline không dùng tool với ReAct Agent có khả năng suy luận, gọi tool, đọc Observation và dùng guardrail an toàn.

## Tóm Tắt Dự Án

Hệ thống hỗ trợ học sinh, sinh viên hoặc người mới đi làm trong các tác vụ:

- gợi ý nhóm nghề dựa trên sở thích, điểm mạnh và kỹ năng hiện có;
- tra cứu nghề nghiệp, kỹ năng cần có, khóa học, việc làm mẫu và roadmap học tập;
- tạo trace `Thought -> Action -> Observation -> Final Answer` để đánh giá agent;
- so sánh khi nào nên dùng chatbot baseline và khi nào nên dùng ReAct Agent;
- xử lý an toàn các yêu cầu thiếu dữ liệu, mâu thuẫn, prompt injection hoặc đòi hỏi cam kết 100%.

Hệ thống chỉ đưa ra gợi ý tham khảo. Không đảm bảo việc làm, mức lương, đầu vào đại học, kết quả tâm lý hay mức độ phù hợp tuyệt đối.

## Kiến Trúc Chính

Repo minh họa 4 cấp độ AI hội thoại:

| Cấp độ | Thành phần | Vai trò trong repo |
| :---: | :--- | :--- |
| 1 | Rule-Based Bot | Demo lịch sử trong `src/ai_levels/level1_rule_based.py` |
| 2 | LLM Chatbot | Baseline trong `CHATBOT_BASELINE_PROMPT`, không gọi tool |
| 3 | ReAct Agent | Vòng lặp trong `src/app.py`, gọi tool từ `AVAILABLE_TOOLS` |
| 4 | Autonomous Agent | Bonus planning/memory trong `src/ai_levels/level4_autonomous_agent.py` và tool memory |

Luồng chạy chính:

```text
config/test_cases.json
        -> src/app.py
        -> src/prompts.py
        -> provider.generate(...)
        -> Action + Action Input
        -> src/tools.py / AVAILABLE_TOOLS
        -> Observation
        -> Final Answer hoặc safe fallback
        -> docs/trace_eval.md
```

## Cấu Trúc Thư Mục

```text
K4-Day03-B5-3-E403/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- config/
|   `-- test_cases.json
|-- src/
|   |-- app.py
|   |-- prompts.py
|   |-- providers.py
|   |-- tools.py
|   `-- ai_levels/
|-- docs/
|   |-- CODELAB.md
|   |-- DANH_SACH_DE_TAI.md
|   |-- PHAN_CONG_CONG_VIEC.md
|   |-- trace_eval.md
|   `-- hybrid_flowchart.mermaid
`-- .codex/
    `-- skills/
        |-- career-product-observability/
        |-- career-tool-engineer/
        `-- career-prompt-integrator/
```

## Phân Công Role

Theo `docs/PHAN_CONG_CONG_VIEC.md`:

| Role | Người phụ trách | MSV | File chính |
| :--- | :--- | :--- | :--- |
| Role 1: Product Architect | Phạm Thanh Hưng | 2A202601468 | `config/test_cases.json` |
| Role 2: Tool Engineer | Phạm Minh Hiếu | 2A202601562 | `src/tools.py` |
| Role 3: Prompt Engineer | Nguyễn Thế Khiêm | 2A202601036 | `src/prompts.py` |
| Role 4: Core Developer / Integrator | Nguyễn Thế Khiêm | 2A202601036 | `src/app.py` |
| Role 5: Observability | Phạm Thanh Hưng | 2A202601468 | `docs/trace_eval.md` |

Các AI Agent hỗ trợ làm việc theo skill:

- `career-product-observability`: Role 1 và Role 5.
- `career-tool-engineer`: Role 2.
- `career-prompt-integrator`: Role 3 và Role 4.

## Tool Hiện Có

`src/tools.py` đang dùng mock data offline và đăng ký các tool sau trong `AVAILABLE_TOOLS`:

| Tool | Mục đích |
| :--- | :--- |
| `get_user_profile` | Lấy hồ sơ người dùng mẫu theo `user_id` |
| `save_user_profile` | Lưu/cập nhật hồ sơ người dùng |
| `run_personality_assessment` | Chạy trắc nghiệm MBTI/Holland/DISC mock |
| `search_careers` | Tìm nghề theo keyword và filter whitelist |
| `match_career_recommendations` | Xếp hạng nghề dựa trên profile và danh sách nghề |
| `search_courses_schools` | Tìm khóa học/trường học theo nghề, level, location |
| `web_search` | Mock web search, không gọi Internet thật |
| `search_jobs` | Tìm tin tuyển dụng mẫu |
| `generate_cv` | Tạo CV dạng `.txt` từ hồ sơ hợp lệ |
| `generate_career_roadmap` | Tạo roadmap học tập/nghề nghiệp |
| `save_conversation_memory` | Lưu tóm tắt phiên sau khi lọc prompt injection |

Lưu ý: một số tool có tính ghi/tác động như `save_user_profile`, `generate_cv`, `generate_career_roadmap`, `save_conversation_memory` được app yêu cầu xác nhận trước khi gọi.

## Cài Đặt Môi Trường

Yêu cầu Python 3.10+.

Trên Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

## Cấu Hình LLM Provider

Mở file `.env` và chọn provider:

```env
LLM_PROVIDER=mock
LLM_MODEL=
```

Provider được hỗ trợ:

- `mock`: chạy offline, không cần API key.
- `gemini`: cần `GEMINI_API_KEY`.
- `openai`: cần `OPENAI_API_KEY`.
- `anthropic`: cần `ANTHROPIC_API_KEY`.
- `openrouter`: cần `OPENROUTER_API_KEY`.

Nếu muốn chạy nhanh không tốn phí hoặc không có key, dùng `LLM_PROVIDER=mock`. Nếu dùng provider thật, điền đúng API key vào `.env` và không commit file `.env`.

## Cách Chạy

Chạy so sánh baseline và ReAct:

```powershell
python src/app.py
```

Chạy riêng baseline:

```powershell
$env:APP_MODE="baseline"
python src/app.py
```

Chạy riêng ReAct:

```powershell
$env:APP_MODE="react"
python src/app.py
```

Chạy lại chế độ mặc định:

```powershell
$env:APP_MODE="compare"
python src/app.py
```

Trên macOS/Linux:

```bash
APP_MODE=react python src/app.py
```

## Kiểm Tra Nhanh

Kiểm tra syntax Python:

```bash
python -m py_compile src/tools.py src/prompts.py src/app.py src/providers.py
```

Kiểm tra tool registry:

```bash
python src/tools.py
```

Kiểm tra provider adapter:

```bash
python src/providers.py
```

Kiểm tra app:

```bash
python src/app.py
```

## Test Cases

`config/test_cases.json` có 5 case chính:

1. Câu hỏi đơn giản, chatbot có thể trả lời trực tiếp.
2. Câu hỏi safety về việc có đảm bảo việc làm/lương cao hay không.
3. Multi-step một tool, gợi ý nghề cho sở thích vẽ, kể chuyện và công nghệ.
4. Multi-step hai tool, Data Analyst và roadmap 8 tuần.
5. Edge case prompt injection, yêu cầu kết luận 100% phù hợp với bác sĩ.

Các case này dùng để chứng minh nên dùng hybrid: câu đơn giản đi chatbot path, câu cần dữ liệu có cấu trúc đi ReAct path, đầu vào nguy hiểm đi safe fallback path.

## Báo Cáo Và Artifact Cần Nộp

Artifact quan trọng:

- `config/test_cases.json`: bộ test cases của Role 1.
- `src/tools.py`: tool registry và mock data của Role 2.
- `src/prompts.py`: baseline prompt, ReAct prompt và guardrails của Role 3.
- `src/app.py`: baseline runner, ReAct loop, parser và executor của Role 4.
- `docs/trace_eval.md`: scoring matrix, baseline log, ReAct trace, failure analysis của Role 5.
- `docs/hybrid_flowchart.mermaid`: sơ đồ phân luồng Chatbot/ReAct/Safe fallback.
- `.codex/skills/`: skill cho các AI Agent cộng tác.

## Quy Tắc Code Chung

- Giữ nhất quán đề tài hướng nghiệp, không để lại demo thời tiết/chuyến bay trong artifact nộp bài.
- Baseline không được gọi tool.
- ReAct Agent phải tạo trace có `Thought`, `Action`, `Observation`, `Final Answer`.
- App là nơi tạo Observation sau khi thực thi tool; model không được tự bịa Observation.
- Tool phải deterministic, offline-friendly và không crash khi input sai.
- Lỗi nghiệp vụ nên trả về `error`, `error_message`, `success=False`, hoặc fallback an toàn để app tiếp tục xử lý.
- Không đảm bảo 100% về nghề nghiệp, việc làm, mức lương, đầu vào hay kết quả tâm lý.
- Không commit `.env`, API key, token, PII, cache hoặc `__pycache__`.

## Trạng Thái Hiện Tại

Repo đã có:

- 5 test cases theo chủ đề Chatbot Định Hướng Sự Nghiệp.
- Prompt baseline và ReAct đã chuyển sang miền hướng nghiệp.
- 10 tool mock trong `src/tools.py`.
- App có `APP_MODE=baseline|react|compare`, parser Action Input JSON và guardrail `MAX_ITERATIONS`.
- Báo cáo `docs/trace_eval.md` ghi nhận Agentic Fit, baseline log, ReAct trace và failure modes.
- Flowchart hybrid tại `docs/hybrid_flowchart.mermaid`.
- Skill AI Agent trong `.codex/skills/`.

Theo trace hiện tại, ReAct Agent đã có guardrail và tool execution thật, nhưng vẫn cần tiếp tục tối ưu tool routing và prompt termination cho một số case multi-step. Chi tiết nằm trong `docs/trace_eval.md`.

## Git Workflow Gợi Ý

Trước khi sửa:

```bash
git pull
```

Sau khi hoàn thành phần việc:

```bash
git status
git add <files>
git commit -m "Role X: mô tả ngắn gọn"
git push
```

Không dùng `git reset --hard` hoặc xóa thay đổi của người khác nếu chưa được yêu cầu rõ.