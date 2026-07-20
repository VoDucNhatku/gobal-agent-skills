---
name: executing-plans
description: Executing plans for GOBAL AGENT — implements a written plan task by task with per-task verification, plan-reality drift detection, and STOP-and-REGAIN on divergence. Source: superpowers (executing-plans) + gobal-orchestrator stop-regain protocol. Use when you have a written implementation plan to execute. It executes plans; it does NOT write them (use writing-plans) and does NOT replace the final done-gate (use verification-before-completion).
argument-hint: <plan-file>
allowed-tools: Read Write Edit Bash Glob
---

# Executing Plans

> **Source:** superpowers (executing-plans) + stop-regain (gobal-orchestrator)
> **Purpose:** Load plan, review critically, execute task-by-task with verification, report honestly.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

---

## Step 1 — Load, review, inventory assumptions

1. Read the plan file completely.
2. Review critically — identify questions or concerns; raise them with the user BEFORE starting.
3. **List the plan's assumptions** (files/APIs that must exist, framework versions, test
   commands, external services). This list is what Step 2 checks against reality.
4. No concerns → create todos for the plan items and proceed.

## Step 2 — Execute task-by-task (the loop)

For each task, in plan order:
1. Mark in_progress (one task at a time — never batch).
2. **Pre-check:** do the assumptions this task relies on still hold? (path exists, API
   signature matches, dependency installed). Diverged → go to STOP-and-REGAIN below.
3. Follow the plan's steps exactly (plans have bite-sized steps).
4. **Run the task's verification — Iron Law:** no verification command actually run and
   passed = task NOT completed. Never mark done from memory or intention
   (→ `verification-before-completion` for the rationalization table).
5. Mark completed. Discovered extra work → append to the plan as a NEW item; do not
   detour inline (scope guard).

## STOP-and-REGAIN — when reality diverges from the plan

The plan is a prediction; the codebase is the truth. When they disagree:

1. **STOP** — do not silently improvise a different design and keep going.
2. **Name the divergence out loud:** "Plan giả định X, thực tế là Y."
3. Classify:
   - **Small** (renamed file, moved function, extra param): adapt in place, record the
     deviation for the checkpoint report.
   - **Structural** (missing dependency, wrong architecture assumption, API that doesn't
     exist, verification fails repeatedly): return to the user / plan author with the
     divergence + suggested plan change. Do not build on a wrong foundation.
4. Resume only from a verified-correct base.

**Ask for clarification rather than guessing** — also when an instruction is simply unclear.

## Checkpoint reporting

After each phase (or ~3 tasks), report in Vietnamese, 3–5 lines: tasks done (verified) ·
deviations from plan (from STOP-and-REGAIN records) · what's next. A long execution with
zero reported deviations that later turn up in review is a failure of THIS step.

## Step 3 — Complete development

All tasks completed and verified →
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- Use `finishing-a-development-branch` for the final steps.

---

## Remember

- Review critically first; inventory assumptions.
- Follow plan steps exactly; verify EVERY task before marking it done.
- Divergence → STOP-and-REGAIN, never silent improvisation.
- Discovered work becomes a plan item, not an inline detour.
- Never start implementation on main/master without explicit user consent.

## Integration

- `writing-plans` — creates the plan this skill executes
- `using-git-worktrees` — isolated workspace
- `verification-before-completion` — the final done-gate (Iron Law + rationalization table)
- `gobal-orchestrator` — stop-regain protocol is the same discipline at orchestration level
- `finishing-a-development-branch` — completion workflow
