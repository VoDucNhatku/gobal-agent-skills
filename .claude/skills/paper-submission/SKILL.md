---
name: "paper-submission"
description: "Academic manuscript and paper submission worker — drafts, formats, and polishes academic papers for submission to top-tier venues (IEEE Q1/Q2, CVPR, ICCV, ECCV, NeurIPS, etc.). Modes: draft (generate manuscript from synthesis notes), format (apply specific LaTeX templates like IEEEtran/cvpr), rebuttal (draft reviewer responses based on reviews). Triggers — write paper, draft manuscript, format for IEEE, format for CVPR, write rebuttal, chuẩn bị nộp báo, viết bản thảo, phản hồi reviewer. It writes and formats manuscripts; it does NOT conduct the primary research or run experiments (use paper-method, paper-synthesize, or run-on-modal)."
argument-hint: "<topic | conference name> [draft|format|rebuttal]"
allowed-tools: "Read Write Glob Bash"
---

# Paper Submission (Viết & Chuẩn bị Bản thảo)

> **Role:** Transforms research synthesis notes, experiment results, and method notes into submission-ready academic manuscripts (LaTeX/PDF format) tailored to specific conferences/journals.

Binding: `~/.claude/rules/paper-writing-integrity.md` (§1 zero fabricated references, §2
đạo văn, §3 results integrity — [TODO] thay vì bịa số, §6 vị trí trong pipeline) và
`~/.claude/rules/research-proposal-integrity.md` (§1 tier + venue band; draft không được
claim vượt tier trong `notes/claims-ledger.md`).

## Vị trí trong pipeline sản xuất bản thảo (§6 paper-writing-integrity)

Skill này là **khâu đầu** của một chuỗi TUẦN TỰ — mỗi khâu ghi report cạnh bản thảo
(`paper/reports/<stage>.md`); một FAIL quay lại khâu sinh trước khi chuỗi đi tiếp:

```
paper-submission (draft/format · figures → latex-tikz-generator)
   → citation-guard      (zero-orphan · DOI verify · synthesis scan)
   → style-humanizer     (calibrate văn phong DƯỚI bất biến bảo toàn nghĩa §4)
   → latex-fix + compile (math render 2 engine · document compile)
   → ieee-q1-devil-advocate (phản biện đúng bản sẽ nộp · đối chiếu claims-ledger)
   → self-evaluator      (cổng cuối trước khi "done")
```

Chuỗi này SEQUENTIAL (mỗi khâu phụ thuộc output khâu trước) → không parallel hóa; chỉ
figure (latex-tikz-generator) được chạy song song với việc draft prose. Khi kết thúc mode
`draft`/`format`, luôn nêu handoff khâu kế (citation-guard) trong report.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `draft` | Draft manuscript from notes | Starting the writing phase of a paper |
| `format` | Apply specific venue template | Adapting existing text to IEEEtran, CVPR, etc. |
| `rebuttal` | Draft reviewer response | Responding to peer review feedback |

## Procedure

### Mode: draft
1. **Read Inputs:** Read `notes/INDEX.md` and relevant synthesis/method notes (e.g., `notes/synthesize-compare.md`, `notes/*-method.md`).
2. **Structure:** Generate a standard academic structure: Abstract, Introduction, Related Work, Method, Experiments, Conclusion.
3. **Drafting (Vietnamese/English):** As per workbench conventions, draft in the requested language (default to English for standard academic submission, but keep chat in Vietnamese).
4. **Citation Check:** Ensure every claim is backed by a citation from the input notes. Do not hallucinate citations.

### Mode: format
1. **Identify Target:** Determine target venue (e.g., CVPR, ICCV, IEEE Q1).
2. **Template Application:** Use the official LaTeX template for the venue. Structure the `.tex` file with appropriate macros (e.g., `\author`, `\maketitle`, `\bibliographystyle`).
3. **Math & Figures:** Use `latex-math-renderer` guidelines to ensure math is correctly formatted for the specific LaTeX engine. Check that figure references follow venue guidelines.
4. **Output:** Generate the `main.tex` and a `bib` file.

### Mode: rebuttal
1. **Input:** Read the reviewer comments (provided in text or file).
2. **Deconstruct:** Break down reviewer concerns point-by-point.
3. **Draft Response:** Write a respectful, evidence-based response. Cite new experiments or specific sections of the paper where changes were made.
4. **Output:** A rebuttal document (`rebuttal.md` or `rebuttal.tex`).

## Cross-References
- `paper-synthesize` → Provides the raw material for the Related Work section.
- `paper-method` → Provides the raw material for the Method section.
- `latex-tikz-generator` → Figures/diagrams TikZ (chạy song song với draft prose).
- `citation-guard` → Khâu kế: DOI verify + orphan detect + synthesis scan.
- `style-humanizer` → Calibrate văn phong sau citation-guard (giữ bất biến §4).
- `latex-fix` → For repairing any LaTeX formatting issues; then compile.
- `ieee-q1-devil-advocate` → Phản biện Q1 áp chót.
- `self-evaluator` → Cổng cuối.
- `paper-writing-integrity.md` / `research-proposal-integrity.md` → Binding rules.

## Gotchas
- **No Hallucination (§3 integrity):** Do not invent experiment results or citations. If
  data is missing, insert a placeholder (e.g., `[TODO: Insert F1 score from
  <run/log path>]`) and explicitly aggregate all TODOs in the report. Một bản đầy TODO là
  bình thường; một con số bịa là VI PHẠM.
- **Reference provenance (§1 integrity):** Mỗi entry thư mục chỉ vào draft từ (a) note có
  id hoặc (b) lookup verify phiên này (WebFetch CrossRef/doi.org). Không viết reference từ
  trí nhớ model — chưa verify được → tag `[unverified — kiểm tra DOI trước khi nộp]`. Việc
  DOI-verify thực tế do `citation-guard` chạy ở khâu kế.
- **Related Work phải SYNTHESIZE (§2):** không liệt kê tuần tự "A nói X [1]. B nói Y [2]".
  Đan nguồn thành lập luận; verbatim >10 từ liên tiếp → ngoặc kép + cite.
- **Claim ≤ tier ledger:** contribution phrasing khớp tier đã chấm trong
  `notes/claims-ledger.md` — T2 module không được viết như "new paradigm".
- **Strict Templating:** When formatting, adhere strictly to the target venue's official LaTeX template constraints (page limits, font sizes, citation styles).
- **AI-use disclosure:** chính sách khai báo dùng AI của venue là quyết định của TÁC GIẢ —
  nêu policy venue đích một lần, không tự quyết thay (§5 integrity).
