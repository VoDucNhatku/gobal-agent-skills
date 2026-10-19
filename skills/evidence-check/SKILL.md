---
name: "evidence-check"
description: "Checks claims against their evidence before they are trusted or delivered: numbers recomputed from data, statements against the cited passage, reference lists for unverifiable entries, document versions and recorded corrections, and the reasoning that links them. Use for 'có đúng không', 'số này có thật không', 'kiểm tra trích dẫn', and before calling research work done. Triggers — kiểm tra, xác minh, có bịa không, đúng với số liệu không, trích dẫn, tài liệu tham khảo."
---

# evidence-check — what holds, what does not, and what was not checked

Policy: `../_shared/evidence.md` (labels, depth, versions, fabrication patterns).
Reasoning questions: `../_shared/reasoning-check.md`.

## 1. List the claims
Extract the material claims (numbers, comparisons, causal statements, citations, "no prior
work"). Ignore wording that carries no fact.

## 2. Check each claim with the matching method
| Claim type | Method |
|---|---|
| Number or aggregate | recompute from the raw file (script or shown arithmetic); compare |
| Statement about a source | open the cited passage; does it entail the exact scope? |
| Reference entry | identity checked only if looked up (DOI resolver, Crossref, publisher page); otherwise `[chưa xác minh]` — never "đúng" from memory. Flag impossible or suspicious details (issue numbers, DOI patterns, too-good claims) |
| Value that has versions | use the newest declared version; say which and what changed |
| Value from an older note | check `notes/corrections.md` and ledger `T-`/`revised→` rows first |
| Derived, causal or universal claim | the six reasoning questions |

## 3. Report
For each claim: `SUPPORTED / REFUTED / CONTESTED / NEI` + evidence (file:line, table,
command output) + fix (keep / narrow / remove). Then one scope line:
`Đã kiểm: nguồn ☑ số liệu ☑ suy luận ☐ …` — a box is ticked only when that check ran.
Never report "không còn lỗi" if any category was not checked.

For a full manuscript reference audit with orphan detection and DOI lookups, read
`../citation-guard/SKILL.md` and follow it.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
