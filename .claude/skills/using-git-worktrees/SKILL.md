---
name: using-git-worktrees
description: Using git worktrees for GOBAL AGENT — manages isolated git worktrees for parallel development without branch switching. Source: superpowers (using-git-worktrees). Use when starting work on a new task, feature, or bugfix that needs isolation from current workspace.
argument-hint: [branch-name]
allowed-tools: Read Write Bash Glob
---

# Using Git Worktrees

> **Source:** superpowers (using-git-worktrees)
> **Purpose:** Isolated workspaces for parallel development — no more branch switching.

## Overview

Git worktrees let you have multiple branches checked out simultaneously in separate directories. Each worktree has its own working directory but shares the same `.git` repository.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

---

## When to Use Worktrees

| Scenario | Use Worktree? |
|----------|--------------|
| Starting a new feature while main work continues | ✅ Yes |
| Reviewing a PR without disturbing current work | ✅ Yes |
| Running long tests without blocking editor | ✅ Yes |
| Quick fix on existing branch | ❌ No — switch directly |
| Single-task workflow | ❌ No — overkill |

---

## Setup Workflow

### Step 1: Ensure Clean State

```bash
git status
git stash          # If uncommitted changes exist
```

**Cannot create worktree with uncommitted changes in the source branch.**

### Step 2: Create Worktree

```bash
# From main repo root:
git worktree add ../<project>-<branch> -b <branch-name>
```

**Naming convention:** `<project>-<slug>` (e.g., `gobal-agent-auth-fix`)

### Step 3: Verify Setup

```bash
git worktree list
# Expected: Shows new worktree path and branch
```

### Step 4: Install Dependencies (if needed)

```bash
cd ../<project>-<branch>
npm install / pip install -r requirements.txt / etc.
```

---

## Working in a Worktree

- Each worktree is a fully independent workspace
- Commits in one worktree do NOT affect others
- Switching branches in one worktree does NOT affect others
- All worktrees share the same git history and remotes

### Common Operations

```bash
# See all worktrees
git worktree list

# Remove a worktree (after merging/PR created)
git worktree remove ../<project>-<branch>

# Prune stale worktree references
git worktree prune

# Force-remove (if remove fails due to uncommitted changes)
git worktree remove -f ../<project>-<branch>
```

---

## Cleanup Protocol

### After Merge or PR Creation

```bash
# 1. Verify PR is created and CI is green
# 2. Return to main repo
cd <main-repo-path>
# 3. Remove worktree
git worktree remove ../<project>-<branch>
# 4. Prune
git worktree prune
# 5. Switch back to main branch
git checkout main
```

### After Discard

```bash
# 1. Delete branch (force, since work was discarded)
git branch -D <branch-name>
# 2. Remove worktree
git worktree remove ../<project>-<branch>
# 3. Prune
git worktree prune
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Creating worktree with uncommitted changes | Stash or commit first |
| Running `git worktree remove` from inside the worktree | cd out first |
| Forgetting to prune after removal | Run `git worktree prune` |
| Worktree and branch name mismatch | Use consistent naming convention |
| Installing deps in wrong directory | cd into worktree first |

---

## Integration

**Required workflow skills:**
- `executing-plans` → Uses worktrees for isolated plan execution
- `finishing-a-development-branch` → Cleanup after completion
- `brainstorming` → Design before creating worktree

**Companion skills:**
- `code-reviewer` → Review code in isolated worktree
- `tdd-enforcer` → TDD cycle within worktree

---

## Cross-References

- `executing-plans` → Task execution in worktrees
- `finishing-a-development-branch` → Cleanup workflow
- `brainstorming` → Design before implementation
- `writing-plans` → Plan before creating worktree
