---
name: learnings-db
description: Learnings database for GOBAL AGENT — captures lessons learned from every session. Modes: capture (log a learning), query (search learnings), suggest (recommend based on current task), pattern (extract cross-project patterns). Source: gstack (learn, sync-gbrain) + superpowers. It learns; it does NOT apply learnings automatically (that is the orchestrator's decision).
argument-hint: [capture|query|suggest|pattern]
allowed-tools: Read Write Bash Glob
---

# Learnings DB

> **Source:** gstack (learn, sync-gbrain) + superpowers patterns
> **Purpose:** Capture and retrieve lessons learned across sessions.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `capture` | Log a learning | After solving a problem, making a decision |
| `query` | Search learnings | Before starting similar task |
| `suggest` | Recommend based on task | Complex task with historical context |
| `pattern` | Extract cross-project patterns | Periodic review of accumulated learnings |

## What to Capture

- **What worked** — Approach, code pattern, tool that solved the problem
- **What didn't work** — Dead ends, wrong assumptions, failed approaches
- **Patterns discovered** — Reusable insights across projects
- **Mistakes avoided** — Errors caught early, how they were caught
- **Decisions made** — Why, what alternatives were considered

### Success Patterns
- What approach worked well?
- What skill combination was effective?
- What saved tokens?
- What user preference was discovered?

### Failure Patterns
- What went wrong?
- What skill failed or was misapplied?
- What caused token waste?
- What misunderstanding occurred?

### Discoveries
- What pattern was noticed in the codebase?
- What shortcut was found?
- What tool/library is particularly useful here?

### Corrections
- What did the user correct?
- What assumption was wrong?
- What approach should change?

## Learning Format

```markdown
## Learning: <Title>

**Date:** YYYY-MM-DD
**Project:** <project name>
**Context:** What was the situation?

**What happened:**
- ...

**What worked:**
- ...

**What didn't work:**
- ...

**Pattern/Insight:**
- ...

**Tags:** #tag1 #tag2
```

## Storage Format

```
learnings-db/
├── INDEX.md    # Categories + quick reference
├── successes.md # What worked
├── failures.md  # What didn't work
├── discoveries.md # Patterns found
├── corrections.md # User corrections
└── by-domain/  # Organized by domain
    ├── research.md
    ├── code.md
    ├── web.md
    └── business.md
```

## Query by Context

When starting a task:
1. Search learnings for similar tasks
2. Review what worked/didn't work
3. Apply relevant patterns
4. Avoid known pitfalls

## Pattern Extraction

Periodically review learnings to extract cross-project patterns:
- Common failure modes
- Effective approaches by domain
- Stack-specific gotchas
- Tool/technique effectiveness

## Mode: capture

Log a new learning:
1. Categorize (success/failure/discovery/correction)
2. Write entry with: what, why, when, how to apply
3. Update INDEX.md

## Mode: query

Search learnings by keyword or domain. Return relevant entries with context.

## Mode: suggest

Based on current task, suggest relevant past learnings:
1. Analyze current task → identify domain + pattern
2. Search learnings for similar past situations
3. Return: "Trước đây khi làm X, chúng ta thấy Y → gợi ý: Z"

## Integration

- `audit-log` → feeds into learnings-db (decisions → lessons)
- `project-memory` → project-specific learnings
- `gobal-orchestrator` → consults learnings before routing

## Cross-References

- `project-memory` → Project-specific context
- `gobal-orchestrator` → Load learnings at session start; also consults learnings for
  routing decisions (folds the deprecated `skill-router`)
