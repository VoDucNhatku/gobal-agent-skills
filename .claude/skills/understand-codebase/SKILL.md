---
name: "understand-codebase"
description: "Maps an existing codebase into a bounded structural summary using actual file and symbol searches. Use when understanding a repository, explaining a symbol, onboarding, or checking change impact. Triggers — hiểu codebase, map the project, dependency graph, onboard me, impact of this change. It inspects existing code; it does NOT change code or claim a complete static call graph."
allowed-tools: "Read Glob Grep Bash"
argument-hint: "<scan | explain <file|symbol> | onboard | diff> [path-glob]"
---

# Understand Codebase (hiểu codebase qua knowledge graph)

Builds a structural knowledge graph of a real codebase — nodes (module / file / symbol) and edges
(imports / calls / defines) — so the agent (and you) can see how things connect before editing.
Token-bounded by design: file discovery precedes targeted symbol searches and ranged reads.
(Distinct from `knowledge-graph`, which graphs a research paper, not source code.)

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — graph labels/identifiers English,
report Vietnamese; output + preview §3; reuse-before-read §4; strategic reading §6; script-offloading
§9; scope handoff §10). Read at run time; never inline.

## Procedure

### Phase 0 — Resolve mode + scope
Parse mode: `scan` (default) | `explain <file|symbol>` | `onboard` | `diff`. Optional path-glob limits
the scope (e.g. `src/**`). Consult `notes/INDEX.md` and an existing `notes/codebase-graph.md` first
(§4). Reuse only when the recorded commit/file hashes still match; do not claim automatic incremental crawling.

### Phase 1 — Bounded discovery (no bundled crawler)
This skill does not bundle an automatic graph extractor. Use the host's file-search capability or
`rg --files` for paths, then `rg -n` for specific declarations/imports/usages. Exclude dependencies,
build output and generated files; start with project manifests, entry points and at most 20 relevant
files. Read only relevant ranges. If `rg` is absent, use native file/search tools; PowerShell may use
`Get-ChildItem -File` and `Select-String` on an explicit bounded file set. Do not install tools silently.

Record observed file/symbol relationships with file and line locators in `notes/codebase-graph.md`.
Mark inferred dependencies explicitly. Search matches are candidates, not a complete call graph;
do not invent counts, hubs, cycles, JSON state or generated outputs that were not actually produced.

### Phase 2 — mode work
- **`scan`:** report observed modules, entry points and relationships, plus the inspected scope.
  Only report counts derived from actual discovery; mark coverage as partial when bounded.
- **`explain <file|symbol>`:** find the declaration and direct usage/import candidates, then read
  those specific ranges. Distinguish confirmed references from name collisions and dynamic calls.
- **`onboard`:** generate `notes/codebase-onboarding.md` — entry points, the main modules and their
  jobs, the hub files to read first, and a suggested reading order. (Confirm before sharing widely.)
- **`diff`:** run `git diff --name-only`, inspect relevant diffs, and search for changed symbols'
  callers/importers. Report confirmed and possible impact separately; state remaining uncertainty.

### Phase 3 — Preview (§3)
Print a **5-8 line** Vietnamese preview + the saved path(s): counts, top hubs, and for `explain`/
`diff` the dependents/impact list. Never paste the full graph or file bodies into chat.

## Output
- `scan` → `notes/codebase-graph.md` with locators, inspected scope and revision.
- `onboard` → `notes/codebase-onboarding.md`. `explain`/`diff` → chat report only.

## Gotchas
- **Bound context.** Discover paths first; do not read a large repository wholesale.
- **Recheck stale notes.** Compare revision/changed files before reusing a summary.
- **Search is approximate.** It does not prove exhaustive static/dynamic dependencies or cycles.
- **Stay in scope (§10).** This skill MAPS; it does not edit:
  - `→ dùng code-senior cho` thay đổi code (dùng `diff` mode TRƯỚC để biết blast radius).
  - `→ dùng knowledge-graph cho` đồ thị tri thức của bài báo.
