---
name: "knowledge-graph"
description: "Extracts a typed knowledge graph from one paper (or `all`) — typed entities (Method, Model, Dataset, Metric, Concept, Task, Problem, Component, PriorWork) and typed relations as subject—relation→object triples — emits a per-paper triples table + a Mermaid graph, then merges into a cumulative project-wide master graph that de-duplicates shared datasets/metrics/concepts and tags each edge with its source paper. Output prose is Vietnamese (academic); entity/relation labels and identifiers English. Triggers — knowledge graph, đồ thị tri thức, build a KG, extract entities and relations, trích xuất thực thể quan hệ, map the concepts, bản đồ khái niệm, typed triples, what connects these papers, graph of the field. Builds a structured entity–relation graph; it does NOT give prose overview (use paper-read), critique a method (use paper-method), or compare/taxonomize in prose (use paper-synthesize)."
argument-hint: "<id|file|path|all>"
allowed-tools: "Skill Agent Read Write Glob Bash"
---

# Knowledge Graph (đồ thị tri thức)

Turns a paper into a **typed knowledge graph** — entities tagged by type and relations as
`subject —relation→ object` triples — and merges it into one cumulative master graph for the
whole corpus, so the graph grows into a map of the field as you process more papers.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual §1, input
resolution §2, output + preview-not-dump §3, reuse-before-read §4, fidelity §8, mode scaling §7,
script-offloading §9, scope handoff §10). The full entity-type and relation-type vocabulary +
the merge/de-dup rules live in `references/kg-schema.md` — read it when you run; **reference it,
never inline it**. Human-facing prose is Vietnamese (học thuật); type/relation labels and ids
stay English.

## Procedure

### Phase 0 — Resolve target
Resolve `$ARGUMENTS` per §2 (id | filename | path | `all`). If empty/ambiguous, list `papers/`
+ `notes/INDEX.md` and ask **once**. For `all`, process each id, then run one final merge.

### Phase 1 — Reuse-before-read (§4)
Consult `notes/INDEX.md`, then prefer an existing distilled artifact over the raw PDF, in order:
`notes/<id>-read-summary.md` → `notes/<id>-method.md` → `notes/<id>-read-gist.md`. Seed entity/
relation extraction from the note; open the PDF only to fill gaps (e.g. exact dataset/metric
names), reading only high-density regions (§6). For `all` (5+), this reuse is what keeps the
batch token-bounded (§7) — never re-read every PDF when notes exist.

### Phase 2 — Load the schema, then extract
Read `references/kg-schema.md` and follow its type set and relation set **exactly** — do not
invent new types. Extract:
1. **Entities**, each tagged with a type from the fixed set (Method, Model, Dataset, Metric,
   Concept, Task, Problem, Component, PriorWork).
2. **Relations** as triples from the fixed set (proposes, addresses, uses, part-of, based-on,
   evaluated-on, measured-by, improves-over, compared-with, trained-on).
Every triple must be grounded in the source (§8); do not fabricate edges. Missing → omit, never
invent.

### Phase 3 — Build the JSON spec and offload to the script (§9)
Do **not** hand-write the Mermaid block or the master-graph merge by hand. Assemble a compact
JSON spec — `{ paper_id, title, entities: [{id, type, label}], triples: [{s, r, o}] }` — write
it to `/tmp/knowledge-graph_<id>.json`, and call the bundled builder:

```
python "<skills>/knowledge-graph/scripts/kg_builder.py" /tmp/knowledge-graph_<id>.json
```

The script emits the per-paper `notes/<id>-kg.md` (triples table + Mermaid `flowchart LR` with a
classDef per type and labeled edges) **and** merges into `notes/knowledge-graph.md`
(de-duplicating shared datasets/metrics/concepts by normalized label, tagging each edge with the
source id). You provide the facts; the script provides every byte of boilerplate format.

### Phase 4 — Preview (§3)
Print to chat ONLY a **5–7 line** Vietnamese preview + the two saved paths: entity count by type,
triple count, the master graph's new node/edge totals after merge. **Never** paste the triples
table or the Mermaid block into chat.

## Output schema (files)
- `notes/<id>-kg.md` — per-paper: triples table (`Subject | Relation | Object`) + Mermaid graph.
- `notes/knowledge-graph.md` — cumulative master graph (merged, de-duplicated, edges tagged with
  source ids).
Both written by `scripts/kg_builder.py`. If terms are defined, close the per-paper file with a
`## Thuật ngữ (Glossary)` table per §1.

## Gotchas
- **Use the fixed vocabulary (`references/kg-schema.md`).** A free-for-all type set makes the
  master graph un-mergeable; stick to the 9 entity types + 10 relation types.
- **Offload the format (§9).** Never hand-write the Mermaid syntax or the merge logic — emit the
  JSON spec and call `kg_builder.py`. Hand-writing both is the classic token + correctness leak.
- **Reuse notes for `all` (§4/§7).** Re-reading 80 PDFs to extract triples is the failure mode;
  read the distilled notes when they exist.
- **NEVER read the master graph back into context.** Only `kg_builder.py` reads/writes
  `notes/knowledge-graph.md` and `notes/knowledge-graph.json`. The preview node/edge counts come
  from the **script's stdout**, not from re-reading the growing master file — at 80 papers that
  file is large and reading it back defeats the token bound.
- **Triples are grounded (§8).** Every edge traces to the paper; no invented relations, no
  fabricated dataset/metric names.
- **Don't dump to chat (§3).** Table + Mermaid stay in the files; chat gets the count preview +
  paths.
- **Stay in scope (§10).** This skill emits a structured graph. It does not write prose analysis:
  - `→ dùng paper-read cho` overview / summary / intuition / mindmap.
  - `→ dùng paper-synthesize cho` so sánh / phân loại / khoảng trống bằng văn xuôi.
