---
name: design-web
description: Decides the visual direction for a web surface AND verifies it by rendering, screenshotting and measuring — because in practice nearly every real defect is caught by looking, not by thinking harder. Grounds in the subject's own world, asks 2-3 blocking questions, commits ONE decisive token system, then renders the surface, LOOKS at the screenshot, and computes every contrast ratio with scripts/contrast.py before calling it done. Adapts to the target: a standalone surface previews as a self-contained HTML Artifact; a real project is designed in the project's own stack, with no Artifact detour. Modes — direction (default), learn (extract a reference's design architecture, never its skin), content-site, directions N. Triggers — thiết kế web, design a web page, thiết kế giao diện, làm landing page, hướng thiết kế, bảng màu font, palette typography, học style từ web này, knowledge microsite, design a UI, giao diện xấu quá, làm đẹp giao diện, nhìn như AI.
argument-hint: <surface-slug | "url <link>" | freeform brief> [direction|learn|content-site|directions N]
allowed-tools: Read Write Edit WebFetch Glob Grep Bash AskUserQuestion
---

# Design Web (quyết hướng thiết kế — và tự kiểm chứng)

Decides a distinctive, subject-specific visual direction for one web surface, builds it in whatever
medium the target actually is, then **proves it works by looking at it and measuring it**.

## Why this skill is shaped around verification

An earlier version of this skill spent almost all of itself on the decision — grounding, tokens, a
two-pass self-critique — and said nothing about checking the result. A full build under it produced
nine real defects. Where they were caught:

| Caught by | Count |
|---|---|
| Rendering a screenshot and **looking** at it | 4 |
| **Computing** contrast ratios | 3 |
| **Measuring** element positions in a script | 1 |
| Thinking harder / re-reading | **0** |

Deciding well is cheap and mostly goes right. Seeing what you actually shipped is the work.

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — prose Vietnamese, tokens/CSS/
identifiers English; preview-not-dump §3) and `~/.claude/rules/frontend-aesthetics.md` (anti-slop §1,
grounding §2, type §3, colour §4, motion §5, writing §6, quality floor §7, slop clusters §8, one
decisive direction §9). Read at run time; never inline.

## Procedure

### Phase 0 — Resolve the TARGET first, then ground

**Which medium is this?** Getting this wrong is why a design skill gets skipped on real work.

| Target | How you build it | Design record goes |
|---|---|---|
| One-off surface, no repo | Self-contained HTML Artifact (CSP: inline everything) | `notes/design-<slug>.md` |
| **A real project** (Vite/Next/etc.) | **In the project's own stack.** No Artifact detour | `<project>/DESIGN.md` next to the code |

Designing a real app inside an Artifact means designing in one medium and rebuilding in another —
double work, and the preview cannot use the project's real fonts, components or build step. Detect a
project (`package.json`, a framework config) and design *there*.

**Then ground (§2, mandatory):** one sentence each for the **subject**, the **audience**, and this
surface's **single job**. Generic output means this step was skipped.

### Phase 1 — Ask the 2-3 blocking questions (GATE — do not guess)
Ask only the questions whose answers would *change* the design: brand/mood, existing colours or
fonts to honour, the one action the surface must drive, light/dark. Use `AskUserQuestion`. If the
user is unreachable, write the assumptions into the design record instead of hiding them.

### Phase 2 — Commit ONE decisive direction (two-pass, §9)
A **4-6 named-hex token set** (one dominant + one sharp accent + neutrals), **2-3 type roles** with
real weight and size contrast, a **layout concept** with rhythm plus one signature element, and a
**motion budget** (one orchestrated load beats scattered hover tricks; honour `prefers-reduced-motion`).

Query the corpus rather than reciting it:
```
python "<skills>/design-web/scripts/design_search.py" "<mood keywords>" [--kind palette|type|archetype|bans]
```

**Elevation on a dark ground comes from stepped surface tone plus a hairline border, not from drop
shadows.** Shadows on dark just make mud. Five or six surfaces, each a clear step lighter than the one
beneath, is what makes a block read as raised.

### Phase 3 — RENDER, SCREENSHOT, AND LOOK (mandatory — this is the phase that finds things)

Never report a visual result you have not seen.

```bash
npm run build && npx vite preview --port 4173 &     # or the project's own serve
```
```js
// playwright: chromium is usually already on the machine
await page.goto("http://localhost:4173/");
await page.screenshot({ path: "shot.png" });
```

Then **Read the PNG** and inspect it as a critic. Also screenshot every state that exists: hover,
selected, open panel, empty, error, and `reducedMotion: "reduce"`.

Look specifically for what a mental review cannot catch:
- text colliding with other text, or with a background label
- an element pushed off-screen by your own centring or panning logic
- something dimmed so far it is effectively gone
- a panel covering the very thing it describes
- a control whose focus ring, hover state or disabled state you never actually rendered

If a change appears to do nothing, **measure before theorising** — print the value, diff two frames.
A library that caches your accessor will fail silently and look exactly like a CSS problem.

### Phase 4 — Measure contrast; never judge it by eye
```bash
python "<skills>/design-web/scripts/contrast.py" --css <tokens.css> --on=--s0,--s1,--s3 --need 4.5
python "<skills>/design-web/scripts/contrast.py" --pair "#8a6224" "#2e2820" --need 3.0
python "<skills>/design-web/scripts/contrast.py" --fix "#6f6152" --on "#141d38,#2e2820" --need 3.0
```
Body text ≥ **4.5**; large text and **every boundary of an interactive control** ≥ **3.0** (WCAG
1.4.11). That last one is the one that gets missed: a 1.34:1 border on an input looks deliberate and
is invisible to anyone with reduced contrast sensitivity.

The scan reports ink against surfaces only. A token that fails may still be fine where it is actually
used — a decorative hairline is exempt, an input border is not. Judge by usage, not by the list.

### Phase 5 — Lock the record + preview to chat (§3)
Write the design record (location per Phase 0): token table with hex + role, type pairing, layout
concept, motion budget, grounding sentence, and **the measured contrast results**. Chat gets a **6-9
line** Vietnamese preview + paths. Never paste CSS into chat.

## Traps that have shipped past a careful review

- **The reference the user admires is often a slop cluster.** Near-black + neon is cluster (b);
  cream + serif + terracotta is cluster (a) — and that second one is what most "beautiful AI product"
  references actually are. Take the **mechanism** (how it builds elevation, how it separates roles),
  never the **skin**. Say out loud which cluster the reference belongs to and what you took instead.
- **Redrawing another site's layout structure is design plagiarism** even when every line is yours
  (`paper-writing-integrity.md` §2). Redesign it or credit it.
- **CSS Grid makes every bare text node its own item.** `<b>Label</b> — description` inside a grid
  row shatters into one word per line. Use flex, or wrap the text in a single element.
- **Focus lands where the DOM says, not where you meant.** `querySelector("input, button")` returns
  the first match in document order — which in a dialog is usually the close button. Name the target.
- **A dialog with `aria-modal="true"` must trap Tab.** Claiming the attribute without the behaviour
  is worse than not claiming it.
- **One strip doing three jobs does none.** Split UI chrome by how often it is needed: glanceable
  state stays visible, read-once material (legends, shortcuts) goes behind a button.
- **Never ship a control that only looks functional.** A Google button on a static site with no
  backend cannot verify anyone. Disable it, say why, and offer the honest fallback — a decorative
  auth button is the kind of lie that gets relied on.

## Output
- The surface itself, in the target's own medium (Artifact **or** project source).
- The design record with measured contrast.
- Screenshots you have actually looked at.

## Gotchas
- **The blocking-question gate is not optional.** Designing on a guessed mood wastes the whole pass.
- **One decisive direction (§9)**, not five mushy ones. `directions N` is deliberate exploration.
- **Do not dump CSS to chat (§3).**
- **Stay in scope.** This skill decides, builds and verifies the LOOK. It does not:
  - `→ dùng build-ui cho` dựng thêm component/page production trên design record đã khóa.
  - `→ dùng review-frontend cho` chấm anti-slop / a11y một site đã có sẵn.
  - `→ dùng backend-engineer cho` bất kỳ thứ gì cần máy chủ xác minh (auth, quyền, thanh toán).
