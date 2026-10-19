---
name: "admin"
description: "Entry point and router for the research workbench. Use when the user says admin, gives a multi-step research task, or asks for a specialty not covered by another listed skill: writing/LaTeX, study handbooks, translation, web/UI, deploy, CV, code process. Not for one-line questions. Triggers — admin, điều phối, làm giúp nhiều bước, viết paper, sổ tay, dịch, web, deploy, CV."
---

# admin — route, then get out of the way

Your job is to pick the cheapest path that fully answers the request. Routing is not work;
keep it to one decision and hand over.

## 1. Decide the path (one pass)

| Request | Path |
|---|---|
| Narrow question answerable from one file or general knowledge | Answer directly. No skill. |
| Covered by a listed core skill | Load that skill and follow it. |
| A specialty listed in §2 below | Read that skill's `SKILL.md` from disk and follow it. |
| Several independent pieces | Do them in dependency order; parallel workers only if the host has them and the user asked for depth (`admin sâu`). |
| Two readings would change the action materially | Ask one question; otherwise state the assumption and continue. |

Core skills (already in the catalog): `paper-read` (one paper), `paper-synthesize` (many
papers), `research-assess` (judge a proposal, direction or claim), `evidence-check`
(verify claims, numbers, citations), `experiment` (reproduce, train, read logs),
`code-senior` (implement, debug), `research-memory` (ledger, lessons, notes),
`research-write` (manuscript pipeline).

## 2. Specialties not in the catalog
These skills are hidden from the catalog only to save tokens; they are fully usable. Pick one
below, read `../<skill>/SKILL.md` (relative to this file) and follow it as if it had been loaded.

### Writing and LaTeX
| Skill | Use when |
|---|---|
| `paper-submission` | draft, format (IEEEtran, CVPR) or write a rebuttal for a manuscript |
| `paper-storytelling` | restructure a manuscript's narrative (research questions, contributions, results-as-findings) |
| `style-humanizer` | polish wording of a draft without changing numbers, claims or citations |
| `citation-guard` | full reference-list audit with DOI/Crossref lookups and orphan detection |
| `ieee-q1-devil-advocate` | harsh review of a finished manuscript before submission |
| `latex-fix` | math does not render in notes (KaTeX/MathJax) |
| `latex-tikz-generator` | draw a pipeline/architecture figure in TikZ |
| `vi-translate` | faithful academic translation of a passage or paper |

### Learning
| Skill | Use when |
|---|---|
| `study-forge` | printable study handbook from slides, formulas or code |
| `claim-forge` | critical-reading handbook for an argument-based text (economics, law, policy) |
| `study-tutor` | interactive tutoring, practice, quizzes over a session |
| `concept-explainer` | explain one concept at a chosen depth with an analogy |
| `knowledge-quiz` | generate a quiz from notes |
| `knowledge-graph` | typed entity graph from papers |

### Code process
| Skill | Use when |
|---|---|
| `code-reviewer` | structured review of a diff |
| `understand-codebase` | map an unfamiliar repository |
| `spec-writer`, `writing-plans`, `executing-plans` | spec → plan → execute a larger feature |
| `tdd-enforcer`, `test-framework` | test-first work; validating this skill suite |
| `architect`, `requirement-ladder`, `domain-modeling` | architecture docs, requirements, domain models |
| `brainstorming` | explore options before building something new |
| `security-review` | threat model or security audit |
| `using-git-worktrees`, `finishing-a-development-branch`, `requesting-code-review`, `receiving-code-review` | git workflow around a branch |
| `self-evaluator`, `verification-before-completion`, `ship-validator` | final checks before delivery or release |
| `writing-skills` | create or edit a skill in this suite |

### Web and product
| Skill | Use when |
|---|---|
| `design-web` | choose the visual direction of a page |
| `build-ui` | implement UI from a direction or existing tokens |
| `review-frontend` | audit a page for generic design, accessibility, tokens |
| `backend-engineer`, `fullstack-builder` | APIs, data models, vertical slices |
| `build-admin-dashboard`, `scaffold-course-platform` | admin CRUD surfaces, course platform scaffold |
| `scaffold-project` | folder structure and team git workflow for a new repo |

### Ops and other
| Skill | Use when |
|---|---|
| `deploy-admin`, `monitor-setup`, `rollback-manager` | deploy, monitor, roll back |
| `ai-cv-forge` | CV and career profile for an AI graduate |
| `context-compressor`, `token-budget` | the conversation is near its context limit |

## 3. Before research work
If the project has `notes/lessons.md`, read its first 40 lines once per task and apply
the lessons that match. If the request touches novelty, venue or a proposal, the project
scope rule in `../_shared/research-integrity.md` §1 applies. For web research with
several sources, read `references/research-protocol.md` (search budgets, stop rules) and
`references/source-quality.md` only when choosing between conflicting sources.

## 4. Modes
- `admin nhanh` — no workers, no web search unless the fact must be checked; give a bounded
  answer and say what a deeper pass would add.
- `admin sâu` — counts as consent to use subagents/workers when the host has them; use them
  for independent reading or for an independent critic, never for sequential steps.

## 5. Report
Answer first. Then, only if anything was checked or left open:
`Đã kiểm: … · Chưa kiểm: … · Bước tiếp: …`. No invented progress, URLs, numbers or
background tasks.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
