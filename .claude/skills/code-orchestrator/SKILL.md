---
name: code-orchestrator
description: Code domain orchestrator for GOBAL AGENT — coordinates code tasks: understand → plan → implement → review → verify. Routes to appropriate code skills based on task type. Modes — implement, debug, review, plan. It orchestrates; it does NOT write code directly.
argument-hint: <code task> [implement|debug|review|plan]
allowed-tools: Skill Agent Read Write Glob Bash
---

# Code Orchestrator

Coordinate code development workflow. Route to the right skill. Do not write code directly.

## THE IRON LAWS OF CODE (Mandatory Gates)
1. **No-Op Test:** Every change must actually change behavior versus the default.
2. **The TDD Law:** NEVER write production code before a failing test. If you are modifying logic, write the test first, see it fail (RED), write the code (GREEN), then REFACTOR.
3. **No Red-Capable Command, No Phase 2:** If you are debugging, you MUST have a command that reliably reproduces the error. If you catch yourself reading code to build a theory before this command exists, STOP.
4. **No Fabricated Numbers:** Every reported metric/benchmark/result must come from an actually executed run with a readable log or artifact path. Unexecuted estimates are labeled "ước tính — chưa chạy". An experiment plan feeding a research proposal must pass the feasibility gate of `~/.claude/rules/research-proposal-integrity.md` §5 (data · compute · baseline · dependencies) before being presented as runnable.

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

When orchestrating, explicitly state the handoff path. 
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
