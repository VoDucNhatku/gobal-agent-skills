---
name: "paper-read"
description: "Reads and distills ONE paper at a chosen depth/format — the orientation-and-condense Worker of the Workbench suite. Modes — gist (quick should-I-read overview), summary (faithful section-by-section condensation, the default), eli5 (plain-language intuition with one analogy + toy example), mindmap (Mermaid structure diagram). Output prose is Vietnamese (academic), code/identifiers English. Triggers — overview of 003, summarize this paper, what's this paper about, is it worth reading, explain simply, ELI5, give me the intuition, mindmap of the paper, tóm tắt bài báo, bài này nói về gì, có đáng đọc không, giải thích đơn giản, trực giác, sơ đồ tư duy, đọc lướt bài. Condenses ONE paper faithfully; it does NOT critique the method (use paper-method) and does NOT compare across papers (use paper-synthesize). Accepts an id, filename, path, or `all`."
argument-hint: "<id|file|path|all> [gist|summary|eli5|mindmap]"
allowed-tools: "Skill Agent Read Write Glob Bash"
---

# paper-read — distill one paper at a chosen depth

This Worker reads a single paper and produces a faithful Vietnamese distillation at one
of four depths. Depth/format is a **mode parameter**, not four separate skills — one run
produces one artifact in one mode. It folds the legacy AIL skills *paper-overview*,
*paper-summary*, *intuition*, and *paper-mindmap* into a single mode-dispatched Worker.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual §1,
input resolution §2, preview-not-dump §3, reuse §4, strategic reading §6, mode scaling
§7, fidelity §8). It reads that file at run time. The per-mode templates, chat-preview
budgets, and the `all` downscaling table live in `references/depth-modes.md` (pulled on
demand) — this body does **not** duplicate them.

## Inputs
- `$ARGUMENTS` = `<target> [mode]`.
- **target** — a 3-digit id (`003`) · filename / partial title (`pairwise`) · a path
  (`papers/003_*.pdf`) · the literal `all` (every paper in `papers/`). Resolve to a
  concrete file under `./papers/` before reading (§2). If ambiguous, list candidates and
  ask once, then proceed.
- **mode** — one of `gist | summary | eli5 | mindmap`. **Default `summary`** when omitted.

## Mode dispatch (explicit)
Pick exactly ONE mode per run, then follow its spec in `references/depth-modes.md`:

| Mode | Intent | What to read (token economy) | Output shape |
|---|---|---|---|
| `gist` | should-I-read orientation | abstract + intro + conclusion + headings + captions only (§6) | one-liner · problem · core idea · headline results · read-deeper verdict |
| `summary` *(default)* | faithful section-by-section condense | whole paper, section by section; ranged reads for long PDFs | abstract → background → method → experiments → results/ablation → stated limits → glossary |
| `eli5` | plain-language intuition | abstract + method + one running example | the problem plainly · ONE analogy · toy example · why it works · where the analogy breaks |
| `mindmap` | visual structure | headings + abstract + method skeleton | one Mermaid `mindmap` (Problem/Method/Experiments/Results/Limitations) + short reading note |

Do not blend modes. If the user clearly wants critique/math, hand off to `paper-method`;
if they name several papers, hand off to `paper-synthesize` (see Gotchas).

## Procedure

### Phase 0 — Resolve & reuse
Resolve the target to a concrete file (§2) and fix the mode (default `summary`). Then
apply **reuse-before-read** (§4): consult `notes/INDEX.md` and check `notes/` for an
existing fresh `notes/<id>-read-<mode>.md`. If a fresh artifact for this exact id+mode
exists, reuse it (preview + path) instead of re-reading the PDF. Otherwise continue.

### Phase 1 — Read at the mode's depth
Open the resolved PDF with the Read tool and read **only the regions the mode requires**
(§6) — `gist`/`mindmap` stay in high-density regions; `summary` reads the whole paper
with ranged reads for long PDFs; `eli5` reads enough to ground one faithful analogy.
Read the actual source — never distill from the title alone (§8).

### Phase 2 — Write the artifact
Fill the mode's template from `references/depth-modes.md`. Open the file with the
standard research header (`paper id · title · source filename · worker (paper-read) ·
date YYYY-MM-DD`). Human-facing prose is Vietnamese, academic register; on first use of
a technical term write `thuật ngữ tiếng Việt (English term)`; never translate
API/library/model/dataset names (§1). Condense **faithfully** — preserve exact metrics
and ablation deltas; for anything the paper omits write `bài báo không nêu (not stated
in the source)` (§8). The `summary` mode ends with a `## Thuật ngữ (Glossary)` table.

Write the full artifact to **`notes/<id>-read-<mode>.md`** with the Write tool (§3).

### Phase 3 — Preview (PREVIEW-NOT-DUMP)
Print to chat ONLY the mode's fixed-line Vietnamese preview (budget per mode in
`references/depth-modes.md`: gist 5–6 · summary 6–8 · eli5 5–7 · mindmap 5–6 lines) plus
the **absolute saved path**. Never echo the full file — and for `mindmap`, never paste
the Mermaid block into chat (it lives in the file; the preview lists the top branches).

### Phase 4 — Index & hand off
Add/refresh one row in `notes/INDEX.md` (`id · paper-read · path · one-line gist`). End
the preview with the natural next-step handoff (e.g. `→ paper-method` for the
math/critique, `→ paper-to-notebook` to run it).

## `all` — mode scaling by cardinality (§7)
When the target is `all`, do NOT run the full single-paper template per paper. Follow the
scaling table in `references/depth-modes.md`: 2–4 papers (Deep) = one full
`notes/<id>-read-<mode>.md` each; 5+ papers (Overview) = ONE compact block per paper
(one-liner + 2–3 bullets) rolled up into a single `notes/read-<mode>-all.md`, and state
the downscale in the preview. Heavy per-paper deep reads across a large corpus are the
**orchestrator's** parallel-subagent job — note the handoff and stop, do not loop a full
deep read over the whole corpus in one pass (§10).

## Gotchas
- **Mode is a parameter, not four skills.** One mode per run. Default to `summary` only
  when none is given; don't silently produce a different depth than asked.
- **`gist` must stay shallow.** Reading the full body in `gist` defeats the mode — keep
  to abstract/intro/conclusion/headings/captions (§6).
- **Don't critique, don't compare.** This Worker condenses ONE paper faithfully. Method
  critique / math / reproducibility → `→ dùng paper-method`. Cross-paper comparison,
  taxonomy, or gaps → `→ dùng paper-synthesize`. Stay in scope (single-pass, §10).
- **Preview, never dump.** Write the file, print the short preview + path; never echo the
  artifact (or the Mermaid block) into chat (§3).
- **`eli5` honesty guard.** Label the analogy AS an analogy and include where it breaks;
  do not present it as the literal mechanism.
- **Reuse before re-reading.** A fresh `notes/<id>-read-<mode>.md` is reused, not
  regenerated (§4) — only re-read the PDF when no fresh artifact exists.
