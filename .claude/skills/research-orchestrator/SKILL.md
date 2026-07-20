---
name: research-orchestrator
description: Research domain orchestrator cho GOBAL AGENT — quản lý toàn bộ pipeline nghiên cứu học thuật: scope → triage → shard deep-reads → merge → knowledge graph → synthesis → self-check. Gọi trực tiếp khi request thuộc domain nghiên cứu (đọc bài báo, tổng hợp, phân tích phương pháp so sánh). Chạy độc lập, tự mình quản lý subagents, không qua gobal-orchestrator ở mỗi bước. Modes: scope (domain problem → candidate AI technique families, dùng khi CHƯA có papers/), pipeline (full corpus ingest), triage (filter papers), read (read specific paper), synthesize (combine findings).
argument-hint: <research request> [scope|pipeline|triage|read|synthesize]
allowed-tools: Skill Agent WebSearch WebFetch Read Write Glob Bash
---

# Research Orchestrator

> **Purpose:** Coordinate full-stack academic research pipeline. Owns the corpus workflow from intake to Vietnamese deliverable.
> **Principle:** gobal-orchestrator routes HERE once; from this point, this orchestrator owns the entire research lifecycle autonomously.

## Core Responsibility

This orchestrator is the **sole entry point** for research-centered goals. gobal-orchestrator delegates research requests here; from that point all coordination, fan-out, and synthesis happens within this skill. This keeps gobal-orchestrator lightweight (~50 lines routing table) while research-orchestrator carries the heavy pipeline.

## Modes

| Mode | Pipeline | When to Use |
|------|----------|-------------|
| `scope` | Domain problem → 2–4 candidate AI technique families + search keywords | User có ý tưởng domain nhưng CHƯA có papers/ và chưa biết tìm gì (không ghi file, chỉ trả lời chat) |
| `pipeline` | Full: triage → read → method → synthesize → graph | New research topic with papers in `./papers/` |
| `triage` | Filter + rank only | Large corpus (>12 papers), user wants reading plan first |
| `read` | Read specific paper(s) | User named a paper, need summary/detail |
| `synthesize` | Combine existing findings | Multiple papers already read, need comparison/gaps |

## Mode: scope — domain problem → candidate AI technique families

**Domain-neutral** — không khóa cứng vào 1 lĩnh vực (giáo dục/BA/y tế/...), logic dùng
chung cho mọi domain. Chạy khi user mô tả 1 bài toán cụ thể ("dự đoán học sinh bỏ học",
"tự động hóa phân tích yêu cầu dự án") nhưng `papers/` rỗng hoặc chưa tồn tại — tức là
**trước** khi `triage` có gì để lọc.

**Input:** 1 câu mô tả bài toán domain.

**Việc làm:**
1. Nhận diện loại dữ liệu ngầm định trong bài toán (tĩnh theo bảng / theo chuỗi thời gian
   / văn bản / đồ thị quan hệ...) — đây là tín hiệu chính để chọn nhóm kỹ thuật.
2. Liệt kê **2–4 nhóm kỹ thuật AI** khả dĩ, mỗi nhóm: tên kỹ thuật + 1 dòng lý do khớp
   với loại dữ liệu/bài toán + từ khóa tiếng Anh nên search.
3. **Không bịa từ trí nhớ như sự thật chắc chắn.** Nếu mapping domain→kỹ thuật là kiến
   thức phổ biến, đã ổn định (vd: classification cho bảng dữ liệu tĩnh) → nêu thẳng. Nếu
   là subfield mới/thay đổi nhanh (vd: ứng dụng LLM gần đây) → 1 WebSearch nhanh verify
   trước khi nêu, đừng trình bày như chắc chắn nếu chưa search.
4. **Lọc theo feasibility của user** (research-proposal-integrity §5): user nêu constraint
   (sinh viên/thời gian còn lại/GPU/mục tiêu venue) → chỉ giữ nhóm kỹ thuật chạy được
   trong constraint đó; nhóm vượt tầm → nói thẳng "vượt budget hiện tại" thay vì bỏ lửng.

**Output (chat only, không ghi file):** bảng ngắn 2–4 dòng — kỹ thuật | lý do khớp | từ
khóa search. Kết thúc bằng: "Chọn 1–2 hướng rồi tôi WebSearch tìm bài báo theo từ khóa
đó, tải về `papers/`, lúc đó `triage`/`pipeline` mới chạy được."

**Handoff:** sau khi user chọn hướng → WebSearch/WebFetch theo từ khóa đã chọn → tải các
paper thật vào `papers/` → chuyển sang mode `pipeline` hoặc `triage`.

## Full Pipeline (Mode: pipeline — full corpus ingest)

Goal = "hiểu/trích xuất kiến thức từ N papers" với N lớn (≳8). Tuân theo token economy & workbench conventions.
`papers/` rỗng/không tồn tại → chạy mode `scope` trước, đừng vào thẳng Step 1.

### Step 1 — Triage (1 inline call)
`paper-triage` quét toàn `papers/` qua abstract → relevance 0–5, rationale VI, action (deep-read / skim / skip), next-skill.
Đây là filter tiết kiệm token nhất. Thực hiện trực tiếp, không fan-out.

### Step 2 — Shard deep-reads
Nhóm paper cần đọc sâu thành shard ~8–12 ids. Dispatch waves 4–5 Task calls mỗi wave; mỗi subagent chạy `paper-read` summary rồi optional `paper-method`.

**Quy tắc nguyên tắc:** Raw PDF text không được đưa vào context của orchestrator. Mỗi subagent trả về CHỈ path + ≤2k-token manifest. Orchestrator chỉ nhận manifest, không đọc raw PDF.

### Step 3 — Merge rồi drop
Sau mỗi wave: merge `notes/INDEX.md` + ghi log nếu cần `audit-log`. Bỏ manifests khỏi context — chỉ giữ INDEX. Orchestrator không đọc lại full note bodies sau khi đã merge.

### Step 4 — Knowledge graph (optional)
Fan out `knowledge-graph` đọc id đã triage. Merge/shard via script `scripts/kg_builder.py`. Orchestrator KHÔNG đọc file master graph (`notes/knowledge-graph.md`). Chỉ lấy counts từ script stdout.

### Step 5 — Synthesis
`paper-synthesize` (compare/taxonomy/gaps/expand.mp) trên INDEX gists + master graph summary. Không load N distillate đầy đủ cùng lúc. Mỗi claim phải có id nguồn.

### Step 6 — Math sweep (optional)
`latex-fix` lint pass trên notes/ mới sinh nếu synthesis có công thức.

### Step 7 — Self-check (MANDATORY trước khi claim done)
`hallucination-guard` mode `scan` trên deliverable: mỗi claim phải có source (paper id / file path / section). Nếu có claim không nguồn → **refuse ngay**, chỉ rõ cái gì thiếu, regain bằng cách đọc đúng source, fix, rồi scan lại.
Scan bao gồm cả **evaluative claims** (novelty tier, venue-worthiness, "expected gain") theo `~/.claude/rules/research-proposal-integrity.md` §6: venue claim thiếu tier + điều kiện, hoặc công thức thiếu provenance tag ([cited]/[derived]/[design]) → FAIL như claim không nguồn.

**Net cost = O(number of shards), không phải O(number of pages).**

## Fan-Out Criteria (cho mode pipeline)

Fan-out ONLY khi:
1. Sub-tasks independent (no output dependency)
2. Mỗi sub-task ≥ 2k token output
3. User request rõ scope

**Never fan-out:** simple tasks, sequential tasks, exploratory work.

## Mode Scaling (token economy)

| N papers | Approach |
|----------|----------|
| ≤ 4 | Deep read từng paper (summary hoặc eli5) |
| 5–12 | Triage → deep read top 3–4, skim rest |
| > 12 | Triage → deep read top 5, gist cho rest, synthesize |

## Routing Rules (trong domain research)

| Request Type | Primary Skill | Supporting |
|-------------|--------------|------------|
| "Tôi muốn nghiên cứu AI cho domain X (chưa có bài báo)" | mode `scope` (self) | WebSearch sau khi chọn hướng → tải papers/ → `pipeline`/`triage` |
| "Đọc bài báo X" | paper-read | artifact-manager (mode `reuse`) |
| "So sánh N bài về Y" | paper-synthesize | paper-read (×N) |
| "Phân tích phương pháp bài X" | paper-method | paper-read |
| "Lọc bài báo phù hợp" | paper-triage | paper-read |
| "Đồ thị tri thức" | knowledge-graph | paper-read (×N) |
| "Sửa LaTeX" | latex-fix | — |
| "Dịch học thuật" | vi-translate | paper-read |
| "Đề xuất hướng / novelty / venue (Q1, Q4...)" | paper-synthesize (gaps/expand) | `research-proposal-integrity.md` — chấm tier trước, Venue Claim Card + claims-ledger; follow-up → re-read ledger trước khi trả lời |
| "Viết/nộp bài báo, draft manuscript, format IEEE/CVPR, rebuttal" | paper-submission | → chuỗi viết-paper bên dưới |
| "Vẽ figure/pipeline TikZ" | latex-tikz-generator | song song với draft |
| "Verify DOI, orphan citation, synthesis scan" | citation-guard | sau draft |
| "Humanize / giảm AI signature văn phong" | style-humanizer | sau citation-guard, giữ bất biến §4 |
| "Phản biện Q1 / devil's advocate / rejection analysis" | ieee-q1-devil-advocate | áp chót, đối chiếu claims-ledger |

## Chuỗi viết bản thảo (manuscript pipeline — SEQUENTIAL)

Khi request là "viết/nộp bài báo", đây KHÔNG phải fan-out (mỗi khâu phụ thuộc output khâu
trước — xem Fan-Out Criteria: sequential = never parallel). Điều phối tuần tự, mỗi khâu ghi
report cạnh bản thảo (`paper/reports/<stage>.md`), FAIL → quay lại khâu sinh:

```
paper-submission (draft/format) ──figures──> latex-tikz-generator (song song)
        │
        ▼
citation-guard        (zero-orphan · DOI verify CrossRef · synthesis scan)
        ▼
style-humanizer       (calibrate văn phong DƯỚI bất biến bảo toàn nghĩa §4)
        ▼
latex-fix + compile   (math render KaTeX+MathJax · document compile)
        ▼
ieee-q1-devil-advocate (phản biện đúng bản sẽ nộp · cross-check claims-ledger)
        ▼
self-evaluator        (cổng cuối trước "done")
```

Binding cho cả chuỗi: `~/.claude/rules/paper-writing-integrity.md` (§6 là sơ đồ trên).
Chỉ figure-generation được chạy song song với draft prose; phần còn lại tuần tự.

## Source-Driven Research

**Process: DETECT → FETCH → IMPLEMENT → CITE**
1. **DETECT** — loại source (paper, docs, blog, code)
2. **FETCH** — lấy content thực (không phải summary)
3. **IMPLEMENT** — apply findings
4. **CITE** — URLs đầy đủ, deep links, relevant quotes

**Source hierarchy:** Official docs > Academic papers > Official blog > Web standards > NOT: Stack Overflow, blog posts, AI summaries

## Integration (cross-cutting, auto-invoke)

| Skill | Khi nào invoke |
|-------|---------------|
| artifact-manager | Trước khi đọc paper nào → check INDEX.md (mode `reuse`); register all outputs |
| audit-log | Log synthesis decisions |
| token-budget | Estimate cost trước fan-out |
| hallucination-guard | MANDATORY scan trước claim done |

## Report Format (Vietnamese)

```
[3–4 dòng: tóm tắt what happened + verify result]
Rủi ro/giả định: [1 dòng nếu có]
Handoff: [skill nào tiếp theo, nếu có]
Paths: [danh sách file paths]
```

## Stop-Regain Protocol

Khi phát hiện claim không có evidence / đang build trên nền sai:
1. **Dừng** — không tiếp tục
2. **Nói rõ** — "Tôi đang sai ở chỗ X, thiếu Y"
3. **Đọc/verify** đúng nguồn
4. **Fix** nền sai trước khi tiếp tục
5. **Không claim done** cho đến khi verify pass

## Cross-References

- `paper-read` → Read individual papers
- `paper-method` → Methodology analysis
- `paper-synthesize` → Combine findings
- `knowledge-graph` → Build knowledge graph
- `paper-triage` / `paper-triage` → Filter papers
- `vi-translate` → Translation
- `latex-fix` → Math repair
- `paper-submission` → Draft/format/rebuttal manuscript (khâu đầu chuỗi viết)
- `latex-tikz-generator` → Figure/diagram TikZ (song song draft)
- `citation-guard` → DOI verify · orphan detect · synthesis scan
- `style-humanizer` → Style calibration dưới bất biến bảo toàn nghĩa
- `ieee-q1-devil-advocate` → Phản biện Q1 áp chót
- `workbench-conventions.md` → Bilingual policy, token economy rules
- `latex-katex-compat.md` → Cross-platform math rendering rules
- `research-proposal-integrity.md` → Novelty tiers, Venue Claim Card, claims ledger, math provenance, feasibility gate (binding cho mọi output đề xuất ý tưởng)
- `paper-writing-integrity.md` → Zero fabricated refs, đạo văn, results integrity, meaning-preservation invariant, chuỗi viết bản thảo §6
- `course-domain-model.md` → If research domain involves LMS content
