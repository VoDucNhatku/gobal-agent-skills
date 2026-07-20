---
name: artifact-manager
description: Artifact management for GOBAL AGENT — indexes, tracks, and manages file artifacts across sessions. Maintains notes/INDEX.md as central registry. Detects reuse opportunities (don't re-read what exists). Cleans up stale artifacts. Modes: index (build/update INDEX.md), track (register new artifact), reuse (check before reading, with staleness assessment), suggest (find related artifacts for a task), diff (existing artifact vs new requirements), cleanup (archive stale). Absorbs the deprecated reuse-checker skill. Source: gstack (document-generate, context-restore) + addyosmani (context-engineering) + workbench-conventions §4 (REUSE-BEFORE-READ). It manages files; it does NOT generate content.
argument-hint: [index|track|reuse|suggest|diff|cleanup]
allowed-tools: Read Write Bash Glob
---

# Artifact Manager

> **Source:** gstack (document-generate, context-restore) + addyosmani (context-engineering)
> **Purpose:** Track every file GOBAL creates. Reuse before re-creating. Central registry.

## Central Index

`notes/INDEX.md` — always maintained, always loaded before any research/code task.

**Format:**
```markdown
# GOBAL Artifact Index

> Last updated: YYYY-MM-DD

## Research
- [paper-001] notes/001-read-summary.md — Transformer attention mechanism
- [paper-003] notes/003-read-eli5.md — RNN vs Transformer

## Code
- [auth-slice] notes/backend-auth-slice.md — Auth API contract
- [auth-slice] src/api/auth.py — Implemented endpoints

## Design
- [landing-page] notes/design-record-landing.md — Design direction locked
```

---

## Reuse-Before-Read Protocol

Before reading any source (PDF, large file, repo):
1. Check INDEX.md for existing artifact
2. If fresh artifact exists → reuse, do NOT re-read
3. Only read raw source when no distilled artifact exists
4. After creating new artifact → register in INDEX.md

---

## Artifact Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Paper read | `notes/<id>-read-<mode>.md` | `notes/003-read-summary.md` |
| Method analysis | `notes/<id>-method.md` | `notes/003-method.md` |
| Knowledge graph | `notes/<id>-kg.md` | `notes/003-kg.md` |
| Translation | `notes/<id>-<lang>.md` | `notes/003-vi.md` |
| Synthesis | `notes/synthesize-<mode>-<slug>.md` | `notes/synthesize-compare-transformers.md` |
| Backend contract | `notes/backend-<slug>.md` | `notes/backend-auth.md` |
| Security review | `notes/security-review-<slug>.md` | `notes/security-review-auth.md` |
| Design record | `notes/design-<slug>.md` | `notes/design-landing.md` |
| Session summary | `logs/session-summary-<id>.md` | `logs/session-summary-001.md` |
| Token log | `logs/token-usage-<date>.md` | `logs/token-usage-2026-06-29.md` |
| Audit log | `notes/audit-log.md` | Append-only JSON-lines |
| Provenance | `provenance/INDEX.md` | Skill source tracking |

---

## Mode: index

Build or update INDEX.md:
1. Scan project for artifacts (glob patterns above)
2. Categorize by type (Research, Code, Design, Governance)
3. Write/update INDEX.md with id, path, one-line description, date

---

## Mode: track

Register a new artifact:
1. Add entry to INDEX.md with: id, path, description, date
2. Update provenance/INDEX.md if new skill was used

---

## Mode: reuse

Given a query (paper id, topic, file type):
1. Search INDEX.md for matching entries
2. Check file existence (Glob)
3. Assess freshness (staleness table below)
4. Return: path, freshness, recommendation (Reuse/Update/Create)

**Freshness assessment (the staleness rule — absorbed from reuse-checker):**

| Age | Status | Action |
|-----|--------|--------|
| < 1 week | Fresh | **Reuse without question.** Do not regenerate. |
| 1–4 weeks | Current | **Reuse**, but note the date in downstream prompts. |
| 1–3 months | Stale | **Diff check:** compare artifact against source; if source changed, update. |
| > 3 months | Outdated | **Re-create.** Re-read source, create new artifact, archive old one. |

**Output format:**
```
Found: <path or "null">
Freshness: fresh | current | stale | outdated
Recommendation: Reuse | Update | Create New
Reason: <one-line explanation>
should_create_new: true | false
```

---

## Mode: suggest

**Input:** Current task description.
**Action:** Search INDEX.md for related artifacts useful as input/reference (not exact matches).
**Output:** List of relevant artifacts with relevance + how each helps.

---

## Mode: diff

**Input:** Existing artifact path + new requirements.
**Action:** Read both; identify what is missing or changed.
**Output:** Bulleted list of missing information only. Do NOT suggest rewriting the whole
file when only a small fraction is missing — patch the gap.

---

## Mode: cleanup

Scan INDEX.md for stale entries:
1. Check if referenced files still exist
2. Archive or remove stale entries
3. Report: entries cleaned, entries kept

---

## Triggers

- "artifact index", "register artifact", "track artifact", "cleanup artifacts", "reuse check", "artifact missing", "where is X saved".
- Vietnamese: "artifact", "artifact index", "artifact đâu", "đăng ký artifact", "kiểm tra artifact".

## Integration

- `gobal-orchestrator` — auto-invokes before dispatching tasks
- `project-memory` — project-specific artifact retention rules
- `context-compressor` — archives old artifacts during compaction
- `reuse-checker` — DEPRECATED alias of this skill (its staleness protocol + suggest/diff modes now live here)
