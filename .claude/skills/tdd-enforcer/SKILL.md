---
name: "tdd-enforcer"
description: "TDD enforcer for GOBAL AGENT — enforces strict Test-Driven Development with vertical slices. Pipeline: RED (write failing test) → GREEN (minimal code to pass) → REFACTOR (clean up). One test at a time. Modes: enforce (full TDD cycle for new code), slice (vertical slice TDD), retrofit (add tests to existing code), bugfix (Prove-It Pattern). Source: addyosmani (test-driven-development) + superpowers (test-driven-development) + mattpocock (engineering/tdd). It enforces TDD; it does NOT write production code without tests first."
argument-hint: "<feature | component> [enforce|slice|retrofit|bugfix]"
allowed-tools: "Read Write Edit Glob Bash"
---

# TDD Enforcer

> **Source:** addyosmani agent-skills (test-driven-development) + superpowers (test-driven-development) + mattpocock skills (engineering/tdd)
> **Purpose:** Enforce test-first development with vertical slicing.

## The Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

If you wrote code before the test, delete it. Start over. No exceptions.

---

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `enforce` | Full TDD cycle for new code | New feature/component from scratch |
| `slice` | Vertical slice TDD | One complete path through the stack |
| `retrofit` | Add tests to existing code | Legacy code without tests |
| `bugfix` | Prove-It Pattern | Fixing a reported bug |

---

## RED-GREEN-REFACTOR Cycle

### RED — Write Failing Test

1. Write ONE minimal test showing what should happen
2. **Verify RED:** Watch it fail (MANDATORY, never skip)
3. The test must fail for the RIGHT reason (not because of syntax error)

### GREEN — Minimal Code

1. Write simplest code to pass the test
2. **Verify GREEN:** Watch it pass (MANDATORY)
3. No extra features, no "while I'm here"

### REFACTOR — Clean Up

1. Clean up code (only after green)
2. Keep tests passing
3. Remove duplication, improve names, simplify

### Repeat

Go back to RED for next behavior.

---

## Mode: enforce — Full TDD Cycle

### Process

1. **Understand the requirement** — What behavior is needed?
2. **Write failing test** — One test, one behavior
3. **Watch it fail** — Confirm it fails correctly
4. **Write minimal code** — Simplest thing that passes
5. **Watch it pass** — Confirm green
6. **Refactor** — Clean up, keep green
7. **Repeat** — Next behavior

### Good Test Requirements

- **One behavior** per test
- **Clear name** that describes the behavior
- **Real code** (no mocks unless unavoidable)
- **Shows intent** (demonstrates desired API)

---

## Mode: slice — Vertical Slice TDD

### Vertical Slicing (Preferred)

Build one complete path through the stack:
```
DB → API → UI (one feature, end to end)
```

### Why Vertical, Not Horizontal

| Horizontal (WRONG) | Vertical (RIGHT) |
|-------------------|------------------|
| Write all tests first | One test → one implementation → repeat |
| Then all implementation | Each test drives one slice |
| Produces "crap tests" | Tests verify real behavior |

### Slice Process

1. Pick one user-facing behavior
2. Write test for that behavior (RED)
3. Implement just enough to pass (GREEN)
4. Refactor (REFACTOR)
5. Next slice

---

## Mode: bugfix — Prove-It Pattern

### The Prove-It Pattern

```python
Bug report → Write failing test → Confirm bug → Fix → Test passes → Full suite
```

### Steps

1. **Write test that demonstrates bug** — Reproduce the exact failure
2. **Confirm bug** — Test FAILS (proves bug exists)
3. **Implement fix** — Minimal change addressing root cause
4. **Test passes** — Proves fix works
5. **Full suite** — No regressions

### Critical Rule

Never fix a bug without a test that proves the bug existed and now doesn't.

---

## Mode: retrofit — Add Tests to Existing Code

### Process

1. **Read the code** — Understand what it does
2. **Identify key behaviors** — What should this code do?
3. **Write tests for existing behavior** — Not what you wish it did
4. **Run tests** — They should pass (code already works)
5. **Now you have safety net** — Refactor with confidence

### Priority Order

1. Critical paths (auth, payments, data integrity)
2. Bug-prone areas (complex logic, edge cases)
3. Frequently changed code
4. Public interfaces/APIs

---

## Test Pyramid

```
E2E (~5%)
/ \
Integration (~15%)
/ \
Unit Tests (~80%)
```

- **Unit tests:** Fast, isolated, test single units
- **Integration tests:** Test component interactions
- **E2E tests:** Test full user flows (sparingly)

---

## Test Quality Rules

### DAMP Over DRY

**DAMP:** Descriptive And Meaningful Phrases in test names and setup.
Each test should be readable as documentation. Don't sacrifice clarity to avoid duplication.

### Test State, Not Interactions

Assert outcomes, not method calls.

```python
# BAD: expect(mockFn).toHaveBeenCalledWith('x')
# GOOD: expect(result).toBe('expected value')
```

### Real Over Fake

Preference order: Real > Fake > Stub > Mock
Use real implementations when possible. Mocks hide integration problems.

### Arrange-Act-Assert

```python
# Arrange — set up test data
# Act — execute the behavior
# Assert — verify outcome
```

### One Assertion Per Concept

A test should verify ONE behavior. Multiple assertions are OK if they verify the same concept.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Testing mock behavior | Tests that mock exists, not that component works | Use real implementations |
| Test-only methods in production | Session.destroy() only used in tests | Remove test-only methods |
| Mocking without understanding dependencies | Mock breaks test logic | Understand before mocking |
| Incomplete mocks | Only fields you think you need | Include all downstream dependencies |
| Integration tests as afterthought | Written last, brittle | Write alongside unit tests |
| Horizontal slicing | Write all tests first, then all code | Vertical slices: one test → one impl |
| Snapshot abuse | Snapshots that never get reviewed | Snapshots for stable output only |

---

## Common Rationalizations (and why they're wrong)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic |
| "Deleting X hours is wasteful" | Sunk cost fallacy |
| "TDD is dogmatic, I'm being pragmatic" | TDD IS pragmatic |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. |

---

## Browser Testing

Unit tests alone aren't enough for UI.

- Use Chrome DevTools MCP for DOM inspection, console, network, performance, screenshots
- Test actual rendered output, not just component logic
- Verify accessibility (keyboard nav, screen reader)

---

## Cross-References

- `code-senior` → Code quality and implementation patterns
- `debug-investigator` → Systematic debugging when tests reveal bugs
- `code-reviewer` → Review tests as part of code review
- `spec-writer` → Write spec before TDD implementation
- `build-ui` → UI implementation with test coverage
