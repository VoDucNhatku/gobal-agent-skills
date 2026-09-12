# Knowledge Graph Schema

Entity types and relation types for the GOBAL AGENT knowledge graph.
This file is the **single source of truth** and stays in lock-step with
`scripts/kg_builder.py` (its `ENTITY_TYPES` / `RELATION_TYPES` whitelists).
Read it; reference it, never inline it.

## Entity Types

| Label | Description |
|-------|-------------|
| `Method` | A technique, algorithm, or approach |
| `Model` | A named model or architecture |
| `Dataset` | A dataset used for training or evaluation |
| `Metric` | An evaluation metric or measure |
| `Concept` | A general concept or term |
| `Task` | A problem type or task domain |
| `Problem` | A specific problem being addressed |
| `Component` | A building block or subsystem |
| `PriorWork` | A referenced prior paper or work |

## Relation Types (kebab-case — matches `kg_builder.py` whitelist exactly)

| Label | Description | Domain |
|-------|-------------|--------|
| `proposes` | Method/Model proposes an idea | Method/Model → Concept/Problem |
| `addresses` | Method addresses a Problem | Method → Problem |
| `uses` | Component/Method uses a building block | Component/Method → Component/Loss-like |
| `part-of` | Component is part of a larger system | Component → Method/Model |
| `based-on` | Method is based on a PriorWork | Method → PriorWork |
| `evaluated-on` | Method evaluated on a Dataset | Method → Dataset |
| `measured-by` | Method/Model measured by a Metric | Method/Model → Metric |
| `improves-over` | Method beats a PriorWork/baseline | Method/Model → PriorWork |
| `compared-with` | Method is compared with another | Method → Method/PriorWork |
| `trained-on` | Model trained on a Dataset | Model → Dataset |

## Merge / De-dup Rules

1. **Entity dedup:** same label + same normalized name → single node. Normalize: lowercase, strip diacritics for English names, collapse whitespace.
2. **Edge dedup:** if an edge (source, relation, target) exists from any paper, do not re-add on re-run with the same or different paper.
3. **Source tagging:** every edge carries `source_paper: <id>` so provenance is always recoverable.
4. **Node labels:** do not merge across entity types even if strings match (e.g. a `Concept` "BERT" vs a `Model` "BERT" are different nodes).

## Edge Strength

Every edge carries a `strength` tag — inferred by the extractor from the paper's
text, not computed. This lets any downstream reader of the KG (e.g. a future synthesis
pass) weigh evidence quality instead of treating every edge as equally certain.

| Strength | When to assign | Downstream trust |
|----------|---------------|-----------------|
| `primary` | The paper **explicitly states** the relation with evidence (experiment, theorem, table, figure) | High — citable as direct evidence |
| `secondary` | The paper **implies** the relation (architectural diagram, naming convention, "based on X") but does not test it | Medium — useful for trend analysis, not for strong claims |
| `inferred` | The relation is a **reasonable reader inference** not present in the paper (e.g. Method A and Method B share a dataset → `compared-with` inferred) | Low — must flag as inferred in any synthesis |

**Rules:** default to `secondary` when unsure. Never assign `primary` to a
relation the paper does not explicitly test or state. Inferred edges must be
tagged `(inferred)` in the per-paper triples table so any reader can filter or
down-weight them at a glance.
