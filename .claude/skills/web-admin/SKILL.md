---
name: web-admin
description: Web/UI domain admin for GOBAL AGENT — coordinates web development: design direction → build UI → audit → iterate. Routes to appropriate web skills based on task type. Modes — design (design-web only), build (design-web → build-ui), audit (review-frontend only), scaffold (fullstack-builder). It coordinates; it does NOT write UI code directly. Triggers — làm web nhiều bước, thiết kế rồi dựng UI, điều phối web, audit giao diện.
argument-hint: <web task> [design|build|audit|scaffold]
allowed-tools: Skill Agent Read Write Glob Bash
---

# Web Admin

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

### Alias map (tên cũ đã deprecate — giữ stub để không phá tham chiếu cũ)

| Alias cũ | Skill thực | Lý do đổi |
|---|---|---|
| design-ui-direction | design-web | đổi tên cho đúng phạm vi |
| build-ui-component | build-ui (mode `component`) | gộp vào mode |
| latex-math-renderer | latex-fix | repair là chức năng thật; mode render HTML đã bỏ |

> **KHÔNG phải alias:** `build-admin-dashboard` và `scaffold-course-platform` là skill
> sống, độc lập, có `references/` riêng — **không** bị gộp vào `build-ui`. (Bảng này
> từng khai sai là đã gộp; sửa 2026-08-01.)

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
- latex-fix → math repair (KaTeX/MathJax intersection) for math-heavy pages; latex-math-renderer là alias đã deprecate
- fullstack-builder → for new project scaffolding
- backend-engineer → for API layer in fullstack
