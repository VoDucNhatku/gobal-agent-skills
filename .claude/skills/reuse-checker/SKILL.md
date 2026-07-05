---
name: "reuse-checker"
description: "Reuse checker for GOBAL AGENT — verifies whether an artifact, analysis, or output already exists before creating new ones. Checks notes/INDEX.md and artifact-manager. Prevents duplicate work and token waste. Source: gstack (context-restore) + workbench-conventions §4 (REUSE-BEFORE-READ). It checks; it does NOT create artifacts (that's the producing skill's job)."
argument-hint: "<query> [check|suggest|diff]"
allowed-tools: "Read Glob Bash"
---

# Reuse Checker

> **Source:** gstack (context-restore) + workbench-conventions §4 (REUSE-BEFORE-READ)
> **Purpose:** Check before creating. Don't rebuild what already exists.

## Protocol (Mandatory Before Any Creation Task)

1. **Parse Request** — Extract key identifiers (paper ID, topic, UI component name, file type)
2. **Search INDEX.md** — Scan `notes/INDEX.md` for matching entries
3. **Search artifacts** — Check relevant output directories for existing files
4. **Staleness Assessment** — Evaluate freshness (see table below)
5. **Handoff** — Return path to existing artifact + recommendation (Reuse / Update / Create New)

---

## Freshness Assessment (The Staleness Rule)

| Age | Status | Action |
|-----|--------|--------|
| < 1 week | Fresh | **Reuse without question.** Do not regenerate. |
| 1-4 weeks | Current | **Reuse**, but note the date in downstream prompts. |
| 1-3 months | Stale | **Diff Check:** Compare existing artifact against source. If source changed, update. |
| > 3 months | Outdated | **Re-create.** Re-read source, create new artifact, archive old one. |

---

## Mode: check

**Input:** Query (paper id, topic, description)
**Action:** Execute the Protocol.
**Output:**
```
Found: <path or "null">
Freshness: fresh | current | stale | outdated
Recommendation: Reuse | Update | Create New
Reason: <one-line explanation>
should_create_new: true | false
```

---

## Mode: suggest

**Input:** Current task description
**Action:** Search for related artifacts that might be useful as input/reference.
**Output:** List of relevant artifacts with relevance score + how they help.

---

## Mode: diff

**Input:** Existing artifact path + new requirements
**Action:** Read both. Identify what's missing or changed.
**Output:** Bulleted list of missing information. Do NOT suggest rewriting the whole file if only 10% is missing.

---

## Integration

- `gobal-orchestrator` → Runs reuse-checker before dispatching any creation task
- `paper-read` / `paper-method` → Check before re-reading a paper
- `build-ui` → Check before building from design-record
- `research-orchestrator` → Check before deep-reading papers
