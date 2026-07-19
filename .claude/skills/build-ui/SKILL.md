---
name: build-ui
description: Theme-neutral UI builder Worker — turns a locked design-record (notes/design-<slug>.md from design-web) into real, accessible, on-brand front-end code against the project's inferred stack. Modes — component (one accessible component on the locked tokens), page (a full surface composed of components), admin (role-gated CRUD dashboard shell with SERVER-SIDE authorization), scaffold (stand up a theme-neutral project skeleton in the inferred stack). Triggers — build the component, dựng component, build the page, code the UI, dựng giao diện, làm trang admin, admin dashboard, CRUD dashboard, scaffold the project, dựng khung dự án, implement the design. It BUILDS from a design-record; it does NOT decide the look (use design-web first) or audit slop/a11y (use review-frontend).
argument-hint: <component|page|admin|scaffold> <name> [design-slug]
allowed-tools: Read Edit Write Glob Grep Bash
---

# Build UI (dựng giao diện theo design-record)

Builds production front-end code from a **locked design-record**. It does not invent a look — it
implements the one design-web committed. Theme-neutral: infers the stack (Next/React+Tailwind+shadcn,
Vue, plain HTML/CSS, …) from the project. Folds the former build-ui-component, build-admin-dashboard,
and scaffold-course-platform stubs into one mode-parameterized skill (now topic-agnostic).

## Conventions
Binding: `~/.claude/rules/workbench-conventions.md` (bilingual §1 — code English, report Vietnamese;
preview-not-dump §3; scope handoff §10) and `~/.claude/rules/frontend-aesthetics.md` (quality floor
§7 — responsive, focus-visible, all states, reduced-motion; the server-side-authorization rule). The
component catalog + stack matrix live in `references/` — read on demand; never inline. Also subject to
`~/.claude/rules/course-domain-model.md` ONLY when the project actually is a course/LMS (its
authorization rules are universal; the entities are not — do not impose them on other domains).

## Procedure

### Phase 0 — Resolve mode + read the locked design-record FIRST
Parse mode: `component` | `page` | `admin` | `scaffold`. Read `notes/design-<slug>.md` (the locked
tokens, type pairing, layout concept, motion budget) — this is the binding source of truth. If no
design-record exists and the mode needs one (`component`/`page`/`admin`), STOP and hand back to
`design-web` first; do not improvise a look. Infer the project stack by reading manifest/config files.

### Phase 1 — Build against the tokens (apply the anti-runaway-edit contract from code-senior)
- **`component`:** one accessible component using the locked CSS variables/tokens — never ad-hoc
  colors. Quality floor §7: keyboard focus-visible, all of loading/empty/error/success states,
  responsive to mobile, reduced-motion honored. Match the project's existing component conventions.
- **`page`:** compose components per the layout concept (rhythm/asymmetry, the signature element).
- **`admin`:** a role-gated CRUD shell — tables, forms, the management surface. **Authorization is
  SERVER-SIDE** (route handler / server action / RLS / middleware); the client role only decides what
  to RENDER, never what to ALLOW (course-domain-model.md CRITICAL rule). Never gate access on a
  client-side role check.
- **`scaffold`:** stand up a minimal, theme-neutral project skeleton in the inferred stack (folders,
  config, a tokens/theme file wired to the design-record). No hard-coded domain.
When editing existing files, use `Edit` not `Write`, minimal diffs (anti-runaway-edit). New files use
`Write`.

### Phase 2 — Verify + report (§3)
Run the project's build/typecheck/lint or a render check if available; state the real result. Print a
**6-9 line** Vietnamese report: files created/changed (one line each), which design tokens were used,
a11y/state coverage, the verify result, and the handoff (`→ review-frontend` để chấm slop/a11y). Do
NOT paste full component code into chat.

## Output
Front-end source files in the project tree (per its conventions). No `notes/` artifact. Chat gets the
report + paths.

## Gotchas
- **Design-record is binding.** Build from the locked tokens; if it's missing, go back to design-web.
  Inventing colors/fonts here defeats the whole design step.
- **Server-side authorization, always.** A client role is a UI hint, not a security boundary. Re-check
  on the server for every gated read/mutation (course-domain-model.md).
- **Quality floor §7 is non-negotiable.** focus-visible, every state, responsive, reduced-motion.
- **Anti-runaway-edit.** `Edit` over `Write` on existing files; minimal diffs; don't reformat.
- **Don't dump code to chat (§3).** Files hold the code; chat gets the report + paths.
- **Stay in scope (§10).** This skill BUILDS:
  - `→ dùng design-web cho` quyết định + preview giao diện (chạy TRƯỚC).
  - `→ dùng review-frontend cho` chấm anti-slop / a11y sau khi dựng.
  - `→ dùng code-senior cho` logic/back-end không phải UI.
