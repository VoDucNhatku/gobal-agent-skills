# Knowledge Graph Schema

Entity types and relation types for the GOBAL AGENT knowledge graph.
Read this file; reference it, never inline it.

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
| `Architecture` | A system or network architecture |
| `Loss` | A loss function or objective |
| `Hyperparameter` | A configurable training parameter |

## Relation Types

| Label | Description | Domain |
|-------|-------------|--------|
| `trained_on` | Model trained on Dataset | Model → Dataset |
| `evaluated_on` | Method evaluated on Dataset | Method → Dataset |
| `outperforms` | A beats B on Metric | Method/Model → PriorWork |
| `uses` | Component uses Component/Loss | Component → Component/Loss |
| `extends` | Method extends PriorWork | Method → PriorWork |
| `introduces` | Paper introduces Concept/Method | Paper → Concept/Method |
| `reports` | Paper reports Metric result | Paper → Metric |
| `addresses` | Method addresses Problem | Method → Problem |
| `part_of` | Component part of Architecture | Component → Architecture |
| `employs` | Method employs Concept/Loss | Method → Concept/Loss |

## Merge / De-dup Rules

1. **Entity dedup:** same label + same normalized name → single node. Normalize: lowercase, strip diacritics for English names, collapse whitespace.
2. **Edge dedup:** if an edge (source, relation, target) exists from any paper, do not re-add on re-run with the same or different paper.
3. **Source tagging:** every edge carries `source_paper: <id>` so provenance is always recoverable.
4. **Node labels:** do not merge across entity types even if strings match (e.g. a `Concept` "BERT" vs a `Model` "BERT" are different nodes).
