---
name: "receiving-code-review"
description: "Receiving code review for GOBAL AGENT — how to respond to review feedback constructively. Address every comment, fix issues, push back when wrong. Source: superpowers (receiving-code-review). Use when you have received review feedback on your code."
argument-hint: "[feedback-source]"
allowed-tools: "Read Write Edit Bash Glob"
---

# Receiving Code Review

> **Source:** superpowers (receiving-code-review)
> **Purpose:** Respond to feedback constructively — address everything, fix or explain.

## Overview

Review feedback is a gift. Treat it as such. Address every comment. Fix real issues. Explain disagreements. Never ignore feedback.

**Announce at start:** "I'm using the receiving-code-review skill to address this feedback."

---

## Step 1: Read All Feedback First

Before making any changes:

1. Read every comment — don't skim
2. Categorize: bug, style, suggestion, question, false positive
3. Note patterns: same issue in multiple places?
4. Prioritize: bugs > security > style > suggestions

### Categorization Table

| Type | Action | Priority |
|------|--------|----------|
| Bug / correctness issue | Fix immediately | 🔴 Critical |
| Security concern | Fix immediately | 🔴 Critical |
| Performance issue | Fix or explain why acceptable | 🟠 High |
| Missing test | Add test | 🟠 High |
| Style / naming | Fix to match conventions | 🟡 Medium |
| Suggestion / improvement | Fix or discuss | 🟢 Low |
| Question / clarification | Respond with explanation | 🟢 Low |
| Disagreement | Discuss with reasoning | 🟢 Low |

---

## Step 2: Fix Issues

### For Each Issue

1. **Fix it** — if it's clearly correct
2. **Push back** — if you disagree, explain why with evidence
3. **Ask** — if unclear, ask for clarification

### Fix Protocol

```bash
# 1. Make the fix
# 2. Run tests to ensure fix doesn't break anything
npm test
# 3. Commit with reference to review
git commit -m "fix: address review feedback — [specific issue]"
# 4. Push
git push
```

### Never Do This

| Anti-Pattern | Why It's Wrong |
|-------------|----------------|
| Fix only the easy comments, ignore hard ones | Reviewers notice |
| Mark as resolved without actually fixing | Dishonest, wastes time |
| Argue without evidence | "I disagree" ≠ "Here's why" |
| Fix the symptom, not the root cause | Review will find it again |
| Skip tests after fix | Fix might break something else |

---

## Step 3: Respond to Each Comment

### For Fixed Issues

```
✅ Fixed in [commit hash] — [brief description of fix]
```

### For Disagreements

```
🤔 I considered this but chose [X] because:
- [Reason 1 with evidence]
- [Reason 2 with trade-off]
Open to revisiting if you see a better approach.
```

### For Questions

```
📝 [Clear explanation of what/why]
```

### For "Won't Fix"

```
⚠️ Not fixing because [valid reason]:
- [Technical constraint]
- [Trade-off analysis]
Will track in [issue/todo] if needed.
```

---

## Step 4: Push and Notify

After all addressed:

```bash
# Push all fix commits
git push

# Notify reviewer:
"All feedback addressed:
- Fixed: [N] issues (bugs, style, tests)
- Discussed: [M] items (disagreements with reasoning)
- Clarified: [K] questions
Ready for re-review if needed."
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Fixing without understanding the root issue | Ask "why" before fixing |
| Arguing about style preferences | Follow project conventions |
| Ignoring comments you don't understand | Ask for clarification |
| Fixing in isolation without running tests | Always test after changes |
| Taking feedback personally | Feedback is about code, not you |
| "This is how I always do it" | Project conventions > personal habits |

---

## Integration

**Required workflow skills:**
- `requesting-code-review` → The other side of the workflow
- `code-reviewer` → AI review capability
- `verification-before-completion` → Verify fixes work
- `finishing-a-development-branch` → Merge after all addressed

---

## Cross-References

- `requesting-code-review` → Preparing for review
- `code-reviewer` → AI review process
- `verification-before-completion` → Verify fixes
- `finishing-a-development-branch` → Merge workflow
