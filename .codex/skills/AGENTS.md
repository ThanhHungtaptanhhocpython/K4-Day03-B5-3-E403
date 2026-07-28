# Agent Instructions

Du an nay la Lab 03 "Chatbot vs ReAct Agent" voi de tai "Chatbot Dinh Huong Su Nghiep".

Truoc khi sua code, doc:

- `docs/PHAN_CONG_CONG_VIEC.md`
- `docs/QUY_TAC_CODE_VA_REQUIREMENTS.md`
- skill tuong ung trong `.codex/skills/`

Quy tac chinh:

- Role 1 & 5 chi sua `config/test_cases.json` va `docs/trace_eval.md`.
- Role 2 chi sua `src/tools.py`.
- Role 3 & 4 chi sua `src/prompts.py` va `src/app.py`.
- Neu can sua file ngoai role, neu ro ly do va khong ghi de thay doi cua nguoi khac.
- Giu chu de huong nghiep nhat quan; khong de lai demo thoi tiet/chuyen bay trong artifact nop bai.
- Tool phai deterministic, offline-friendly va tra loi loi bang `LOI:` hoac `CANH_BAO:` thay vi crash.
- Baseline chatbot khong duoc goi tool; ReAct Agent phai co trace `Thought -> Action -> Observation -> Final Answer`.
- Khong commit `.env`, API key, token, PII hoac cache.

Kiem tra toi thieu truoc khi bao hoan thanh:

```bash
python -m py_compile src/tools.py src/prompts.py src/app.py
python src/app.py
```
