# Workbench Conventions (binding for all Workbench skills)

These are the shared, binding conventions for every skill in the Workbench global
suite (`workbench-orchestrator`, `paper-read`, `paper-method`, `paper-synthesize`,
`reading-triage`, `knowledge-graph`, `vi-translate`, `paper-to-notebook`,
`run-on-modal`, `scaffold-course-platform`, `design-ui-direction`,
`build-ui-component`, `build-admin-dashboard`, `review-frontend`, `latex-fix`,
`audit-log`, and any future skill). Each skill cites this file in **one line** and
reads it **at run time only** — keeping it out of the always-loaded context.

Each skill applies these rules unless its own `SKILL.md` explicitly overrides one.

---

## 1. Language policy (BILINGUAL — mandatory)
- **Human-facing prose** — explanations, clarifying questions, plans, progress
  updates, chat previews, report bodies, glossary text: **Vietnamese, academic
  register (học thuật)**. On first use of a technical term write
  `thuật ngữ tiếng Việt (English term)`; afterwards the Vietnamese form may stand
  alone but the English term must stay recoverable.
- **Machine-facing content** — code, code comments, file/identifier names, JSON
  keys, config, CLI commands, commit messages, and the literal CONTENT of any
  generated source file (`.py`, `.ts`, `.tsx`, `.ipynb`, `modal_app.py`, etc.):
  **English**.
- The `workbench-orchestrator` converses with the user in **Vietnamese**.
- Never invent a Vietnamese term for a concept with no settled translation — keep
  the English term and gloss it. Never translate API / library / function /
  dataset / model names.
- Any distillation artifact that defines terms ends with a
  `## Thuật ngữ (Glossary)` table: `| English | Tiếng Việt | Giải thích ngắn |`.
- `language` / `--to <lang>` may be overridden per invocation (e.g. `vi-translate`
  to a non-Vietnamese target). Default human language is Vietnamese.

## 2. Input resolution (`$ARGUMENTS`)
- **Research id forms accepted:** a 3-digit paper id (`003`) · a filename or partial
  title (`pairwise`, `004_Image`) · an absolute/relative path
  (`papers/003_*.pdf`) · the literal `all` (operate on every paper in `papers/`).
  Resolve the id → a concrete file under `./papers/`.
- **Web surface forms:** a named surface/route slug (`pricing`, `course-card`), an
  existing file path, or a free-text description.
- Resolve to a **concrete target before doing any work**. If `$ARGUMENTS` is empty
  or genuinely ambiguous, **ask once** (list the candidates), then proceed. Never
  guess silently.

## 3. Output location & the PREVIEW-NOT-DUMP rule (token economy — MANDATORY)
- Write the **full artifact** to its output file (see §3a) with the Write tool.
- Then print to chat **only**: a fixed-size preview (each skill states its line
  budget, typically **5–10 lines**, key points in Vietnamese) **plus the absolute
  saved path**. **Never echo full file contents into chat.**
- **Pure-query / digest / summary modes** print to chat and write **no file**.

## 3a. Output directories — artifacts land in the CURRENT PROJECT cwd, never global
| Domain | Output dir (relative to project cwd) | Naming |
|---|---|---|
| Research | `notes/` (flat; create if missing) | `<id>-<skill>[-<mode>].md` (per-skill naming governs) |
| Research manifest | `notes/INDEX.md` | one row per artifact: `id · worker · path · one-line gist` |
| Code | `notebooks/`, project root | `<id>.ipynb`, `modal_app.py` |
| Web | the project's own source tree | follows the project's conventions |
| Web preview / design record | Artifact (claude.ai) + `notes/design-<slug>.md` | the chosen direction + tokens |
| Governance | `notes/audit-log.md` | append-only JSON-lines |

Each research artifact opens with a header block: paper id · title · source
filename · worker name · date (`YYYY-MM-DD`).

## 4. REUSE-BEFORE-READ rule (token economy — MANDATORY)
- Before ingesting any **raw source** (PDF, repo, large file), check `notes/` for an
  existing **distilled artifact** for this id, in the skill's declared priority
  order (e.g. `run-on-modal` checks `notes/<id>-method.md` →
  `notes/<id>-read-summary.md` before opening the PDF).
- **Reuse if present and fresh** (same session/day, or explicitly reconfirmed by the
  user); otherwise read the raw source.
- Consult `notes/INDEX.md` first to discover what already exists.

## 5. Stable-id & deterministic naming (token economy)
- Use deterministic `<id>-<skill>[-<mode>].md` names so a downstream lookup is a
  **path test, not a search**. Research id = the 3-digit paper id; web id = a kebab
  `<surface>` slug; code id = the paper id.

## 6. Strategic / partial reading (token economy)
- Orientation and triage work reads only **high-density regions** — abstract,
  introduction, conclusion, section headings, figure/table captions. Full ingestion
  only where the deliverable genuinely requires it. Use **ranged reads** for long
  PDFs and large files (read by page range, not the whole file at once).

## 7. Mode scaling by cardinality (token economy)
- Breadth skills scale **per-item output DOWN as N grows**: Deep mode (2–4 items) =
  full detail / ~3 suggestions each; Overview mode (5+ items / `all`) = high-level /
  1 each. This caps total output linearly instead of letting it explode.

## 8. Fidelity
- Read the **actual** source with the Read tool — never analyze from a title alone.
- Distillation skills condense **faithfully**; they do not invent results. If the
  source does not state something, write
  `bài báo không nêu (not stated in the source)`.
- Preserve all quantitative results exactly (metrics, dataset sizes, ablation
  deltas). Every cross-paper / cross-source claim is attributable to a specific
  source.

## 9. Script-offloading rule (token economy — MANDATORY where a script is bundled)
- If the skill bundles a builder/linter script under its `scripts/` dir, it **must**
  emit only a compact **JSON spec** and call the script to produce the file. It must
  **never hand-write the file's boilerplate format** (nbformat JSON, Modal app
  envelope, scaffold commands, CRUD boilerplate, KG merge, log line).
- The skill body lists exactly what the script auto-inserts, so the model never
  duplicates it.
- Spec temp files use a **collision-free, OS-portable** path relative to the project
  cwd: `.tmp/<skill>_<id>_<mode>.json` (safe for parallel subagents writing at the same
  time). **Never hardcode `/tmp/...`** — it silently fails on Windows (no `/tmp`
  filesystem). If the harness exposes a session-scoped scratchpad directory, prefer
  that instead of `.tmp/`.

## 10. Single-pass & scope boundaries
- Each non-orchestrator skill is **lightweight / single-pass** with a hard scope
  boundary and an explicit `→ dùng skill Z cho việc Y` handoff note. Heavy
  multi-pass work (reading many papers, building a whole platform) is the
  **orchestrator's** job (parallel subagents), not a single Worker's.

## 11. Token-budget self-check (authoring & runtime)
- A `SKILL.md` body stays **under 500 lines**; binding detail lives in `rules/` or
  the skill's `references/` (one level deep, never nested chains).
- A subagent returns to the orchestrator **only** a saved path + a small distilled
  summary (target 1–2k tokens) — never the raw PDF/repo/full artifact.

## 12. Relationship to deep / multi-agent harnesses
- These skills are the lightweight everyday layer. For an exhaustive,
  fact-checked, multi-source literature report, defer to a dedicated deep-research
  harness rather than chaining Workers by hand.
