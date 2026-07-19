---
name: build-admin-dashboard
description: Generates production-grade admin surfaces with CRUD tables, role-gated access, and analytics. Modes: admin, scaffold, audit. Requires design tokens from design-web.
argument-hint: <resource-key>
allowed-tools: Skill Agent Read Write Edit Glob Bash Grep
---

# Build Admin Dashboard — Admin Surface Builder

> **Purpose:** Produce an authenticated admin shell with CRUD tables, search/filter, role-gated access, and an analytics snapshot so an operator can manage platform resources without leaving the seat.

## Role and scope

This skill generates production-grade admin surfaces using the project’s chosen UI stack and token system. It consumes design tokens from `design-web` (`notes/design-<slug>.md`) and accesses the `references/` data that ships with this skill for layout patterns and component defaults.

It **does not** run without an authenticated context. The owner of any rendered admin screen still needs a server-side authorization boundary (RLS / server action / route handler). This skill only produces the client orchestration; security remains server-side.

## Modes

| Mode | Use it when | Output |
|------|-------------|--------|
| `admin` (default) | Build one CRUD resource with role-gated shell | Scaffolded page/routes + tables + search/filter + actions |
| `scaffold` | Bootstrap the entire admin module (resources + nav + layout shell) | Directory of pages + shared shell + i18n stub |
| `audit` | Review an existing admin module for slop, a11y, and token consistency | Findings in chat or file |

## Procedure

1. Read the existing design token file (`notes/design-<slug>.md`) or ask up to 3 focused blocker questions when the design has not been created yet.
2. Enumerate the target resources (properties, relations, searchable fields, role matrix).
3. Scaffold routes, pages, and a shared shell with:
   - data table w/ sort + filter + pagination,
   - inline create/edit/delete actions gated by role,
   - optimistic UI + error/empty/loading states,
   - audit log entries via `audit-log` for mutating actions.
4. Wire a server-side authorization boundary (RLS policy / route handler / server action) so every mutation and every gated read is authorized.
5. Run `review-frontend` at the end of an admin build to catch slop and a11y regressions before handoff.

## Design tokens

This skill reads the locked design file created by `design-web`. Always reuse tokens from the saved artifact; do not invent new colors, type scale, or spacing values inline.

## Integration

Required cross-cutting skills used by this skill:
- `design-web` — locked token source (read `notes/design-<slug>.md`)
- `review-frontend` — post-build a11y + slop audit
- `audit-log` — record mutations with materiality filter
- `token-budget` — estimate fan-out cost before spawning subagents
- `reuse-checker` — check existing admin modules/specs before rebuilding

## Triggers

- "build admin", "scaffold dashboard", "CRUD table", "admin shell", "role-gated UI", "xây trang quản trị", "dựng admin", "bảng quản lý", "quản lý tài nguyên".
