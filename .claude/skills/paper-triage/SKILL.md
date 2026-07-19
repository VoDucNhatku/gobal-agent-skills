---
name: reading-triage
description: Ranks every paper in papers/ against a research question via a fast abstract-level pass — assigning each a relevance score, a one-line rationale, an action (deep-read / skim / skip), and the next worker skill to run on it. The cheap planning entry point you run BEFORE any deep read, so you spend expensive full-reads only where they pay off. Triggers — triage, triage the papers, what should I read first, reading order, where do I start, prioritize papers, rank papers, which papers matter, build a reading plan, xếp thứ tự đọc, đọc bài nào trước, ưu tiên đọc, lọc bài báo, lập kế hoạch đọc, bài nào liên quan. Reads only high-density regions (title, abstract, headings); it does NOT deep-read or condense a paper (use paper-read), analyze a method (use paper-method), or compare papers (use paper-synthesize).
argument-hint: <research question / focus>
allowed-tools: Skill Agent Read Write Glob Bash
---

# Reading Triage (lọc & xếp thứ tự đọc)

This skill is the **cheap filter before the expensive read**. Given a research
question, it scans every paper in `./papers/` at the abstract level only and returns a
ranked reading plan: for each paper a relevance score, a one-line rationale in
Vietnamese, a recommended action, and the next Worker skill to run. It is a single,
lightweight planning pass — it never deep-reads, condenses, or critiques a paper.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual
policy, input resolution, output location & PREVIEW-NOT-DUMP, strategic reading). It
reads that file at run time. Human-facing output is **Vietnamese (academic register)**;
paper ids, filenames, and Worker skill names stay as-is. This skill bundles no script
and pulls no satellite rules file.

## Inputs
- `$ARGUMENTS` = the **research question / focus** (free text), e.g. "pairwise
  ranking losses for retrieval" or "diffusion models cho ảnh y khoa".
- If `$ARGUMENTS` is empty, ask **once** in Vietnamese for the research question, then
  proceed. Do not guess the focus.
- Corpus = every PDF in `./papers/`. If `./papers/` is missing or empty, say so in
  Vietnamese and stop.

## Procedure

### Phase 1 — Enumerate the corpus
List `./papers/*.pdf` with Glob. Derive each paper's stable id from its filename (the
leading 3-digit id where present, else assign sequential ids in filename order). Build
the working set as `(id, filename)` pairs. Consult `notes/INDEX.md` if it exists, to
note which papers already have distilled artifacts (those can often be scored from the
existing note rather than re-opened).

### Phase 2 — Strategic abstract-level read (token economy — §6)
For each paper, read **only the high-density regions**: title, abstract, and the
section headings (and the conclusion's first lines if the abstract is thin). Use a
**ranged read** — open just the first 1–2 pages of the PDF, never the whole file. The
entire point of triage is to NOT pay the full-read cost here; resist the urge to read
bodies, figures, or math.

**Warm re-run (token bound):** if `notes/INDEX.md` already has a one-line gist row for an
id, score that paper **from the INDEX gist row only** — do **not** open its note body
(`<id>-read-summary.md` / `<id>-method.md`). At corpus scale (e.g. 80 papers) opening every
note body would pull the whole corpus back into triage's single context, which is exactly the
cost triage exists to avoid. Open the PDF's first pages only for an id with **no** INDEX row.

### Phase 3 — Score each paper against the question
For every paper assign:
- **`score`** — relevance to the research question on a **0–5** scale (5 = directly
  on-topic and central; 0 = unrelated). Score on topical fit, not on paper quality.
- **`action`** — derived from the score band:
  - `score >= 4` → **deep-read**
  - `score 2–3` → **skim**
  - `score <= 1` → **skip**
- **`rationale`** — one line, Vietnamese, why this score (what in the abstract
  connects to — or misses — the question). Faithful to the abstract; do not invent
  findings the abstract does not state (§8).
- **`next`** — the Worker skill to run next on this paper, matched to intent:
  - deep methodology / math / reproducibility → `paper-method`
  - faithful condensation / orientation / intuition / mindmap → `paper-read`
  - typed entities & relations → `knowledge-graph`
  - full translation → `vi-translate`
  - (a `skip` paper gets `next: —`)

### Phase 4 — Rank & write the plan
Sort papers by `score` descending (ties → ascending id). Write the full ranked plan to
`notes/reading-triage-<slug>.md`, where `<slug>` is a short kebab slug of the research
question. Use the template below. Then update `notes/INDEX.md` with a row for this
artifact (`id · worker · path · one-line gist`); create `notes/` and `INDEX.md` if
absent.

### Phase 5 — Preview to chat (PREVIEW-NOT-DUMP — §3)
Print to chat **only** a fixed preview: a one-line Vietnamese summary of the corpus and
question, the **top 3–5 papers** as `id · score · action · next`, the count by action
band (`deep-read N · skim M · skip K`), and the **absolute saved path**. Never echo the
full plan into chat.

## Output template
Write this to `notes/reading-triage-<slug>.md`:

```markdown
# Reading Triage — <câu hỏi nghiên cứu>
Câu hỏi (research question): <full question, original wording>
Worker: reading-triage · Ngày (date): <YYYY-MM-DD> · Corpus: papers/ (N papers)

## Bảng xếp hạng (Ranked plan)
| Rank | id | Paper (filename / title) | Score (0–5) | Action | Next skill | Lý do (rationale, VI) |
|---|---|---|---|---|---|---|
| 1 | 003 | 003_pairwise_ranking.pdf | 5 | deep-read | paper-method | Trọng tâm: đề xuất pairwise loss đúng câu hỏi |
| 2 | 001 | 001_triplet.pdf        | 3 | skim      | paper-read   | Liên quan gián tiếp qua triplet loss |
| … |   |                         |   |           |              |  |

## Tổng hợp hành động (Action summary)
- deep-read: <ids>
- skim: <ids>
- skip: <ids>

## Đề xuất thứ tự đọc (Suggested reading order)
1. <id> — <one line, what to extract and with which skill>
2. …
```

The header block (worker · date · corpus size) and the rationale column are mandatory.
Keep each rationale to a single line.

## Gotchas
- **Do not deep-read here.** Triage that opens full bodies has defeated its own
  purpose — it is the filter that protects the expensive reads. Stay at the abstract /
  headings level, ranged reads only.
- **Score topical fit, not prestige.** A famous paper that does not address the
  question is a `skip`; an obscure one that nails it is a `deep-read`.
- **Don't fabricate relevance.** If an abstract is too thin to judge, score it
  conservatively and say `tóm tắt không đủ để đánh giá (abstract too thin)` in the
  rationale — never imagine results to justify a score.
- **Reuse existing notes.** If a paper already has a distilled artifact in `notes/`,
  score from that note; do not re-open the PDF.
- **Stay in lane (single-pass, §10).** Triage produces a *plan*, not the reading. Hand
  off each paper with its `next` field: → dùng `paper-read` / `paper-method` /
  `paper-synthesize` / `knowledge-graph` / `vi-translate` cho việc đọc sâu. Don't
  start condensing or comparing here.
- **Preview, not dump.** Only the top-N table + counts + path go to chat; the full
  ranked plan lives in the file.
