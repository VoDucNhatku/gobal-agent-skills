---
name: hallucination-guard
description: Hallucination guard for GOBAL AGENT — prevents fabricated content in code, citations, metrics, and file references. Every claim must have a verifiable source. Modes — verify (check a specific claim), scan (scan output for unverified claims), source-check (validate citations). Source: addyosmani (doubt-driven-development) + workbench-conventions §8 (fidelity). It guards; it does NOT generate content.
argument-hint: [verify|scan|source-check]
allowed-tools: Read Bash Glob WebSearch
---

# Hallucination Guard

> **Source:** addyosmani agent-skills (doubt-driven-development) + workbench-conventions §8 (fidelity)
> **Purpose:** No fabricated code, metrics, citations, or file paths. Every claim has a source.

## Core Rules

1. **Physical Truth over Documentation (Anti-Assumption)** — NEVER trust static documentation (e.g., inventories, test reports) as the absolute truth for file counts or workspace state. ALWAYS verify by counting or listing the physical files via tools (`list_dir`, `run_command`).
2. **Global Context Awareness** — Do not assume the search scope is limited to the current working directory. Always scan the entire workspace root before concluding a file, skill, or project does not exist.
3. **Source verification** — Every factual claim needs a source: file path, URL, paper id, or "suy luận từ context"
4. **Code execution check** — Run code before claiming "works"
5. **Confidence scoring** — Every output gets a confidence level:
   - **High:** verified by code/experiment or direct source read
   - **Medium:** read source but not independently verified
   - **Low:** inference from context, not verified → flag as "suy luận"
4. **No phantom references** — Every file path must exist. Every API name must be real.

---

## Hallucination Patterns to Catch

| Pattern | Example (wrong) | Fix |
|---------|-----------------|-----|
| Invented file path | `src/utils/helper.py` (doesn't exist) | Glob to verify first |
| Invented API | `User.objects.filter_by()` (wrong method) | Read actual code |
| Fabricated metric | "accuracy improved by 15%" (no source) | State "chưa xác minh" |
| Fake citation | "as shown in [Doe 2024]" (not in sources) | Only cite what exists |
| Confident guess | "the answer is X" (no evidence) | Say "không biết, cần kiểm tra" |
| Invented config | `max_tokens: 8192` (not in source) | Read actual config file |
| Fake error message | "Error: connection timeout" (not observed) | Quote actual error verbatim |
| Hallucinated paper result | "paper achieved 98% accuracy" (not in paper) | Read paper's actual results section |
| Venue overclaim | "hướng này đủ Q1" (no tier, no conditions) | Grade per `~/.claude/rules/research-proposal-integrity.md` §1 — claim = band + điều kiện, ghi claims-ledger |
| Untagged formula | equation in a proposal with no provenance | Tag [cited]/[derived]/[design] per integrity rules §4; [derived] needs a shown sanity check |
| Phantom expected gain | "sẽ tăng ~5% Acc" (no run behind it) | State "chưa chạy — ước lượng [design]" or remove |

---

## Mode: verify

**Input:** A specific claim
**Process:**
1. Identify what would prove/disprove the claim
2. Check available sources (files, web, previous outputs)
3. Return: `verified` / `refuted` / `uncertain` + evidence

**Output format:**
```
Claim: <the claim>
Status: verified | refuted | uncertain
Evidence: <what confirms or contradicts>
Source: <file path, URL, or "no source found">
```

---

## Mode: scan

**Input:** An output text (code, analysis, report)
**Process:**
1. Scan for every factual claim
2. For each claim: can it be verified from available context?
3. Return: list of flagged items with suggested fixes

**Output format:**
```
## Scan Results

### Flagged Claims
1. [line/context] "<claim>" — Status: unverified | Fix: <suggestion>
2. ...
```

---

## Mode: source-check

**Input:** A list of citations (file paths, URLs, paper IDs, API names)
**Process:**
1. For each citation: does it exist? Is it accessible?
2. Return: valid/invalid list with details

---

## Integration with Other Skills

- `paper-read` / `paper-method` → Verify claims against actual paper content
- `code-senior` → Verify API signatures before using them
- `research-orchestrator` → Scan subagent outputs before synthesis
- `self-evaluator` → Hallucination guard is one of its 4 check dimensions

---

## Red Flags — STOP

- About to cite a paper/URL/file you haven't actually read
- About to claim code "works" without running it
- About to use an API name from memory instead of reading the code
- "I'm pretty sure" / "I think" / "probably" — these mean uncertain, not verified
- About to name a venue tier (Q1/Q4/hội nghị) without a graded novelty tier + upgrade conditions (integrity rules §1–2)
- About to answer a follow-up on a prior proposal from conversation memory instead of re-reading `notes/claims-ledger.md` + the proposal note
