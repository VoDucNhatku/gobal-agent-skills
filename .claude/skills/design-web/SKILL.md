---
name: "design-web"
description: "Flagship web/UI design Worker — decides a real, theme-neutral visual direction for a web surface and renders a self-contained HTML Artifact preview, then locks it as a design-record other skills build against. It GROUNDS in the subject's own world, asks the user 2-3 blocking questions before designing (never guesses), commits ONE decisive token system, and self-reviews for AI-slop before presenting. Modes — direction (default), learn (extract the design architecture of a reference site/URL or a described style without copying assets), content-site (pull real copy from the research workers then design around it), directions N (emit N candidates for early exploration). Triggers — design a web page, thiết kế web, thiết kế giao diện, làm landing page, design direction, hướng thiết kế, palette + typography, bảng màu font, học style từ web này, learn this site's design, web tóm tắt kiến thức, knowledge microsite, design a UI. It decides + previews the look; it does NOT build production components (use build-ui) or audit an existing site (use review-frontend)."
argument-hint: "<surface-slug | \"url <link>\" | freeform brief> [direction|learn|content-site|directions N]"
allowed-tools: "Read Write WebFetch Glob Grep Bash"
---

# Design Web (thiết kế giao diện web — flagship)

Decides a distinctive, subject-specific visual direction for ONE web surface and previews it as a
self-contained HTML Artifact, then writes a **locked design-record** (`notes/design-<slug>.md`) that
`build-ui` and `review-frontend` treat as the source of truth. Theme-neutral: the subject comes from
the user, not a hard-coded domain.

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — human prose Vietnamese, all
tokens/CSS/identifiers English; output + preview §3) and `~/.claude/rules/frontend-aesthetics.md`
(the full taste rulebook — anti-slop §1, grounding §2, type §3, color §4, motion §5, writing §6,
quality floor §7, slop-cluster §8, one-decisive-direction §9). **Reference both at run time; never
inline them.** Heavy design knowledge lives in on-disk CSVs queried by a script (below), not in this
body — so deep coverage costs almost nothing in always-loaded context.

## Procedure

### Phase 0 — Resolve surface, mode, ground
Resolve `$ARGUMENTS`: a surface slug (`pricing`, `knowledge-site`), `url <link>` (mode `learn`), or
a freeform brief. Parse mode: `direction` (default) | `learn` | `content-site` | `directions N`.
**Ground first (§2, mandatory):** name in one sentence each — the **subject** (what this is about),
the **audience**, and the surface's **single job**. Distinctive choices come from the subject's own
world; "generic" means you skipped grounding.

### Phase 1 — Ask the 2-3 blocking questions (MANDATORY GATE — do not guess)
Before committing any token, ask the user the **2-3 questions whose answers would change the design**
— and only those. The agent decides WHICH questions from the context; do not run a fixed
questionnaire and do not ask what you can reasonably infer. Typical blockers: brand/mood (e.g.
"nghiêm túc học thuật hay trẻ trung năng động?"), any existing brand colors/logo/font to honor,
the one action the surface must drive, light/dark, and (for `content-site`) which papers/notes are
the content. Use `AskUserQuestion` if available. **Never proceed to Phase 3 on assumptions** — if
the user is unreachable, state the assumptions explicitly in the design-record. Understand context;
ask about the right things, not everything.

### Phase 2 — Pull knowledge (script-offloaded) + mode work
Query the design corpus instead of reciting it from memory — top-3 rows only:
```
python "<skills>/design-web/scripts/design_search.py" "<subject/mood keywords>" [--kind palette|type|archetype|bans]
```
It returns the best rows from `references/palettes.csv`, `references/type-pairings.csv`,
`references/style-archetypes.csv`, `references/anti-slop-bans.csv` (banned defaults per vertical).
- **`learn`:** WebFetch the reference URL (or read the user's description), extract the design
  ARCHITECTURE — layout grammar, type-pairing logic, color strategy, motion language — and append it
  as a new row to `references/style-archetypes.csv` via the script's `--add` flag. Then design FROM
  that architecture; **never copy its assets/text** (that is theft, and off-subject).
- **`content-site`:** the surface needs real copy. **Call the research workers** — `paper-triage`
  then `paper-read`/`paper-synthesize` — to produce the actual content into `notes/`, then design the
  surface around that real content. Never lorem (§ build with real content).

### Phase 3 — Commit ONE decisive direction (two-pass, §9)
Pick ONE decisive choice per dimension (do not hedge): a **4-6 named-hex token system** (one dominant
+ one sharp accent + neutrals, WCAG AA verified §4), **2-3 type roles** (display/body/[mono], extreme
weight + size contrast, self-hosted faces §3), a **layout concept** with rhythm/asymmetry + one
signature element, and a **motion budget** (orchestrated load > scattered hover, `prefers-reduced-
motion` honored §5). Set 2-3 inferred DIALS (VARIANCE / MOTION / DENSITY, 1-10) so the direction is
decisive, not mushy. **Two-pass self-review-for-slop (§1/§8):** does any part read like the
cream/serif/terracotta, near-black/acid, broadsheet-rule, or SaaS-purple-gradient default, or use
Inter/Roboto/system-ui as the only face? If yes → revise and note what changed and why.
`directions N` mode: emit N candidates, each run through the §1/§8 checklist; label it a Workbench
product choice, NOT Anthropic guidance (§9).

### Phase 4 — Preview + lock the record (§3)
Render a **self-contained HTML Artifact** from `assets/artifact-preview-template.html` — swap only the
`:root` token values + sample copy, keep the layout skeleton; inline CSS only (CSP forbids external
fonts/images/scripts — embed faces as `@font-face` data URIs). Then write the **locked design-record**
`notes/design-<slug>.md`: the token table (hex + role), the type pairing, the layout concept, the
motion budget, the dials, and the grounding sentence — this is what `build-ui` reads. Print to chat a
**6-9 line** Vietnamese preview: the direction in one line, the dominant + accent hex, the type
pairing, the Artifact link, and the design-record path. **Never** paste the full CSS/HTML into chat.

## Output
- HTML Artifact (preview) + `notes/design-<slug>.md` (locked source-of-truth for build-ui).
- For `learn`: also a new row in `references/style-archetypes.csv`.

## Gotchas
- **The blocking-question gate is not optional.** Designing on guessed brand/mood wastes a full
  Artifact render. Ask 2-3 targeted questions first; infer the rest; state any assumption you must make.
- **One decisive direction (§9), not five mushy ones.** Default mode commits one; `directions N` is a
  deliberate exploration mode, not the norm.
- **Self-review for slop before presenting (§1/§8).** Catch the default look in the plan, not after
  the user sees it.
- **Offload the corpus.** Query `design_search.py` for palettes/type/archetypes — do not carry the
  whole design knowledge in the body (token economy).
- **Don't dump CSS to chat (§3).** The tokens live in the Artifact + design-record; chat gets the
  6-9 line preview + links.
- **Stay in scope.** This skill DECIDES and PREVIEWS the look. It does not:
  - `→ dùng build-ui cho` dựng component/page/admin production theo design-record đã khóa.
  - `→ dùng review-frontend cho` chấm anti-slop / a11y một site đã có.
