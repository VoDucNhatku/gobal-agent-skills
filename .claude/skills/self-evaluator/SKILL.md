---
name: self-evaluator
description: Self-evaluation for GOBAL AGENT — checks output quality before delivery. Verifies completeness, accuracy, token efficiency, and hallucination risk. Modes — evaluate (full check), quick-check (fast pass/fail), post-mortem (analyze past failures). Source: superpowers (writing-skills) + gstack (retro) + addyosmani (definition-of-done). It evaluates; it does NOT fix issues (that's the producing skill's job).
argument-hint: [evaluate|quick-check|post-mortem]
allowed-tools: Read Bash Glob
---

# Self Evaluator

> **Source:** superpowers (writing-skills) + gstack (retro) + addyosmani (definition-of-done)
> **Purpose:** Check output quality before delivery. Four dimensions, binary pass/fail.

## Evaluation Dimensions

### 1. Completeness
- [ ] All user requirements addressed?
- [ ] All promised artifacts written to disk (not just described)?
- [ ] Handoff instructions clear (next skill, file paths)?
- [ ] No "TBD", "TODO", or placeholder text?
- [ ] Glossary present (if artifact contains technical terms)?

### 2. Accuracy / Fidelity
- [ ] Every claim has a source (file path, URL, paper id)?
- [ ] No fabricated metrics, hyperparameters, shapes?
- [ ] Code tested and verified (not "should work")?
- [ ] Quantitative results match source exactly?
- [ ] Cross-source claims attributed to specific source?
- [ ] Venue/novelty claims graded (tier + band + điều kiện, Venue Claim Card) per `~/.claude/rules/research-proposal-integrity.md`?
- [ ] Claims consistent with `notes/claims-ledger.md` — any change declared via REVISION protocol (no silent recalibration)?
- [ ] Every equation in a proposal carries a provenance tag ([cited]/[derived]/[design])?

### 3. Token Efficiency
- [ ] Chat output ≤ preview budget (5-10 lines)?
- [ ] No file content dumped into chat?
- [ ] No redundant context loaded?
- [ ] Preview-not-dump followed?
- [ ] Progressive disclosure respected (rules cited, not inlined)?

### 4. Hallucination Guard
- [ ] No invented file paths?
- [ ] No invented API signatures?
- [ ] No invented citations?
- [ ] Uncertain claims flagged as "suy luận"?
- [ ] Confidence score assigned to each major claim?

---

## Mode: evaluate

Run full 4-dimension checklist. Return:

```markdown
## Self-Evaluation: <artifact>

### Results
| Dimension | Status | Issues |
|-----------|--------|--------|
| Completeness | ✅ PASS / ❌ FAIL | ... |
| Accuracy | ✅ PASS / ❌ FAIL | ... |
| Token Efficiency | ✅ PASS / ❌ FAIL | ... |
| Hallucination Guard | ✅ PASS / ❌ FAIL | ... |

### Overall: PASS / FAIL

### Issues Found
1. [dimension] [severity] <issue> — Fix: <suggestion>
```

**Fail condition:** Any dimension with a Critical issue = overall FAIL.

---

## Mode: quick-check

Fast pass: Completeness + Hallucination Guard only.
Return: pass/fail + top 3 issues + one-line recommendation.

Use before: chat responses that contain claims, code snippets, or file references.

---

## Mode: post-mortem

Analyze a past failure:
1. **What went wrong?** — Which dimension failed?
2. **Which check missed it?** — Why didn't the evaluation catch it?
3. **How to prevent?** — Add new check, tighten existing one, or add rationalization counter
4. **Pattern?** — Is this a recurring failure mode?

---

## Red Flags — STOP and Re-Evaluate

- About to claim "done" without running evaluate
- Any dimension has unchecked items
- "Should be fine" without verification
- Skipping evaluation because "it's simple"
- Uncertainty about any claim's source

---

## Integration

- `gobal-orchestrator` → Runs evaluate before delivering multi-step outputs
- `paper-read` / `paper-method` → Fidelity dimension checks source adherence
- `code-senior` → Accuracy dimension checks code correctness
- `hallucination-guard` → Hallucination dimension (shared checks)
- `audit-log` → Post-mortem findings feed into correction entries
