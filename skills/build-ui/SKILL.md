---
name: "build-ui"
description: "Builds accessible, on-brand front-end code against the project's own stack, then proves it renders — screenshot it, look at it, measure the contrast of what shipped. Uses a design record when one exists; when none does, reads the tokens already in the project rather than stopping, and only asks when there is genuinely nothing to build on. Modes — component (one accessible component on the locked tokens), page (a surface composed of components), admin (role-gated CRUD shell with SERVER-SIDE authorization), scaffold (a theme-neutral project skeleton). Triggers — dựng component, build the component, build the page, code the UI, dựng giao diện, làm trang admin, admin dashboard, CRUD dashboard, dựng khung dự án, scaffold the project, implement the design, sửa giao diện. It BUILDS and verifies; it does not decide the look (design-web) or audit an existing site (review-frontend)."
---

# Build UI (dựng giao diện — và chứng minh nó hiện đúng)

Builds production front-end code in the project's own stack, then verifies what actually rendered.
Theme-neutral: the stack (Next/React+Tailwind, Vue, Vite+TS, plain HTML/CSS, …) is inferred from the
project, never assumed.

## Conventions
Binding: `../../rules/workbench-conventions.md` (bilingual §1 — code English, report Vietnamese;
preview-not-dump §3; scope handoff §10) and `../../rules/frontend-aesthetics.md` (quality floor §7
— responsive, focus-visible, every state, reduced-motion; server-side authorization). The component
catalog is in `references/component-catalog.md`, read on demand. `../../rules/course-domain-model.md`
applies ONLY when the project really is a course/LMS — its authorization rules are universal, its
entities are not.

## Procedure

### Phase 0 — Find the tokens; do not stall for a missing document

A design record is the best input, not a precondition. An earlier version of this skill hard-stopped
whenever `notes/design-<slug>.md` was absent, which is most of the time on a real project — so it was
simply never used. Look in order and take the first that answers:

| Look for | Then |
|---|---|
| A design record — `DESIGN.md` beside the code, `notes/design-<slug>.md`, or the path given | Build to it. It is binding |
| The project's own token file (`tokens.css`, `theme.ts`, `tailwind.config`, CSS custom properties) | Build to those. **Extend the existing system; never start a second one** |
| A component library already in use | Follow its conventions and its existing overrides |
| Genuinely nothing — an empty repo | Ask ONE question, or `→ design-web` if the look is the real question |

Parse mode: `component` | `page` | `admin` | `scaffold`. Infer the stack from manifest/config files.
Never introduce ad-hoc hex values when a token exists for the job.

### Phase 1 — Build (anti-runaway-edit contract)
- **`component`** — one accessible component on the existing tokens. Quality floor §7: visible
  keyboard focus, **all** of loading/empty/error/success, responsive to mobile, reduced-motion honoured.
- **`page`** — compose components per the layout concept; keep the rhythm and the signature element.
- **`admin`** — role-gated CRUD shell. **Authorization is SERVER-SIDE** (route handler / server action
  / RLS / middleware). The client role decides only what to RENDER, never what to ALLOW.
- **`scaffold`** — minimal theme-neutral skeleton in the inferred stack, with the token file wired up.

`targeted file editing capability` on existing files with minimal diffs; `file writing capability` only for new ones. Do not reformat what you did
not change.

**Never ship a control that only looks functional.** A button wired to nothing, a form that discards
its input, a sign-in that verifies nobody — disable it and say why, or do not draw it. A decorative
control is the kind of lie someone later relies on.

### Phase 2 — Render it and LOOK (mandatory)

Type-checking proves it compiles, not that a human can use it. Serve the project and screenshot every
state you built:

```bash
npm run build && npx vite preview --port 4173 &     # or the project's own serve command
```
```js
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto("http://localhost:4173/");
await page.screenshot({ path: "shot.png" });
// and: hover, focus, open, empty, error, { reducedMotion: "reduce" }
```

Then **Read the PNG**. Look for what a type-checker cannot see: text colliding with text, an element
pushed off-canvas by your own layout maths, a state you styled but never rendered, a control whose
focus ring never appears. Collect the console errors too — a silent `pageerror` is a shipped bug.

If a change appears to do nothing, **measure before theorising**: print the value, diff two frames. A
library that caches a callback fails silently and looks exactly like a CSS problem.

### Phase 3 — Measure contrast on what shipped
```bash
python "../design-web/scripts/contrast.py" --css <the project's token file> --on=<grounds> --need 4.5
```
Body text ≥ **4.5**; large text and **every boundary of an interactive control** ≥ **3.0** (WCAG
1.4.11). Control borders are the ones that get missed — a 1.34:1 outline on an input looks intentional
and is invisible to a good share of readers. Judge a flagged token by where it is used: a decorative
hairline is exempt, an input border is not.

### Phase 4 — Report (§3)
A **6-9 line** Vietnamese report: files created/changed, which tokens were used, state + a11y
coverage, **the verify result including what the screenshot showed**, and the handoff. Never paste
component code into chat.

## When to run the whole chain

Most surfaces need all three, in order, and each stage owns its own verification:

```
design-web      decide the look · render · look · measure   →  design record
   ↓
build-ui        build in the project stack · look · measure  →  source files
   ↓
review-frontend audit anti-slop + WCAG + AI-tells            →  findings
```

Skip `design-web` when the project already has a token system worth extending. Never skip Phase 2.

## Output
Front-end source in the project tree, plus screenshots you have actually looked at. No `notes/`
artifact. Chat gets the report and the paths.

## Gotchas
- **Extend the existing token system, never open a second one.** Two palettes in one project is worse
  than a mediocre single palette.
- **Server-side authorization, always.** A client role is a UI hint; re-check on the server for every
  gated read and mutation.
- **Quality floor §7 is not optional** — focus-visible, every state, responsive, reduced-motion.
- **A dialog claiming `aria-modal="true"` must trap Tab.** Claiming the attribute without the
  behaviour is worse than not claiming it.
- **Focus lands where the DOM says, not where you meant.** `querySelector("input, button")` returns
  the first match in document order — in a dialog that is usually the close button. Name the target.
- **CSS Grid makes every bare text node its own item.** `<b>Label</b> — description` in a grid row
  shatters into one word per line. Use flex, or wrap the text in one element.
- **Anti-runaway-edit.** Minimal diffs; a small fix never becomes a rewrite.
- **Stay in scope (§10).** This skill BUILDS and VERIFIES:
  - `→ dùng design-web cho` quyết định hướng thiết kế khi project chưa có hệ token.
  - `→ dùng review-frontend cho` chấm anti-slop / a11y toàn diện sau khi dựng.
  - `→ dùng backend-engineer cho` bất cứ thứ gì cần máy chủ xác minh (auth, quyền, thanh toán).
  - `→ dùng code-senior cho` logic không phải giao diện.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
