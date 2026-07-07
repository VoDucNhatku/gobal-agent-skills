# ATS Rules 2025 — ai-cv-forge internal reference

> Skill-internal. Used by ai-cv-forge modes when formatting cv.md and profile output.
> ATS = Applicant Tracking System (the software companies use to parse incoming applications).
> Source: aggregate of Greenhouse, Lever, Ashby, Taleo, iCIMS, Workday parser behavior + career-ops pdf mode template rules (verified by user's actual runs).

---

## 1. Determining Rules (HARD — must follow)

### Document format
- **Format**: Markdown output → PDF via career-ops generate-pdf.mjs (uses Puppeteer headless Chrome)
- **Page size**: a4 (most of world) or letter (US/Canada) — infer from candidate location
- **Color**: Black text on white background — ATS treats color-only headers as text; decorative colors are dropped in parsing
- **Font**: Space Grotesk headings + DM Sans body (self-hosted in career-ops same as pdf mode). Fall back to system sans if skill run outside career-ops.
- **Margins**: 0.6in all sides
- **Max length**: 1 page (fresh grad ceiling). 2 pages unacceptable unless extraordinary experience.

### Section headers (ATS keyword anchoring)
Use these EXACT section headers (case matters for some parsers):

1. **Professional Summary** (not "Summary", not "Profile")
2. **Work Experience** (or "Internship & Work Experience" for fresh grad)
3. **Projects** (NOT "Personal Projects" — some parsers drop "personal" as fluff)
4. **Education**
5. **Skills** (NOT "Technical Skills" — "Skills" is the ATS-recognized token)

Optional sections (add if relevant):
- Certifications
- Awards & Competitions
-Publications (if papers — use exact "Publications")
- Open Source / Community

ATS drops "Portfolio", "Repos", "Talks" as noise — fold these into Projects or add as sub-bullets.

### Section order (optimized for 6-second scan)
1. Header (name + contact)
2. Professional Summary — keyword-dense, 3-4 lines
3. Work Experience / Internship / Teaching
4. Projects
5. Education
6. Skills

Skip "Objective" — ATS treats it as fluff; Summary wins on keyword count.

---

## 2. Hard Don'ts (ATS will break / reject)

| Don't | Why |
|---|---|
| Two-column layout | Most ATS read left-to-right; two-column scramble, drop right column entirely |
| Text in images/SVGs | ATS can't OCR in most cases — text inside logos/icons vanishes |
| Critical info in header/footer | Many ATS ignore header/footer region — contact info in clear body text |
| Nested tables | Unreliable — use simple lists instead |
| Fancy Unicode / em-dashes / smart quotes | `generate-pdf.mjs` normalizes these, but write as ASCII dashes/quotes to be safe |
| Abbreviations without expansion first time | ATS has no context: "LLM" on its own may not match "large language model" keyword |
| Non-standard section headers | "What I do" or "About me" → won't match recruiter's keyword search |
| Excessive bullet depth (>3 levels) | Flattens weirdly |
| Skills listed as sentence ("I am skilled in X, Y, and Z") | Needs to be parseable units — pipe-separated, comma-separated listed, or bullet list work |
| "References available upon request" | Waste of a line; obvious; ATS noise |

---

## 3. Yesses (ATS-friendly patterns)

| Do | Why |
|---|---|
| Standard section headers (exact names above) | Recruiter search + ATS metadata matching |
| Single-column | Safest across all ATS |
| Bullets start with verb (past tense for past roles, present for current) | ATS parses activity sentences better |
| Keywords inline naturally ("Enhanced RAG pipeline using LangChain and Chroma") | Matches both human and ATS |
| URLs as Markdown `[repo](url)` | Both clickable in PDF text-layer AND ATS-extractable |
| Parenthetical jargon expansion first use | "Large Language Model (LLM)" — both tokens indexed |
| Quantified bullets | Numbers pass both ATS diversity check and human scan |
| Skills in a dedicated 6-12 item list | Easy to match against JD requirements |

---

## 4. Industry-Specific Checks for AI Roles

### LLM / GenAI specific
- Ensure these tokens appear SOMEWHERE in the parsed form: LLM, RAG, vector database, prompt, fine-tune, eval, agent, pipeline, API
- "LLM" alone is weak — pair with something actionable: "RAG pipeline with LLM backend"
- "AI" token alone is too broad — pair with domain: "AI for legal doc classification"

### Python-required roles
- "Python" keyword must appear
- Framework if relevant: "PyTorch", "TensorFlow", "HuggingFace", "scikit-learn"
- Data stack: Pandas, NumPy, SQL — well-known enough to pass implicitly

### MLOps / Platform roles
- "MLflow", "Docker", "Kubernetes", "CI/CD", "monitoring", "deployment"
- Cloud provider name helps (AWS/GCP/Azure)
- Model registry mention: MLflow, W&B, Sagemaker, Vertex

---

## 5. Human-Side Checks (what a recruiter still judges despite ATS)

| Check | How to pass |
|---|---|
| Visual scan within 6 seconds | Lead with strongest metric in first bullet of first project |
| Metric presence | Every section should have at least 1 number |
| Link verification | All clickable; test before sending |
| Grammar / verb tense consistency | Use past tense for past roles; present for current/ongoing |
| Jargon level appropriate to target company | Startup = acceptable to say "RAG + LangChain"; Consulting = explain in plain to a partner |
| Cover letter present when asked | Career-ops auto-generates this based on JD |
| File naming | `Lastname-Firstname-CV-YYYY-MM-DD.pdf` (ATS extracts from filename sometimes) |
| File size | < 2 MB; if heavy images, compress. Plain-text + minimal SVG is fine |

---

## 6. PDF Generation Script Behavior (career-ops `generate-pdf.mjs`)

- Automatically normalizes Unicode (em-dash → `--`, smart quotes → straight, zero-width → delete)
- Kills duplicate whitespace
- Uses Puppeteer headless Chromium — print media CSS
- Output path: `output/cv-{candidate}-{company}-{date}.pdf`
- Page-break CSS: `page-break-inside: avoid` on section, bullet group

When ai-cv-forge creates cv.md, assume `generate-pdf.mjs` will process it. So:
- Use Markdown standard: `#`, `##`, `###` headings, `- ` bullets (NOT `*`)
- Don't embed HTML unless safe (inline SVG, complex tables → avoid)
- Don't use tables for layout (use lists)

---

## 7. AT Scorecard (Quick Self-Check Before Export)

After drafting cv.md, run through:

- [ ] One-page? (Fresh grad = YES)
- [ ] All 5 required sections present?
- [ ] Each bullet has verb, tool, result?
- [ ] At least 1 metric per section?
- [ ] All links clickable?
- [ ] "Professional Summary" header exact?
- [ ] Skills section structured as list?
- [ ] Keyword from target JD appears at least 3–4x?
- [ ] No "passionate about", no levers/spearheads?
- [ ] No two-column layout?
- [ ] No text inside images?
- [ ] File will be named correctly when exported?
