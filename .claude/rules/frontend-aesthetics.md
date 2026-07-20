# Frontend Aesthetics (binding for Workbench web/UI skills)

Anti-slop, type, color, motion, and review rules pulled by **`design-web`**,
**`build-ui`**, and **`review-frontend`**. Each of those skills cites this
file in one line and reads it at run time only (kept out of always-loaded context).
This file is subordinate to `~/.claude/rules/workbench-conventions.md` (bilingual
policy, preview-not-dump); on any conflict, the master conventions win.

Core principle: models sample the high-probability center of their training data, so
without deliberate constraint they converge on safe, generic, **interchangeable** UI.
Every rule below exists to push output off that center toward a choice specific to
*this* subject, audience, and single job.

---

## 1. The AI-slop checklist (what to NEVER ship)
A surface is "slop" when it could belong to any product. Refuse / rework if it shows:
- **Generic system fonts** — Inter, Roboto, Arial, Helvetica, `system-ui`, or any
  default sans used for everything with no display/body contrast.
- **Purple-on-white or purple-on-dark gradients** — the `#7C3AED → #DB2777` SaaS
  gradient, "blurple" hero blobs, evenly-spread pastel rainbows.
- **Predictable layouts** — centered hero + 3 feature cards + accordion FAQ + CTA
  band, every section the same full-width padded box, no rhythm or asymmetry.
- **Cookie-cutter components** — untouched default shadcn/Material with default radius,
  default shadow, default spacing scale, no brand expression anywhere.
- **Emoji as icons** — 🚀✨🎯 standing in for a real icon set; emoji in buttons,
  nav, feature bullets, or empty states.
- **Timid color** — five colors at equal weight, no dominant, no decisive accent.
- **Flat dead backgrounds** — pure `#FFFFFF` / `#000000` fills with no atmosphere.
- **The three recurring slop clusters:** (a) warm cream + serif + terracotta
  "editorial"; (b) near-black + acid-green/vermilion "cyber"; (c) broadsheet
  hairline-rule "newspaper". Recognizable defaults — escape, don't reach for them.

## 2. Grounding before design (mandatory first step)
Before choosing any token, name in one sentence each: the **subject** (what this
course/product is about), the **audience**, and the **single job** of this surface.
Draw concrete choices from the subject's own world (a coding bootcamp ≠ a yoga studio
≠ a finance certification). Generic = no grounding.

## 3. Type pairing
- Use **distinctive, characterful type** with clear role separation: a display face
  (used with restraint for headings / one hero moment), a complementary body face, and
  optionally a utility/mono face for code, data, prices, and labels.
- **Self-hostable safe options** (bundle the font files, do NOT hotlink — Artifacts
  block external hosts and project CSP often does too): Space Grotesk, Sora,
  Clash Display, Satoshi, General Sans, Fraunces, Newsreader, Source Serif 4,
  IBM Plex (Sans/Serif/Mono), JetBrains Mono, Geist / Geist Mono. License-check before
  shipping; all of the above have self-host-friendly licenses.
- **Extreme weight contrast** (100/200 hairline vs 700/900 heavy) and **size jumps of
  3x+** between display and body. Timid 400-vs-600 contrast reads as slop.

## 4. Color system (cohesive token palette)
- Define **4–6 named hex values** as CSS custom properties (a token set), not ad-hoc
  inline colors. One **dominant** color carries the surface; one **sharp accent** does
  the high-emphasis work; the rest are neutrals/support. Avoid the five-equal-colors
  trap.
- Express in CSS variables (and OKLCH where the project supports it) so the same tokens
  drive light/dark and the shadcn theme. Backgrounds get **atmosphere** (subtle
  gradient, grain, or pattern), not a flat fill.
- **Contrast / WCAG 2.2 AA is a hard floor, not a nice-to-have:** body text ≥ **4.5:1**,
  large text (≥24px or ≥19px bold) and UI/icon boundaries ≥ **3:1**. State must never be
  conveyed by color alone (add icon/text/shape). Verify the accent against its
  background, not just black-on-white.

## 5. Motion
- Motion adds atmosphere and hierarchy, never decoration for its own sake. Prefer a
  high-impact **orchestrated page-load** (staggered `animation-delay`) over scattered
  hover wiggles. CSS-only animation for plain HTML/Artifacts; the Motion library for
  React where the project already uses it.
- **`prefers-reduced-motion: reduce` is mandatory.** Wrap non-essential transitions so
  they collapse to an instant state change; never trap meaning (loading, success) only
  inside an animation a reduced-motion user won't see.

## 6. Writing is design material
Active voice; user-side labels ("Manage notifications", not "webhook config");
consistent verbs across a flow (a "Publish" button yields a "Published" toast); errors
give direction, not blame; empty states invite the next action. (Human-facing copy in
the actual product follows the project's own language; Workbench chat prose stays
Vietnamese per the master conventions.)

## 7. Quality floor (every component, before "done")
Responsive down to mobile · visible keyboard `:focus-visible` on every interactive
element · all of loading / empty / error / success states designed · reduced-motion
honored · watch CSS specificity conflicts (no `!important` arms race) · **never gate UI
on a client-side role — authorization is enforced server-side** (see
`course-domain-model.md`).

## 8. The slop-cluster checklist (what `review-frontend` runs)
Score each; any failure is a finding (severity-coded in the report):
1. **Type** — distinctive faces? real weight + size contrast? no bare system font?
2. **Color** — 4–6 cohesive tokens, one dominant + one decisive accent? no SaaS-purple
   gradient? atmospheric (not flat) background?
3. **Layout** — rhythm/asymmetry, or generic stacked boxes? one signature element
   present?
4. **Components** — branded, or untouched library defaults?
5. **Icons** — a real icon set, with **zero emoji-as-icons**?
6. **A11y** — WCAG AA contrast, focus-visible, reduced-motion, keyboard reachable,
   state not color-only?
7. **Copy** — active voice, user-side labels, consistent verbs, actionable errors,
   inviting empty states?
8. **Slop clusters** — not the cream/serif/terracotta, near-black/acid, or
   broadsheet-rule default?

## 9. One decisive direction vs proposing multiple (read this carefully)
Anthropic's own guidance favors **one decisive, creative choice per dimension**,
refined by an **internal two-pass loop** (brainstorm a compact token system → critique
"does any part read like a generic default?" → revise → build from the revised plan).
Anthropic does **not** advocate showing the user several finished UI options to pick
from, and the skill-authoring guidance separately warns against offering too many
options. So: the **default** is one decisive direction via the two-pass critique.
A `--directions N` multi-option mode is a deliberate **Workbench product choice** for
early exploration — when a skill uses it, label it as a product choice, **not** as
Anthropic guidance, and still run each candidate through the §1/§8 slop checklist.
