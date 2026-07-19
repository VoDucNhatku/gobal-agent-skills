---
name: web-orchestrator
description: Web/UI domain orchestrator for GOBAL AGENT — coordinates web development: design direction → build UI → audit → iterate. Routes to appropriate web skills based on task type. Modes — design (design-web only), build (design-web → build-ui), audit (review-frontend only), scaffold (fullstack-builder). It orchestrates; it does NOT write UI code directly.
argument-hint: <web task> [design|build|audit|scaffold]
allowed-tools: Skill Agent Read Write Glob Bash
---

# Web Orchestrator

Coordinate web/UI development. Route to the right skill.

## Pipeline

```
Web Request
│
▼
design-web (if no design exists)
│
▼
build-ui (implement from design-record)
│
▼
review-frontend (audit UI for quality and slop)
│
▼
Iterate if needed
│
▼
Vietnamese report + artifacts
```

## Routing Rules

### Alias map (các tên cũ — chỉ giữ để không phá routing cũ; đổi tên thực bên dưới)

| Alias cũ | Skill thực | Lý do đổi |
|---|---|---|
| design-web | design-web | tên chuẩn theo Workbench |
| build-ui | build-ui | tên chuẩn theo Workbench |
| build-ui-component | build-ui (mode `component`) | gộp vào mode |
| build-admin-dashboard | build-ui (mode `admin`) | gộp vào mode |
| scaffold-course-platform | build-ui (mode `scaffold`) | gộp vào mode |
| latex-fix | latex-fix | tên chuẩn theo Workbench |

### Routing Rules (tên thực)

| Request Type | Primary Skill | Supporting Skills |
| ------------- | -------------- | ------------------ |
| "Thiết kế giao diện X" | `design-web` | — |
| "Dựng UI component/page/admin/scaffold từ design-record" | `build-ui` | mode: `component`/`page`/`admin`/`scaffold` |
| "Audit giao diện / slop / a11y" | `review-frontend` | build-ui |
| "Render / sửa công thức toán (KaTeX + MathJax)" | `latex-fix` | — |
| "Scaffold fullstack app" | `build-ui` (mode `scaffold`) + `backend-engineer` | design-web nếu chưa có design-record |
| "Build backend API / auth / DB" | `backend-engineer` | code-senior, security-review |
| "Fix UI bug" | `build-ui` / `code-senior` | review-frontend (audit sau fix) |

## Mode: design
Design direction only. No implementation. Output: design-record.

## Mode: build
Full build pipeline: design-web (if needed) → build-ui → review-frontend.

## Mode: audit
Audit existing UI. Output: findings + optional fixes.

## Mode: scaffold
Fullstack scaffold: detect stack → generate project structure → basic CRUD.

## Integration
- design-web → always first for new UI work
- build-ui → reads locked design-record FIRST
- review-frontend → checks production readiness and slop
- latex-math-renderer → for math-heavy pages
- fullstack-builder → for new project scaffolding
- backend-engineer → for API layer in fullstack
