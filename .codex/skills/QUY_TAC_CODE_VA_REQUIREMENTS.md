# Quy Tac Code Va Requirement Chung

Tai lieu nay ap dung cho du an "Chatbot Dinh Huong Su Nghiep" trong Lab 03: Chatbot vs ReAct Agent.

## Muc Tieu San Pham

Xay dung mot chatbot/agent huong nghiep giup hoc sinh, sinh vien hoac nguoi moi di lam:

- hieu so thich, diem manh, rang buoc va muc tieu nghe nghiep;
- goi y nhom nghe phu hop dua tren du lieu mau trong tool;
- tra cuu ho so nghe nghiep, ky nang can co va y tuong portfolio;
- de xuat lo trinh hoc tap ngan han;
- so sanh chatbot baseline voi ReAct Agent qua trace co bang chung.

Agent chi dua goi y tham khao. Khong duoc dam bao viec lam, muc luong, dau vao dai hoc, chan doan tam ly, hay ket luan "100% phu hop".

## Pham Vi File Theo Role

- Role 1 & 5: chi phu trach `config/test_cases.json` va `docs/trace_eval.md`.
- Role 2: chi phu trach `src/tools.py`.
- Role 3 & 4: chi phu trach `src/prompts.py` va `src/app.py`.
- Cac file dung chung nhu `README.md`, `requirements.txt`, `.env.example` chi sua khi ca nhom thong nhat.

Neu can sua file ngoai pham vi role, ghi ro ly do trong commit message hoac bao cho nguoi phu trach file do.

## Requirement Chung

San pham hoan thanh phai co:

- 5 test cases dung chu de huong nghiep trong `config/test_cases.json`.
- Baseline chatbot chay khong goi tool.
- ReAct Agent co vong lap `Thought -> Action -> Observation -> Final Answer`.
- Toi thieu 3 tool huong nghiep deterministic trong `src/tools.py`.
- Guardrail `MAX_ITERATIONS` de tranh lap vo han.
- Xu ly loi tool bang chuoi `LOI:` hoac `CANH_BAO:` thay vi crash.
- Trace log trong `docs/trace_eval.md` co it nhat mot case thanh cong va mot edge case/fallback.
- Cac ten tool trong prompt, app, test cases va `AVAILABLE_TOOLS` phai khop nhau.

## Code Rules

Viet code Python theo cac quy tac sau:

- Uu tien code ro rang, de doc, it abstraction.
- Khong hardcode demo thoi tiet/chuyen bay trong san pham huong nghiep.
- Khong goi API that neu chua duoc yeu cau; tool nen chay offline bang data mau.
- Moi tool phai co docstring neu ro purpose, input, output, error behavior va example.
- Tool tra ve string; neu co nhieu truong du lieu, tra ve JSON string hop le.
- App la noi tao `Observation`; model khong duoc tu bia Observation.
- Parser Action phai bao loi an toan khi cu phap sai, tool khong ton tai hoac tham so sai.
- Khong de mot test case loi lam dung toan bo chuong trinh.
- Khong commit `.env`, API key, token, PII hoac file cache.
- Giu output console ngan gon, co cau truc, de Role 5 paste vao bao cao.

## Prompt Rules

Prompt baseline:

- tra loi nhu chatbot huong nghiep thong thuong;
- khong noi da tra cuu tool/database;
- khong dua ket luan tuyet doi ve tuong lai nghe nghiep.

Prompt ReAct:

- liet ke dung tool co trong `AVAILABLE_TOOLS`;
- ep format `Thought`, `Action`, `Observation`, `Final Answer`;
- chi dung `Final Answer` khi da du bang chung hoac khi cau hoi don gian khong can tool;
- khi gap dau vao thieu/mau thuan/nguy hiem, hoi lai hoac fallback an toan.

## Tool Contract Chung

Tool huong nghiep nen theo bo toi thieu:

- `match_careers(interests, strengths, constraints)`
- `get_career_profile(career_name)`
- `recommend_learning_path(target_career, current_skills, duration_weeks)`

Moi tool can:

- chay deterministic voi cung input;
- tra ve du bang chung de agent tong hop;
- co thong diep loi ro rang neu thieu input hoac career khong duoc ho tro;
- khong dua loi khuyen nguy hiem hoac khang dinh qua chac chan.

## Test Va Kiem Tra Truoc Khi Nop

Chay cac lenh sau tu root repo:

```bash
python -m py_compile src/tools.py src/prompts.py src/app.py
python src/app.py
```

Kiem tra thu cong:

- `config/test_cases.json` parse duoc va co dung 5 case.
- Baseline khong goi tool.
- ReAct trace co Action va Observation that tu tool.
- Edge case khong crash va khong ket luan tuyet doi.
- `docs/trace_eval.md` co Agentic Fit, trace va nhan xet so sanh.

## Git Rules

Moi moc nen commit rieng:

- `Moc 1: Scoring Matrix & Dinh hinh`
- `Moc 2: Chatbot Baseline & Tool Specs`
- `Moc 3: ReAct Agent Loop & Safeguards`
- `Moc 4: Cross Audit & Hybrid Flowchart Hoan thanh`

Truoc khi code:

```bash
git pull
```

Sau khi hoan thanh phan viec:

```bash
git status
git add <files-minh-sua>
git commit -m "Role X: mo ta ngan gon"
git push
```

Khong dung `git reset --hard` hoac xoa thay doi cua nguoi khac neu chua duoc yeu cau ro.
