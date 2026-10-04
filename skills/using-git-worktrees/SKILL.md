---
name: "using-git-worktrees"
description: "Using git worktrees for GOBAL AGENT — manages isolated git worktrees for parallel development without branch switching. Use when starting work on a new task, feature, or bugfix that needs isolation from current workspace."
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
| Quick fix on existing branch | ❌ No — keep the existing checkout and user changes |
| Single-task workflow | ❌ No — overkill |

---

## Setup Workflow

### Step 1: Inspect and preserve source state

```bash
git status --short
git worktree list --porcelain
```

Uncommitted changes in the source do not prevent creating a separate worktree from a
commit. They are not copied into the new checkout. Do not automatically stash, commit,
reset or switch the source branch; preserve user work. If the task needs those changes,
reuse the current checkout or ask how they should be carried over.
See [Git's worktree manual](https://git-scm.com/docs/git-worktree).

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

```

If removal refuses dirty files, stop and inspect the exact target; do not turn that error
into forced deletion. A PR being created does not mean local changes are safely preserved.

---

## Cleanup Protocol

### After Merge or PR Creation

```bash
# 1. Verify needed work is preserved and inspect the exact target's status
git -C ../<project>-<branch> status --short
# 2. If clean and no longer needed, return to main repo
cd <main-repo-path>
# 3. Remove worktree
git worktree remove ../<project>-<branch>
# 4. Prune
git worktree prune
```

### After Discard

Discard requires explicit user authorization covering the exact target path and branch.
Inspect uncommitted files and unmerged commits first, and preserve a recoverable snapshot
when needed. Prefer normal removal and merged-branch deletion; if either refuses, report
the reason. No routine force-delete recipe and no inferred permission from "cleanup".

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Assuming dirty source blocks a new worktree | Leave source changes alone; the new checkout starts from a commit |
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


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
