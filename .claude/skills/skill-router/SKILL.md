---
name: skill-router
description: Skill router for GOBAL AGENT — routes requests to optimal skills based on task type. Modes: route (find best skill), discover (find available skills), suggest (recommend workflow). Source: gstack (router architecture) + addyosmani (using-agent-skills) + superpowers (using-superpowers). It routes; it does NOT invoke skills (that is the orchestrator's job).
argument-hint: <request> [route|discover|suggest|recommend|analyze]
allowed-tools: Read Write Bash Glob
---

# Skill Router

> **Source:** gstack (router architecture) + addyosmani (using-agent-skills) + superpowers (using-superpowers)
> **Purpose:** Route requests to the right skill.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `route` | Find best skill for request | User asks something, unsure which skill |
| `discover` | Find available skills | What skills do I have? |
| `suggest` | Recommend workflow | Complex task needing multiple skills |

## Router Architecture (from gstack)

Root skill dispatches to specialized skills:
- Planning → spec-writer, paper-read
- Building → code-senior, build-ui, backend-engineer
- Reviewing → code-reviewer, review-frontend, security-review
- Debugging → debug-investigator
- Deploying → deploy-orchestrator, ship-validator
- Learning → study-tutor, concept-explainer

## Decision Tree

```
User request
  ├── "Build/create/implement" → design-web → build-ui / code-senior
  ├── "Review/audit/check" → code-reviewer / review-frontend / security-review
  ├── "Fix/debug/error" → debug-investigator
  ├── "Plan/spec/design" → spec-writer → design-web
  ├── "Deploy/ship" → ship-validator / run-on-modal → deploy-orchestrator
  ├── "Learn/explain" → study-tutor → concept-explainer
  ├── "Research/paper" → paper-read → paper-synthesize
  ├── "Understand codebase" → understand-codebase → knowledge-graph
  └── "Turn paper into code / Notebook" → paper-to-notebook
```

## Skill Discovery (from superpowers)

- **Check before acting:** Even 1% chance a skill applies = MUST check
- **Skill priority:** Process skills first (brainstorming, debugging), then implementation
- **Rigid skills:** TDD, systematic-debugging must be followed exactly
- **Flexible skills:** Patterns can be adapted to context

## Cross-References

- `gobal-orchestrator` → Main orchestrator
- `learnings-db` → Learn which skill combos work
- `project-memory` → Project context for routing

## Mode: route

Find optimal skill(s) for a request:
1. Parse request → extract intent + domain + complexity
2. Check learnings-db for past similar requests
3. Check success rates per skill for this request type
4. Return: primary skill + supporting skills + confidence

### Routing Factors
| Factor | Weight | Source |
|--------|--------|--------|
| Skill description match | High | SKILL.md frontmatter |
| Past success rate | High | learnings-db |
| Token efficiency | Medium | logs/token-usage-*.md |
| User preference | Medium | project-memory/preferences.md |
| Recency | Low | Recent sessions weighted higher |

## Mode: recommend

Suggest skill improvements:
1. Analyze usage patterns (which skills invoked together, which skipped)
2. Identify gaps (requests with no good skill match)
3. Identify bloat (skills rarely used, high token cost)
4. Recommend: merge, split, deprecate, or create new skills

## Mode: analyze

Usage pattern analysis:
1. Read logs/ for skill invocation history
2. Calculate: invocation frequency, success rate, token cost, user satisfaction
3. Identify: most/least used, highest/lowest token cost, best/worst success rate
4. Report: patterns + recommendations

## Integration
- learnings-db → source of routing intelligence
- audit-log → routing decision history
- gobal-orchestrator → primary consumer of routing recommendations
- artifact-manager → track skill performance metrics
