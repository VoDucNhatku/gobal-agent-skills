# Dispatch Protocol — chỉ đọc khi thật sự fan-out

> `admin/SKILL.md` chỉ `Read` file này khi request đã qua cửa **heavy path** (đa bước
> HOẶC đa skill). Fast path không bao giờ chạm tới đây. Đọc một lần, không đọc lại.

---

## Worker registry

Một dòng mỗi worker. Chi tiết bên trong worker chỉ load just-in-time trong subagent
chạy nó.

```
RESEARCH (topic-agnostic — suy ra research context rồi inject vào từng spec)
  paper-triage       — xếp hạng corpus theo 1 câu hỏi (entry point rẻ nhất)
  paper-read         — 1 paper, depth gist|summary|eli5|mindmap|think
  paper-method       — 1 paper, method sâu: critique | recipe
  paper-synthesize   — nhiều paper: compare | taxonomy | gaps | expand
  knowledge-graph    — typed triples + master graph tích lũy (merge offload sang script)
  vi-translate       — dịch đầy đủ, trung thành (param --to <lang>)

PAPER WRITING (chuỗi TUẦN TỰ — paper-writing-integrity §6; chỉ figure chạy song song)
  paper-submission   — draft | format | rebuttal (template venue, kỷ luật TODO)
  paper-storytelling — cấu trúc SARD + pipeline/headline figure (thay khâu draft)
  latex-tikz-generator — TikZ/pgfplots figure (khâu DUY NHẤT an toàn chạy song song)
  citation-guard     — zero-orphan + verify DOI + synthesis scan
  style-humanizer    — hiệu chỉnh văn phong DƯỚI bất biến bảo toàn nghĩa §4
  ieee-q1-devil-advocate — phản biện tiền-nộp, đối chiếu claims-ledger

CODE & RUN MODELS
  code-senior        — implement/debug/review, có Algorithm Justification Gate
  understand-codebase— map repo lạ thành summary bounded token
  tdd-enforcer       — RED → GREEN → REFACTOR nghiêm ngặt
  debug-investigator — root-cause trước, không sửa khi chưa có giả thuyết falsifiable
  spec-writer        — spec yêu cầu có gate review
  code-reviewer      — review 6 trục, test trước implementation
  paper-to-notebook  — paper → .ipynb chạy được (reproduce|run-results)
  run-on-modal       — paper → modal_app.py trên serverless GPU (+cost)

WEB & UI (theme-neutral — style đến từ design brief của project, không từ registry này)
  design-web         — hướng thiết kế anti-slop + tokens + preview HTML → design-record
  build-ui           — component | page | admin | scaffold từ design-record đã lock
  build-admin-dashboard — CRUD admin surface, phân quyền server-side + analytics
  scaffold-course-platform — khung dự án LMS/bán khóa học trên course domain model
  fullstack-builder  — dựng trọn 1 feature xuyên frontend + backend
  review-frontend    — audit slop + a11y + token, driven bằng screenshot → report HTML
  backend-engineer   — API contract-first + hardening biên bảo mật
  security-review    — STRIDE + rubric kiểu OWASP

UTIL / GOVERNANCE
  latex-fix          — sửa KaTeX/MathJax hàng loạt trên notes/
  audit-log          — log quyết định đã lọc theo materiality (gọi tại điểm quyết định)
  artifact-manager   — track artifact + check reuse trước khi đọc lại (mode `reuse`)
  token-budget       — ước tính chi phí trước fan-out
  hallucination-guard— scan bịa đặt, BẮT BUỘC trước khi claim done
```

---

> **Test fan-out đã chạy ở `admin/SKILL.md` rồi** (≥2 việc con độc lập · mỗi việc ≥2k
> token · scope rõ). Đọc được tới đây tức là đã qua test hoặc user gõ `admin sâu`.
> Tiêu chí nằm ở SKILL.md chứ không ở đây — nếu để dưới này thì phải trả 3.9k token
> mới biết là *không* nên trả.

## Model Selection Policy

| Model | Dùng cho |
|---|---|
| Haiku | Triage, trích xuất đơn giản, đọc gist |
| Sonnet | Implement, code, dựng UI, phân tích method sâu (mặc định) |
| Opus | Synthesis phức tạp, suy luận, lập kế hoạch xuyên domain |

---

## Procedure

### Phase 0 — Clarify & classify (tiếng Việt)
Đọc goal từ `$ARGUMENTS` hoặc hội thoại. Quy về **domain** (research / code / web /
mixed) và **target cụ thể** (paper id, surface, lựa chọn stack). Xem `notes/INDEX.md`
TRƯỚC để biết cái gì đã có (reuse). Hỏi **tối đa 1 câu**, và chỉ khi nó chặn việc lập
kế hoạch; còn lại cứ tiến hành.

### Phase 1 — Quyết định độ sâu (mặc định là đơn giản)
- **SOLO (không subagent)** khi một skill rõ ràng phủ được goal, hoặc task rẻ / phụ
  thuộc / tương tác → invoke worker inline.
- **Fan out** chỉ khi sub-task thật sự độc lập *và* giá trị biện minh được chi phí.

### Phase 2 — Lập kế hoạch & viết context cho từng co-worker
Mỗi sub-task cần một spec 4 phần (đây là toàn bộ context subagent isolated nhận được —
nó **không** thấy lịch sử của admin):

```markdown
## Objective
[Một dòng: làm gì, cho target nào — vd "tóm tắt bài 003"]

## Output Format
- Skill: [tên skill]  · Mode: [mode nếu có]
- Write to: [path — vd notes/003-read-summary.md]
- Return: CHỈ đường dẫn đã lưu + 5–8 ý chính tiếng Việt. KHÔNG dump nội dung file.

## Tools & Sources
- Reuse: [artifact notes/ đã có cần check trước]
- Read: [chỉ những gì cần thiết]

## Boundaries & Settings
- Model: [Haiku triage | Sonnet code/method | Opus synthesis]
- Single-pass · không wander sang scope worker khác · không dump file vào reply
```

Suy ra **shared context một lần** (chủ đề nghiên cứu / stack / design brief) rồi inject
chỉ lát cắt liên quan vào từng spec. Ghi plan vào `notes/INDEX.md` (và TodoWrite nếu có)
để nó sống sót qua context compaction.

→ **Audit (`scope-decision`):** khi cố ý include/exclude một paper/topic/surface và lựa
chọn đó không hiển nhiên → theo skill `audit-log`. Bỏ qua với plan thường quy.

### Phase 3 — Dispatch & control
- **Việc độc lập → nhiều `Task` call trong MỘT message** = subagent song song trong
  context cô lập. Nhắm 3–5 concurrent khi việc chia sạch. Mỗi subagent invoke worker
  được giao, đọc/ghi nặng trong context **riêng**, chỉ trả về path + summary 1–2k token
  — context của admin không bao giờ thấy PDF/repo/artifact đầy đủ.
- **Việc nhanh hoặc phụ thuộc →** invoke worker inline.
- **Scale effort:** tìm 1 dữ kiện → 1 worker; so sánh → 2–4; đọc sâu nhiều paper hoặc
  dựng nguyên platform → nhiều, chia nhỏ.
- **Monitor:** subagent trả về rỗng, lỗi, hoặc ghi file ngắn bất thường → re-dispatch
  **một lần** với chỉ dẫn rõ hơn trước khi báo thất bại.
- **Ví dụ mixed-domain** ("dựng LMS + theme + trang quản trị"): `build-ui scaffold`
  **trước** (khung project, chưa cần design-record) → `design-web` (lock design-record)
  → song song `build-ui admin` + `build-ui component` cho các surface chính →
  `review-frontend`. Tuần tự phần phụ thuộc, song song phần còn lại.

### Phase 3b — Corpus ingest (N paper lớn — fan-out bounded token)
Goal là "hiểu / trích xuất kiến thức từ N paper" với N lớn (≳8) → **không** deep-read mù:

1. **Triage trước (1 inline call).** `paper-triage` xếp hạng cả corpus từ abstract +
   dòng gist trong `notes/INDEX.md` (không mở note body) → plan kèm worker `next` cho
   từng id. Chỉ riêng bước này đã cho biết paper nào đáng đọc đắt.
2. **Shard các deep-read.** Gom id cần đọc sâu thành shard ~8–12. Dispatch theo **wave
   4–5 `Task` call** (1 subagent/shard, chạy `paper-read` summary rồi tùy chọn
   `paper-method`). Mỗi subagent chạy trong context **riêng**, trả về CHỈ path + manifest
   ≤2k token — không bao giờ trả text PDF hay body file. **Raw paper text do đó không
   bao giờ vào context của admin.**
3. **Merge rẻ, rồi drop.** Sau mỗi wave, merge các row trả về vào `notes/INDEX.md` (key
   theo `id+worker` để lần chạy lại với mode mới ghi đè chứ không nhân bản) và **bỏ
   manifest của wave khỏi working context** — từ đó chỉ dựa vào INDEX rẻ.
4. **Trích xuất tri thức (tùy chọn).** Fan out `knowledge-graph` trên các id đã đọc;
   merge offload sang script, master graph **không bao giờ đọc ngược** vào context —
   chỉ script chạm vào nó. Admin chỉ lấy counts từ stdout.
5. **Synthesis ở quy mô corpus.** Đưa `paper-synthesize` (compare/taxonomy/gaps) cả
   corpus — nhưng nó suy luận trên INDEX gist + master graph summary, KHÔNG phải N
   distillate đầy đủ (tự shard nếu cần sâu hơn). Mỗi claim phải có id nguồn.
6. **Math sweep (tùy chọn).** Chạy `latex-fix` lint trên `notes/` mới sinh nếu synthesis
   có công thức.

**Net: chi phí admin ~tuyến tính theo số shard, không theo số trang.**

### Phase 4 — Collect
Verify mọi artifact kỳ vọng có tồn tại thật. Cập nhật `notes/INDEX.md`
(`id · worker · path · gist một dòng`). Gom các ý chính trả về. Chỉ mở full artifact khi
synthesis thật sự cần body của nó.

### Phase 5 — Synthesize
Tạo ra đúng deliverable mà goal yêu cầu — bảng so sánh xuyên paper, draft related-work,
danh sách gap, feature đã dựng — suy luận trên **summary đã distill** (không phải raw
dump), có trích id. **Không chỉ nối file của các worker lại.**

→ **Audit (`synthesis-framing` / `cross-source-assumption`):** khi chọn lăng kính tổng
hợp, hoặc khi coi hai nguồn là liên quan mà không có bằng chứng tường minh → theo skill
`audit-log`. Bỏ qua khi chỉ có một cách framing hợp lý.

### Phase 6 — Self-check rồi Report
**BẮT BUỘC trước khi claim done:** `hallucination-guard` mode `scan` trên deliverable —
mỗi claim phải có source (paper id / file path / section). Có claim không nguồn →
**refuse ngay**, chỉ rõ cái gì thiếu, regain bằng cách đọc đúng source, fix, scan lại.

Scan bao gồm cả **evaluative claim** (novelty tier, venue-worthiness, "expected gain")
theo `~/.claude/rules/research-proposal-integrity.md` §6: venue claim thiếu tier + điều
kiện, hoặc công thức thiếu provenance tag (`[cited]`/`[derived]`/`[design]`) → FAIL như
claim không nguồn.

Rồi trả lời tiếng Việt gọn: đã làm gì, kết quả tổng hợp (hoặc vị trí `notes/` của nó),
và link tới từng artifact.

---

## Gotchas

- **Đừng fan-out cho việc rẻ.** Một bản tóm tắt hay một component là inline call, không
  phải subagent.
- **Mỗi subagent chỉ được trả path + summary** — nếu spec cho phép subagent dump nguyên
  file về, token economy vỡ.
- **Tuần tự hóa phần phụ thuộc.** Scaffold trước khi theme; đọc trước khi synthesize;
  triage trước khi deep-read corpus lớn.
- **Đừng tự cài lại một worker.** Không worker nào khớp → tự làm và ghi chú rằng có thể
  đáng dựng worker mới — đừng ép worker ra ngoài scope của nó.
- **Context isolation là bất khả xâm phạm.** Admin không bao giờ đọc raw PDF, không bao
  giờ đọc master knowledge graph, không bao giờ đọc lại full note body sau khi merge.

## Cross-cutting (auto-invoke khi fan-out)

| Skill | Khi nào |
|---|---|
| `token-budget` | Ước tính chi phí TRƯỚC fan-out |
| `artifact-manager` (mode `reuse`) | Trước khi tạo artifact mới / đọc lại nguồn |
| `audit-log` | Tại điểm quyết định non-obvious (scope, framing) |
| `context-compressor` | Khi context phình gần giới hạn |
| `hallucination-guard` | BẮT BUỘC trước khi claim done |
| `self-evaluator` | Cổng cuối trước khi giao |

> Cross-cutting riêng của research pipeline (`hallucination-guard`, `knowledge-graph`,
> `latex-fix`) do `research-admin` tự quản lý khi đã route sang đó — admin KHÔNG invoke
> chúng trực tiếp nữa.
