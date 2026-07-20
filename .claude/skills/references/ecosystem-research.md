# Ecosystem research — 8 famous Claude Code skill repos (verified findings)

> On-demand reference (NOT in always-loaded context — progressive disclosure, saves tokens).
> Captured 2026-06-28 by a multi-agent research workflow (runId wf_33ae306d-388). Star counts are
> what each GitHub page literally displayed at fetch time — treat as point-in-time, not audited.
> Purpose: if Workbench is ever redesigned, the raw source material is here — no need to re-research.

## Quick verification table

| Repo | Verified | Stars (as shown) |
|---|---|---|
| `obra/superpowers` | yes | 240k |
| `anthropics/skills` | yes | ~156k stars |
| `https://github.com/mattpocock/skills` | yes | 148,253 stars |
| `garrytan/gstack` | yes | 117k stars |
| `nextlevelbuilder/ui-ux-pro-max-skill` | yes | 97 |
| `Egonex-AI/Understand-Anything` | yes | 68 |
| `addyosmani/agent-skills` | yes | 67 |
| `Leonxlnx/taste-skill` | yes | ~52,000 stars |


---

## obra/superpowers (https://github.com/obra/superpowers)

- **Verified:** True
- **Stars (as shown):** 240k (the GitHub page displays "240k"; the user's "204K" appears to be a transposed/inflated figure). Note: this is plausibly a very popular repo but I report only what the page literally showed.

**What it is:** An agentic skills framework and software-development methodology for coding agents. Description verbatim: "An agentic skills framework & software development methodology that works." It ships composable, kebab-case "skills" (each a SKILL.md) plus bootstrap instructions that force the agent to use them, installable as a plugin across many harnesses (Claude Code, Codex, Cursor, Gemini CLI, Copilot CLI, Kimi, OpenCode, Antigravity, Pi, Factory Droid). It turns the agent into a disciplined engineer by gating every step (design before code, failing test before implementation, review before done).

**Workflow / methodology:** A 7-phase sequential pipeline, each phase a skill that auto-activates at a gate: (1) brainstorming -> (2) using-git-worktrees -> (3) writing-plans -> (4) subagent-driven-development / executing-plans -> (5) test-driven-development (RED-GREEN-REFACTOR) -> (6) requesting-code-review -> (7) finishing-a-development-branch. Each phase hands off to the next and refuses to skip ahead (e.g. brainstorming's "ONLY skill invoked after brainstorming is writing-plans"; code review's "Critical issues block progress").

**Skills / commands it ships:**
- `brainstorming`
- `writing-plans`
- `executing-plans`
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`
- `receiving-code-review`
- `using-git-worktrees`
- `finishing-a-development-branch`
- `writing-skills`
- `using-superpowers`

**Token-economy / verification / anti-mistake mechanisms:**
- Skill-invocation mandate as a hard gate: 'If you think there is even a 1% chance a skill might apply...YOU ABSOLUTELY MUST invoke the skill' — and the check happens BEFORE clarifying questions or any action (description: 'requiring skill invocation before ANY response including clarifying questions').
- Progressive disclosure via SKILL.md + satellite reference files: a skill's body links out to deeper docs loaded only on demand (e.g. TDD links '[testing-anti-patterns.md](testing-anti-patterns.md)'). Frontmatter description is terse and trigger-shaped so the loader can match cheaply before pulling the full body.
- TDD 'Iron Law' verification gate: 'NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST' and the anti-mistake remedy 'Write code before the test? Delete it. Start over. No exceptions.'
- Verification Checklist as a terminal gate: an 8-item checklist where 'Can't check all boxes? You skipped TDD. Start over.', plus a 'Red Flags - STOP and Start Over' section ('All of these mean: Delete code. Start over with TDD.').
- Two-stage subagent review (spec compliance, THEN code quality) with a fresh subagent dispatched per task — isolates context per task so a long plan doesn't bloat one agent's context.
- Brainstorming hard gate: 'Do NOT invoke any implementation skill, write any code... until you have presented a design and the user has approved it', plus a self-review step scanning the spec for placeholders/contradictions before asking for approval.
- Design-doc artifact persisted to a deterministic path (docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md) and committed to git — durable shared memory across phases.

**Ideas worth adapting into Workbench:**
- Adopt a single 'using-superpowers'-style dispatcher skill that runs FIRST every session and forces skill-discovery before any reply — the Workbench already has workbench-orchestrator, but borrow the explicit '1% chance => you MUST invoke' rule so workers never silently skip the right skill, and make the check precede even clarifying questions.
- Add a TDD-style 'Iron Law' + terminal Verification Checklist to the CODE skills (paper-to-notebook, run-on-modal): e.g. 'no reported metric without a cell that actually ran it; can't check all boxes => the notebook is not done.' This gives reproduce/run-results modes a hard self-gate matching the existing fidelity rule ('do not invent results').
- Encode the Brainstorm->Plan->Execute->Review pipeline as explicit handoff gates inside the Workbench orchestrator: each worker names the ONLY next skill allowed (superpowers' 'terminal state requirement'), instead of relying on the orchestrator to remember. Mirrors the existing '-> dùng skill Z cho việc Y' handoff note but makes it a refusal-gate, not advice.
- Steal the deterministic, git-committed design-spec artifact (docs/.../YYYY-MM-DD-<topic>-design.md) as the analog of notes/design-<slug>.md: brainstorming writes a dated design doc, self-reviews it for placeholders/contradictions, THEN asks approval. Apply the same 'self-review for placeholders before presenting' pass to design-ui-direction and paper-synthesize outputs.
- Use superpowers' two-stage, fresh-subagent-per-task review pattern for token economy: dispatch an isolated subagent per paper/per task so each one's context stays small (matches §11 'subagent returns only a path + 1-2k token summary'), then run a two-stage review = (a) did it meet the task spec, (b) is the artifact quality good — before merging into INDEX.md.
- Mirror the per-skill 'Common Rationalizations' debunking table and 'Red Flags - STOP and Start Over' section in Workbench skills as a cheap anti-slop / anti-shortcut device — e.g. review-frontend already has a slop checklist; add an explicit 'rationalizations that mean you skipped grounding -> start over' table per §8.
- Keep the superpowers progressive-disclosure shape that Workbench conventions already mandate (SKILL.md < 500 lines, detail in rules/ or references/ one level deep): superpowers validates the pattern at scale (14 skills, satellite .md files like testing-anti-patterns.md). Reinforce that worker SKILL.md frontmatter descriptions stay terse + trigger-shaped so matching is cheap before the body loads.
- Adopt the explicit RED-GREEN-REFACTOR-then-COMMIT cadence (commit after each green) for run-on-modal / paper-to-notebook iterative builds, so each working increment is checkpointed — analogous to superpowers committing the spec and using git-worktrees for an isolated, clean-baseline workspace per task.

**Verbatim quotes:**
- > An agentic skills framework & software development methodology that works.
- > a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them
- > If you think there is even a 1% chance a skill might apply...YOU ABSOLUTELY MUST invoke the skill
- > description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
- > The Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
- > Write code before the test? Delete it. Start over. No exceptions.
- > Can't check all boxes? You skipped TDD. Start over.
- > Enforces RED-GREEN-REFACTOR: write failing test, watch it fail, write minimal code, watch it pass, commit. Deletes code written before tests.
- > Breaks work into bite-sized tasks (2-5 minutes each). Every task has exact file paths, complete code, verification steps.
- > two-stage review (spec compliance, then code quality)
- > Critical issues block progress.
- > Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.
- > design spec saved to docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md
- > references testing-anti-patterns.md


---

## anthropics/skills (https://github.com/anthropics/skills)

- **Verified:** True
- **Stars (as shown):** ~156k stars (the "204K" figure is inflated; GitHub showed "156k" at fetch time)

**What it is:** Anthropic's official public repository of Agent Skills. A "Skill" is a folder containing a SKILL.md (YAML frontmatter + markdown instructions) plus optional bundled scripts/, references/, and assets/, that Claude dynamically loads for specialized tasks. The repo ships four source-available document skills (docx/pdf/pptx/xlsx) that power Claude's real document capabilities, plus ~13 example/teaching skills, an Agent Skills spec, and a skill template. Skills are registered as Claude Code plugins via .claude-plugin/marketplace.json (three plugins: document-skills, example-skills, claude-api). Repo explicitly disclaims that examples are "provided for demonstration and educational purposes only."

**Workflow / methodology:** Two distinct workflows. (1) Authoring methodology (skill-creator): a five-stage iterative loop — Capture Intent -> Interview & Research -> Draft SKILL.md -> Test & Evaluate (with-skill run vs baseline run, programmatic assertion grading, benchmark.json with pass-rate/timing/token deltas, HTML viewer) -> Improve & Iterate; followed by a separate description-optimization loop (generate 20 trigger/no-trigger evals, run_loop on a 60/40 train/held-out split, pick best_description). (2) Document-editing methodology (docx/pptx/xlsx): treat the file as a ZIP of XML and use a strict unpack -> edit-raw-XML-in-place -> pack+validate pipeline driven by bundled scripts (scripts/office/unpack.py, pack.py, validate.py), rather than regenerating the file. The pdf skill encodes operation->library routing (pypdf manipulate / pdfplumber extract / reportlab create / pytesseract OCR).

**Skills / commands it ships:**
- `docx`
- `pdf`
- `pptx`
- `xlsx`
- `algorithmic-art`
- `brand-guidelines`
- `canvas-design`
- `claude-api`
- `doc-coauthoring`
- `frontend-design`
- `internal-comms`
- `mcp-builder`
- `skill-creator`
- `slack-gif-creator`
- `theme-factory`
- `web-artifacts-builder`
- `webapp-testing`

**Token-economy / verification / anti-mistake mechanisms:**
- Three-tier progressive disclosure (the core token-economy mechanism): metadata name+description (~100 words) ALWAYS in context; SKILL.md body (<500 lines) loaded only when the skill triggers; bundled resources (scripts/references/assets, effectively unlimited) loaded only as needed.
- Conditional reference loading: SKILL.md points to sibling files with an explicit when-to-read gate, e.g. pdf says 'If you need to fill out a PDF form, read FORMS.md and follow its instructions'; reference files >300 lines get a table of contents so the model can jump to the right section.
- Hard size budget: 'Keep SKILL.md under ~500 lines'; oversized content must be split into references/.
- Script-offloading for repeated/deterministic work: recurring patterns across test runs become bundled scripts (e.g. office/unpack.py, pack.py, validate.py, comment.py) so the model calls a script instead of regenerating boilerplate.
- Pack-time validation as an anti-mistake gate: validate.py auto-repairs invalid durableId and missing xml:space=preserve; element-ordering and 8-digit-hex RSID rules are enforced.
- Eval-based verification gate before 'done': with-skill vs baseline runs spawned in the SAME turn (to avoid timing misalignment), programmatic assertion grading (fields text/passed/evidence), reading transcripts (not just outputs) to catch unproductive work, and a human-review viewer pass before self-evaluation.
- Description-optimization with train/held-out split to prevent overfitting trigger phrasing.
- Explicit negative-scope statements (docx applies to .docx but NOT pdf/xlsx/Google Docs) to prevent mis-triggering.

**Ideas worth adapting into Workbench:**
- Adopt the canonical three-tier progressive-disclosure budget verbatim as the Workbench standard: ~100-word metadata always-on, SKILL.md <500 lines on trigger, references/scripts/assets on demand. This matches workbench-conventions §11 and gives a concrete number to enforce.
- Add a real TEST/EVAL harness to the suite (currently absent). Borrow skill-creator's pattern: for each worker skill, run a with-skill vs no-skill baseline in the same turn, grade quantitative assertions programmatically, and emit a benchmark.json with pass-rate + token-delta + timing mean±stddev. This would let the orchestrator prove a skill actually saves tokens / improves output, not just assert it.
- Steal the description-optimization loop (run_loop.py over 20 should-trigger / should-not-trigger evals on a 60/40 train/held-out split, select best_description) to tune the trigger lists of the Workbench skills — those long Vietnamese+English trigger phrase lists are exactly what this optimizes, and the held-out split guards against overfitting.
- Adopt the unpack -> edit-raw-XML-in-place -> pack+validate pipeline as a model for latex-fix and any 'repair an existing artifact' skill: operate on a parsed/expanded form, edit only the offending spans, then run a validator script that auto-repairs known defects — mirrors latex-fix's 'fix only flagged spans' rule and adds a validation gate.
- Copy the explicit 'when to read this file' gating sentence pattern ('If you need X, read FILE.md and follow its instructions') into every Workbench SKILL.md citation of rules/ and references/, plus the '>300 lines gets a table of contents' rule, so satellite rule files are jumped-into, not fully ingested.
- Encode hard-won anti-mistake constants as explicit DO/NEVER bullets the way docx does (e.g. 'Always set page size explicitly — default is A4 not US Letter', 'Always use WidthType.DXA — percentages break in Google Docs', 'Never use Unicode subscript/superscript in ReportLab — renders as black boxes'). The Workbench code/web skills should ship an equivalent curated gotcha list (e.g. money in integer cents, server-side entitlement) as terse imperatives.
- Add a package/distribution step (scripts/package_skill -> .skill file) and a marketplace.json-style manifest so the Workbench suite is installable as Claude Code plugins grouped by domain (research / code / web), exactly as anthropics/skills groups document-skills vs example-skills vs claude-api.
- Use skill-creator's authoring rule 'explain the WHY behind instructions to leverage LLM reasoning, and generalize from feedback rather than overfitting to examples' as a style rule when revising the Workbench SKILL.md bodies — prefer principles over enumerated special-cases.
- Adopt the operation->library routing-table format from the pdf skill (a small table mapping task -> the one correct tool) for run-on-modal (GPU-tier table) and paper-to-notebook (code-source routing: Papers With Code -> GitHub -> HF), keeping the decision logic compact and scannable.
- Use a per-skill workspace convention like skill-creator's <skill-name>-workspace/iteration-N/eval-ID/ for any iterative Workbench mode, instead of scattering temp files — complements the existing /tmp/<skill>_<id>_<mode>.json collision-free spec rule.

**Verbatim quotes:**
- > Skills teach Claude how to complete specific tasks in a repeatable way.
- > Metadata (~100 words): name and description always in context; SKILL.md body (<500 lines): loaded when skill triggers, kept 'lean'; Bundled resources (unlimited): scripts, references, and assets loaded as needed
- > references/ (documentation, >300 lines get table of contents)
- > If you need to fill out a PDF form, read FORMS.md and follow its instructions
- > A .docx file is fundamentally 'a ZIP archive containing XML files.'
- > python scripts/office/pack.py unpacked/ output.docx --original document.docx
- > Always set page size explicitly — defaults to A4, not US Letter
- > Always use WidthType.DXA — percentage widths break in Google Docs
- > Never use Unicode subscript/superscript characters in ReportLab PDFs—they render as black boxes
- > Spawn with-skill AND baseline runs in the same turn to prevent timing misalignment
- > Read transcripts, not just outputs, to catch unproductive work the skill may be generating
- > Keep SKILL.md under ~500 lines; split oversized content into references
- > scripts/run_loop iteratively tests descriptions on 60% training / 40% held-out test splits, selecting the best by test score to avoid overfitting
- > provided for demonstration and educational purposes only
- > Public repository for Agent Skills


---

## https://github.com/mattpocock/skills

- **Verified:** True
- **Stars (as shown):** 148,253 stars (confirmed via GitHub API stargazers_count, 2026-06-28; forks 12,826, watchers 944). The user's "204K" is NOT accurate.

**What it is:** A published Claude Code skills pack by Matt Pocock — "Skills for Real Engineers. Straight from my .claude directory." Installed via `npx skills@latest add mattpocock/skills`. It is a curated, composable set of agent skills organized into engineering/, productivity/, and misc/ folders, built around a single thesis: agentic coding fails in four predictable ways (misalignment, verbosity, broken code, architectural decay), and each skill is a targeted countermeasure. Skills are deliberately "small, easy to adapt, and composable" and "work with any model." The flagship workflow chains user-invoked orchestration skills (PRD -> issues -> implement) on top of model-invoked discipline skills (tdd, diagnosing-bugs, domain-modeling, codebase-design).

**Workflow / methodology:** grill/align -> to-prd -> to-issues (vertical slices) -> implement, with tdd + diagnosing-bugs as the model-invoked discipline layer and improve-codebase-architecture run periodically against decay

**Skills / commands it ships:**
- `engineering/ask-matt (router meta-skill)`
- `engineering/grill-with-docs`
- `engineering/grill-me (productivity)`
- `engineering/to-prd`
- `engineering/to-issues`
- `engineering/implement`
- `engineering/tdd`
- `engineering/diagnosing-bugs`
- `engineering/triage`
- `engineering/domain-modeling`
- `engineering/codebase-design`
- `engineering/improve-codebase-architecture`
- `engineering/prototype`
- `engineering/resolving-merge-conflicts`
- `engineering/setup-matt-pocock-skills`
- `productivity/handoff`
- `productivity/teach`
- `productivity/writing-great-skills`
- `productivity/grilling`
- `misc/git-guardrails-claude-code`
- `misc/migrate-to-shoehorn`
- `misc/scaffold-exercises`
- `misc/setup-pre-commit`

**Token-economy / verification / anti-mistake mechanisms:**
- Progressive disclosure as an explicit rule: keep SKILL.md lean, push reference material to a linked .md file in the skill folder named for what it holds — 'Push too little down and the top bloats; push too much and you hide material the agent actually needs.'
- The No-Op Test for every sentence: 'Does it change behaviour versus the default? A weak leading word is a no-op; the fix is a stronger word.' Failing sentences are deleted entirely, not trimmed.
- Trigger de-duplication: 'One trigger per branch. Synonyms that rename a single branch are duplication' — duplicated triggers waste tokens without improving reliability.
- CONTEXT.md domain glossary as a token-economy device: a shared jargon doc (e.g. 'materialization cascade') cuts verbosity, standardizes naming, and reduces token spend.
- TDD verification gates: 'Never write code before a failing test'; RED->GREEN->REFACTOR; 'Never refactor while RED. Get to GREEN first'; reject horizontal slicing ('DO NOT write all tests first, then all implementation').
- diagnosing-bugs hard gate: 'No red-capable command, no Phase 2' — a reproducing/failing loop must exist before ANY hypothesis. 'If you catch yourself reading code to build a theory before this command exists, stop.'
- disable-model-invocation: true on synthesis/router skills (to-prd, ask-matt) so they only run when the user explicitly invokes them — preventing the agent from auto-firing an expensive orchestration skill.
- Triage label gate: PRDs publish to the tracker with a 'ready-for-agent' label, so only vetted work flows to implementation.

**Ideas worth adapting into Workbench:**
- Adopt the user-invoked vs model-invoked split explicitly in the Workbench suite. Pocock's rule maps cleanly onto Workbench: user-invoked = orchestration (the workbench-orchestrator), model-invoked = reusable discipline (paper-read, paper-method, etc.). His hard rule 'a user-invoked skill may invoke model-invoked skills, but never another user-invoked one' is a clean anti-recursion guarantee worth encoding into the orchestrator.
- Build an 'ask-matt'-style router meta-skill for Workbench: a single user-invoked skill carrying a literal intent->skill decision table (e.g. 'one paper, quick read -> paper-read gist; method math -> paper-method critique; many papers -> paper-synthesize'). This solves the 'unambiguous calling' / personalization angle by making routing a documentation table a human or agent reads, not fuzzy trigger-matching. Pocock's framing: 'router skill: one user-invoked skill that names the others.'
- Steal the No-Op Test for every SKILL.md sentence and trigger line: 'Every sentence must change behaviour versus the default.' This directly serves workbench-conventions.md section 11 (SKILL.md under 500 lines) — make it an authoring gate, not just a length cap.
- Steal 'One trigger per branch; synonyms that rename a single branch are duplication.' The Workbench trigger lists are currently long and synonym-heavy (e.g. paper-read lists ~15 triggers, many bilingual synonyms). Pocock argues those waste tokens without improving reliability — worth auditing, though Workbench's bilingual policy is a legitimate reason to keep VN+EN pairs.
- Adopt CONTEXT.md as a first-class token-economy artifact alongside notes/INDEX.md. A per-project domain glossary (Pocock's 'materialization cascade' example) compresses every downstream prompt. Workbench already mandates a Glossary table per artifact (section 1) — promote it to a single living CONTEXT.md the orchestrator maintains and every worker reads, mirroring his approach.
- Port the diagnosing-bugs reproduction-first gate to code-running skills (run-on-modal, paper-to-notebook): require a 'red-capable command' (a failing/assertable repro that hits the exact symptom) before any fix hypothesis — 'No red-capable command, no Phase 2.' This is a strong anti-mistake mechanism the Workbench code path currently lacks.
- Port the 3-5 ranked falsifiable-hypotheses format ('If <X> is the cause, then <changing Y> will make the bug disappear') and 'share rankings with the user, they reshuffle priority instantly' into any Workbench debugging/repro-failure handling.
- Adopt 'tracer-bullet vertical slices' for to-issues-style decomposition: each unit of work is 'a narrow but COMPLETE path through every layer' that is 'demoable or verifiable on its own,' published in dependency order. For Workbench this maps to scaffolding a course platform as thin end-to-end slices (one feature through schema->API->UI->test) rather than horizontal layers — fits the orchestrator's parallel-subagent model.
- Adopt the to-prd seam-minimization heuristic for the web/scaffold path: 'Prefer existing seams; aim for the highest seam level; minimize seam count (ideal: one); confirm with the user before proceeding.' A concrete design-quality gate.
- Borrow the disable-model-invocation:true pattern for Workbench's expensive synthesis skills (paper-synthesize, the orchestrator) so the agent cannot auto-fire a costly multi-source pass — it runs only on explicit user intent, protecting the token budget.
- Borrow the explicit four-failure-mode framing as the suite's README spine. Workbench currently lists conventions; a parallel 'these are the N ways research+code+web agents fail, and here is the skill that counters each' framing makes the suite legible and sells the why of each skill.
- Adopt 'Front-load the skill's leading word — the description is where it does its invocation work.' Workbench descriptions often open with the skill name; leading with the strongest trigger verb improves auto-invocation reliability.

**Verbatim quotes:**
- > Skills for Real Engineers. Straight from my .claude directory.
- > designed to be small, easy to adapt, and composable. They work with any model.
- > User-invoked skills are reachable only when you type them (e.g. /grill-me); their job is to orchestrate. Model-invoked skills can be invoked by you or reached for automatically by the agent when the task fits; they hold the reusable discipline. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.
- > Front-load the skill's leading word — the description is where it does its invocation work.
- > One trigger per branch. Synonyms that rename a single branch are duplication.
- > router skill: one user-invoked skill that names the others.
- > Push too little down and the top bloats; push too much and you hide material the agent actually needs.
- > Does it change behaviour versus the default? A weak leading word is a no-op; the fix is a stronger word.
- > DO NOT write all tests first, then all implementation.
- > Never refactor while RED. Get to GREEN first.
- > This is the skill. Everything else is mechanical. ... No red-capable command, no Phase 2.
- > If you catch yourself reading code to build a theory before this command exists, stop.
- > If <X> is the cause, then <changing Y> will make the bug disappear.
- > a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- > a completed slice is demoable or verifiable on its own
- > Prefer existing seams over new ones; aim for the highest possible seam level; minimize seam count across the codebase (ideal: one).
- > Turn the current conversation into a PRD and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed.
- > There's a problem with the materialization cascade (vs the verbose 'a lesson inside a section of a course is made real').


---

## garrytan/gstack (https://github.com/garrytan/gstack)

- **Verified:** True
- **Stars (as shown):** 117k stars (17.4k forks), as displayed on the GitHub repo page on 2026-06-28. The user's claimed "204K stars" is NOT what the page shows and appears inflated. Caveat: even 117k is implausibly high for a niche Claude Code skill repo and could not be cross-checked against a second source; treat it as "what the page reports," not independently confirmed.

**What it is:** An open-source "software factory" by Garry Tan that turns Claude Code into a virtual engineering team. It ships a large suite of slash-command skills (README markets it as "Twenty-three specialists and eight power tools"; CLAUDE.md says "30+ major skills"), each a generated SKILL.md, organized around a sprint methodology Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect. All Markdown, all slash commands, MIT licensed. The user's "25 skills" is roughly right but the repo's own framing is 23 specialist roles + 8 power tools; the actual top-level command count is ~45 including iOS/setup/utility variants.

**Workflow / methodology:** Sprint pipeline: Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect. Planning is gated by a stack of adversarial role-review skills (/office-hours product interrogation, /plan-ceo-review strategic scope, /plan-eng-review architecture lockdown, /plan-design-review, /plan-devex-review); /autoplan chains CEO->design->eng reviews automatically. Build: /design-shotgun (4-6 mockup variants) -> /design-html (production HTML). Review/test: /review (staff-eng audit), /qa (live browser), /codex (independent OpenAI cross-model review as a pass/fail gate), /cso (OWASP+STRIDE). Release: /ship -> /land-and-deploy -> /canary. Reflect: /retro, /learn (persistent memory). Repo thesis: "The sprint structure is what makes parallelism work. Without a process, ten agents is chaos."

**Skills / commands it ships:**
- `/office-hours`
- `/plan-ceo-review`
- `/plan-eng-review`
- `/plan-design-review`
- `/plan-devex-review`
- `/autoplan`
- `/design-consultation`
- `/design-shotgun`
- `/design-html`
- `/design-review`
- `/review`
- `/qa`
- `/qa-only`
- `/devex-review`
- `/cso`
- `/codex`
- `/ship`
- `/land-and-deploy`
- `/canary`
- `/document-release`
- `/document-generate`
- `/browse`
- `/connect-chrome`
- `/pair-agent`
- `/learn`
- `/retro`
- `/investigate`
- `/spec`
- `/careful`
- `/freeze`
- `/unfreeze`
- `/guard`
- `/gstack-upgrade`
- `/make-pdf`
- `/diagram`
- `/benchmark`
- `/context-restore`
- `/ios-qa`
- `/ios-fix`
- `/ios-design-review`

**Token-economy / verification / anti-mistake mechanisms:**
- PROGRESSIVE DISCLOSURE via a `preamble-tier` frontmatter field on every SKILL.md (confirmed real: /ship is preamble-tier 4, /design-html is tier 2). CLAUDE.md: 'preamble-tier skills are loaded into context only when the user explicitly requests them, keeping the command surface small and preserving token budget for agent reasoning.' A curated command list is surfaced first; the full ~1500-2000-line SKILL.md loads only on demand.
- TOKEN-BUDGET GUARDRAIL: generated SKILL.md files trigger a warning above ~160KB (~40K tokens) to catch feature creep, explicitly a soft flag not a hard cap ('prompt caching makes the marginal cost of larger skills small').
- VERIFICATION GATE / anti-rationalization in /ship: 'NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE'; 'should work' / 'I'm confident' does NOT count as evidence, fresh test output required if code changed after the test step. Every verification step re-runs on every invocation; only side-effecting actions are idempotent.
- EXPLICIT stop policy: documented 'Never Stop For' (auto-handle trivial decisions) vs 'Always Stop For' (judgment calls only) lists, so the agent runs straight through except at real gates.
- CROSS-MODEL SECOND-OPINION GATE: /codex runs an independent OpenAI review as pass/fail (a [P1] finding on 200+ line diffs blocks ship), reducing single-model blind spots.
- DETERMINISTIC OFFLOADING: version bumps, PR-title formatting, review-log reads delegated to named scripts ('Use gstack-version-bump classify deterministically — never hand-roll VERSION writes'), keeping the model out of mechanical work.
- STALENESS DETECTION: review-readiness computed from a local JSONL review log; a review older than 7 days or behind current HEAD is flagged stale with the elapsed-commit count.
- Prompt-injection defense layer (ML classifier + Haiku voting + canary tokens) for the browser tools.

**Ideas worth adapting into Workbench:**
- Adopt an explicit `preamble-tier` field (or equivalent) in each Workbench SKILL.md to formalize progressive disclosure: surface only a thin command list + one-line trigger set by default, load the full skill body only on invocation. Same token-economy goal as Workbench's cite-rules-in-one-line/read-at-runtime convention, but applied to the skills themselves with a machine-readable tier an orchestrator can budget against.
- Steal the /ship anti-rationalization gate for the code domain (run-on-modal / paper-to-notebook): forbid 'completion claims without fresh verification evidence' — never report a notebook/Modal run as working without fresh execution output; 'should work is not evidence.' Bakes the fidelity rule into a hard runtime gate.
- Add a documented 'Never Stop For' vs 'Always Stop For' decision list to workbench-orchestrator so it auto-handles trivial choices (naming, MICRO bumps) and only interrupts for genuine judgment calls (scope decisions, cross-source assumptions) — pairs with the audit-log materiality concept.
- Add a cross-model / adversarial second-opinion gate analogous to /codex: have paper-method or paper-synthesize optionally re-check a claim or critique with an independent pass before it lands, as pass/fail rather than ambient hope. Fits the deep-research 'adversarially verify claims' step.
- Build a review-staleness mechanism into notes/INDEX.md like gstack's JSONL review log: stamp each distilled artifact with source mtime/commit, and when a downstream skill reuses it (REUSE-BEFORE-READ rule), auto-flag 'note from {date} may be stale — source changed' instead of silently reusing.
- Mirror /design-html's hard constraints in build-ui-component/Artifacts: 'self-contained, zero external deps, inline everything, pixel-match the approved mockup, never lorem ipsum, surgical Edit not full-regenerate in the refinement loop.' Matches the Artifact CSP constraints and frontend-aesthetics anti-slop rules and makes web skills more deterministic.
- Generate SKILL.md from a .tmpl + a script (gstack: 'never edited directly... bun run gen:skill-docs') so boilerplate/frontmatter is script-produced and the human writes only judgment parts — extends the Workbench script-offloading rule to the skill docs themselves, preventing drift and merge-conflict corruption.
- Set a soft token-budget warning per skill body (gstack warns ~40K tokens) rather than a silent hard cap — Workbench already mandates <500-line bodies; a generated warning would enforce it automatically.
- Use the staged auto-chained review pattern (CEO->eng->design->devex via /autoplan) as a template for a research analog: an auto-chained reading-triage -> paper-read -> paper-method -> paper-synthesize pass the orchestrator runs without re-prompting, each stage gating the next.

**Verbatim quotes:**
- > Twenty-three specialists and eight power tools, all slash commands, all Markdown, all free, MIT license.
- > The sprint structure is what makes parallelism work. Without a process, ten agents is chaos.
- > preamble-tier skills are loaded into context only when the user explicitly requests them, keeping the command surface small and preserving token budget for agent reasoning
- > NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.
- > 'Should work' or 'I'm confident' is not evidence. Fresh test output required if code changed post-Step 5.
- > Use gstack-version-bump classify deterministically—never hand-roll VERSION writes.
- > When an approved mockup exists, pixel-match it. Use real content from the mockup, never lorem ipsum.
- > self-contained with 30KB overhead, zero deps


---

## nextlevelbuilder/ui-ux-pro-max-skill

- **Verified:** True
- **Stars (as shown):** 97.1k stars (10.2k forks), per the live GitHub repo page on 2026-06-28. NOT the "204K" the user mentioned — that figure is inflated.

**What it is:** An MIT-licensed AI "design intelligence" skill that turns a UI/UX request into a full design system. Its core is NOT prose-in-prompt: it ships ~15 CSV "databases" (styles, colors, typography, products, ui-reasoning, ux-guidelines, landing, charts, icons, etc.) under src/ui-ux-pro-max/data/, queried at runtime by a Python BM25 + regex hybrid search engine (search.py / core.py). The agent runs the search script per domain, gets back 3 ranked rows, and assembles a design system from them — so the design knowledge lives on disk and only the relevant rows enter context. Installs via `npm i -g ui-ux-pro-max-cli` then `uipro init --ai <claude|cursor|windsurf|copilot>`; works as the `ui-ux-pro-max` slash command or auto-activates. Claims 67 UI styles, 161 color palettes, 57 font pairings, 161 industry reasoning rules, 99 UX guidelines, across 10 tech stacks.

**Workflow / methodology:** Four-step, search-driven: (1) Analyze requirements — extract product type, audience, style keywords, tech stack; (2) Generate design system (mandatory) via `--design-system` flag — runs five parallel searches (product-type match, style, color palette, landing pattern, typography pairing) and composes Pattern + Style + Colors + Typography + Effects + Anti-patterns + Pre-delivery checklist; (3) Supplement with domain-specific searches (product/style/color/typography/ux); (4) Apply stack-specific implementation guidelines. Persists output as a hierarchical design-system/MASTER.md (global source of truth) with per-page overrides in design-system/pages/[page].md, where page rules supersede master — a cascade so later component work re-reads the locked decisions instead of re-deriving them.

**Skills / commands it ships:**
- `ui-ux-pro-max (primary slash command / auto-activated skill)`
- `.claude/skills/design`
- `.claude/skills/design-system`
- `.claude/skills/ui-styling`
- `.claude/skills/brand`
- `.claude/skills/banner-design`
- `.claude/skills/slides`
- `CLI: `uipro init --ai <platform>``
- `search.py flags: --design-system, --domain <product|style|color|typography|landing|chart|ux|google-fonts|react|web|prompt>, --stack <framework>, --persist, --page, -n/--max-results (default 3), -f/--format, --json`

**Token-economy / verification / anti-mistake mechanisms:**
- Externalized knowledge base: design rules live in on-disk CSVs (styles.csv, colors.csv, ui-reasoning.csv, etc.) queried by a Python BM25+regex engine — only the top-N matching rows enter the prompt, not the whole corpus. This is the central token-economy move.
- Hard result cap: search.py defaults to MAX_RESULTS=3 and truncates each field to 300 chars in markdown output, bounding tokens per query.
- Progressive disclosure: SKILL.md is a thin router; the heavy data is fetched on demand via the script, and templates/base/quick-reference.md is loaded selectively rather than inlined.
- Severity-tagged, priority-ordered rule cascade (Priority 1 Accessibility CRITICAL → 5 Layout HIGH) so the most safety-critical gates can't be skipped; each ui-reasoning row also carries its own Severity column (HIGH).
- Pre-delivery verification gate / anti-pattern checklist run before handoff: contrast >=4.5:1, 44x44 touch targets, focus-visible, prefers-reduced-motion, safe-area, no-emoji-as-icons, dark-mode tested independently (not an inverse of light).
- Decision_Rules as machine-readable conditional logic: each industry rule stores a JSON branch (e.g. {"if_data_heavy":"add-glassmorphism"}) so the recommendation adapts to context instead of being a static blob.
- Persisted MASTER.md design system as durable shared memory — decisions are written once and re-read, avoiding re-derivation across many component generations.
- Symlink propagation of the single source-of-truth data into .claude/ / .factory/ / .shared/ so multiple host platforms read identical CSVs (no duplicated, drifting copies).

**Ideas worth adapting into Workbench:**
- Externalize the design/research knowledge into queryable CSV/JSONL 'databases' + a tiny BM25/regex search script, and have the skill SHELL OUT to it returning only top-3 rows. This is exactly the Workbench script-offloading + preview-not-dump principle applied to a knowledge corpus — adapt it so build-ui-component / design-ui-direction query a tokens/palettes/styles table on disk instead of carrying the catalog in SKILL.md. Keeps always-loaded context tiny while giving deep coverage.
- Hard-cap results (default n=3) and truncate each field to ~300 chars at the SCRIPT level, not by asking the model to be brief — makes token spend deterministic and matches the suite's mode-scaling-by-cardinality rule.
- A per-industry reasoning row schema: UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Key_Effects, Decision_Rules (JSON conditionals), Anti_Patterns, Severity. Adapt this exact column set for design-ui-direction so a course-platform vertical (e.g. coding-bootcamp vs finance-cert) yields grounded, non-generic tokens — directly serving frontend-aesthetics.md §2 'grounding before design'.
- Store color palettes as full SEMANTIC-TOKEN rows (Primary/On-Primary/Secondary/Accent/Background/Foreground/Card/Muted/Border/Destructive/Ring + Notes) with a Notes field that records WCAG adjustments, e.g. 'Accent adjusted from #F97316 for WCAG 3:1'. This gives build-ui-component a ready shadcn-shaped, contrast-verified token set and bakes the AA floor into the data itself.
- Machine-readable conditional Decision_Rules (JSON branches like {"if_data_heavy":"add-glassmorphism","must_have":"wcag-aaa-compliance"}) embedded per row, so recommendations branch on context rather than being static — a cheap way to make design-ui-direction adaptive without extra model reasoning.
- Persisted MASTER.md + per-page override cascade as durable design memory (page rules supersede master). Mirror this in notes/design-<slug>.md so every later component generation re-reads locked tokens instead of re-deriving them — saves tokens across a multi-component build and enforces consistency.
- A severity-coded, priority-ORDERED gate list (Accessibility=Priority1 CRITICAL down to Layout=Priority5) plus a concrete pre-delivery anti-pattern checklist (no emoji icons, 44x44 targets, focus-visible, prefers-reduced-motion, dark-mode tested independently, safe-area, no hardcoded hex). This is a ready-made scoring rubric for review-frontend's §8 slop-cluster pass — adopt the severity coding and the 'dark mode is NOT an inverse of light mode' check.
- Its anti-pattern data explicitly bans 'AI purple/pink gradients' for healthcare — same instinct as frontend-aesthetics.md §1 SaaS-purple ban. Worth encoding banned-default tokens per vertical as DATA, not prose, so the slop checklist is enforced at lookup time.
- Single source-of-truth data dir symlinked/synced to multiple host targets (.claude/.factory/.shared) — relevant if Workbench skills ever need to share one rules corpus across host platforms without drifting copies; aligns with the suite's 'cite the rules file, read at run time' pattern.

**Verbatim quotes:**
- > An AI SKILL that provide design intelligence for building professional UI/UX multiple platforms
- > Stars: 97.1k / Forks: 10.2k / License: MIT
- > 67 UI Styles ... 161 Color Palettes ... 57 Font Pairings ... 161 Industry-Specific Reasoning Rules
- > Search engine: Python scripts (search.py, core.py) implementing BM25 + regex hybrid matching
- > No,UI_Category,Recommended_Pattern,Style_Priority,Color_Mood,Typography_Mood,Key_Effects,Decision_Rules,Anti_Patterns,Severity
- > 8,Healthcare App,Social Proof-Focused,Neumorphism + Accessible & Ethical,Calm blue + Health green,...,Bright neon colors + Motion-heavy animations + AI purple/pink gradients,HIGH
- > No,Product Type,Primary,On Primary,Secondary,On Secondary,Accent,On Accent,Background,Foreground,Card,Card Foreground,Muted,Muted Foreground,Border,Destructive,On Destructive,Ring,Notes
- > Trust blue + orange CTA contrast [Accent adjusted from #F97316 for WCAG 3:1]
- > Results are capped using --max-results (default: 3) ... truncated values (capped at 300 characters per field)
- > Creates design-system/MASTER.md as the global source of truth ... Page rules supersede master rules when both exist
- > Priority 1 Accessibility CRITICAL Contrast >=4.5:1 ... Priority 4 Style Selection HIGH ... SVG icons (no emoji)
- > Dark mode designed as inverse of light mode (causes desaturation/legibility failure)


---

## Egonex-AI/Understand-Anything

- **Verified:** True
- **Stars (as shown):** 68.6k stars (5.7k forks) as shown on the GitHub landing page on 2026-06-28. NOT the "204K" the user cited — that number is inflated/unverified.

**What it is:** A multi-platform AI-coding plugin (Claude Code, Codex, Cursor, Copilot, Gemini CLI) that turns any codebase into an interactive, explorable knowledge graph. A 6-7 agent pipeline combines deterministic Tree-sitter static parsing with LLM summarization to build a typed node/edge graph (files, functions, classes, architectural layers, business domains), then serves it through a force-directed web dashboard with search, guided tours, diff-impact analysis, and a persona-adaptive UI. Tagline: "Graphs that teach > graphs that impress. Turn any code into an interactive knowledge graph you can explore, search, and ask questions about." MIT license, Yuxiang Lin / Infinite Universe, Inc. Stack: TypeScript ~71%, JS ~16%, Python ~9%, Astro ~2.5%.

**Workflow / methodology:** scan (project-scanner: discover files, detect languages/frameworks) -> analyze in parallel (file-analyzer: Tree-sitter extracts imports/defs/call-sites deterministically, LLM adds plain-English summaries/tags) -> architecture-analyzer assigns layers -> domain-analyzer extracts business domains/flows -> tour-builder generates dependency-ordered learning tours -> graph-reviewer validates completeness + referential integrity (inline by default, full LLM pass under --review) -> serve via dashboard (explore/search/chat/diff/onboard). Re-runs are incremental: only changed files re-analyzed. A separate wiki/article track uses article-analyzer + knowledge-graph-guide for Karpathy-pattern LLM wikis.

**Skills / commands it ships:**
- `/understand — scan whole codebase and build the knowledge graph`
- `/understand-dashboard — open the interactive web visualization`
- `/understand-chat [question] — ask questions about the codebase`
- `/understand-diff — analyze impact of current (uncommitted) changes`
- `/understand-explain [file/function] — deep-dive a specific file or function`
- `/understand-onboard — generate an onboarding guide for new team members`
- `/understand-domain — extract business domains, flows, and process steps`
- `/understand-knowledge [path] — analyze Karpathy-pattern LLM wikis/articles`
- `Command modifiers: --language [en|zh|zh-TW|ja|ko|ru], --auto-update (post-commit incremental hook), --review (full LLM graph validation)`

**Token-economy / verification / anti-mistake mechanisms:**
- Incremental-by-default re-analysis: only changed files are re-analyzed on subsequent runs, so the expensive full pass is paid once. Quote: 'The initial /understand analyzes your whole codebase and can consume a significant number of tokens on large projects' — subsequent runs are 'incremental by default — only changed files are re-analyzed.'
- Deterministic-first split: Tree-sitter extracts structural facts (imports, definitions, call sites) deterministically; the LLM only does what static analysis cannot (summaries, tags, layer assignment). This bounds LLM token use to interpretation, not fact-extraction.
- Pre-resolved importMap handed to file-analyzers so the LLM does not re-derive cross-file references (anti-mistake + token saver). Quote: file analyzers run with a 'pre-resolved importMap' to prevent re-derivation errors.
- Dedicated verification agent: graph-reviewer 'validates graph completeness and referential integrity,' running inline by default with an opt-in heavier --review full-LLM pass — a cheap-gate / expensive-gate tiering.
- Bounded parallelism: file analyzers run 'up to 5 concurrent, 20-30 files per batch' — caps fan-out instead of unbounded explosion.
- Progressive disclosure at the UI layer: persona-adaptive dashboard 'adjusts its detail level based on who you are — junior dev, PM, or power user.'
- Privacy/cost escape hatch: 'point your platform at a local model provider' for enterprise/privacy needs.

**Ideas worth adapting into Workbench:**
- Deterministic-extract / LLM-interpret split: have a bundled parser (Tree-sitter for code, an abstract/section parser for papers) produce the hard FACTS, and reserve the LLM strictly for summaries/tags/relations. This is exactly the token-economy spirit of the Workbench rules (§9 script-offloading) and would make knowledge-graph and paper-method cheaper and less hallucination-prone — the LLM never re-derives what a script can extract.
- A dedicated graph-reviewer verification agent as a separate gate, with a cheap inline pass + an opt-in --review full-LLM pass. The Workbench KG/synthesis skills could add a referential-integrity check (every triple's subject/object resolves to a real extracted entity; no dangling source-paper tags) as a final gate, tiered cheap-vs-thorough.
- Pre-resolved importMap pattern: build the cross-reference index ONCE deterministically and hand it to every per-item subagent so none of them re-derive it. Maps directly to Workbench's notes/INDEX.md shared-memory idea — pass the resolved id->path->gist map into every subagent's task spec so parallel workers never re-scan.
- Incremental-by-default with a stable cache keyed on changed inputs: only re-process what changed since the last run. The Workbench REUSE-BEFORE-READ rule (§4) is the manual version; this makes it automatic — a content-hash / mtime check that skips re-distilling an unchanged paper, and a --auto-update style hook.
- Bounded parallel batching (max 5 concurrent, 20-30 items/batch) as an explicit knob — gives the orchestrator a concrete fan-out cap and per-batch sizing instead of dispatching N subagents blindly; pairs well with the §7 mode-scaling-by-cardinality rule.
- Persona-adaptive output detail (junior dev / PM / power user) as a progressive-disclosure dimension: the same graph, different detail levels. Workbench could add a --persona (or reuse its Deep/Overview modes) so one distilled artifact renders at multiple altitudes without re-running analysis.
- Guided tours ordered by dependency: auto-generate a dependency-ordered reading/learning path through the graph. paper-synthesize or knowledge-graph could emit a 'suggested traversal order' over the master graph (read this paper before that one) instead of a flat triples table.
- Multi-target output via a --language modifier baked into the command, rather than a separate translate step — aligns with the bilingual policy and could let any Workbench artifact emit its human-facing prose in a chosen language in one pass.
- One graph that powers many lenses (explore / chat / diff-impact / onboard / domain) from a single build — mirrors building the master KG once and running compare/taxonomy/gaps lenses over it, amortizing the expensive extraction across many cheap downstream queries.
- Separate article-analyzer track for prose/wikis vs the code track — a clean precedent for keeping the research-paper extraction pipeline and the code-extraction pipeline distinct but sharing the same graph/dashboard substrate.

**Verbatim quotes:**
- > Graphs that teach > graphs that impress. Turn any code into an interactive knowledge graph you can explore, search, and ask questions about.
- > The initial /understand analyzes your whole codebase and can consume a significant number of tokens on large projects.
- > incremental by default — only changed files are re-analyzed
- > Tree-sitter parses source code deterministically to extract structural facts (imports, definitions, call sites), while LLMs read the parsed structure plus original source to produce plain-English summaries, tags, architectural layer assignments.
- > validates graph completeness and referential integrity
- > File analyzers run with a pre-resolved importMap to prevent re-derivation errors.
- > File analyzers run in parallel (up to 5 concurrent, 20–30 files per batch).
- > The dashboard adjusts its detail level based on who you are — junior dev, PM, or power user.
- > --review — Runs full LLM graph validation (graph-reviewer runs inline by default)


---

## addyosmani/agent-skills

- **Verified:** True
- **Stars (as shown):** 67.3k stars (7.3k forks) — NOT the ~204K the user cited; that number is inflated/false.

**What it is:** A collection of "production-grade engineering skills for AI coding agents," organized as a 6-phase software-development lifecycle. Each skill is a process (steps, checkpoints, exit criteria) the agent follows, not reference docs it reads. Shipped as Claude Code skills + slash commands, with parallel command dirs for Gemini/opencode. MIT licensed. Real, populated repo (verified across README, skills/, commands/, references/ and 4 individual SKILL.md files).

**Workflow / methodology:** A gated 6-phase lifecycle: Define (interview-me → idea-refine → spec-driven-development) → Plan (planning-and-task-breakdown) → Build (incremental-implementation + test-driven-development, one slice at a time) → Verify (browser-testing-with-devtools, debugging-and-error-recovery) → Review (code-review, simplification, security, performance) → Ship (git, CI/CD, docs/ADRs, observability, launch). Encoded mantra: "Spec before code → Small, atomic tasks → One slice at a time → Tests are proof → Improve code health → Faster is safer." Skills compose: a feature runs idea-refine → spec-driven-development → planning-and-task-breakdown → ...; a bug fix only needs debugging-and-error-recovery → test-driven-development → code-review-and-quality. Hard rule: "Do not advance to the next phase until the current one is validated."

**Skills / commands it ships:**
- `SLASH COMMANDS (commands/*.toml, 8): /spec, /plan (planning.toml), /build, /test, /review, /webperf, /code-simplify, /ship — plus a '/build auto' mode that plans+implements in one approved pass`
- `SKILLS (skills/ has 24 dirs = 22 lifecycle + using-agent-skills meta + the breakdown below). Define: interview-me, idea-refine, spec-driven-development`
- `Plan: planning-and-task-breakdown`
- `Build: incremental-implementation, test-driven-development, context-engineering, source-driven-development, doubt-driven-development, frontend-ui-engineering, api-and-interface-design`
- `Verify: browser-testing-with-devtools, debugging-and-error-recovery`
- `Review: code-review-and-quality, code-simplification, security-and-hardening, performance-optimization`
- `Ship: git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration, documentation-and-adrs, observability-and-instrumentation, shipping-and-launch`
- `Meta: using-agent-skills`
- `REFERENCES (references/*.md, loaded on demand): definition-of-done, testing-patterns, security-checklist, performance-checklist, accessibility-checklist, observability-checklist, orchestration-patterns`

**Token-economy / verification / anti-mistake mechanisms:**
- Progressive disclosure: 'The SKILL.md is the entry point. Supporting references load only when needed, keeping token usage minimal.' The using-agent-skills meta-skill is a discovery flowchart that routes to the right skill instead of loading all knowledge upfront.
- Per-skill anti-rationalization tables (Excuse | Reality) that pre-empt corner-cutting — e.g. TDD: '"I'll write tests after" → "You won't. Tests after-the-fact test implementation, not behavior."'
- Verification gates as explicit exit-criteria checklists per phase; spec phase cannot advance without 'The human has reviewed and approved the spec' + 'Success criteria are specific and testable'.
- Definition-of-done reference as a standing gate across Correctness/Quality/Integration/Documentation/Ship-readiness, with 'unverified work is not done' and 'Code runs and behaves as intended, verified at runtime, not just compiled.'
- doubt-driven-development: adversarial fresh-context review of non-trivial decisions with bounded stop-conditions (stop when next iteration is trivial, OR 3 cycles done → escalate to user, OR user approves) and 'Never silently skip cross-model review in interactive doubt cycles.'
- Bug-fix 'Prove-It' pattern: write a failing reproduction test BEFORE the fix (gate, not suggestion).

**Ideas worth adapting into Workbench:**
- Add an Excuse|Reality anti-rationalization table to each Workbench worker skill. e.g. paper-method: '"I read the abstract, that's enough" → the method section states the actual losses; reading-triage: '"This paper looks relevant, deep-read it" → score it first, spend full-reads only where they pay off.' This directly hardens §8 Fidelity against the model skipping the actual-source read.
- Ship a definition-of-done reference file per domain (research / code / web) that every worker cites in one line and reads at runtime — mirrors how Workbench already factors rules into satellite files, but adds an explicit runtime GATE ('artifact not done until X verified') rather than just style guidance.
- Adopt explicit phase exit-criteria checklists in workbench-orchestrator: do not dispatch the next worker until the current artifact passes a small checklist (e.g. notes/INDEX.md row written, glossary present, paths absolute). Encodes the orchestrator's gating as data, not prose.
- Port doubt-driven-development's bounded adversarial-review loop into a research 'doubt' mode: subject a cross-source synthesis claim to a fresh-context re-check, with the SAME stop-conditions (trivial findings OR 3 cycles → escalate OR user approves) to avoid infinite loops — fits paper-synthesize's cross-source-assumption risk and audit-log's materiality model.
- Mirror their command/skill split: thin .toml slash commands (verbs: /spec /plan /build /test /review /ship) that route into heavier SKILL.md processes. Workbench could expose verb-style entry commands (/triage, /read, /method, /synthesize, /scaffold) over the existing skills for faster invocation.
- Use their 'Process, not prose' framing as an authoring test for Workbench SKILL.md files: each must contain steps + checkpoints + exit criteria, not just reference knowledge — a concrete authoring quality bar to add to workbench-conventions §11.
- Steal the 'Prove-It' gate for run-on-modal / paper-to-notebook reproduce mode: before claiming a reproduction works, require a runtime artifact (eval numbers vs paper's reported numbers) — 'verified at runtime, not just compiled' applied to ML repro.
- Add a 'surface assumptions immediately' step (from spec-driven-development) to workbench-orchestrator's clarify phase: list assumptions before writing the per-worker task spec, inviting one correction pass — cheaper than re-running subagents.

**Verbatim quotes:**
- > Skills encode the workflows, quality gates, and best practices that senior engineers use when building software.
- > Process, not prose. ... workflows agents follow, not reference docs they read.
- > Verification is non-negotiable. ... Tests are proof — 'seems right' is not done.
- > "I'll write tests after" → "You won't. Tests after-the-fact test implementation, not behavior."
- > "I'm confident, skip doubt" → "Confidence correlates poorly with correctness on novel problems. Moments of certainty hide blind spots."
- > "I'll doubt at the end with /review" → "/review is a final gate. Doubt-driven catches wrong directions early when course-correction is cheap."
- > Code runs and behaves as intended, verified at runtime, not just compiled ... unverified work is not done.
- > Do not advance to the next phase until the current one is validated.
- > The SKILL.md is the entry point. Supporting references load only when needed, keeping token usage minimal.
- > Stop looping when: Next iteration returns only trivial findings, or 3 cycles completed (escalate to user), or User explicitly approves ... Never silently skip cross-model review in interactive doubt cycles.


---

## Leonxlnx/taste-skill (https://github.com/Leonxlnx/taste-skill)

- **Verified:** True
- **Stars (as shown):** ~52,000 stars (52k shown on the repo page; 3.6k forks). NOT the "204K" the user cited — the inflated figure is wrong.

**What it is:** A portable "anti-slop" frontend design skill suite for AI coding agents (Claude Code, Cursor, ChatGPT/Codex). It ships a set of SKILL.md files that inject professional layout, typography, motion, color, and spacing discipline into agent-generated UI so the output stops looking like generic LLM "slop." The flagship skill (design-taste-frontend) drives output with three tunable 1-10 "dials" (VARIANCE / MOTION / DENSITY) inferred from the brief, plus a large catalog of hard bans and a final mechanical pre-flight checklist. Install via `npx skills add https://github.com/Leonxlnx/taste-skill`. MIT licensed.

**Workflow / methodology:** A 5-phase design-first agent workflow encoded as numbered sections read top-to-bottom: (0) Brief inference — read page kind / vibe / audience / brand / constraints and emit a one-line "design read" BEFORE writing code; (1) Dial configuration — set DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY (each 1-10) from a signal->dial inference table; (2) Design-system selection — pick an official system (Material/Fluent/Carbon/Primer/shadcn/etc.) when the brief matches one, else Tailwind+Motion, never mix; (3) Build & guardrails — apply architecture + typography/color/layout/motion discipline and avoid an explicit list of "AI tells"; (14) Pre-Flight Check — a ~45-54 point mechanical checklist that must ALL pass ("If a single checkbox cannot be honestly ticked, the page is not done").

**Skills / commands it ships:**
- `design-taste-frontend (taste-skill, the flagship v2)`
- `design-taste-frontend-v1 (taste-skill-v1, legacy)`
- `gpt-taste (gpt-tasteskill, stricter GPT/Codex variant)`
- `image-to-code (image-to-code-skill, image-first pipeline)`
- `redesign-existing-projects (redesign-skill, audit & improve existing UI)`
- `high-end-visual-design (soft-skill, premium/calm)`
- `full-output-enforcement (output-skill, forces complete output)`
- `minimalist-ui (minimalist-skill, Notion/Linear editorial)`
- `industrial-brutalist-ui (brutalist-skill, Swiss/mechanical)`
- `stitch-design-taste (stitch-skill, Google Stitch-compatible)`
- `imagegen-frontend-web`
- `imagegen-frontend-mobile`
- `brandkit`

**Token-economy / verification / anti-mistake mechanisms:**
- Progressive disclosure by read-frequency: sections layered so 0-2 (brief/dials/systems) are read first, 3 at build setup, 4-5 consulted mid-build per-problem, 6-10 on-demand, 11-12 only when redesign mode is detected, 13-14 as final gates — i.e. load rules only when context demands them
- A final mechanical 'Pre-Flight Check' (Section 14, ~45-54 boxes) acting as a hard verification gate before output is considered done
- Many rules are framed as binary 'Pre-Flight Fail' conditions (e.g. 3rd consecutive zigzag section, wrapped desktop CTA, duplicate CTA intent, any visible em-dash) — a self-audit gate the agent must check against rather than vibes
- Anti-mistake hard bans of known LLM failure patterns: em-dash absolute ban (Section 9.G, 'the #1 visual Tell'), banned scroll listeners (window.addEventListener('scroll')), banned fake div-based screenshots, banned default fonts (Inter) and a banned beige+brass 'premium' palette with a rotation rule
- NO explicit token-economy / no-re-read mechanism: README and SKILL.md document none; the doc 'assumes the agent reads top-to-bottom once, then uses section references as lookup anchors' — progressive disclosure is by document structure only, not enforced budgeting

**Ideas worth adapting into Workbench:**
- Adopt the 1-10 'dial' abstraction (VARIANCE / MOTION / DENSITY) inferred from brief signals via a lookup table — a compact, decisive way to encode 'one decisive direction' that maps cleanly onto Workbench's frontend-aesthetics.md goal of escaping the high-probability center. Workbench's build-ui-component / design-ui-direction could expose 2-3 such dials with a signal->value inference table instead of prose.
- Encode bans as binary 'Pre-Flight Fail' conditions, not soft advice. Workbench's review-frontend §8 slop checklist could become a mechanical pass/fail gate where any unticked box blocks 'done' — mirrors taste-skill's 'If a single checkbox cannot be honestly ticked, the page is not done.'
- Mechanical, COUNTABLE layout rules that an agent can self-verify without judgment: zigzag-alternation cap (max 2 consecutive image+text splits), layout-family at-most-once-per-page, max 1 eyebrow per 3 sections, bento cells == content count, nav single-line + 64-80px height cap, hero must fit viewport with pt-24 max. These are far more enforceable than 'add rhythm/asymmetry.'
- A rotation/anti-repetition rule across projects ('if the previous premium-consumer project used beige+brass, this one MUST use a different family') — directly addresses the slop-cluster problem in frontend-aesthetics.md §1 by making the model avoid its OWN prior default, not just a static blocklist.
- Concrete typography micro-rules worth porting verbatim: ban Inter as default and prefer Geist/Outfit/Cabinet Grotesk/Satoshi; emphasize with italic/bold of the SAME font (never inject a random serif word into a sans headline); italic-descender clearance (leading-[1.1] + pb-1 for y/g/j/p/q). frontend-aesthetics.md §3 currently only mandates weight/size contrast — these add specificity.
- Motion-must-be-motivated gate: before any animation, require a named reason (hierarchy / storytelling / feedback / state transition) and ban 'it looked cool'; marquee max-once-per-page; only animate transform+opacity; reduced-motion mandatory above MOTION>3. Tighter than frontend-aesthetics.md §5's general guidance and trivially checkable.
- Progressive-disclosure-by-section pattern for the SKILL bodies themselves: order rules by read-frequency and gate redesign-only sections behind a 'redesign mode detected' trigger, so the agent only pulls heavy rule blocks when context demands — aligns with workbench-conventions.md §3/§11 token-economy goals (note: taste-skill does this by document structure, NOT a real no-re-read mechanism, so Workbench's references/-one-level-deep approach is actually stronger and worth keeping).
- Design-system honesty rule: when a brief matches an established system (enterprise->Fluent, IBM->Carbon, GitHub->Primer, SaaS->shadcn) install the official package rather than hand-rolling its CSS, and never mix systems. A cheap correctness + token win for scaffold-course-platform / build-ui-component.
- An explicit 'AI Tells to avoid' enumerated blocklist (neon glows, pure #000, gradient-text headers, three equal feature cards, 'John Doe'/'Acme' placeholder names, fake-perfect 99.99% numbers, hand-rolled SVG icons, 'Scroll' cues, version labels in hero). frontend-aesthetics.md §1 has a checklist but this list is more concrete and copy lifts directly into review-frontend.
- Image-asset strategy as a ranked fallback with a hard ban on the failure mode: real generated/stock images first, placeholder slots if not, but NEVER fake div-rectangle 'product previews' or hand-rolled SVG dashboards ('A pure-text page is not minimalism. It is incomplete work.'). Useful guardrail for any Workbench skill that emits a landing page.

**Verbatim quotes:**
- > Taste-Skill - gives your AI good taste. stops the AI from generating boring, generic slop
- > The Anti-Slop Frontend Framework for AI Agents
- > Em-dash (—) is COMPLETELY banned. It is the LLM's signature stylistic crutch and it is the #1 visual Tell in production tests. There is no 'limited use' allowance.
- > If your output contains a single — or – anywhere visible to the user, the output fails the Pre-Flight Check and must be rewritten. This rule is non-negotiable
- > Default Inter is discouraged. Pick Geist, Outfit, Cabinet Grotesk, Satoshi
- > use italic or bold of the SAME font. Do NOT inject a random serif word into a sans headline
- > Once an accent color is chosen for a page, it is used on the WHOLE page. Pick one accent, lock it, audit every component
- > This palette is BANNED as the default reach for premium-consumer briefs. Every premium-consumer site uses this exact palette
- > ZIGZAG ALTERNATION CAP: Max 2 sections in a row with image+text-split pattern. The 3rd consecutive is a Pre-Flight Fail
- > Before adding any animation, ask: 'what does this animate communicate?' Valid answers: hierarchy, storytelling, feedback, state transition. Invalid: 'it looked cool'
- > DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos); MOTION_INTENSITY: 6 (1=Static, 10=Cinematic); VISUAL_DENSITY: 4 (1=Art Gallery, 10=Cockpit)
- > If a single checkbox cannot be honestly ticked, the page is not done
- > Before touching code or tweaking dials, infer what the user actually wants. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.
- > A pure-text page is not minimalism. It is incomplete work. Even minimalist sites need real images


---

## Token-economy best practices (web research)

**Principles:**
- Progressive disclosure / three-tier loading: keep only YAML name+description always-loaded (~100 tokens/skill, max 1024 chars description); SKILL.md body (Level 2) loads only when triggered (target <5k tokens); reference files + scripts (Level 3) load only when read/executed (effectively unlimited, zero cost until accessed). [overview]
- Keep SKILL.md body under 500 lines; split into separate files when approaching the limit. [best-practices: Token budgets]
- Concise-is-key: the context window is a public good; add only what Claude doesn't already know ('does this paragraph justify its token cost?'). Anthropic's good PDF example is ~50 tokens vs ~150 for the verbose one. [best-practices: Concise is key]
- SKILL.md is a table of contents pointing to detail; keep references ONE level deep (deep nesting triggers partial `head -100` previews and incomplete reads). [best-practices: Avoid deeply nested references]
- Domain-partition reference files (finance.md / sales.md...) so a task loads only its slice; add a table-of-contents to any reference file >100 lines so partial reads still see full scope. [best-practices: Pattern 2 + Structure longer reference files]
- Script-offloading: prefer bundled deterministic scripts over prose/code-gen — script code never enters context, only its output costs tokens ('sorting via token generation is far more expensive than running a sort'); scripts are also more reliable and consistent. State whether Claude should EXECUTE vs read-as-reference. [overview: Efficient script execution + best-practices: Provide utility scripts]
- Description in third person, stating both WHAT it does and WHEN to use it with concrete trigger terms — Claude selects among 100+ skills from the description alone. [best-practices: Writing effective descriptions]
- Scope tools via the skill's allowed-tools frontmatter; avoid bloated/overlapping tool sets ('if engineers can't pick the tool, neither can the model') and consolidate (one schedule_event beats list_users+list_events+create_event). [tools-reference frontmatter + writing-tools-for-agents]
- Match degrees of freedom to task fragility: high-freedom prose for open tasks; low-freedom exact scripts ('Run exactly this... do not add flags') for fragile/destructive ones. [best-practices: Set appropriate degrees of freedom]
- Just-in-time context: hold lightweight identifiers (file paths, stored queries, links) and load data at runtime instead of pre-loading; compact long sessions by summarizing and discarding redundant tool outputs. [effective-context-engineering]
- Cap tool-response size (Claude Code defaults to 25,000 tokens; Bash output 30,000 chars) via pagination/filtering/truncation with sane defaults, offer concise-vs-detailed modes, and make truncation/error text steer toward token-cheap strategies (many small targeted searches over one broad one). [writing-tools-for-agents + tools-reference]
- Find the smallest set of high-signal tokens; pitch instructions at the right altitude (specific enough to guide, flexible enough to leave heuristics) and teach via a few canonical examples, not exhaustive rules. [effective-context-engineering]
- Hygiene: no time-sensitive content (use an 'old patterns' <details> block), consistent terminology, one default + escape hatch instead of many options, forward-slash paths only. [best-practices: content guidelines / anti-patterns]
- Evaluation-driven, iterative authoring: build 3 evals from observed gaps BEFORE writing docs, write minimal instructions to pass them, test on Haiku/Sonnet/Opus, refine via a Claude-A-authors / Claude-B-uses loop while watching real navigation. [best-practices: Evaluation and iteration]
- Subagent isolation for token economy: spawn a subagent (own context window) for heavy exploration — the parent sees only the final distilled result, not intermediate tool calls; cap work with maxTurns. [tools-reference: Agent tool behavior]

**Clarify-before-acting (ask the right questions, don't guess):** Resolve the target to something concrete first, then ask once only when guessing would create rework. Anthropic exposes the AskUserQuestion tool specifically to 'gather requirements or clarify ambiguity' [tools-reference], and plan mode shifts Claude from assumption-making to confirmation-seeking. The token-cheap, high-signal pattern (neonwatty / Claude Code docs) is Read -> Identify the single blocking decision -> Ask -> Explain tradeoffs -> Proceed: (1) gather enough context FIRST ('if the skill asks before reading the repo, it asks lazy questions'); (2) ask only about scope, risk, or intent — never details the agent can infer or the codebase can answer; (3) compress the real decision into 2-3 strong, mutually-exclusive multiple-choice options with each option's tradeoff spelled out, rather than open-ended or generic questions; (4) for feature work, targeted rounds surface hidden assumptions, edge cases, user roles/permission boundaries, data-lifecycle, and failure modes BEFORE implementation instead of mid-sprint; (5) never silently guess, but also don't turn focused work into a survey — skip the question when the answer is cheaply discoverable. This stays token-cheap because one structured multiple-choice question costs far less than rebuilding the wrong thing. (Matches the user's own workbench-conventions §2: resolve to a concrete target first, and if genuinely ambiguous 'ask once (list the candidates), then proceed; never guess silently.')

**Anti-runaway-edit (small fix must not become full rewrite):** Claude Code's edit contract structurally prevents small edits from becoming full rewrites or breaking unrelated code [tools-reference: Edit tool behavior]. Mechanisms: (1) Prefer Edit over Write for existing files — docs state explicitly 'For partial changes to an existing file, Claude uses Edit instead of Write'; Write creates/OVERWRITES the whole file (no append/merge), so it is reserved for new files or deliberate full replacement. (2) Read-before-edit STALENESS check: Claude must have read the file in the current conversation AND the file must not have changed on disk since that read — this runs first, before any string matching, so an edit against a stale view fails rather than clobbering concurrent changes (Write enforces the same read-first rule for existing paths). (3) Exact-match: old_string must match byte-for-byte including whitespace/indentation (no regex/fuzzy), so a too-broad pattern simply fails instead of silently matching the wrong region. (4) Uniqueness: old_string must appear exactly once — if it appears more than once Claude must add surrounding context to pin the single occurrence or set replace_all:true deliberately, preventing accidental edits to unrelated identical lines. (5) Minimal-diff discipline: the guidance to keep old_string minimal-but-unique plus the colorized diffs-first workflow keeps each change surgical, reviewable, and easy to revert. (6) Verification gates AFTER the edit: the LSP tool 'after each file edit automatically reports type errors and warnings so Claude can fix issues without a separate build step', and skills should bundle a validate -> fix -> repeat feedback loop (plan-validate-execute with a verifiable intermediate file, e.g. changes.json validated before applying) plus a test/lint run, so a broken edit is caught immediately rather than shipped. For non-file/whole-region edits, NotebookEdit targets a single cell by cell_id rather than string-replacing across the notebook, the same minimal-blast-radius principle.

**Sources:**
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://code.claude.com/docs/en/tools-reference
- https://github.com/anthropics/skills
- https://neonwatty.com/posts/askuserquestion-claude-code-skill/
