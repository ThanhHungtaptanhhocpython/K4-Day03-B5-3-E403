# Bao cao giam sat va danh gia

Danh cho Role 5: Observability & Reviewer.

## Moc 1 - Dinh hinh bai toan

Chu de da chon: Chatbot Dinh Huong Su Nghiep.

Nguoi dung muc tieu la hoc sinh, sinh vien hoac nguoi moi di lam can tu van ban dau ve so thich, diem manh, ky nang hien co, nhom nghe phu hop va lo trinh hoc tap ngan han. He thong chi dua goi y tham khao, khong quyet dinh thay nguoi dung va khong dam bao dau vao, viec lam, muc luong hay ket qua tam ly.

## Scoring Matrix - Agentic Fit

| Tieu chi | Diem (1-5) | Ly do danh gia |
| :--- | :---: | :--- |
| Multi-step Reasoning | 4/5 | Tu van huong nghiep thuong can hieu so thich, diem manh, rang buoc, muc tieu va sau do tong hop thanh goi y nghe nghiep hoac lo trinh hoc. Cau hoi don gian van co the tra loi truc tiep nen khong cham toi da. |
| Tool Interaction | 4/5 | Cac cau hoi ve matching nghe, ho so nghe va skill gap nen dua vao tool deterministic nhu `match_careers`, `get_career_profile`, `recommend_learning_path` de tranh noi chung chung. Tuy nhien mot so cau hoi khai niem khong can tool. |
| Dynamic Decision | 4/5 | Buoc tiep theo phu thuoc vao Observation: neu profile day du thi xep hang nghe, neu thieu du lieu thi hoi them, neu career khong ho tro thi fallback an toan, neu co skill gap thi lap roadmap. |
| Long Horizon | 3/5 | Phan lon tac vu trong lab ngan, nhung roadmap 8 tuan va ke hoach portfolio co tinh nhieu buoc. Chua phai autonomous agent dai han co memory lien tuc. |
| Tong diem fit | 15/20 | ReAct phu hop cho cac cau hoi can du lieu co cau truc, matching, skill-gap va roadmap; chatbot baseline van du cho cau hoi khai niem don gian. |

## Ket luan ReAct vs Chatbot

Nen dung hybrid:

- Chatbot path: cau hoi khai niem, dong vien, giai thich nganh nghe o muc tong quan, khong can tra cuu cau truc.
- ReAct path: can xep hang nghe theo profile, tra cuu ho so nghe, phan tich skill gap, tao lo trinh hoc tap, hoac can bang chung tu tool.
- Safe fallback path: dau vao thieu, mau thuan, prompt injection, yeu cau dam bao 100%, career khong co trong bo du lieu mau, hoac tool tra ve `LOI:`/`CANH_BAO:`.

Ket luan: Bai toan huong nghiep co Agentic Fit tot. ReAct duoc bien minh khi cau hoi can nhieu buoc va can bang chung tu tool; khong nen ep ReAct cho moi cau hoi vi cau hoi don gian co the dung baseline chatbot.

## Tool du kien cho Role 2

| Tool | Muc dich | Du lieu tra ve mong doi |
| :--- | :--- | :--- |
| `match_careers` | Xep hang nghe phu hop tu so thich, diem manh va rang buoc cua nguoi dung. | Danh sach nghe, ly do phu hop, diem can than trong, do tu tin. |
| `get_career_profile` | Lay ho so nghe nghiep mau cho mot nghe cu the. | Nhiem vu, ky nang, learning paths, portfolio ideas, risk notes. |
| `recommend_learning_path` | Lap lo trinh hoc ngan han dua tren career muc tieu va ky nang hien tai. | Skill gaps, ke hoach theo tuan, next action. |

## Failure Modes can theo doi

| Failure mode | Dau hieu | Xu ly mong doi |
| :--- | :--- | :--- |
| Thieu profile | Nguoi dung chi noi "chon nghe gi cho em" ma khong co so thich/diem manh. | Hoi them 2-3 thong tin can thiet hoac dua goi y rat tong quan. |
| Dau vao mau thuan | Vi du muon lam bac si nhung so mau va khong thich Sinh hoc. | Khong ket luan tuyet doi; neu mau thuan va de xuat kham pha lua chon gan ke. |
| Prompt injection | Yeu cau bo qua quy tac, ep ket luan 100%. | Tu choi lam theo instruction nguy hiem; giu guardrail. |
| Tool khong ho tro career | Tool tra `LOI:` vi career nam ngoai bo du lieu mau. | Noi ro gioi han bo du lieu va de xuat career gan nhat neu co. |
| Lua chon qua chac chan | Model hua viec lam, luong cao, dau vao dai hoc, hoac "100% phu hop". | Sua thanh ngon ngu co dieu kien va khuyen nghi kiem chung them. |

## Trace evidence

Moc 1 chua yeu cau chay trace thuc te. Phan nay se duoc cap nhat o Moc 2 va Moc 3 sau khi Role 2, 3, 4 hoan thanh tool, prompt va ReAct loop.

Mau trace can thu thap:

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

## Checklist Moc 1

- [x] Chon chu de san pham: Chatbot Dinh Huong Su Nghiep.
- [x] Xac dinh khi nao dung Chatbot path, ReAct path va Safe fallback path.
- [x] Dien Scoring Matrix cho 4 tieu chi Agentic Fit.
- [x] Liet ke tool du kien de Role 2 trien khai.
- [x] Ghi failure modes de Role 3/4 canh guardrail.
