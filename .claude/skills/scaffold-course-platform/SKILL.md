---
name: "scaffold-course-platform"
description: "Scaffolds a course-selling LMS platform. Modes: scaffold. Reads stack defaults from references/stack-matrix.md, overrides recorded in audit-log."
argument-hint: "<resource-key>"
allowed-tools: "Skill Agent Read Write Edit Glob Bash Grep"
---

# Scaffold Course Platform — Scaffold Reference

> **Purpose:** Provide the reference stack matrix and scaffold rules for a course-selling platform used by `code-orchestrator`. Act as the registry-resolved entrypoint; the canonical defaults live in `references/`.

## Role

This skill does not build the entire platform alone. It is the gatekeeper that `code-orchestrator` and `web-orchestrator` consult before writing any project file. The heavy design and content scaffolding is delegated via fan-out to `design-web`, `build-ui`, and `build-admin-dashboard`.

## Modes

| Mode | Use it when | Output |
|------|-------------|--------|
| `stack` (default) | Resolve the approved layer stack for a new project | Stack matrix summary |
| `scaffold` | Bootstrap project skeleton from the approved stack | Project tree + README stub + first-page scaffold |
| `audit` | Verify a scaffold against the approved stack matrix | Findings only |

## Procedure

1. Read `references/stack-matrix.md` for the approved layer choices (frontend, backend, database, auth, payments, storage). If a layer is intentionally overridden, record it in `audit-log` before continuing.
2. For `scaffold` mode, produce: directory map, framework-specific init commands, environment variable stub, and a `README.md` mapping each layer.
3. Keep domain model guidance aligned with `course-domain-model.md`; do not introduce entity shapes that diverge from the authorized schema.
4. For payments, default to the approved provider (Stripe or LemonSqueezy) and require server-side webhook verification — never gate access on a client-side role.
5. After scaffolding, hand off to `design-web` + `build-ui` so branding and components are generated against the saved design file.

## Scaffold procedure detail

For `scaffold` mode, emit exactly these artifacts unless the user overrides:

- `apps/web/` — Next.js app (or equivalent) with route groups for marketing, course viewer, and admin
- `apps/api/` or `server/` — backend entry with auth, course, enrollment, and payment webhook routes
- `packages/ui/` — shared component library primed by `build-ui`
- `packages/db/` — schema + migrations matching `course-domain-model.md`
- `.env.example` — list of required env vars with descriptions; never commit real secrets
- `README.md` — one paragraph per layer, init commands, and the approved provider URL

For every webhook route, add a TODO comment where the signature verification belongs so the implementation cannot accidentally accept unverified events.

## Anti-patterns

- ❌ Gate access in the client (JWT in localStorage, `useUser().role`, hidden CSS class). A role claim in the browser is a UI hint, not a security boundary.
- ❌ Grant access on a client-side `/success` redirect. Access comes from the payment webhook writing an `Order` + `Enrollment`.
- ❌ Invent entity shapes that diverge from the authorized domain model. Align with `course-domain-model.md` first.
- ❌ Skip the post-scaffold handoff to `design-web`. Branding produced without a locked token file is slop-by-default.

## Triggers

- "scaffold course platform", "new course site", "xây nền tảng khóa học", "dựng LMS", "init course project".

## Integration

- `code-orchestrator` — primary caller
- `design-web` / `build-ui` — branding and components
- `build-admin-dashboard` — admin shell
- `audit-log` — record stack decisions
- `token-budget` — estimate cost before spawning subagents
