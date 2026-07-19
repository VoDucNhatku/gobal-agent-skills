---
name: understand-codebase
description: Maps an existing codebase into a token-bounded knowledge graph so the agent understands structure before changing anything — modules, files, key symbols (functions/classes/exports) and their edges (imports, calls, defines). Modes — scan (build/refresh the codebase graph into notes/codebase-graph.md, incremental on re-run), explain <file|symbol> (deep-dive one node and its dependents/dependencies), onboard (generate an onboarding guide from the graph), diff (impact analysis of uncommitted changes — what depends on what changed). Offloads the graph merge to a script and never reads the master graph back into context. Triggers — understand the codebase, hiểu codebase, map the project, sơ đồ dự án, what calls this, cái gì gọi hàm này, dependency graph, đồ thị phụ thuộc, onboard me, impact of this change, ảnh hưởng thay đổi, where is X used. It maps an existing codebase; it does NOT change code (use code-senior) or extract a paper's graph (use knowledge-graph).
argument-hint: <scan | explain <file|symbol> | onboard | diff> [path-glob]
allowed-tools: Read Glob Grep Bash
---

# Understand Codebase (hiểu codebase qua knowledge graph)

Builds a structural knowledge graph of a real codebase — nodes (module / file / symbol) and edges
(imports / calls / defines) — so the agent (and you) can see how things connect before editing.
Token-bounded by design: a script does the heavy crawl + merge; only summaries enter context.
(Distinct from `knowledge-graph`, which graphs a research paper, not source code.)

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — graph labels/identifiers English,
report Vietnamese; output + preview §3; reuse-before-read §4; strategic reading §6; script-offloading
§9; scope handoff §10). Read at run time; never inline.

## Procedure

### Phase 0 — Resolve mode + scope
Parse mode: `scan` (default) | `explain <file|symbol>` | `onboard` | `diff`. Optional path-glob limits
the scope (e.g. `src/**`). Consult `notes/INDEX.md` and an existing `notes/codebase-graph.md` first
(§4) — `scan` is INCREMENTAL: re-running only re-crawls changed files.

### Phase 1 — Crawl + build the graph (script-offloaded, §9)
Do NOT hand-read every file or hand-write the graph. Run the bundled crawler, which walks the tree,
extracts symbols + edges per language (regex-based, dependency-free), and writes/merges the graph:
```
python "<skills>/understand-codebase/scripts/cb_builder.py" scan [--root <dir>] [--glob "<pattern>"]
```
It emits `notes/codebase-graph.md` (module → file → symbol tree + an edge table) and a machine-state
`notes/codebase-graph.json`. The crawler reads files; your context does NOT — you read only its
stdout summary (counts + the largest hubs). **Never read codebase-graph.md back into context** at
scale — query the JSON via the script's `explain`/`diff` subcommands instead.

### Phase 2 — mode work
- **`scan`:** report the shape — module/file/symbol counts, the top hub files (most depended-on), and
  any obvious cycle the crawler flags. Strategic (§6): you do not read file bodies, only the graph.
- **`explain <file|symbol>`:** `cb_builder.py explain <name>` returns that node + its direct
  dependents and dependencies (1 hop). Read those specific files only if a deeper explanation is
  needed — not the whole tree.
- **`onboard`:** generate `notes/codebase-onboarding.md` — entry points, the main modules and their
  jobs, the hub files to read first, and a suggested reading order. (Confirm before sharing widely.)
- **`diff`:** `cb_builder.py diff` reads `git diff --name-only` and reports the impact set — what
  symbols/files depend on the changed ones (the blast radius), so a change isn't shipped blind.

### Phase 3 — Preview (§3)
Print a **5-8 line** Vietnamese preview + the saved path(s): counts, top hubs, and for `explain`/
`diff` the dependents/impact list. Never paste the full graph or file bodies into chat.

## Output
- `scan` → `notes/codebase-graph.md` + `notes/codebase-graph.json` (written by the script).
- `onboard` → `notes/codebase-onboarding.md`. `explain`/`diff` → chat report only.

## Gotchas
- **Offload the crawl (§9).** `cb_builder.py` reads the tree and builds/merges the graph; your context
  reads only its stdout. Hand-reading a large repo into context is the failure mode.
- **Never read the master graph back (token bound).** Query it via `explain`/`diff`; don't load
  `codebase-graph.md` whole at scale.
- **Incremental scan (§4).** Re-running `scan` re-crawls only changed files; reuse the prior graph.
- **Regex extraction is approximate.** It maps structure well but isn't a full parser — flag, don't
  fabricate, uncertain edges.
- **Stay in scope (§10).** This skill MAPS; it does not edit:
  - `→ dùng code-senior cho` thay đổi code (dùng `diff` mode TRƯỚC để biết blast radius).
  - `→ dùng knowledge-graph cho` đồ thị tri thức của bài báo.
