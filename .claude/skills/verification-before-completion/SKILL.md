---
name: verification-before-completion
description: Verification before completion for GOBAL AGENT — standalone verification gate that must pass before claiming any work is done. Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION. Source: superpowers (verification-before-completion). Use when work is supposedly complete and you are about to claim it done.
argument-hint: [what-to-verify]
allowed-tools: Read Write Bash Glob
---

# Verification Before Completion

> **Source:** superpowers (verification-before-completion)
> **Purpose:** Iron Law verification gate — never claim done without fresh proof.

## Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION.**

Every claim of completion must be backed by a verification step run AFTER the work was done, not before. If you didn't watch it succeed with your own eyes, it didn't succeed.

---

## The Verification Protocol

### Step 1: Define What "Done" Means

Before verifying, explicitly state the acceptance criteria:
- What should work?
- What should the output look like?
- What would failure look like?

### Step 2: Run the Verification

**Run the actual verification command — do not assume, do not skip.**

```bash
# Examples (pick what applies):
npm test                    # Tests pass
pytest tests/ -v            # All tests green
go test ./...               # Go tests pass
cargo test                  # Rust tests pass
npm run build               # Build succeeds
python -m pytest --cov      # Coverage threshold met
```

**Watch the output.** Confirm all tests pass, build succeeds, or the command exits 0.

### Step 3: Check the Output

- Tests: All pass, no unexpected skips
- Build: No errors, output artifact exists
- Lint: No errors (or only pre-approved suppressions)
- Type check: No errors

### Step 4: Report Results

**If verification passes:**
```
✅ Verified: [what was verified] — all [N] checks passed.
```

**If verification fails:**
```
❌ Verification failed: [what failed] — [error summary].
Stopping. Fix required before claiming completion.
```

---

## Common Anti-Patterns (Rationalization Table)

| Excuse | Reality |
|--------|---------|
| "The tests passed earlier" | Earlier ≠ now. Re-run. |
| "It should work" | Should ≠ does. Verify. |
| "I'm confident it's correct" | Confidence ≠ evidence. Run the test. |
| "The build succeeded last time" | Last time ≠ this time. Rebuild. |
| "I'll verify after the user tests it" | You verify first. The user confirms second. |
| "It's a small change, it can't break anything" | Small changes break things. Always verify. |
| "The linter didn't complain" | Linter ≠ tests. Both matter. |
| "I checked manually" | Manual check ≠ automated verification. Run the suite. |

---

## When to Verify

| Situation | Must Verify? |
|-----------|-------------|
| After writing any code | ✅ Yes |
| After fixing a bug | ✅ Yes — regression test |
| After refactoring | ✅ Yes — same behavior |
| After adding a feature | ✅ Yes — new tests pass |
| After updating dependencies | ✅ Yes — nothing broke |
| Before claiming "done" | ✅ Always |
| Before creating a PR | ✅ Yes — CI equivalent |
| After merging | ✅ Yes — integration check |

---

## Verification Checklist

Before claiming any work complete:

- [ ] Ran the full test suite (not just a subset)
- [ ] All tests passed (green)
- [ ] Build/compile succeeded
- [ ] No new warnings introduced
- [ ] Type check passed (if applicable)
- [ ] Lint passed (if applicable)
- [ ] Watched the output — didn't just check exit code

---

## Integration

**Required workflow skills:**
- `tdd-enforcer` → Red-green-refactor cycle
- `code-reviewer` → Review before merge
- `finishing-a-development-branch` → Complete after verified
- `executing-plans` → Verify each task before marking complete

---

## Cross-References

- `tdd-enforcer` → TDD cycle with verification
- `code-reviewer` → Review process
- `finishing-a-development-branch` → Completion workflow
- `self-evaluator` → Self-assessment after verification
