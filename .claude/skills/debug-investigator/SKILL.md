---
name: debug-investigator
description: Systematic debug investigator for GOBAL AGENT — finds root cause before attempting fixes. Four phases: investigate → pattern analysis → hypothesis → fix. Iron law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. Modes: investigate (Phase 1-2), hypothesis (Phase 3), fix (Phase 4), bisect (git bisect for regressions). Source: addyosmani (debugging-and-error-recovery) + superpowers (systematic-debugging) + mattpocock (engineering/diagnosing-bugs). It investigates; it does NOT apply fixes without completing Phase 1-3 first.
argument-hint: <bug description | error> [investigate|hypothesis|fix|bisect]
allowed-tools: Read Write Edit Glob Bash Grep
---

# Debug Investigator

> **Source:** addyosmani agent-skills (debugging-and-error-recovery) + superpowers (systematic-debugging) + mattpocock skills (engineering/diagnosing-bugs)
> **Purpose:** Systematic root-cause investigation before any fix.

## The Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Random fixes waste time and create new bugs.

---

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `investigate` | Phase 1-2: Reproduce + Pattern Analysis | New bug, unknown cause |
| `hypothesis` | Phase 3: Form and test hypothesis | After investigation, before fix |
| `fix` | Phase 4: Implement fix with guard | After hypothesis verified |
| `bisect` | git bisect for regressions | Bug appeared after known good state |

---

## Stop-the-Line Rule

When something breaks:

1. **STOP** — Stop adding features
2. **PRESERVE** — Preserve evidence (logs, state, error messages)
3. **DIAGNOSE** — Use triage checklist below
4. **FIX** — Root cause, not symptom
5. **GUARD** — Add regression test
6. **RESUME** — Only after verification

---

## Phase 1: Root Cause Investigation

### Triage Checklist (6 steps)

1. **Reproduce** — Make failure happen reliably. Exact steps. Does it happen every time?
2. **Localize** — Which layer? (UI / API / Database / Build / External / Test)
3. **Reduce** — Minimal failing case. Strip away everything unrelated.
4. **Fix Root Cause** — Ask "Why?" until actual cause (5 Whys technique)
5. **Guard Against Recurrence** — Write regression test
6. **Verify End-to-End** — Full flow works, not just the fix

### Investigation Steps

1. **Read error messages carefully** — Don't skip past errors/warnings. They contain clues.
2. **Check recent changes** — git diff, recent commits, new dependencies, environmental differences
3. **Gather evidence in multi-component systems** — Log data at each component boundary
4. **Trace data flow backward** — Through call stack from symptom to source

---

## Phase 2: Pattern Analysis

1. **Find working examples** — Similar working code in same codebase
2. **Compare against references** — Read completely, understand fully
3. **Identify differences** — List every difference, however small
4. **Understand dependencies** — What does this code depend on? What depends on it?

---

## Phase 3: Hypothesis and Testing

1. **Form single hypothesis** — State clearly: "I think X is root cause because Y"
2. **Test minimally** — Smallest possible change, one variable at a time
3. **Verify before continuing** — Does this confirm or refute hypothesis?
4. **When you don't know** — Say "I don't understand X" (not guess)

### Red Flags

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "One more fix attempt" (when already tried 2+)

### If 3+ Fixes Failed

**STOP. Question Architecture.** Discuss with human partner. You're fixing symptoms, not root cause.

---

## Phase 4: Implementation

1. **Create failing test case** — Simplest possible reproduction
2. **Implement single fix** — Address root cause, ONE change at a time
3. **Verify fix** — Test passes, no regressions
4. **If fix doesn't work** — Return to Phase 1
5. **Add regression test** — Guard against recurrence

---

## Mode: bisect — Git Bisect for Regressions

```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good <known-good-sha>

# Run test automatically
git bisect run npm test -- --grep "failing test"

# When found
git bisect log # see the culprit commit
git bisect reset # return to original state
```

---

## Non-Reproducible Bugs

### Types and Strategies

| Type | Strategy |
|------|----------|
| Timing-dependent | Add timestamps, artificial delays, increase loop count |
| Environment-dependent | Compare versions, data, config between working/broken |
| State-dependent | Check globals, shared caches, mutation order |

### Goal

Higher reproduction rate, not clean repro. Loop 100x, parallelize, add stress.

---

## Defense in Depth (4 Layers)

Add validation at multiple layers:

1. **Entry point** — Validate input at API boundary
2. **Business logic** — Validate state transitions
3. **Environment guards** — Validate assumptions about runtime
4. **Debug instrumentation** — Log key state transitions

---

## Condition-Based Waiting

Replace arbitrary timeouts with condition polling:

```python
# BAD: sleep(5) # hope it's enough
# GOOD: waitFor(() => element.exists(), timeout=5000) # poll until condition
```

---

## 10 Ways to Build a Feedback Loop (mattpocock)

In order of preference:

1. **Failing test** — Fastest, most reliable
2. **Curl/HTTP script** — For API debugging
3. **CLI invocation** — For script/tool debugging
4. **Headless browser script** — For UI debugging
5. **Replay captured trace** — For timing-dependent bugs
6. **Throwaway harness** — For isolated reproduction
7. **Property/fuzz loop** — For edge case discovery
8. **Bisection harness** — For regression isolation
9. **Differential loop** — Compare two versions
10. **HITL bash script** — Manual but structured

### Tighten the Loop

- Make it faster
- Make it sharper (more deterministic)
- A 30-second flaky loop is barely better than no loop
- A 2-second deterministic one is tight

---

## Cross-References

- `code-senior` → Code quality patterns for fixes
- `tdd-enforcer` → Write regression test after fix
- `code-reviewer` → Review fix before merge
- `security-review` → Security implications of bug
