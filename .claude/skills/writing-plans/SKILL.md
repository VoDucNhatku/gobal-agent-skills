---
name: "writing-plans"
description: "Writing plans for GOBAL AGENT — creates detailed implementation plans from a spec or requirements. Bite-sized tasks (2-5 min each), exact file paths, complete code in every step, no placeholders. Source: superpowers (writing-plans). Use when you have a spec before touching code."
argument-hint: "<spec-file | requirements>"
allowed-tools: "Read Write Bash Glob"
---

# Writing Plans

> **Source:** superpowers (writing-plans)
> **Purpose:** Turn a spec into a bite-sized, executable implementation plan.

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the codebase and questionable taste. Document everything: which files to touch, code, testing, docs. Give the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `notes/plan-<slug>.md`

---

## Scope Check

If the spec covers multiple independent subsystems, suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

---

## File Structure

Before defining tasks, map out which files will be created or modified:
- Design units with clear boundaries and well-defined interfaces
- Prefer smaller, focused files over large ones
- Files that change together should live together
- In existing codebases, follow established patterns

---

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate.

**Each step is one action (2-5 minutes):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

---

## Plan Document Header

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **Goal:** [One sentence describing what this builds]
> **Architecture:** [2-3 sentences about approach]
> **Tech Stack:** [Key technologies/libraries]

## Global Constraints
[Project-wide requirements — version floors, dependency limits, naming rules]

---
```

---

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks]
- Produces: [what later tasks rely on]

- [ ] **Step 1: Write the failing test**
```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**
```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**
Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

---

## No Placeholders

Every step must contain the actual content. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code)
- Steps that describe what to do without showing how
- References to types/functions not defined in any task

---

## Self-Review

After writing the complete plan:
1. **Spec coverage:** Skim each section/requirement. Can you point to a task that implements it?
2. **Placeholder scan:** Search for red flags from "No Placeholders" section.
3. **Type consistency:** Do types/method signatures in later tasks match earlier tasks?

Fix issues inline.

---

## Execution Handoff

After saving the plan:

> "Plan complete and saved to `notes/plan-<slug>.md`. Two execution options:
>
> 1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks
> 2. **Inline Execution** — Execute tasks in this session, batch execution with checkpoints
>
> Which approach?"

---

## Cross-References

- `brainstorming` → Provides the spec this plan implements
- `spec-writer` → Formal specification (alternative input)
- `executing-plans` → Executes the plan
- `subagent-driven-development` → Subagent execution pattern
