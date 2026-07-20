---
name: project-memory
description: Project memory for GOBAL AGENT — persists project context across sessions using file-based memory. Modes: save (store context), recall (load context), update (modify existing), compact (summarize old context). Source: gstack (context-save/restore, sync-gbrain) + addyosmani (context-engineering) + superpowers (progress ledger). It remembers; it does NOT make decisions based on memory (that is the orchestrator's job).
argument-hint: <project> [save|recall|update|compact]
allowed-tools: Read Write Bash Glob
---

# Project Memory

> **Source:** gstack (context-save/restore, sync-gbrain) + addyosmani (context-engineering) + superpowers (progress ledger)
> **Purpose:** Persist project context across sessions.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `save` | Store context | End of session, important decision |
| `recall` | Load context | Start of session, context switch |
| `update` | Modify existing | Decision changed, new info |
| `compact` | Summarize old context | Context getting too long |

## Context Hierarchy (from addyosmani)

Load in this order (persistent → transient):

1. **Rules Files** (CLAUDE.md) — always loaded, project conventions
2. **Memory Files** (project-memory) — decisions, preferences, known issues
3. **Spec/Architecture Docs** — per feature/session
4. **Relevant Source Files** — per task
5. **Error Output/Test Results** — per iteration
6. **Conversation History** — accumulates, compacts

### Brain Dump at Session Start

Provide everything needed in structured block:
```
## Project Context
- Stack: ...
- Current goal: ...
- Recent decisions: ...
- Known issues: ...
- Active tasks: ...
```

### Selective Include

Only load what is relevant to current task. Don't flood context with everything.

## Memory File Structure (canonical — the ONE layout every mode reads/writes)

```
project-memory/
  ├── INDEX.md            # Memory index — read first; one line per file
  ├── context.md          # Project overview: stack, structure, goals
  ├── decisions.md        # Key decisions with rationale (why, not just what)
  ├── preferences.md      # User/codebase preferences
  ├── known-issues.md     # Bugs, limitations, workarounds
  └── progress/
      ├── current.md      # Active tasks, blockers, next steps (the ledger)
      └── archive/        # Completed work summaries (compact target)
```

`CLAUDE.md` stays at the project ROOT (loaded by the harness as a rules file, per the
hierarchy above) — this skill references it but never stores or edits it.

## Progress Ledger (from superpowers)

File-based tracking that survives context compaction:

- Track progress in ledger file after each task
- After compaction, trust ledger and git log over recollection
- Format: task status, blockers, next steps

## Session Tracking (from gstack)

- Session files with TTL (auto-cleanup old sessions)
- Track: active tasks, recent decisions, pending questions

## Context Compaction Strategy

When context gets long:
1. Summarize conversation progress
2. Move detailed info to memory files
3. Keep only active context in conversation
4. Start fresh sessions when switching features

## Cross-References

- `gobal-orchestrator` → Load memory at session start
- `learnings-db` → Cross-project learnings
- `context-compressor` → Token optimization
- `understand-codebase` → Codebase context

## What to Remember

### Project Context
- Project name, type, tech stack
- Directory structure (key paths)
- Active branches, recent commits
- Known issues / technical debt

### Decisions
- Architecture decisions (why, not just what)
- Technology choices (trade-offs considered)
- Design decisions (approved direction)
- Scope decisions (what's in/out)

### User Preferences
- Communication style (formal/casual, detail level)
- Code style preferences
- Review preferences (what to flag, what to skip)
- Workflow preferences (TDD, branch strategy, etc.)

### Active State
- Current task / sprint
- Blockers and dependencies
- Next steps planned

## Storage Format

One layout only — the canonical **Memory File Structure** above (`project-memory/` in
the project root). Active state lives in `progress/current.md`; there is no separate
`active-state.md`. Every mode targets these exact paths.

## Mode: save
Store current context to memory files. Merge with existing (don't overwrite).

## Mode: recall
Load relevant memory at session start. Return summary of what's known.

## Mode: update
Modify existing memory entry. Append new decisions, update active state.

## Principles
- Save early, save often
- Include "why" not just "what"
- Prune stale information
- Never save sensitive data (secrets, PII)
