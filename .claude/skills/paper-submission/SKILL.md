---
name: "paper-submission"
description: "Academic manuscript and paper submission worker — drafts, formats, and polishes academic papers for submission to top-tier venues (IEEE Q1/Q2, CVPR, ICCV, ECCV, NeurIPS, etc.). Modes: draft (generate manuscript from synthesis notes), format (apply specific LaTeX templates like IEEEtran/cvpr), rebuttal (draft reviewer responses based on reviews). Triggers — write paper, draft manuscript, format for IEEE, format for CVPR, write rebuttal, chuẩn bị nộp báo, viết bản thảo, phản hồi reviewer. It writes and formats manuscripts; it does NOT conduct the primary research or run experiments (use paper-method, paper-synthesize, or run-on-modal)."
argument-hint: "<topic | conference name> [draft|format|rebuttal]"
allowed-tools: "Read Write Glob Bash"
---

# Paper Submission (Viết & Chuẩn bị Bản thảo)

> **Role:** Transforms research synthesis notes, experiment results, and method notes into submission-ready academic manuscripts (LaTeX/PDF format) tailored to specific conferences/journals.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `draft` | Draft manuscript from notes | Starting the writing phase of a paper |
| `format` | Apply specific venue template | Adapting existing text to IEEEtran, CVPR, etc. |
| `rebuttal` | Draft reviewer response | Responding to peer review feedback |

## Procedure

### Mode: draft
1. **Read Inputs:** Read `notes/INDEX.md` and relevant synthesis/method notes (e.g., `notes/synthesize-compare.md`, `notes/*-method.md`).
2. **Structure:** Generate a standard academic structure: Abstract, Introduction, Related Work, Method, Experiments, Conclusion.
3. **Drafting (Vietnamese/English):** As per workbench conventions, draft in the requested language (default to English for standard academic submission, but keep chat in Vietnamese).
4. **Citation Check:** Ensure every claim is backed by a citation from the input notes. Do not hallucinate citations.

### Mode: format
1. **Identify Target:** Determine target venue (e.g., CVPR, ICCV, IEEE Q1).
2. **Template Application:** Use the official LaTeX template for the venue. Structure the `.tex` file with appropriate macros (e.g., `\author`, `\maketitle`, `\bibliographystyle`).
3. **Math & Figures:** Use `latex-math-renderer` guidelines to ensure math is correctly formatted for the specific LaTeX engine. Check that figure references follow venue guidelines.
4. **Output:** Generate the `main.tex` and a `bib` file.

### Mode: rebuttal
1. **Input:** Read the reviewer comments (provided in text or file).
2. **Deconstruct:** Break down reviewer concerns point-by-point.
3. **Draft Response:** Write a respectful, evidence-based response. Cite new experiments or specific sections of the paper where changes were made.
4. **Output:** A rebuttal document (`rebuttal.md` or `rebuttal.tex`).

## Cross-References
- `paper-synthesize` → Provides the raw material for the Related Work section.
- `paper-method` → Provides the raw material for the Method section.
- `latex-fix` → For repairing any LaTeX formatting issues.

## Gotchas
- **No Hallucination:** Do not invent experiment results or citations. If data is missing, insert a placeholder (e.g., `[TODO: Insert F1 score from experiment]`) and explicitly mention it in the report.
- **Strict Templating:** When formatting, adhere strictly to the target venue's official LaTeX template constraints (page limits, font sizes, citation styles).
