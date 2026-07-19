---
name: ship-validator
description: Ship validator for GOBAL AGENT — pre-deployment validation with verification-before-completion discipline. Modes: validate (run all checks), quick (critical checks only), report (generate validation report). Source: addyosmani (shipping-and-launch) + superpowers (verification-before-completion). It validates; it does NOT deploy (use deploy-orchestrator).
argument-hint: [validate|quick|report]
allowed-tools: Read Bash Glob Grep
---

# Ship Validator

> **Source:** addyosmani agent-skills (shipping-and-launch) + superpowers (verification-before-completion)
> **Purpose:** Pre-deployment validation with evidence-based verification.

## The Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

## Modes

| Mode | Checks | When to Use |
|------|--------|-------------|
| `validate` | All checks | Before any production deploy |
| `quick` | Critical only | Fast check before PR |
| `report` | All + generate report | Documentation/audit |

## Pre-Launch Checklist

### Code Quality
- [ ] All tests pass (not "should pass" — actually pass)
- [ ] Lint clean (0 errors, not partial check)
- [ ] Type check passes
- [ ] Build succeeds (exit 0, not just lint passing)
- [ ] No console.log or debugger statements

### Security
- [ ] No secrets in code (no API keys, passwords, tokens)
- [ ] No secrets in logs
- [ ] Input validation on all endpoints
- [ ] Auth checks on protected routes
- [ ] CORS configured correctly
- [ ] Security headers present
- [ ] Dependencies audited (npm audit / pip audit clean)

### Performance
- [ ] Core Web Vitals within budget (LCP ≤2.5s, INP ≤200ms, CLS ≤0.1)
- [ ] Images optimized (WebP/AVIF, srcset)
- [ ] Bundle size within budget
- [ ] No memory leaks in long-running pages

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Color contrast WCAG AA (4.5:1)
- [ ] Screen reader tested
- [ ] Touch targets ≥44px

### Infrastructure
- [ ] Environment variables set in deploy target
- [ ] Database migrations run
- [ ] CDN/cache configured
- [ ] SSL certificate valid
- [ ] Domain DNS correct

### Documentation
- [ ] README updated
- [ ] API docs current
- [ ] CHANGELOG updated
- [ ] Migration guide (if breaking changes)

## Verification Protocol

### The Gate Function

For EACH claim:
1. **IDENTIFY** — What command proves this claim?
2. **RUN** — Execute the FULL command (fresh, complete)
3. **READ** — Full output, check exit code, count failures
4. **VERIFY** — Does output confirm the claim?
5. **ONLY THEN** — Make the claim

### Common Failures

| Claim | Requires |
|-------|----------|
| Tests pass | Test command output: 0 failures (not previous run) |
| Linter clean | Linter output: 0 errors (not partial check) |
| Build succeeds | Build command: exit 0 |
| Bug fixed | Test original symptom: passes |
| Requirements met | Line-by-line checklist (not tests passing) |

### Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification

## Cross-References

- `deploy-orchestrator` → Execute deployment after validation
- `code-senior` → Code quality standards
- `security-review` → Security audit
- `monitor-setup` → Post-deploy monitoring

## Validation Checklist

### 1. Tests
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] No skipped/failing tests
- [ ] Coverage adequate (project threshold)

### 2. Security
- [ ] No secrets in code (grep for key patterns)
- [ ] No secrets in git history
- [ ] Dependencies scanned (no critical CVEs)
- [ ] Authz on all protected endpoints
- [ ] Input validation at all boundaries

### 3. Code Quality
- [ ] No debug logging in production code
- [ ] No console.log / print statements
- [ ] No commented-out code blocks
- [ ] Error handling complete (not just happy path)

### 4. Configuration
- [ ] Environment variables documented
- [ ] Default config safe for production
- [ ] Feature flags set correctly
- [ ] CORS configured for production origins

### 5. Dependencies
- [ ] Lockfile committed (package-lock, poetry.lock, etc.)
- [ ] No unexpected dependency changes
- [ ] No known critical vulnerabilities

### 6. Documentation
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Migration notes (if schema changed)

## Mode: validate
Run full checklist. Report pass/fail per item. Block deploy if any Critical fails.

## Mode: quick
Run only Critical checks: tests, secrets, CVEs. Fast gate.

## Mode: report
Generate validation report: timestamp, checks run, results, recommendations.

## Integration
- code-reviewer → code quality
- security-review → security audit
- deploy-orchestrator → deploy coordination
