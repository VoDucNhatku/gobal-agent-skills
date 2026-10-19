---
name: "research-write"
description: "Runs the manuscript pipeline for a research paper: draft or restructure from notes, figures, citation audit, style pass, LaTeX build, pre-submission review, rebuttal. Use when writing, formatting or revising a paper or report. Triggers — viết paper, bản thảo, nộp bài, format IEEE/CVPR, rebuttal, trả lời reviewer, viết báo cáo nghiên cứu."
argument-hint: "<draft|restructure|figure|cite|style|build|review|rebuttal> <path>"
allowed-tools: "Skill Read Write Edit Glob Grep Bash"
---

# research-write — manuscript pipeline

Integrity rules for every stage: `../_shared/rules/paper-writing-integrity.md`
(no fabricated references, no invented results — use `[TODO: metric from <log>]`, no
copied prose, meaning-preserving style edits). Claims in the draft never exceed the
project's ledger (`notes/claims-ledger.md`).

## Stages (sequential; a failing stage returns to the one that produced the input)
| Stage | Skill to read and follow | Output |
|---|---|---|
| draft / format / rebuttal | `../paper-submission/SKILL.md` | `paper/` sources |
| restructure narrative | `../paper-storytelling/SKILL.md` | revised outline and sections |
| figures (parallel with drafting) | `../latex-tikz-generator/SKILL.md` | `.tex` figures |
| cite | `../citation-guard/SKILL.md` | `paper/reports/citations.md` |
| style | `../style-humanizer/SKILL.md` | edited text + invariant diff |
| build | `../latex-fix/SKILL.md`, then compile | PDF + compile log |
| review | `../ieee-q1-devil-advocate/SKILL.md`, with venue wording governed by `../_shared/research-integrity.md` | `paper/reports/review.md` |

Run only the stages the user asked for. Each stage writes its report next to the
manuscript and states what it checked.

## Before calling a draft done
Every number traces to `notes/experiments.md` or a log; every reference is either looked up
or marked `[chưa xác minh]`; the review stage has run on the version that will be submitted.
Use `evidence-check` on the results and claims sections.
