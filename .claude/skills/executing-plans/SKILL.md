---
name: "executing-plans"
description: "Executing plans for GOBAL AGENT — implements a written plan task by task with verification checkpoints. Source: superpowers (executing-plans). Use when you have a written implementation plan to execute."
argument-hint: "<plan-file>"
allowed-tools: "Read Write Edit Bash Glob"
---

# Executing Plans

> **Source:** superpowers (executing-plans)
> **Purpose:** Load plan, review critically, execute all tasks, report when complete.

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

---

## The Process

### Step 1: Load and Review Plan

1. Read plan file completely
2. Review critically — identify questions or concerns
3. If concerns: raise with user before starting
4. If no concerns: create todos for plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- Use `finishing-a-development-branch` for final steps

---

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

---

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

---

## Remember

- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

---

## Integration

**Required workflow skills:**
- `using-git-worktrees` — Ensures isolated workspace
- `writing-plans` — Creates the plan this skill executes
- `finishing-a-development-branch` — Complete development after all tasks
