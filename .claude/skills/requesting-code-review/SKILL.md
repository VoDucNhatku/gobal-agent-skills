---
name: requesting-code-review
description: Requesting code review for GOBAL AGENT — prepares a branch for review by ensuring it meets quality standards before requesting human or AI review. Source: superpowers (requesting-code-review). Use when implementation is complete and you want a review before merge.
argument-hint: [branch-name]
allowed-tools: Read Write Bash Glob
---

# Requesting Code Review

> **Source:** superpowers (requesting-code-review)
> **Purpose:** Prepare and request review — don't waste reviewer's time with half-finished work.

## Iron Law

**NEVER REQUEST REVIEW ON UNVERIFIED WORK.**

Before requesting review, you must have:
1. Run the full test suite — all pass
2. Run the linter — no errors
3. Run the type checker — no errors (if applicable)
4. Read every changed file yourself

---

## Pre-Review Checklist

### Automated Checks

```bash
# Run ALL of these:
npm test                    # or pytest, cargo test, go test
npm run lint                # or equivalent
npm run typecheck           # if applicable
npm run build               # ensure it compiles
```

**All must pass before requesting review.**

### Self-Review

Read every file you changed. Look for:
- [ ] Debug prints left in (`console.log`, `print`, `println!`)
- [ ] Commented-out code
- [ ] Unused imports/variables
- [ ] Hardcoded values that should be config
- [ ] Error messages that leak internals
- [ ] Inconsistent naming with codebase style
- [ ] Missing or outdated docstrings/comments

### Commit Hygiene

```bash
git log --oneline -10       # Review recent commits
```

Each commit should:
- Tell a coherent story (not "fix stuff", "wip", "asdf")
- Be small enough to review (not 50 files changed)
- Have a clear message: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`

**Squash WIP commits before requesting review.**

---

## The Review Request

### Format

```
## Summary
[1-2 sentences: what this PR does and why]

## Changes
- [Key change 1]
- [Key change 2]
- [Key change 3]

## Testing
- [How you tested this]
- [What scenarios were covered]

## Checklist
- [ ] Tests pass (ran `npm test`)
- [ ] Lint passes (ran `npm run lint`)
- [ ] Self-reviewed all changed files
- [ ] No debug prints or commented-out code
- [ ] Commits are clean and descriptive
```

### What Reviewers Need

| Provide | Why |
|---------|-----|
| Context/background | Reviewer may not know the history |
| What you changed | Don't make them guess |
| How you tested it | Shows rigor, helps them verify |
| Screenshots/demos | For UI changes — thousand words |
| Migration notes | If DB schema, API, or config changed |

---

## Common Mistakes

| Mistake | Impact |
|---------|--------|
| Requesting review before tests pass | Wastes reviewer time |
| "Can you look at this?" with no context | Reviewer must reverse-engineer intent |
| 1000-line PR | Overwhelming, low-quality review |
| Mixing concerns (feature + refactor + fix) | Hard to review, hard to revert |
| No test coverage for new code | Reviewer must write tests for you |
| Leaving debug code in | Looks unprofessional, may ship |

---

## PR Size Guidelines

| Size | Lines Changed | Review Quality |
|------|--------------|----------------|
| Small | < 200 | Excellent — thorough review possible |
| Medium | 200-500 | Good — review in one sitting |
| Large | 500-1000 | Marginal — consider splitting |
| Too large | > 1000 | Split into multiple PRs |

---

## Integration

**Required workflow skills:**
- `verification-before-completion` → Must pass before requesting review
- `code-reviewer` → The review itself (AI or human)
- `receiving-code-review` → Handling feedback
- `finishing-a-development-branch` → Merge after approved

**Companion skills:**
- `tdd-enforcer` → Tests must exist before review
- `writing-plans` → Plan should be implemented before review

---

## Cross-References

- `receiving-code-review` → Handling review feedback
- `code-reviewer` → AI review capability
- `verification-before-completion` → Pre-review verification
- `finishing-a-development-branch` → Merge workflow
