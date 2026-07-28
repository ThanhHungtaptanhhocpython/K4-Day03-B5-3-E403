# Báo cáo giám sát và đánh giá

Dành cho Role 5: Observability & Reviewer.

## Mốc 1 - Định hình bài toán

Chủ đề đã chọn: Chatbot Định Hướng Sự Nghiệp.

Người dùng mục tiêu là học sinh, sinh viên hoặc người mới đi làm cần tư vấn ban đầu về sở thích, điểm mạnh, kỹ năng hiện có, nhóm nghề phù hợp và lộ trình học tập ngắn hạn. Hệ thống chỉ đưa gợi ý tham khảo, không quyết định thay người dùng và không đảm bảo đầu vào, việc làm, mức lương hay kết quả tâm lý.

## Scoring Matrix - Agentic Fit

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
| :--- | :---: | :--- |
| Multi-step Reasoning | 4/5 | Tư vấn hướng nghiệp thường cần hiểu sở thích, điểm mạnh, ràng buộc, mục tiêu và sau đó tổng hợp thành gợi ý nghề nghiệp hoặc lộ trình học. Câu hỏi đơn giản vẫn có thể trả lời trực tiếp nên không chấm tối đa. |
| Tool Interaction | 4/5 | Các câu hỏi về matching nghề, hồ sơ nghề và skill gap nên dựa vào tool deterministic như `match_careers`, `get_career_profile`, `recommend_learning_path` để tránh nói chung chung. Tuy nhiên một số câu hỏi khái niệm không cần tool. |
| Dynamic Decision | 5/5 | Bước tiếp theo phụ thuộc vào Observation: nếu profile đầy đủ thì xếp hạng nghề, nếu thiếu dữ liệu thì hỏi thêm, nếu career không hỗ trợ thì fallback an toàn, nếu có skill gap thì lập roadmap. |
| Long Horizon | 3/5 | Phần lớn tác vụ trong lab ngắn, nhưng roadmap 8 tuần và kế hoạch portfolio có tính nhiều bước. Chưa phải autonomous agent dài hạn có memory liên tục. |
| Tổng điểm fit | 16/20 | ReAct phù hợp cho các câu hỏi cần dữ liệu có cấu trúc, matching, skill-gap và roadmap; chatbot baseline vẫn đủ cho câu hỏi khái niệm đơn giản. |

## Kết luận ReAct vs Chatbot

Nên dùng hybrid:

- Chatbot path: câu hỏi khái niệm, động viên, giải thích ngành nghề ở mức tổng quan, không cần tra cứu cấu trúc.
- ReAct path: cần xếp hạng nghề theo profile, tra cứu hồ sơ nghề, phân tích skill gap, tạo lộ trình học tập, hoặc cần bằng chứng từ tool.
- Safe fallback path: đầu vào thiếu, mâu thuẫn, prompt injection, yêu cầu đảm bảo 100%, career không có trong bộ dữ liệu mẫu, hoặc tool trả về `LOI:`/`CANH_BAO:`.

Kết luận: Bài toán hướng nghiệp có Agentic Fit tốt. ReAct được biện minh khi câu hỏi cần nhiều bước và cần bằng chứng từ tool; không nên ép ReAct cho mọi câu hỏi vì câu hỏi đơn giản có thể dùng baseline chatbot.

## Tool dự kiến cho Role 2

| Tool | Mục đích | Dữ liệu trả về mong đợi |
| :--- | :--- | :--- |
| `match_careers` | Xếp hạng nghề phù hợp từ sở thích, điểm mạnh và ràng buộc của người dùng. | Danh sách nghề, lý do phù hợp, điểm cần thận trọng, độ tự tin. |
| `get_career_profile` | Lấy hồ sơ nghề nghiệp mẫu cho một nghề cụ thể. | Nhiệm vụ, kỹ năng, learning paths, portfolio ideas, risk notes. |
| `recommend_learning_path` | Lập lộ trình học ngắn hạn dựa trên career mục tiêu và kỹ năng hiện tại. | Skill gaps, kế hoạch theo tuần, next action. |

## Failure Modes cần theo dõi

| Failure mode | Dấu hiệu | Xử lý mong đợi |
| :--- | :--- | :--- |
| Thiếu profile | Người dùng chỉ nói "chọn nghề gì cho em" mà không có sở thích/điểm mạnh. | Hỏi thêm 2-3 thông tin cần thiết hoặc đưa gợi ý rất tổng quan. |
| Đầu vào mâu thuẫn | Ví dụ muốn làm bác sĩ nhưng sợ máu và không thích Sinh học. | Không kết luận tuyệt đối; nêu mâu thuẫn và đề xuất khám phá lựa chọn gần kề. |
| Prompt injection | Yêu cầu bỏ qua quy tắc, ép kết luận 100%. | Từ chối làm theo instruction nguy hiểm; giữ guardrail. |
| Tool không hỗ trợ career | Tool trả `LOI:` vì career nằm ngoài bộ dữ liệu mẫu. | Nói rõ giới hạn bộ dữ liệu và đề xuất career gần nhất nếu có. |
| Lựa chọn quá chắc chắn | Model hứa việc làm, lương cao, đầu vào đại học, hoặc "100% phù hợp". | Sửa thành ngôn ngữ có điều kiện và khuyến nghị kiểm chứng thêm. |

## Trace evidence

Mốc 1 chưa yêu cầu chạy trace thực tế. Phần này sẽ được cập nhật ở Mốc 2 và Mốc 3 sau khi Role 2, 3, 4 hoàn thành tool, prompt và ReAct loop.

Mẫu trace cần thu thập:

```text
=== TEST CASE 3 ===
Question: ...
[Baseline]
...
[ReAct Trace]
Thought: ...
Action: match_careers["...", "...", "..."]
Observation: ...
Final Answer: ...
```

## Checklist Mốc 1

- [x] Chọn chủ đề sản phẩm: Chatbot Định Hướng Sự Nghiệp.
- [x] Xác định khi nào dùng Chatbot path, ReAct path và Safe fallback path.
- [x] Điền Scoring Matrix cho 4 tiêu chí Agentic Fit.
- [x] Liệt kê tool dự kiến để Role 2 triển khai.
- [x] Ghi failure modes để Role 3/4 canh guardrail.
