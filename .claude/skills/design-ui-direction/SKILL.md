---
name: design-ui-direction
description: Design intelligence data for GOBAL AGENT — citation library (anti-slop bans, palettes, type pairings, style archetypes). Quoted at runtime by design-web and review-frontend. It is data, not logic; it does NOT issue instructions, generate code, or make UI decisions.
argument-hint: (none — auto-loaded by peer skills)
allowed-tools: Skill Agent Read Write Glob Bash
---

# Design UI Direction — Reference Data

> **Role:** This directory holds **shared design reference tables** consumed by `design-web` and `review-frontend` at runtime.
> This file is a stub so the skill registry resolves it; the actual content lives in `references/`.

## References (auto-read by peer skills)

| File | Consumer | Purpose |
|------|----------|---------|
| `design-web/references/anti-slop-bans.csv` | design-web, review-frontend | Explicitly banned patterns (fonts, gradients, layouts) |
| `design-web/references/palettes.csv` | design-web | Named hex token sets by archetype |
| `design-web/references/type-pairings.csv` | design-web | Display + body face pairings |
| `design-web/references/style-archetypes.csv` | design-web, review-frontend | Named mood/industry archetypes |

## Assets

| File | Purpose |
|------|---------|
| `assets/artifact-preview-template.html` | Preview scaffold for design artifacts |

## How It's Used

`design-web` reads these tables to ground palette, type, and layout choices in concrete tokens rather than defaults. `review-frontend` reads `anti-slop-bans.csv` + `style-archetypes.csv` to score outputs.
This skill **never runs alone** — invoke `design-web` or `review-frontend` for actual design work.
