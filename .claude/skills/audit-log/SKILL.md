---
name: "audit-log"
description: "Append-only governance log of MATERIAL AI decisions in a research project — records only the choices that would change the project if absent (scope-decision = a paper/topic intentionally included or excluded; synthesis-framing = the lens chosen to combine sources; cross-source-assumption = treating two sources as connected without explicit evidence). Auto-stamps timestamp + entry id; offloads the line format to a bundled script. Output is English JSON-lines in notes/audit-log.md. Triggers — log this decision, audit log, ghi nhật ký quyết định, record this choice, why did we exclude, governance log, audit summary, materiality. Typically CALLED BY workbench-orchestrator at non-obvious choice points, not invoked directly; it does NOT do analysis (use the worker skills)."
argument-hint: "<json-spec | \"summary\" | \"clear\">"
allowed-tools: "Skill Agent Read Write Glob Bash"
---

# Audit Log (nhật ký quyết định — governance)

An append-only log of **material** AI decisions, so a research project's non-obvious choices
are traceable. Built to be called by `workbench-orchestrator` (and any Worker) at the moments
the conventions flag — not as routine narration.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (output location §3a:
`notes/audit-log.md`, append-only JSON-lines; script-offloading §9; scope handoff §10). Log
entries are **English** (machine-facing content, §1). It reads the convention file at run time.

## The materiality filter (the whole point)
Log an entry **only** if it is one of these three event types — reject everything else:
- **`scope-decision`** — a paper / topic / surface intentionally **included or excluded**, where
  the choice is non-obvious (not "obviously in scope from the request").
- **`synthesis-framing`** — the **lens** chosen to combine sources (e.g. "group by learning
  paradigm, not by year"), when more than one framing was sensible.
- **`cross-source-assumption`** — treating two sources as **connected** without the source
  stating it (an inferred link the synthesis leans on).

If a decision is routine, obvious, or reversible-without-consequence, **do not log it** — noise
defeats an audit log. This filter is the skill's reason to exist.

## Procedure

### Phase 0 — Parse `$ARGUMENTS`
One of:
- a **JSON spec** (a decision to log) — see schema below;
- the literal **`summary`** — print counts by event type + the last 10 entries (no write);
- the literal **`clear`** — archive the current log to `notes/audit-log-archive-<date>.md` and
  reset (confirm once before clearing).

### Phase 1 — Apply the materiality filter
For a JSON spec, verify `event_type` ∈ {`scope-decision`, `synthesis-framing`,
`cross-source-assumption`}. If it is anything else, **refuse to log** and say why (one Vietnamese
line). Do not water down the filter.

### Phase 2 — Offload the line format (§9)
Do **not** hand-write the JSON line or the timestamp. Write the decision spec to
`/tmp/audit-log_entry.json` and call the bundled appender, which auto-fills `timestamp` (ISO
8601), `entry_id`, and `session` (date), validates the event type, and appends one line to
`notes/audit-log.md`:

```
python "<skills>/audit-log/scripts/audit_append.py" /tmp/audit-log_entry.json
# or:  python "<skills>/audit-log/scripts/audit_append.py" --summary
# or:  python "<skills>/audit-log/scripts/audit_append.py" --clear
```

### Phase 3 — Preview (§3)
Print to chat ONLY a **2–4 line** confirmation: the event type, the one-line decision, the new
entry id, and the path. For `summary`, print the counts + the last entries as returned by the
script. Never echo the whole log into chat.

## Entry JSON spec (you provide → the script completes)
```json
{
  "actor": "workbench-orchestrator",
  "event_type": "scope-decision",
  "target": "paper 005",
  "decision": "Excluded from the synthesis corpus",
  "rationale": "Survey paper, not a primary method — out of scope for the gap analysis",
  "alternatives_considered": "Include as background context",
  "artifacts": ["notes/synthesize-gaps-viewpoint.md"]
}
```
The script adds `timestamp`, `entry_id`, `session`. Fields `actor`, `event_type`, `decision`,
`rationale` are required; `target`, `alternatives_considered`, `artifacts` optional.

## Output
- `notes/audit-log.md` — append-only, one JSON object per line (written by the script).
- chat — the 2–4 line confirmation only.

## Gotchas
- **Materiality is the point.** Logging routine/obvious choices makes the log useless. Three
  event types only; refuse the rest.
- **Offload the format (§9).** Never hand-write the JSON line or timestamp — call
  `audit_append.py`. Hand-writing risks malformed lines and clock drift.
- **Append-only.** Never edit or delete past entries; `clear` archives, it does not erase.
- **Called, not narrated.** This is invoked by the orchestrator at flagged choice points — not a
  running commentary on every step.
- **Stay in scope (§10).** This skill records decisions; it does not make them or do analysis —
  `→ dùng` the worker skills for the actual work.
