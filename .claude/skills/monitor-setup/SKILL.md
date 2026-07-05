---
name: "monitor-setup"
description: "Monitoring setup for GOBAL AGENT — configures observability for deployed applications. Modes: setup (new monitoring), verify (check existing), dashboard (create dashboard), alerts (configure alerts). Source: addyosmani (observability-and-instrumentation). It sets up; it does NOT investigate incidents (use debug-investigator for that)."
argument-hint: "<app | service> [setup|verify|dashboard|alerts]"
allowed-tools: "Read Write Bash Glob"
---

# Monitor Setup

> **Source:** addyosmani agent-skills (observability-and-instrumentation)
> **Purpose:** Configure observability — metrics, logs, alerts, dashboards.

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `setup` | New monitoring config | Deploying new service |
| `verify` | Check existing setup | Audit current observability |
| `dashboard` | Create dashboard | Visualize key metrics |
| `alerts` | Configure alerts | Set up incident notification |

## Step 1: Define "Working"

Before adding any instrumentation, write 2-4 on-call questions:

1. Can a user complete the core flow?
2. Is the API responding within SLA?
3. Are background jobs processing?
4. Is the database healthy?

These questions determine WHAT to measure.

## Step 2: Pick the Right Signal

| Signal | Answers | Use For |
|--------|---------|---------|
| Metrics | "How many / how fast?" | Rate, errors, duration |
| Traces | "Where is the time spent?" | Distributed request flow |
| Logs | "Why did it happen?" | Context, debugging |

## Step 3: Structured Logging

### Pattern

```python
# BAD: string interpolation
logger.info(f"Payment {id} failed for user {userId}")

# GOOD: structured fields
logger.warn({
    "event": "payment_failed",
    "paymentId": id,
    "provider": "stripe",
    "errorCode": err.code,
    "attempt": n
}, "payment failed")
```

### Rules

- JSON format for machine parsing
- Stable event names (don't change randomly)
- Correlation IDs mandatory (trace every request)
- NEVER log: passwords, tokens, PII, raw request bodies

## Step 4: Metrics (RED/USE)

### RED (for services)
- **Rate:** Requests per second
- **Errors:** Error rate (4xx, 5xx)
- **Duration:** P50, P95, P99 latency

### USE (for resources)
- **Utilization:** CPU, memory, disk usage
- **Saturation:** Queue depth, connection pool
- **Errors:** Error rate by resource

## Step 5: Distributed Tracing

- Use OpenTelemetry for vendor-neutral tracing
- Trace key user journeys
- Sample appropriately (not 100% in production)

## Step 6: Alerting

### Rules

1. Must be actionable — if page wakes you up, it must need human action
2. Must link to runbook — how to investigate/fix
3. Must have justified threshold/duration
4. Two severities only: **page** (wake up) and **ticket** (next business day)

### Cardinality Rule

Labels from small fixed sets only.
- **NEVER:** user IDs, raw URLs, error message text as labels
- These explode cardinality and break monitoring systems

### Alert Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Alert on everything | Alert fatigue | Only alert on symptoms |
| No runbook link | Can't act on alert | Link to investigation steps |
| Too many severities | Confusion | Page vs ticket only |
| Threshold without justification | Random noise | Base on historical data |

## Step 7: Verify the Telemetry

- Trigger a test event → verify it appears in dashboard
- Check logs are structured and searchable
- Verify traces show complete request flow
- Test alerts fire correctly (in staging)

## Cross-References

- `deploy-orchestrator` → Deploy with monitoring
- `debug-investigator` → Use logs/traces for debugging
- `ship-validator` → Validate before deploy

## Observability Stack

### Metrics (RED)
- **Rate** — Requests per second
- **Errors** — Error rate (4xx + 5xx)
- **Duration** — Response time (p50, p95, p99)

### Logs
- Structured JSON format
- Stable event names
- Correlation IDs for request tracing
- No PII/secrets in logs

### Alerts
| Severity | Response Time | Channel |
|----------|--------------|---------|
| Critical | Immediate | PagerDuty / SMS |
| Warning | 15 min | Slack / Email |
| Info | Daily digest | Email |

### Dashboard
Key panels:
1. Request rate over time
2. Error rate by endpoint
3. Response time percentiles
4. System resources (CPU, memory, disk)
5. Error log stream (latest)

## Mode: setup
Full monitoring setup:
1. Detect app type (web service, API, batch job)
2. Recommend observability stack (Prometheus, Grafana, etc.)
3. Generate config files
4. Instrument code (metrics endpoints, log format)
5. Configure alerts
6. Create dashboard

## Mode: verify
Check existing monitoring:
1. What's currently monitored?
2. Are RED metrics present?
3. Are alerts configured?
4. Is dashboard accessible?
5. Gaps → recommend additions

## Mode: dashboard
Create/update dashboard:
1. Identify key metrics for this service
2. Design dashboard layout
3. Generate dashboard config (Grafana JSON, etc.)

## Integration
- deploy-orchestrator → deploy coordination
- debug-investigator → incident investigation
- backend-engineer → instrumentation in code
