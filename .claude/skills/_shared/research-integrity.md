# Research integrity: novelty, venue, feasibility

Read only when an answer grades novelty, names a venue or tier (Q1–Q4, conference,
workshop), or proposes a research direction. Replaces `rules/research-proposal-integrity.md`.

## 1. The project decides first
Before any venue or novelty statement, read the project's own scope:
`notes/claims-ledger.md` rows marked `SCOPE` and every `active` row, plus the project's
protocol/README. If the project says it does not assign venue bands, do not assign one —
quote that row and answer the underlying question (feasibility, evidence gaps) instead.
Project scope overrides this rubric.

## 2. Intervention type (description, not a venue verdict)
| Type | What changes |
|---|---|
| recipe | loss term, reweighting, schedule, data trick, backbone swap |
| module | a component is redesigned and the change is the contribution |
| reformulation | the problem, representation or inference process is redefined |

The type describes the intervention. It is not evidence about any venue's editorial bar;
a specific venue is judged only by that venue's published criteria.

## 3. When a venue band is allowed
Only when the user asks and the project scope permits. Write it as a band with the
conditions that would have to hold, in the same sentence. `Venue band: chưa gán — <why>,
<what would allow it>` is a valid answer. Never promise a band without conditions; never
upgrade a band because the user pushes back.

## 4. Revisions
A claim changes only with evidence. Record the evidence class of the revision:
`run result` · `full method read` · `abstract only` · `inference` · `user argument`.
`abstract only` or `inference` may add a note "đề xuất sửa"; it does not change the claim.
Append a new ledger row and mark the old one `revised→<id>`; never edit history.

## 5. Formulas in proposals
Tag each: `[cited]` (source contains it), `[derived]` (derivation shown plus one sanity
check: limit case, dimension, or numeric example), `[design]` (heuristic; carries
`[cần thực nghiệm]`).

## 6. Feasibility gate
A proposal is "runnable" only if data, compute (with the basis of the estimate), a trusted
baseline number and every external dependency are named. Otherwise write
"chưa chạy được như mô tả" and list what is missing.
