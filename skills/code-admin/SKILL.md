---
name: "code-admin"
description: "Code domain admin for GOBAL AGENT — coordinates code tasks: understand → plan → implement → review → verify. Routes to appropriate code skills based on task type. Modes — implement, debug, review, plan. It coordinates; it does NOT write code directly. Triggers — task code nhiều bước, điều phối code, làm tính năng, sửa bug, review code, viết spec rồi code."
---

# Code Admin

Coordinate code development workflow. Route to the right skill. Do not write code directly.

## The four gates — enforced by the WORKERS, not here

These used to be written out in this file. That was a real hole: they only loaded if you came through
this router, and calling `code-senior` directly — the normal way anyone works — skipped every one of
them. **A gate you can walk around by picking another door is not a gate.** They now live inside the
skill that does the work, so the entry path no longer matters:

| Gate | Enforced in |
|---|---|
| **No-Op Test** — the change must actually change behaviour | `code-senior` Phase 2 |
| **No Fabricated Numbers** — every metric comes from a real run with a log path | `code-senior` Phase 2 |
| **TDD Law** — no production code before a failing test | `tdd-enforcer` (its own Iron Law) |
| **No red-capable command, no Phase 2** — reproduce before theorising | `debug-investigator` (its own Iron Law) |

An experiment plan feeding a research proposal must also clear the feasibility gate in
`../../rules/research-proposal-integrity.md` §5 (data · compute · baseline · dependencies) before
being called runnable.

## Pipeline Workflow

```
Code Request
│
▼
1. understand-codebase (Mandatory for new projects)
│
▼
2. Route by Mode:
├── plan → spec-writer
├── implement → code-senior (must follow TDD; its Algorithm Justification Gate
│                 covers complexity + provenance for real algorithmic choices)
├── debug → debug-investigator
├── review → code-reviewer
└── notebook → paper-to-notebook
│
▼
3. post-implementation-review (code-reviewer)
│
▼
4. Verification & Commit (Verify all tests pass)
```

## Routing Rules & Handoff

When coordinating, explicitly state the handoff path.
*Example: "Route to `code-senior` to implement the sorting algorithm. Next required skill: `code-reviewer`."*

| Request Type | Primary Skill | Prerequisite Skill |
|-------------|--------------|--------------------|
| "Build feature X" | `code-senior` | `spec-writer` |
| "Fix bug in X" | `debug-investigator` | `understand-codebase` |
| "Review this code" | `code-reviewer` | None |
| "Understand codebase" | `understand-codebase`| None |
| "Write spec for X" | `spec-writer` | `understand-codebase` |
| "Code tái lập bài báo / Implement paper" | `paper-to-notebook` | `paper-method` |

## Verification Checklist (Before declaring Done)
Before you conclude any implementation or debug task, verify:
- [ ] Are all unit tests passing?
- [ ] Was the "No-Op Test" passed? (Does this actually change behavior?)
- [ ] Is the architectural pattern consistent with the rest of the codebase?
- [ ] Has the code been reviewed by `code-reviewer`?
- [ ] Every reported number traceable to an executed run (log/artifact path) — no fabricated results (Iron Law 4)?

If any box is unchecked, you are NOT done. Route back to `code-senior` or `debug-investigator`.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
