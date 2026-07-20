# Research Proposal Integrity (binding for idea-proposal & venue-claim outputs)

Satellite rules file pulled at run time by `gobal-orchestrator`, `research-orchestrator`,
`paper-synthesize` (gaps/expand), `paper-method`, and ANY skill that proposes research
ideas, grades novelty, or names a venue tier (Q1/Q2/Q4/conference). Subordinate to
`~/.claude/rules/workbench-conventions.md`; skills cite this file in one line and read it
at run time only.

**The failure this file exists to prevent** (observed 2026-07-07, project 034): a
direction was presented under the label "lộ trình Q1"; when the user probed, the claim
was walked back ("cái này một mình không đủ Q1"). That drift — overclaim at proposal
time, downgrade under scrutiny — is a calibration failure, not a knowledge failure.
Every rule below forces calibration AT PROPOSAL TIME and consistency ACROSS turns.

---

## 1. Novelty-tier rubric (grade BEFORE any venue word is written)

| Tier | Definition | Examples | Defensible venue band |
|---|---|---|---|
| **T1 — recipe** | New loss term, reweighting, training trick, data trick, backbone swap, schedule insight. No architectural change. | +ranking loss; heteroscedastic reweighting of an existing loss; freeze schedules | Workshop / Scopus conference / Q4. **NEVER Q1 alone.** |
| **T2 — module** | A module is redesigned or replaced; the architecture meaningfully changes and the change is the contribution. | Replacing a conv extrapolator with a splatting/attention field; a new fusion module with distinct mechanism | Q2–Q3 solid. Q1 only WITH a T3 element or exceptional breadth. |
| **T3 — reformulation** | The problem, representation, or inference process itself is redefined, with mathematical grounding. | New problem statement; structured-field representation replacing point features; principled active-inference policy | Q1 candidate WHEN carried by a T2 implementation + journal-grade breadth. |

Hard rules:
- A venue claim is **always a band + conditions**, never a point promise. Correct form:
  "T1 → đủ tầm hội nghị/Q4; lên Q1 cần [điều kiện X, Y]". The upgrade conditions are
  PART of the claim, stated in the same breath — not discovered later.
- **Q1 checklist** (all required): (T2 or T3) · breadth (≥2 datasets, full ablation,
  serious baselines) · related-work novelty scan done (not assumed). Missing any →
  write "Q1 conditional on ⟨missing items⟩", never bare "Q1".
- The tier of a **combination** equals the tier of its strongest **verified** component
  — not the sum of hopes. Three T1 tricks do not make a T2.
- Grading is written down (Venue Claim Card, §2) before the proposal is presented.

## 2. Venue Claim Card (required block in every proposal artifact)

```
### Venue Claim Card
- Proposal: <one line>
- Novelty tier: T1|T2|T3 — <one-line justification against §1>
- Venue band: <band> (điều kiện lên đỉnh band: <prerequisites>)
- Downgrade triggers: <what discovery/result would lower this claim>
- Confidence: high|medium|low — <why>
- Ledger: C-<seq> (§3)
```

A proposal note without this card is incomplete — `self-evaluator` fails it.

## 3. Claims ledger (consistency across turns and sessions)

- File: `notes/claims-ledger.md` in the **project cwd** (create on first claim).
  Append-only; one row per venue/novelty claim:

  `| C-<seq> | YYYY-MM-DD | <proposal, one line> | T? | <venue band + conditions> | active / revised→C-n | <artifact path> |`

- **Before answering ANY follow-up** about a previously proposed idea (its novelty,
  venue, feasibility): re-read `notes/claims-ledger.md` + the proposal note. Do NOT
  answer from conversation memory — memory is where drift happens.
- **Revision protocol** (extends stop-regain): when a claim must change:
  1. Quote the prior claim and its ledger id.
  2. State `REVISION` + the specific cause (new evidence · user counter-argument ·
     rubric misapplied at proposal time — name which).
  3. Append a new ledger row; mark the old row `revised→C-new`.
  4. Update the proposal artifact itself (not just the chat).
  Silent recalibration is a violation even when the new answer is more honest — the
  drift itself must be named.

## 4. Math provenance (no formula without a tag)

Every equation in a proposal carries exactly one tag:

- **[cited]** — copied/adapted from a named source (paper id · file path · URL). The
  source must actually contain it; adapting changes must be listed.
- **[derived]** — derived in place; the derivation is shown AND passes ≥1 stated sanity
  check: stationary-point / limiting-or-degenerate case / dimensional consistency.
- **[design]** — a heuristic or design choice with no proof; MUST carry
  `[cần thực nghiệm]` and must never be phrased with [derived]-level confidence.

Forbidden: a [design] formula presented as guaranteed; citing a source for a formula it
does not contain; any "expected gain ≈ X%" with no executed run behind it.

## 5. Experiment-feasibility gate (a proposal is runnable, or says it is not)

A proposal may be presented as actionable ONLY if it states:
1. **Data** — which dataset, on hand or not, contains the required annotation or not.
2. **Compute** — fits the stated budget/GPU, with the estimate and its basis (a real
   prior run beats a guess; cite which).
3. **Baseline** — a trusted baseline number exists. If the user's own reproduction
   diverges from the paper, all comparisons target the INTERNAL baseline and the
   proposal says so.
4. **Dependencies** — every external model/teacher/checkpoint/dataset named is verified
   downloadable, or flagged `[phải xác minh trước khi chốt]` WITH a named fallback.

Any of 1–4 unknown → label the proposal "chưa chạy được như mô tả (not runnable as
stated)" — do not let the label be implied or discovered later.

## 6. Evaluative claims are scannable claims (extends hallucination-guard)

`hallucination-guard` treats the following as flaggable claims, not opinions: novelty
tier assertions · venue-worthiness assertions · "first to do X" / "SOTA" assertions ·
expected-improvement numbers. Each needs rubric grounding (§1) or an explicit
`[suy luận]` flag. "Nghe hợp lý" is not grounding.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| calibration drift | trôi hiệu chuẩn | Khẳng định mạnh lúc đề xuất, rút lại khi bị chất vấn |
| venue band | dải venue | Khoảng venue bảo vệ được (kèm điều kiện), thay cho lời hứa điểm |
| claims ledger | sổ khẳng định | File append-only ghi mọi claim novelty/venue để giữ nhất quán |
| provenance tag | nhãn nguồn gốc | [cited]/[derived]/[design] — mỗi công thức phải mang đúng một |
