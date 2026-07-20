# Paper Writing Integrity (binding for manuscript-production skills)

Satellite rules file pulled at run time by `paper-submission`, `citation-guard`,
`style-humanizer`, `latex-tikz-generator`, `ieee-q1-devil-advocate`, and any future
writing skill. Subordinate to `~/.claude/rules/workbench-conventions.md`; complements
`~/.claude/rules/research-proposal-integrity.md` (novelty/venue calibration). Skills cite
this file in one line and read it at run time only.

Core rule: **the manuscript never claims more than the notes and the claims ledger
support** — writing is presentation, not escalation.

---

## 1. Zero fabricated references

- A bibliography entry may enter the draft ONLY from: (a) a user-provided source or a
  distilled note with an id (`notes/<id>-*.md`), or (b) a lookup **verified this
  session** — WebFetch `https://api.crossref.org/works/<DOI>` or `https://doi.org/<DOI>`
  and confirm title/authors/venue/year match.
- **Never write a reference from model memory alone.** Memory-recalled → verify online
  first; no network access → tag `[unverified — kiểm tra DOI trước khi nộp]` and list it
  in the audit report. Presenting an unverified entry as verified = FAIL.
- Retraction screening only when actually look-up-able (WebSearch); otherwise write
  "chưa kiểm tra retraction" — do not fabricate a clean bill.
- Every quantitative claim in Related Work traces to a note id or a verified source.

## 2. Plagiarism discipline (đạo văn)

- **Draft from your OWN distilled notes** (`notes/*`), never by transcribing source-paper
  prose. Verbatim >10 consecutive words from any source → quotation marks + citation;
  otherwise rewrite in the author's own argumentative structure.
- Related Work must SYNTHESIZE (citation-guard's synthesis scan enforces this): no
  "A said X [1]. B said Y [2]." serial listing.
- **Figures:** a diagram that mirrors another paper's figure STRUCTURE is plagiarism of
  design even when redrawn from scratch in TikZ. Either redesign (abstraction /
  perspective-shift) or caption "adapted from [x]". "Scanner không quét được TikZ" is NOT
  a license — the standard is originality, not detectability.
- Self-plagiarism: text reused from the author's own prior papers → flag for rewrite or
  self-citation.

## 3. Results integrity

- **No invented experiment numbers, ever.** Missing result → `[TODO: <metric> từ
  <run/log path>]`, aggregated in the report. A draft full of TODO placeholders is
  normal; a draft with one fabricated number is a violation.
- Reported numbers match run logs / notes exactly (conventions §8). When the user's
  reproduction diverges from the original paper, comparisons target the INTERNAL
  baseline and the text says so (research-proposal-integrity §5.3).
- Contribution claims match the graded tier in `notes/claims-ledger.md` — a T1
  contribution is never phrased as a new paradigm.

## 4. Meaning-preservation invariant (any style pass)

A style edit (`style-humanizer` or inline polish) may change WORDING ONLY. Frozen
invariants: numbers & units · math · citation keys and their attachment sentences ·
claim strength (shown / suggests / may) · hedges · direction of every comparison.
After editing, diff-check the invariants; any drift → revert that span. Style edit ≠
substance edit.

## 5. Honest claims about the writing itself

- Never claim the text "passes" any AI detector or plagiarism scanner — that is
  unverifiable. The only verifiable claim: "đã giảm AI-signature theo heuristic
  checklist".
- Venue AI-use disclosure (IEEE policy etc.) is the AUTHOR's decision and
  responsibility — surface the question once with the venue's stated policy; do not
  decide it silently.

## 6. Standard manuscript pipeline (optimal chaining order)

```
paper-submission draft/format  (figures → latex-tikz-generator)
        │
        ▼
citation-guard        — zero-orphan · DOI verify (§1) · synthesis scan (§2)
        │
        ▼
style-humanizer       — style calibration under invariant §4
        │
        ▼
latex-fix + compile   — math renders (latex-katex-compat), document compiles
        │
        ▼
ieee-q1-devil-advocate — adversarial review vs notes/claims-ledger.md
        │
        ▼
self-evaluator        — final gate before "done"
```

- Each stage writes its report NEXT TO the manuscript (`paper/reports/<stage>.md`);
  a FAIL loops back to the producing stage before the chain continues.
- `ieee-q1-devil-advocate` runs after style/format so it reviews what would actually be
  submitted; its Novelty section grades against research-proposal-integrity §1 (T1/T2/T3)
  and cross-checks the claims ledger — draft claiming above the ledger's tier =
  automatic finding.
- Orchestration: the chain is SEQUENTIAL (each stage depends on the previous output) —
  per fan-out criteria this is never parallelized; only figure generation
  (latex-tikz-generator) may run parallel to prose drafting.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| fabricated reference | trích dẫn bịa | Entry thư mục sinh từ trí nhớ model, không verify được |
| orphan citation | trích dẫn mồ côi | In-text không có trong reference list hoặc ngược lại |
| meaning-preservation invariant | bất biến bảo toàn nghĩa | Những thứ sửa văn phong không được đổi: số liệu, toán, citation, độ mạnh claim |
| synthesis quality | chất lượng tổng hợp | Related Work phải đan nguồn thành lập luận, không liệt kê tuần tự |
