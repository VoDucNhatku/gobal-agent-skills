---
name: workbench-admin
description: DEPRECATED alias (2026-08-01) — điều phối đã gộp hết vào admin. Stub này chỉ redirect, không tự điều phối. Nếu bị gọi, chuyển ngay sang admin với cùng input; quy trình Phase 0–6 và worker registry chi tiết nay nằm ở admin/references/dispatch-protocol.md.
argument-hint: (deprecated — dùng admin)
allowed-tools: Skill Read
---

# workbench-admin — DEPRECATED alias → `admin`

Skill này đã ngừng phát triển (2026-08-01). Toàn bộ chức năng điều phối nằm ở
**`admin`** — file này chỉ tồn tại để các tham chiếu cũ không gãy.

## Nếu skill này bị gọi

Chuyển ngay sang `admin` với cùng input.

| Nội dung cũ (workbench-admin) | Nay nằm ở |
|---|---|
| Routing tree, domain registry, fan-out criteria | `admin/SKILL.md` |
| Worker registry chi tiết | `admin/references/dispatch-protocol.md` |
| Procedure Phase 0–6 (clarify → dispatch → collect → synthesize → report) | `admin/references/dispatch-protocol.md` |
| Corpus ingest pipeline (triage → shard → merge → KG → synthesize) | `admin/references/dispatch-protocol.md` § Phase 3b |
| Context spec 4 phần cho subagent | `admin/references/dispatch-protocol.md` § Phase 2 |
| Gotchas | `admin/references/dispatch-protocol.md` § Gotchas |

## Lý do deprecate

`workbench-admin` và `admin` là hai bản điều phối gần trùng khít: **87 trên 174 dòng
của `admin` giống hệt `workbench-admin`**, cùng routing tree, cùng domain table, cùng
fan-out criteria, cùng anti-patterns — chỉ khác chỗ `workbench-admin` có thêm quy trình
Phase 0–6 và worker registry chi tiết hơn.

Giữ cả hai nghĩa là mỗi lần sửa quy tắc điều phối phải sửa hai chỗ, và hai bản chắc chắn
sẽ trôi lệch nhau. Cách gộp **không** phải nối hai file lại — làm vậy thì mọi lần gọi
`admin` (kể cả chỉ để hỏi một câu) đều phải nạp ~5.3k token.

Thay vào đó: phần điều phối nặng (thứ chỉ dùng khi thật sự fan-out) được tách sang
`admin/references/dispatch-protocol.md`, chỉ `Read` khi request rơi vào nhánh 4. Kết quả:
`admin` cho việc rẻ còn **1.449 token** (trước: 2.492 ở `admin`, 3.738 ở
`workbench-admin`), còn quy trình Phase 0–6 tốt hơn của `workbench-admin` vẫn được giữ
nguyên cho việc nặng.
