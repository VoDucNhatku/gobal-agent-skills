# Workbench — bộ skill nghiên cứu global cho Claude Code

Bộ skill global (đặt ở `~/.claude/skills/`, dùng được cho **mọi** project) để **đọc — phân tích —
tổng hợp — viết code — điều phối** tài liệu nghiên cứu học thuật. Hợp nhất **chuẩn Agent Skills
chính thức của Anthropic** (định dạng `SKILL.md`, progressive disclosure) với **độ phủ rộng và
token-economy** học từ bộ AIL-Premium. Giao tiếp **tiếng Việt học thuật**; code/định danh tiếng Anh.

> Theme-neutral: không gắn cứng chủ đề. Mỗi project khai báo ngữ cảnh (paper-ids, chủ đề) trong
> `papers/` + `notes/INDEX.md`; các skill suy ra ngữ cảnh lúc chạy, không hard-code đề tài nào.

## Danh sách skill (11 — nghiên cứu)

| Nhóm | Skill | Làm gì | Mode |
|---|---|---|---|
| **Điều phối** | `workbench-orchestrator` | Con chính: nhận mục tiêu lớn → chia việc → fan-out subagent song song → tổng hợp. Giữ `notes/INDEX.md` làm bộ nhớ chung. | — |
| **Đọc** | `reading-triage` | Xếp hạng cả corpus theo câu hỏi NC (quét abstract) → kế hoạch đọc | single-pass |
| | `paper-read` | Đọc & cô đọng MỘT bài | gist · summary · eli5 · mindmap |
| | `vi-translate` | Dịch trung thực, đầy đủ + glossary | `--to <lang>` |
| **Phân tích** | `paper-method` | Đọc sâu phương pháp MỘT bài | critique · recipe |
| | `knowledge-graph` | Trích entity–relation có kiểu → graph + master graph gộp | single / all |
| **Tổng hợp** | `paper-synthesize` | Tổng hợp NHIỀU bài | compare · taxonomy · gaps · expand |
| **Code** | `paper-to-notebook` | Bài báo → notebook `.ipynb` chạy được | reproduce · run-results |
| | `run-on-modal` | Bài báo → `modal_app.py` GPU serverless + chi phí | reproduce · run-results · inference |
| **Tiện ích** | `latex-fix` | Sửa math render trên cả KaTeX + MathJax | lint → fix |
| | `audit-log` | Nhật ký quyết định material (governance) | log · summary · clear |

(Ngoài ra có nhánh **WEB/UI** — `scaffold-course-platform`, `design-ui-direction`,
`build-ui-component`, `build-admin-dashboard`, `review-frontend` — cho việc dựng web bán khóa học,
không thuộc phạm vi nghiên cứu.)

## Token economy (4 cơ chế cốt lõi — học từ AIL + đúng progressive disclosure của Anthropic)

1. **PREVIEW-NOT-DUMP** — ghi artifact đầy đủ vào `notes/`, chat chỉ in preview 5–10 dòng + đường
   dẫn. Không bao giờ đổ nguyên file vào chat.
2. **REUSE-BEFORE-READ** — trước khi mở PDF thô, kiểm tra `notes/INDEX.md` + artifact đã chưng cất;
   tái dùng nếu còn mới.
3. **Mode-scaling theo cardinality** — N nhỏ thì chi tiết sâu; N lớn (≥5, hay `all`) thì 1 dòng/bài.
   Tổng output tăng tuyến tính, không bùng nổ.
4. **Script-offloading** — skill phát một JSON spec rồi gọi script dựng (`kg_builder.py`,
   `nb_builder.py`, `modal_builder.py`, `latex_lint.py`, `audit_append.py`); **không** tự viết tay
   boilerplate (nbformat JSON, Modal envelope, Mermaid, JSON-line). Code script không vào context —
   chỉ output vào.

→ Cộng với **progressive disclosure 3 tầng của Anthropic**: metadata (name+description, ~100 token,
luôn nạp) → SKILL.md body (chỉ nạp khi trigger, <5k) → references/scripts (nạp theo nhu cầu).

## Luồng "nhiều bài báo" (corpus-ingest — token-bounded)

`workbench-orchestrator` xử lý N bài lớn mà không nổ token:
**triage** (chỉ đọc abstract + INDEX) → **shard** thành ~8–12 nhóm → **fan-out theo lô 4–5 subagent**
(mỗi subagent chạy trong context riêng, **chỉ trả path + summary ≤2k token**, không trả text PDF) →
**merge vào INDEX rồi bỏ manifest** → tổng hợp từ INDEX/master-graph (không nạp lại N bài). Chi phí
orchestrator ~tuyến tính theo số shard, không theo số trang.

## Cách dùng

- **Gõ trực tiếp** một skill: `/paper-read 003 summary`, `/paper-synthesize 001 003 008 compare`.
- **Hoặc** nói mục tiêu lớn cho `/workbench-orchestrator` (vd: "hiểu hết các bài trong papers/, so
  sánh phương pháp và tìm gap") — nó tự điều phối.
- Output research → `notes/`; notebook → `notebooks/`; Modal app → `modal_apps/`.

## Rules dùng chung (đọc lúc chạy, cite một dòng — không inline)

- `~/.claude/rules/workbench-conventions.md` — song ngữ, output + preview, reuse, fidelity,
  mode-scaling, script-offloading, scope handoff.
- `~/.claude/rules/latex-katex-compat.md` — bảng tương thích KaTeX/MathJax cho math.
