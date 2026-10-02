# Antigravity Evidence-First Admin — Design

> Status: approved in conversation; implementation specification
> Date: 2026-10-02
> Target: GOBAL AGENT repository and Antigravity IDE

## 1. Problem

The repository currently distributes Claude-oriented skills under `.claude/skills/`.
Its `admin` and `hallucination-guard` instructions state that claims must be honest and
sourced, but they do not enforce a claim-to-evidence workflow. A model can therefore:

- confuse Claude Code, Gemini CLI, and Antigravity IDE paths or capabilities;
- treat a created file as proof that a skill was registered and activated;
- attach a real URL to a claim that the cited passage does not support;
- count copied or syndicated pages as independent corroboration;
- smooth missing or conflicting evidence into an unjustified conclusion;
- report completion after a static edit without checking product behaviour.

The repository also lacks a native Antigravity plugin, Windows-first install/update
instructions, strict YAML validation, and a regression suite for evidence-grounded
research behaviour.

## 2. Goals

1. Make the repository directly installable as a native Antigravity plugin.
2. Make `/admin` evidence-first for factual, current, disputed, and high-risk requests.
3. Keep creative, transformative, and local-file tasks fast; do not force web research
   where external evidence cannot improve the result.
4. Require claim-level provenance for material factual claims.
5. Distinguish source identity, source quality, claim support, corroboration, and answer
   calibration instead of treating “has a URL” as verification.
6. Preserve Claude compatibility while preventing the Claude and Antigravity
   distributions from drifting.
7. Provide structural validators, behavioural regression fixtures, and a real IDE smoke
   test before claiming that installation works.

## 3. Non-goals

- Guarantee that a language model can never hallucinate.
- Bundle a paid search provider or require API keys for the base installation.
- Copy the full STORM, PaperQA2, GPT Researcher, or Microsoft Agent Framework runtime.
- Turn every `/admin` request into a long multi-agent research job.
- Rank sources by country. Jurisdiction and fitness for the claim matter more than
  whether a source is Vietnamese or international.
- Treat a model-based evaluator as sole proof of correctness.

## 4. Selected approach

Use a hybrid, dependency-light architecture:

1. A short Antigravity `always_on` rule enforces universal epistemic invariants.
2. `/admin` remains the entry point and selects a bounded evidence lane by task risk.
3. Detailed research instructions live in on-demand references, not the always-on rule.
4. Research state is represented by a task contract, fact ledger, source cards,
   claim-evidence ledger, and progress ledger.
5. A deterministic validator checks structure and provenance completeness.
6. Semantic entailment remains an explicit review step; it is never claimed as proven
   merely because a URL resolves.
7. Antigravity artifacts are deterministically generated from the Claude-oriented
   canonical source and committed with a drift check.

This approach borrows mechanisms rather than framework dependencies:

- STORM: perspective-guided question planning and evidence-first outlining.
- SAFE/FActScore: atomic factual claim decomposition.
- ALCE: citation correctness and citation completeness as separate checks.
- PaperQA2: claim-to-passage provenance and evidence reranking.
- Microsoft Magentic orchestration: fact/progress ledgers and stall-aware replanning.
- DeepResearch Bench: coverage, depth, instruction-following, readability, and citation
  support as separate evaluation dimensions.

## 5. Repository architecture

```text
gobal-agent-skills/
├── plugin.json                         # Antigravity plugin marker
├── config/
│   ├── antigravity-skills.txt          # exact canonical name inventory
│   └── antigravity-compatibility.yml   # explicit host path/tool mappings
├── skills/                             # generated Antigravity-native skill tree
├── rules/
│   └── evidence-first.md               # short always_on invariant
├── scripts/
│   ├── build_antigravity.py            # deterministic generator/checker
│   ├── install-antigravity.ps1          # safe Windows install/update helper
│   └── validate_evidence.py             # ledger structural validator
├── pilot/                              # generated, namespaced, non-production canary
│   ├── skills/admin-evidence-pilot/
│   ├── rules/admin-evidence-pilot.md
│   └── manifest.json                   # exact file hashes
├── docs/
│   └── ANTIGRAVITY.md                  # install, update, verify, troubleshoot
├── evals/
│   └── admin-research/
│       ├── cases.yml                    # behavioural regression cases
│       └── rubric.md                    # human + model-assisted scoring rubric
├── notes/
│   ├── INDEX.md
│   └── design-antigravity-evidence-first.md
└── .claude/
    ├── rules/                           # canonical shared rules
    └── skills/                          # canonical skills
        └── admin/
            ├── SKILL.md
            ├── references/
            │   ├── dispatch-protocol.md
            │   ├── research-protocol.md
            │   ├── source-quality.md
            │   └── claim-ledger.md
            └── resources/
                └── claim-ledger.example.yml
```

### 5.1 Single source of truth

`.claude/skills/` remains canonical in this change to avoid breaking existing users.
`scripts/build_antigravity.py` generates root `skills/` by:

1. discovering every canonical skill directory;
2. strictly parsing frontmatter;
3. emitting only Antigravity-supported manifest fields (`name`, `description`);
4. quoting YAML scalars deterministically;
5. copying scripts, references, resources, and examples;
6. translating known host-specific paths only through explicit mappings;
7. rejecting unresolved `~/.claude/` runtime dependencies in generated output;
8. vendoring any runtime helper needed by an installed skill;
9. normalizing generated text to LF while preserving binary bytes;
10. matching an exact committed skill/file inventory and rejecting orphan output;
11. comparing generated output with the committed tree in `--check` mode.

Unknown host-specific references fail the build. They are never replaced by a blind
global string substitution.

### 5.2 Plugin layout

The repository root is the plugin root. `plugin.json` contains only fields supported by
the official schema. No empty `mcp_config.json` is created. An MCP configuration is added
only if a real, tested MCP server is introduced later.

The native install paths are:

- global plugin: `~/.gemini/config/plugins/gobal-agent-skills/`;
- workspace plugin: `<workspace>/.agents/plugins/gobal-agent-skills/`;
- direct skill fallback: `~/.gemini/config/skills/<skill-name>/`.

The preferred installation is the plugin because it packages skills and behavioural
rules as one versioned unit.

## 6. Runtime architecture

```text
User request
    │
    ▼
Task contract and risk classification
    │
    ├── Transform/create/local evidence only ──► existing fast path
    │
    ├── Low-risk factual ──────────────────────► quick evidence lane
    │
    ├── Current/disputed/multi-facet ──────────► standard evidence lane
    │
    └── High-risk/exhaustive ──────────────────► deep evidence lane
                                                   │
                                                   ▼
Fact ledger → facet plan → source discovery → full-source reading
                                                   │
                                                   ▼
Source cards → claim-evidence ledger → contradiction/gap loop
                                                   │
                                                   ▼
Evidence-bound outline → synthesis → citation/completion audit
```

### 6.1 Universal evidence-first rule

The `always_on` rule is deliberately short. It enforces:

- resolve outcome, target product/runtime, constraints, and observable completion;
- treat Claude Code, Gemini CLI, Antigravity IDE, `.claude`, `.gemini`, and
  `.antigravity-ide` as different systems until evidence proves a relationship;
- keep claims as observed, inferred, or unknown;
- a created/copied file is not proof of registration, indexing, activation, or runtime
  behaviour;
- user counter-evidence immediately invalidates the contradicted explanation;
- completion reports separate changed, verified, unverified, and blocked facts.

Detailed research procedure is not duplicated in the always-on rule because Antigravity
injects always-on rules on every turn and enforces a shared token budget.

### 6.2 Task contract

Before factual research, `/admin` records:

- requested outcome and deliverable;
- target product, entity, population, jurisdiction, and time scope;
- constraints and exclusions;
- freshness requirement;
- evidence standard and risk tier;
- observable acceptance criteria;
- search and iteration budget.

One concise clarification is asked only when competing interpretations would materially
change the action. Otherwise `/admin` proceeds with explicit assumptions.

### 6.3 Evidence lanes

#### Fast non-research lane

Use for rewriting, brainstorming, translation, local-file transformation, and other work
where external factual research is not part of the requested outcome. The honesty and
completion invariants still apply.

#### Quick evidence lane

Use for a narrow, low-risk fact. Open the strongest available primary source, read the
relevant passage, cite it adjacent to the claim, and mark any unresolved uncertainty.
One authoritative primary source may be sufficient for an exact specification or an
official first-party statement.

#### Standard evidence lane

Use for current, comparative, recommendation, disputed, or multi-facet questions.
Create 2–6 facets, search primary and counter-evidence queries, deduplicate source
origins, and maintain a compact claim ledger.

#### Deep evidence lane

Use for exhaustive requests or high-impact decisions. Independent facets may run in
parallel, but synthesis waits for all evidence manifests. Persist the full ledger and
run the complete audit. Medical, legal, financial, and safety conclusions require
strong sources, explicit limitations, and a human-review recommendation.

### 6.4 Runtime cost and latency policy

Regression suites, build validation, and product smoke tests are release-time gates. They
do not run on every `/admin` request. Runtime work is bounded by evidence lane:

| Lane | Default search budget | Parallelism | Ledger persistence | Runtime audit |
|---|---|---:|---|---|
| Fast non-research | no web search | none | none | completion invariants only |
| Quick evidence | one batched search; open one or two strongest sources | none | in-context mini-ledger | direct support check |
| Standard evidence | up to two search rounds; open only sources needed for material claims | none by default | compact ledger; save only when reuse is valuable | support, quality, and targeted counter-evidence |
| Deep evidence | up to three research rounds | at most three independent workers | persisted full ledger | all verification gates |

These are operation ceilings, not wall-clock promises. Network, source accessibility, and
model latency are variable. `/admin` minimizes cost by:

- batching searches and source opens;
- auditing only material factual claims, not connective prose;
- accepting one authoritative primary source for an exact low-risk specification;
- requiring independent corroboration only when claim risk, volatility, or dispute
  justifies it;
- reusing fresh source cards and project artifacts;
- passing compact evidence manifests rather than raw pages to the coordinator;
- stopping as soon as the acceptance criteria and evidence gates pass.

`/admin nhanh` never dispatches subagents. A high-risk request that cannot be responsibly
resolved inside the quick budget returns a provisional answer with explicit limitations
or asks the user to allow the deeper lane; it does not manufacture certainty.

## 7. Research flow

### 7.1 Fact ledger

Before searching, classify known information:

- `VERIFIED_OR_GIVEN`: directly observed or supplied by the user;
- `LOOKUP`: externally verifiable fact that requires a source;
- `DERIVE`: conclusion that must show its supporting claims;
- `ASSUMPTION_OR_UNKNOWN`: not yet supported.

### 7.2 Facet and query plan

- Simple question: one facet.
- Complex question: 2–6 non-overlapping facets.
- Disputed question: at least one counter-evidence facet.
- Vietnam-specific question: query authoritative Vietnamese sources; add international
  sources for comparison when useful, not as a substitute for Vietnamese jurisdiction.
- Search snippets discover URLs only. They are not evidence.
- A source can support a claim only after the relevant full page, document section, or
  repository file has been opened and inspected.

### 7.3 Source cards

Every source used for a material claim records:

```yaml
source_id: SRC-001
canonical_url: https://example.org/document
title: Exact source title
author_or_org: Accountable author or publisher
published_at: 2026-09-01
accessed_at: 2026-10-02T12:00:00+07:00
source_type: official_docs
primary_for: product specification
origin_id: ORIGIN-001
version: v2.1
current_status: current
locator: Section 3.2
stance: support
limitations: First-party source; not independent evidence of product quality
```

For high-risk or volatile web evidence, additionally store a content hash and an archive
URL when legally and technically appropriate.

### 7.4 Claim ledger

Material factual claims are atomic and scoped:

```yaml
claim_id: CLM-001
text_atomic: Antigravity IDE discovers global skills from the configured skill folder.
claim_type: product_configuration
scope:
  entity: Antigravity IDE
  time: 2026-10-02
  jurisdiction: global
risk: medium
volatility: periodic
status: SUPPORTED
confidence: high
evidence:
  - source_id: SRC-001
    locator: Antigravity IDE skill locations
    stance: support
    entailment: direct
quality:
  directness: primary
  authority: official
  currency: current
  independence: first_party
  contextual_fit: exact_product
fatal_flags: []
conflicts: []
derived_from_claim_ids: []
decision_rationale: Official current product documentation states the location.
```

Allowed status values:

- `SUPPORTED`: available evidence supports the atomic claim;
- `REFUTED`: available evidence contradicts it;
- `CONTESTED`: credible evidence disagrees;
- `NEI`: not enough information.

`NEI` is not treated as false. `CONTESTED` is not resolved by counting URLs.

### 7.5 Source quality

Source quality and claim entailment are independent checks. A high-quality source can be
misquoted, and a biased first-party source can still be authoritative for its own
published configuration.

Evaluate each source on:

1. directness and primary-source fit;
2. authority and accountability;
3. method and traceability;
4. currency, version, correction, and retraction state;
5. independence and conflicts of interest;
6. contextual fit: product version, jurisdiction, population, language, and time.

Hard failures override any aggregate judgement:

- fabricated or unresolvable reference;
- cited passage does not entail the claim;
- retracted evidence used as current support;
- wrong product, version, jurisdiction, population, or time scope;
- no identifiable upstream source.

Source counts use `origin_id`. Multiple pages copied from one press release count as one
origin family.

### 7.6 Progress and stop loop

After each research round, `/admin` answers:

1. Is the request satisfied?
2. Which material claims are still `NEI` or `CONTESTED`?
3. Did the round add new evidence?
4. Are queries or source origins repeating?
5. What is the smallest next action that could resolve a gap?

Default maximums are three research rounds and three parallel workers. Stop earlier when
all material claims pass or two consecutive rounds add no material evidence. On a stall,
re-plan once; then report the unresolved gap instead of manufacturing closure.

### 7.7 Evidence-bound synthesis

- Build the outline from verified claims, not from a model-memory draft.
- Writers may not introduce new material factual claims outside the ledger.
- Synthesize across claims and disagreements; do not concatenate source summaries.
- Lead with the answer, then explain evidence, trade-offs, conflicts, and limitations in
  language appropriate to the user.
- Place citations next to the claim they support.
- Clearly label deductions and unknowns.

## 8. Verification gates

1. **Atomicity:** every material claim is independently testable and scoped.
2. **Identity:** URL/DOI/file resolves to the stated title, author, and version.
3. **Entailment:** the cited passage supports the exact claim.
4. **Quality floor:** no hard failure; source quality matches claim risk.
5. **Independence:** corroboration counts origin families, not URLs.
6. **Counter-evidence:** disputed/high-risk claims include a falsification search.
7. **Coverage:** every material factual claim has evidence or an explicit non-supported
   status.
8. **Calibration:** wording confidence does not exceed evidence status.
9. **Completion:** installation and code claims require fresh command output and, where
   applicable, product-level behaviour verification.

## 9. Failure behaviour

- Inaccessible source: mark it unverified; find an authoritative alternative; do not
  cite a search snippet as a replacement.
- Paywall: use accessible metadata for identity only; do not claim body support without
  access to the relevant passage.
- Source conflict: preserve both evidence paths and mark `CONTESTED` until scope,
  definitions, or authority resolve the difference.
- Unsupported claim: remove, weaken, or label `NEI`; never add a decorative citation.
- Tool or model failure: quote the exact error and preserve partial verified results.
- User counter-evidence: retract the contradicted claim and restart from the affected
  ledger node.
- Product configuration: static validation can pass while runtime discovery fails; report
  these as separate states.

## 10. Installer and update behaviour

`install-antigravity.ps1` is deliberately limited to the Direct/Global topology used for
the local rollout. Native plugin installation remains Antigravity's own
`/plugin install <local-path>` workflow. The script must:

- resolve paths from its own location or explicit parameters;
- support a safe global direct install and a separately namespaced pilot install;
- validate the source plugin before copying or cloning;
- preserve unrelated user skills, plugins, rules, and MCP configuration;
- refuse unmanaged collisions unless `-Force` is explicitly passed;
- back up overwritten managed files when forced;
- stage and hash-validate the complete update before swapping managed paths;
- automatically restore the previous tree after any mid-update failure;
- record installed content hashes in the ownership manifest;
- refuse to overwrite or delete user-modified managed files unless `-Force` first backs
  them up;
- reject reparse-point/junction escapes from the resolved profile root;
- never delete the entire `skills`, `plugins`, or `rules` directory;
- print the installed path, component counts, reload step, and smoke-test commands;
- return a non-zero exit code on validation or copy failure.

Update is a transactional, manifest-aware file operation. It does not reset local changes.
Uninstall removes only paths recorded in the ownership manifest whose current hash still
matches the installed hash; drifted files are preserved unless explicitly forced and backed up.

## 11. Validation and testing

### 11.1 Static validation

- Strictly parse every canonical and generated `SKILL.md` frontmatter.
- Confirm directory name and `name` match and descriptions meet Antigravity limits.
- Parse `plugin.json` and every Antigravity rule frontmatter.
- Confirm canonical/generated exact-name and exact-file inventory parity.
- Confirm all referenced bundled resources and scripts exist.
- Reject unresolved host-specific paths in the generated tree.
- Run the generator twice and require byte-identical output with no stale/orphan files.
- Run clean-checkout gates on Windows and Linux under the repository EOL policy.
- Run `build_antigravity.py --check` in CI to detect drift.

### 11.2 Evidence validator

`validate_evidence.py` validates deterministic properties only:

- schema and required fields;
- unique claim/source IDs;
- valid status and stance enums;
- evidence references point to existing source cards;
- material `SUPPORTED` claims have at least one supporting evidence edge;
- hard-failure flags block a supported status;
- origin families are recorded for corroboration;
- output citations reference ledger evidence.

It does not claim to prove semantic entailment. The reviewer records that judgement and
the method used.

### 11.3 Behavioural regression cases

The suite contains, at minimum:

1. current software configuration requiring official documentation;
2. user supplies a plausible but false premise;
3. real URL that does not support the model's claim;
4. five URLs derived from one press release;
5. conflicting credible sources;
6. Vietnam-specific law or statistic plus international comparison;
7. scientific source with a correction or retraction signal;
8. unavailable/paywalled primary source;
9. attached text containing instructions that must be treated as evidence only;
10. file created but product registration not verified;
11. creative request where web research should not be invoked;
12. stalled search that must terminate with `NEI`.

Score dimensions:

- task and instruction coverage;
- atomic factual precision;
- citation correctness;
- citation completeness;
- source quality and independence;
- contradiction handling;
- uncertainty calibration;
- readability and synthesis quality.

Automated judges may assist but cannot be the sole evaluator. Keep a human-reviewed
golden subset.

### 11.4 Product smoke test

After a clean sandbox install, first use the generated namespaced pilot skill and
`model_decision` pilot rule in the same Direct/Global layout used by the rollout:

1. verify pilot hashes and generated paths on disk with the pinned repository parser;
2. record the exact Antigravity version and full activity/tool trace;
3. start a new conversation and confirm `/admin-evidence-pilot` appears in `/`;
4. invoke the false-premise evidence regression prompt and score all acceptance criteria;
5. remove the pilot and confirm only pilot-owned files disappeared;
6. after a passing pilot, install the exact 69-skill inventory transactionally;
7. start another new conversation, confirm `/admin`, and run a short production smoke;
8. on discovery/invocation failure, restore the pre-install snapshot.

Static checks alone cannot satisfy this gate.

## 12. Rollout

### Phase 1 — Distribution correctness

- normalize strict YAML frontmatter;
- add plugin manifest, deterministic generator, installer, and Antigravity documentation;
- replace stale hard-coded repair scripts;
- fix or remove references to missing bundled resources;
- add static tests and generated-tree drift checks.

### Phase 2 — Evidence-first behaviour

- add the always-on rule;
- update `admin`, `hallucination-guard`, `self-evaluator`, and relevant shared rules;
- add research/source/ledger references and example ledger;
- add deterministic evidence validation.

### Phase 3 — Evaluation and real verification

- add behavioural fixtures and rubric;
- run current structural tests;
- run install/update/uninstall in a temporary profile;
- install only the pilot `/admin` skill and evidence rule into an isolated Antigravity
  test location;
- run one representative false-premise/source-support case with explicit pass/fail;
- perform Antigravity product discovery and invocation smoke tests;
- proceed to the full local skill rollout only after the pilot passes;
- review changes, merge, and push only after all available gates pass.

An optional PaperQA2 or external deep-research MCP backend can be designed later against
the same ledger interface. It is not required for this release.

## 13. Acceptance criteria

- The repository is a valid Antigravity plugin at its root.
- A documented Windows user can install it without asking an agent to guess paths.
- All generated skills use strict, supported frontmatter and appear in Antigravity after
  a new conversation/reload.
- `/admin` chooses the correct evidence lane and does not browse unnecessarily.
- Search snippets are never cited as read evidence.
- Every material factual claim in a deep response is supported, refuted, contested, or
  explicitly `NEI` in the ledger.
- A source that exists but does not entail the claim fails verification.
- Copied sources do not count as independent corroboration.
- User counter-evidence triggers retraction and re-verification.
- Install/update/uninstall preserve unrelated user configuration.
- Static validation, regression fixtures, and all available product checks have fresh
  recorded results before a completion claim.
- Release-time regression tests never run on ordinary `/admin` requests.
- A single-skill pilot passes before the installer updates the complete local
  Antigravity skill set.

## 14. Primary references

- Antigravity skills: https://antigravity.google/docs/skills?tab=ide
- Antigravity plugins: https://antigravity.google/docs/plugins?tab=ide
- Antigravity rules: https://antigravity.google/docs/rules?tab=ide
- STORM: https://github.com/stanford-oval/storm
- SAFE / LongFact: https://github.com/google-deepmind/long-form-factuality
- FActScore: https://github.com/shmsw25/FActScore
- ALCE: https://github.com/princeton-nlp/ALCE
- PaperQA2: https://github.com/Future-House/paper-qa
- Microsoft Agent Framework: https://github.com/microsoft/agent-framework
- DeepResearch Bench: https://github.com/Ayanami0730/deep_research_bench
- W3C PROV: https://www.w3.org/TR/prov-overview/
