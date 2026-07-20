---
name: deploy-orchestrator
description: Deploy orchestrator for GOBAL AGENT — coordinates deployment pipeline: validate → ship → monitor → rollback. Modes: ship (pre-ship validation + deploy), monitor (setup monitoring), rollback (emergency rollback), canary (staged rollout). Source: addyosmani (ci-cd-and-automation, shipping-and-launch) + gstack (land-and-deploy, ship). It orchestrates; it does NOT execute deploy commands directly.
argument-hint: <deploy task> [ship|monitor|rollback|canary]
allowed-tools: Skill Read Write Bash Glob
---

# Deploy Orchestrator

> **Source:** addyosmani agent-skills (ci-cd-and-automation, shipping-and-launch) + gstack (land-and-deploy, ship)
> **Purpose:** Coordinate deployment pipeline with quality gates.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `ship` | Pre-ship validation + deploy | Ready to deploy |
| `monitor` | Setup monitoring | Post-deploy observability |
| `rollback` | Emergency rollback | Something went wrong |
| `canary` | Staged rollout | Gradual traffic shift |
| `modal-gpu` | Deploy AI to Serverless GPU | Run models on Modal cloud |

## Ship: Pre-Ship Validation

### Quality Gate Pipeline

Run ALL gates in order. No gate can be skipped:

1. **Lint** — Code style, no errors
2. **Type Check** — TypeScript/Python types pass
3. **Unit Tests** — All pass
4. **Build** — Production build succeeds
5. **Integration Tests** — Cross-component tests pass
6. **E2E Tests** (optional) — Critical paths work
7. **Security Audit** — No new vulnerabilities
8. **Bundle Size** — Within budget

### Pre-Launch Checklist

- [ ] Code quality: lint clean, types pass, tests pass
- [ ] Security: no new vulnerabilities, secrets not exposed
- [ ] Performance: Core Web Vitals within budget
- [ ] Accessibility: WCAG AA minimum
- [ ] Infrastructure: deploy config ready, env vars set
- [ ] Documentation: README updated, API docs current

### Feature Flag Strategy

```
Deploy with flag OFF
  → Enable for team
    → Canary (5%)
      → Gradual (25% → 50% → 100%)
        → Clean up (within 2 weeks)
```

Every flag has:
- **Owner:** Who is responsible
- **Expiration:** When to remove it
- **Cleanup deadline:** Within 2 weeks of full rollout

### Rollout Decision Thresholds

| Metric | Advance | Hold | Roll back |
|--------|---------|------|-----------|
| Error rate | Within 10% baseline | 10-100% above | >2x baseline |
| P95 latency | Within 20% | 20-50% above | >50% above |
| Client JS errors | No new types | <0.1% sessions | >0.1% sessions |
| Business metrics | Neutral/positive | Decline <5% | Decline >5% |

### Rollback Triggers

- Error rate >2x baseline
- P95 latency >50% above baseline
- User reports spike
- Data integrity issues
- Security vulnerability discovered

## Monitor: Post-Deploy Observability (handoff — không chép nội dung)

Toàn bộ chi tiết kỹ thuật — on-call questions, structured logging, RED/USE metrics,
alerting rules, cardinality rule — thuộc về **`monitor-setup`**; invoke skill đó thay vì
lặp lại ở đây. Orchestrator này chỉ quyết định **khi nào**: monitoring phải sẵn sàng
TRƯỚC khi bật canary, và được verify lại sau mỗi lần deploy.

## Rollback: Emergency Procedures (handoff — không chép nội dung)

Chi tiết — decision matrix, 5-step rollback process, blue-green switch, schema-migration
safety — thuộc về **`rollback-manager`**; invoke skill đó. Orchestrator này chỉ giữ phần
quyết định: bảng **Rollout Decision Thresholds** ở trên là nguồn canonical duy nhất cho
cả 3 cột Advance/Hold/Roll back (rollback-manager chỉ trích cột Roll back, không lặp lại
bảng); mode `rollback` bên dưới nói thứ tự gọi.

## Cross-References

- `code-senior` → Code quality before deploy
- `security-review` → Security audit before ship
- `ship-validator` → Pre-launch validation
- `monitor-setup` → Observability setup
- `rollback-manager` → Rollback procedures

## Pipeline

```
Deploy Request
│
▼
ship-validator (pre-ship checks)
│
▼
Deploy (user executes or CI runs)
│
▼
monitor-setup (if not already configured)
│
▼
Rollback available if needed
```

## Routing Rules

| Request Type | Primary Skill | Supporting Skills |
|-------------|--------------|-------------------|
| "Deploy to production" | ship-validator | code-reviewer, security-review |
| "Setup monitoring" | monitor-setup | — |
| "Rollback deployment" | rollback-manager | monitor-setup |
| "Pre-ship check" | ship-validator | code-reviewer, security-review |
| "Chạy trên Modal / VRAM estimate" | run-on-modal | — |

## Mode: modal-gpu
1. Run run-on-modal to estimate VRAM and generate Modal app
2. Review cost estimate with user
3. Deploy function to Modal

## Mode: ship
1. Run ship-validator (all checks must pass)
2. If checks fail → report issues, stop
3. If checks pass → present deploy options
4. After deploy → verify health

## Mode: monitor
1. Check existing monitoring setup
2. If none → setup from scratch
3. If exists → verify coverage, suggest improvements

## Mode: rollback
1. Assess situation (partial deploy? full failure?)
2. Determine rollback strategy (revert commit? switch version?)
3. Execute rollback
4. Verify recovery

## Integration
- ship-validator → pre-deployment gate
- monitor-setup → observability
- rollback-manager → emergency recovery
- code-reviewer → code quality gate before deploy
- security-review → security gate before deploy
