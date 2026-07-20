---
name: rollback-manager
description: Rollback manager for GOBAL AGENT — handles emergency rollback of deployments. Modes: assess (evaluate situation), execute (perform rollback), verify (confirm recovery). Source: addyosmani (shipping-and-launch, ci-cd-and-automation) + gstack (land-and-deploy). It manages rollback; it does NOT investigate root cause (use debug-investigator).
argument-hint: <incident | deployment> [assess|execute|verify]
allowed-tools: Read Write Bash Glob
---

# Rollback Manager

> **Source:** addyosmani agent-skills (shipping-and-launch, ci-cd-and-automation) + gstack (land-and-deploy)
> **Purpose:** Emergency rollback with structured decision-making.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `assess` | Evaluate situation | Incident detected |
| `execute` | Perform rollback | Decision to rollback made |
| `verify` | Confirm recovery | After rollback deployed |

## Decision Matrix

| Situation | Action |
|-----------|--------|
| Error rate >2x baseline | Rollback immediately |
| P95 latency >50% above | Rollback immediately |
| Data corruption | Rollback + investigate |
| Security vulnerability | Rollback + incident response |
| Performance degradation | Hold or rollback based on thresholds |
| User reports spike | Assess severity, likely rollback |

## Rollback Triggers

The full Advance/Hold/Roll-back threshold table (error rate, P95 latency, client JS
errors, business metrics) is owned by **`deploy-orchestrator`** (`### Rollout Decision
Thresholds`) — it decides the whole canary progression, not just rollback. This skill
only needs the **Roll back** column: error rate >2x baseline, P95 latency >50% above,
client JS errors >0.1% sessions, business metrics decline >5%. Same numbers, single
source — invoke `deploy-orchestrator` if Advance/Hold values are needed too.

## Rollback Process

### 1. Assess
- What's the impact? (users affected, severity)
- What's the suspected cause?
- Is there a quick fix or do we need to roll back?
- Check: Can we hotfix instead?

### 2. Decide
- Rollback: Previous known-good version
- Hotfix: Targeted fix on top of current
- Hold: Monitor, don't act yet

### 3. Execute
- Deploy previous version (git revert / previous image)
- Keep current version tagged for investigation
- Don't delete anything until verified stable

### 4. Verify
- Metrics return to baseline
- Error rate normalizes
- User reports stop
- Core flows work end-to-end

### 5. Investigate (parallel)
- While stable, investigate root cause
- Use debug-investigator for systematic approach
- Document findings for post-mortem

## Rollback Safety

- **Data migrations:** Rollback must handle schema changes safely
- **Feature flags:** Can disable without redeploying
- **Database:** Consider rollback scripts for schema changes
- **External integrations:** Verify external state after rollback

## Cross-References

- `deploy-orchestrator` → Deployment coordination
- `debug-investigator` → Root cause analysis
- `ship-validator` → Pre-deploy validation
- `monitor-setup` → Verify metrics after rollback

## Mode: assess

Evaluate the situation:
1. **Scope** — Full outage or partial? Which services affected?
2. **Last known good** — Identify last working version (git tag, deploy timestamp)
3. **Impact** — Revenue/users affected? SLA breach?
4. **Strategy options:**
   - Revert commit (git revert)
   - Switch to previous version (blue-green)
   - Rollback database migration (if applicable)
   - Feature flag disable (if applicable)

Output: assessment + recommended strategy + risk of each option.

## Mode: execute

Perform the rollback:
1. Confirm strategy with user (unless critical — then execute immediately)
2. Execute chosen strategy
3. Verify rollback completed (version check, health check)
4. Monitor for stability (5 min observation)

## Mode: verify

Confirm recovery:
1. Health checks pass?
2. Error rates back to normal?
3. Key metrics restored?
4. User-facing functionality working?
5. Rollback complete → document incident

## Rollback Principles
- Speed over perfection in emergencies
- Preserve evidence for post-mortem
- Communicate status to stakeholders
- Never rollback without knowing what broke (assess first)
- Always verify after rollback

## Integration
- deploy-orchestrator → deploy coordination
- monitor-setup → verify health after rollback
- debug-investigator → root cause analysis (after recovery)
