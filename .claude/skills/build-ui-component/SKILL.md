---
name: build-ui-component
description: Builds one accessible, on-brand component grounded in the locked design system. Reads the design token file and component catalog in references/component-catalog.md.
argument-hint: <component-name>
allowed-tools: Skill Agent Read Write Edit Glob Bash Grep
---

# Build UI Component — Component Builder

> **Purpose:** Produce one accessible, theme-consistent component on demand, reading the locked design token file and component catalog in references/.

## Role

This skill ships components only; design direction, anti-slop decisions, and token choices already exist in `notes/design-<slug>.md`. The canonical component patterns and named variants live in `references/component-catalog.md` so this body stays small.

## Modes

| Mode | Use it when | Output |
|------|-------------|--------|
| `component` (default) | Build a single component | Single-file component + tests + a11y notes |
| `variant` | Add an alternate size / tone / state variant | Updated component + changelog note |
| `audit` | Review one component against slop checklist and WCAG 2.1 AA | Findings only |

## Procedure

1. Read `notes/design-<slug>.md`. If missing, ask up to 3 blocker questions before guessing.
2. Read `references/component-catalog.md` for canonical patterns, naming, and props schema.
3. Build the component with semantic HTML, visible `:focus-visible` state, contrast >= 4.5:1, and `prefers-reduced-motion` collapsing non-essential transitions.
4. Wire events to the project data layer (do not stub interactions).
5. Handoff to `review-frontend` for slop + a11y audit.

## Accessibility Guardrails

- Ensure every interactive element has a visible focus indicator (`:focus-visible`).
- Deliver skeleton / empty / error states when the component is wired to async data.
- Preserve `prefers-reduced-motion` semantics: non-essential transitions collapse to instant state change.
- State must never be conveyed by color alone — pair with icon or text variant.

## Triggers

- "build component", "new button", "new modal", "new card", "component for this", "tạo component", "làm button".

## Integration

- `design-web` — design token source
- `review-frontend` — post-build audit
- `token-budget` — estimate cost before any fan-out
- `reuse-checker` — reuse before creating new

## Anti-Runaway Contract

1. Prefer Edit over Write — modify the smallest existing surface that contains the change.
2. Read before edit — re-read the target file when the Read cache is stale (different offset, fresh call).
3. Small fix stays small — if a surgical edit touches more than a reasonable slice, stop, re-scope, and ask.
4. Verify before claiming done — run the project's typecheck / lint / test for the touched region. Do not claim completion without fresh verification.
