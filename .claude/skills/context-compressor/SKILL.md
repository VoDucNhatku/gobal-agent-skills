---
name: context-compressor
description: Context compression for GOBAL AGENT — reduces context size when approaching token limits. Strategies: summarization (condense conversation history), artifact offloading (push content into files), progressive disclosure (load only what's needed). Source: addyosmani (context-engineering) + gstack (context-save/restore). It compresses; it does NOT delete important state (that's the orchestrator's judgment).
argument-hint: [summarize|offload|prune]
allowed-tools: Read Write Bash
---

# Context Compressor

> **Source:** addyosmani (context-engineering) + gstack (context-save/restore)
> **Purpose:** Reduce context size without losing essential information.

## When to Compress

Triggered when:
- Working buffer < 30% of session budget
- Conversation history > 50k tokens
- Too many artifacts loaded simultaneously
- Before dispatching parallel subagents (free up context for coordination)

---

## Strategies

### 1. Summarization

Condense conversation history into a brief summary:
- **Keep:** Decisions made, current task state, key findings, active blockers
- **Drop:** Full code dumps, repeated explanations, resolved discussions, tool call results
- **Output:** 5-10 line summary written to `logs/session-summary-<id>.md`
- **Format:** Markdown with sections: Context, Decisions, Current State, Next Steps

### 2. Artifact Offloading

Move large content from context to files:
- Full file contents → reference by path only
- Long tables → write to file, keep header in context
- Code blocks → write to file, keep signature in context
- Tool call results → summarize, keep only the conclusion

### 3. Progressive Disclosure Enforcement

The tier definitions (metadata → skill body → references) are owned by **`token-budget`**
— single source, not duplicated here. This skill only ACTS on them:

**Action:** If a skill's references/ are loaded but no longer needed, drop them from context.

### 4. Prune Unused Artifacts

Remove artifacts no longer needed:
- Check artifact-manager index for stale entries
- Keep only artifacts from current task chain
- Archive old artifacts to `logs/archive/`

---

## Mode: summarize

Condense current context into brief summary. Write to file, replace context with reference.

### Summary Template

```markdown
## Session Summary <id>

**Date:** YYYY-MM-DD
**Project:** <name>

### Context
<2-3 lines: what we're working on>

### Decisions Made
- <decision 1 with rationale>
- <decision 2 with rationale>

### Current State
- Task: <what's being worked on>
- Progress: <what's done, what's next>
- Blockers: <any>

### Key Findings
- <finding 1>
- <finding 2>

### Next Steps
1. <step 1>
2. <step 2>
```

---

## Mode: offload

Identify large content in context → write to file → replace with path reference.

### Priority Order for Offloading
1. Tool call results (largest, most redundant)
2. Full file contents (replace with path + key sections)
3. Long tables/lists (write to file, keep summary)
4. Code blocks (write to file, keep signature)

---

## Mode: prune

Scan loaded artifacts → archive stale ones → update index.

### Pruning Rules
- Artifacts from completed tasks → archive
- Artifacts > 3 months old → archive (unless actively referenced)
- Duplicate artifacts → keep newest, archive older
- Never prune: current task artifacts, INDEX.md, active memory files

---

## Integration

- `gobal-orchestrator` → Triggers compression when buffer < 30%
- `project-memory` → Offloads old context to memory files
- `artifact-manager` → Prunes stale artifacts
- `token-budget` → Monitors context size, triggers compression
