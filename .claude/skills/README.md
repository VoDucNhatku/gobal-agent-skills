# GOBAL Agent Skills — thư mục cài đặt

Thư mục này là thứ được copy vào `~/.claude/skills/`.

**Tài liệu đầy đủ (66 skill, kiến trúc, token economy) nằm ở README gốc của repo.**

## Có gì trong đây

| Đường dẫn | Là gì |
|---|---|
| `<tên-skill>/SKILL.md` | 66 skill, mỗi thư mục một skill |
| `admin/references/dispatch-protocol.md` | Quy trình điều phối nặng — `admin` chỉ đọc khi thật sự fan-out |
| `references/ecosystem-research.md` | Ghi chép nghiên cứu 8 repo skill khác (đọc on-demand) |
| `PLAN.md` | Nhật ký kế hoạch/tiến độ của bộ skill |
| `test-framework/scripts/test_skills.py` | Validator cấu trúc cho cả bộ skill |
| `../rules/` | 6 file rule ràng buộc, nhiều skill đọc lúc chạy |

## Điểm vào

Gọi **`admin`** cho mọi thứ — nó tự chọn nhánh rẻ nhất:

| Request | Đi đâu | Chi phí |
|---|---|---|
| Hỏi nhanh · tra cứu · đọc 1 file | `admin` trả lời thẳng | ~1.4k tok |
| Đúng 1 skill phủ được | `admin` gọi thẳng skill đó | + skill |
| Nhiều bước, 1 domain | `research-admin` · `code-admin` · `web-admin` · `deploy-admin` | + sub-admin |
| Đa domain hoặc chạy song song | `admin` đọc `dispatch-protocol.md` → Phase 0–6 | + ~3.9k tok |

Hoặc gõ thẳng tên skill khi đã biết mình cần gì: `/paper-read 003 summary`,
`/paper-synthesize 001 003 008 compare`.

Output: research → `notes/` · notebook → `notebooks/` · Modal app → `modal_apps/`.

## Token economy (4 cơ chế cốt lõi)

1. **Preview-not-dump** — artifact đầy đủ ghi vào `notes/`, chat chỉ in 5–10 dòng + đường dẫn.
2. **Reuse-before-read** — kiểm tra `notes/INDEX.md` trước khi mở lại PDF thô.
3. **Mode-scaling theo cardinality** — N nhỏ đọc sâu; N lớn thì 1 dòng/bài. Output tăng
   tuyến tính, không bùng nổ.
4. **Script-offloading** — skill phát JSON spec rồi gọi script dựng (`kg_builder.py`,
   `nb_builder.py`, `modal_builder.py`, `latex_lint.py`, `audit_append.py`) thay vì tự viết
   boilerplate. Code script không vào context, chỉ output vào.

Cộng với progressive disclosure 3 tầng: metadata (~120 tok/skill, luôn nạp) → SKILL.md body
(chỉ khi trigger) → `references/`, `scripts/` (nạp theo nhu cầu).

## Rules dùng chung (đọc lúc chạy, cite một dòng — không inline)

- `~/.claude/rules/workbench-conventions.md` — song ngữ, output + preview, reuse, fidelity,
  mode-scaling, script-offloading, scope handoff
- `~/.claude/rules/latex-katex-compat.md` — bảng tương thích KaTeX/MathJax
- `~/.claude/rules/research-proposal-integrity.md` — novelty tier, Venue Claim Card, claims ledger
- `~/.claude/rules/paper-writing-integrity.md` — zero fabricated refs, chuỗi viết bản thảo
- `~/.claude/rules/frontend-aesthetics.md` — anti-slop, motion budget
- `~/.claude/rules/course-domain-model.md` — domain model LMS

---

> File này từng liệt kê riêng một danh sách 11 skill và đã trôi lệch khỏi thực tế (còn gọi
> `reading-triage`, `design-ui-direction`, `build-ui-component` — đều đã đổi tên hoặc
> deprecate). Nay chỉ trỏ về README gốc để khỏi phải bảo trì hai danh sách. — 2026-08-01
