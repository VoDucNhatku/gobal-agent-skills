---
name: finishing-a-development-branch
description: Finishing a development branch for GOBAL AGENT — guides completion of development work by presenting structured options for merge, PR, or cleanup. Source: superpowers (finishing-a-development-branch). Use when implementation is complete and all tests pass.
argument-hint: <branch-name>
allowed-tools: Read Write Bash Glob
---

# Finishing a Development Branch

> **Source:** superpowers (finishing-a-development-branch)
> **Purpose:** Guide completion of development work with clear options.

## Overview

Core principle: Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

---

## Step 1: Verify Tests

Before presenting options, verify tests pass:

```bash
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures. Cannot proceed with merge/PR until tests pass. Stop.

**If tests pass:** Continue to Step 2.

---

## Step 2: Detect Environment

Determine workspace state:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | No cleanup |

---

## Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main — is that correct?"

---

## Step 4: Present Options

**Normal repo and named-branch worktree:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD:**

```
Implementation complete. You're on a detached HEAD.

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

---

## Step 5: Execute Choice

### Option 1: Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
# Verify tests on merged result
git branch -d <feature-branch>
```

### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>
# Do NOT clean up worktree — user needs it for PR iteration
```

### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

### Option 4: Discard

**Confirm first:** "This will permanently delete: Branch <name>, All commits, Worktree at <path>. Type 'discard' to confirm."

If confirmed: force-delete branch, cleanup worktree.

---

## Step 6: Cleanup Workspace

Only for Options 1 and 4:

```bash
# If worktree under .worktrees/ or worktrees/:
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

---

## Common Mistakes

- Skipping test verification before offering options
- Cleaning up worktree for Option 2 (user needs it for PR iteration)
- Deleting branch before removing worktree
- Running `git worktree remove` from inside the worktree

---

## Cross-References

- `deploy-orchestrator` → Deploy coordination
- `code-reviewer` → Review before merge
- `using-git-worktrees` → Workspace management
