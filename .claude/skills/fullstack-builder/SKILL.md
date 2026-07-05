---
name: "fullstack-builder"
description: "Fullstack builder for GOBAL AGENT — scaffolds and implements fullstack features with vertical slices. Modes: scaffold (new project), add-feature (add to existing), integrate (connect layers). Source: gstack (design-html, spec) + addyosmani (frontend-ui-engineering, incremental-implementation) + superpowers. It builds; it does NOT decide design direction (use design-web) or write specs (use spec-writer)."
argument-hint: "<project | feature> [scaffold|add-feature|integrate]"
allowed-tools: "Read Write Edit Glob Bash"
---

# Fullstack Builder

> **Source:** gstack (design-html, spec) + addyosmani (frontend-ui-engineering, incremental-implementation) + superpowers
> **Purpose:** Scaffold and implement fullstack features with vertical slices.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `scaffold` | New project structure | Starting a new project |
| `add-feature` | Add feature to existing | Extending existing codebase |
| `integrate` | Connect layers | Connecting frontend to backend |

## Increment Cycle

```
Implement → Test → Verify → Commit → Next slice
   ^                              |
   |______________________________|
```

## Scaffold: New Project

### Stack Detection

Detect from context or ask:
- Frontend: React, Next.js, Vue, Svelte, Astro
- Backend: Node/Express, Python/FastAPI, Go, etc.
- Database: PostgreSQL, MongoDB, SQLite
- Styling: Tailwind, CSS modules, styled-components

### Project Structure

```
project/
  ├── src/
  │   ├── components/     # Reusable UI
  │   ├── pages/          # Routes/views
  │   ├── api/            # Backend handlers
  │   ├── models/         # Data models
  │   ├── lib/            # Shared utilities
  │   └── styles/         # Global styles
  ├── tests/
  ├── docs/
  └── config files
```

### Generated Items

1. Project structure with best-practice layout
2. Base configuration (linting, formatting, testing)
3. CRUD skeleton (one resource, end-to-end)
4. Basic auth (if requested)
5. README with setup instructions

## Add Feature: Vertical Slice

### Component Architecture (addyosmani)

- **Colocate everything:** component + test + stories + hook + types in same folder
- **Composition over configuration:** Build small, compose into larger
- **Keep components focused:** One thing per component
- **Separate data fetching from presentation:** Container/presentation pattern

### State Management Hierarchy

```
Local → Lifted → Context → URL → Server → Global store
```

Avoid prop drilling >3 levels. Use the simplest solution that works.

## Integrate: Connect Layers

### API Integration Pattern

1. Define contract first (types/interfaces)
2. Implement backend handler
3. Implement frontend consumer
4. Wire together with error handling
5. Test the full flow

### Integration Checklist

- [ ] Types shared between frontend and backend
- [ ] Error handling at every boundary
- [ ] Loading states in UI
- [ ] Error states in UI
- [ ] Auth check on protected routes
- [ ] CORS configured correctly

## Implementation Rules

- **Rule 0:** Simplicity First
- **Rule 0.5:** Scope Discipline — touch only what task requires
- **Rule 1:** One Thing at a Time
- **Rule 2:** Keep It Compilable
- **Rule 3:** Feature Flags for Incomplete Features

## Cross-References

- `design-web` → Design before scaffolding
- `build-ui` → UI implementation
- `code-senior` → Code quality patterns
- `backend-engineer` → Backend implementation
- `tdd-enforcer` → Test-first for new features

## Stack Detection

| Signal | Stack |
|--------|-------|
| `next.config.*` exists | Next.js |
| `package.json` has "react" | React |
| `package.json` has "vue" | Vue |
| No JS framework detected | Vanilla or ask user |
| `manage.py` exists | Django |
| `requirements.txt` has "fastapi" | FastAPI |
| `go.mod` exists | Go |
| `Cargo.toml` exists | Rust |

If no signal → ask user for stack preference.

## Mode: scaffold

### Project Structure
Generate based on detected/specified stack:

```
project/
├── src/
│   ├── components/     # Reusable UI
│   ├── pages/          # Routes (or app/ for Next.js App Router)
│   ├── lib/            # Utilities, helpers
│   ├── styles/         # Global styles
│   └── types/          # TypeScript types
├── tests/
│   ├── unit/
│   └── integration/
├── public/             # Static assets
├── config files        # package.json, tsconfig, etc.
└── README.md
```

### Generated Items
1. Project structure (directories + config files)
2. Base component library (Button, Input, Card, Modal)
3. Routing setup (if applicable)
4. Basic CRUD skeleton (1 entity as example)
5. Auth skeleton (login/logout, session management)
6. Test setup (framework config + example test)
7. README with setup instructions

### Quality Standards
- TypeScript strict mode (if TS)
- ESLint + Prettier configured
- Environment variable pattern established
- Error boundary / error handling pattern
- Loading + error + empty states in components

## Mode: add-feature
Add a feature to existing project:
1. Read existing structure (understand-codebase)
2. Follow existing patterns
3. Generate feature files in correct locations
4. Wire up routing/integration

## Mode: setup
Configuration only:
1. Detect or ask for stack
2. Generate config files (tsconfig, eslint, etc.)
3. Set up folder structure
4. No code implementation

## Integration
- design-web → for design decisions
- build-ui → for UI implementation
- backend-engineer → for API layer
- code-senior → for implementation quality
- tdd-enforcer → for test setup
