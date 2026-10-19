---
disable-model-invocation: true
name: "token-budget"
description: "Token budget manager for GOBAL AGENT — estimates, allocates, and tracks token usage per task and per session. Invoked before any fan-out dispatch or large operation. Enforces progressive disclosure tiers (Tier 1 ~100 token metadata, Tier 2 <5k token body, Tier 3 on-demand). Modes — estimate (calculate cost for a task), allocate (distribute budget across sub-tasks), track (log actual usage), overflow (handle budget exceeded: compress/shard/skip). It manages budgets; it does NOT execute tasks. Triggers — ước tính token, tốn bao nhiêu token, chi phí, budget, trước khi fan-out."
allowed-tools: "Read Bash"
argument-hint: "<task description> [estimate|allocate|track|overflow]"
---

# Token Budget

> **Source:** GOBAL evidence-first design and preflight amendment, shared resource budget.
> **Purpose:** Bound operations and context without assuming a vendor's model capacity.

## Hard gate

Use one aggregate budget for the entire request: coordinator, sub-admins, workers,
retries and verification all draw from it. Never give each worker the full shared pool.
Use runtime-reported context/token limits and actual usage when available. If the host
does not expose a metric, label it unknown; do not manufacture counts or savings.
No fixed vendor context assumption or unmeasured parallel-cost multiplier is portable.

## Evidence lane allocation

| Lane | Rounds | Queries | Source opens | Workers total |
|---|---:|---:|---:|---:|
| Fast non-research | 0 research | 0 default | 0 default | By justified task scope |
| Quick evidence | 1 | 3 | 2 | 0 |
| Standard evidence | 2 | 6 | 6 | 0 by default |
| Deep evidence | 3 | 12 | 12 | min(host capacity, 3) |

These are design ceilings, not measured optimum or latency guarantees. Count query
strings and source retrievals even when batched. Select Deep explicitly before research
delegation. Across non-research dispatch, use at most min(host capacity, 3) workers too;
their code/build tools follow the task's separately stated resource constraints.
If subagents are unavailable, sequential execution uses the same allocations.
Supplied local-source reading has an explicit files/pages/ranges budget; it is not
disguised as free unlimited ingestion. Search budget follows admin's on-demand protocol.

## Progressive disclosure

Tier 1 metadata is discovered by the host; its token cost varies by tokenizer and registry.
Tier 2 bodies load only for skills actually used; Tier 3 references/resources load only
when required. Keep context relevant, and retain direct passages needed for claim review.
Do not trade away verification to meet a speculative token estimate.

## Mode: estimate

Resolve task facets, evidence lane, local reading volume and available host capacity.
Estimate token/resource needs from actual source sizes and host measurements where possible;
label estimates as estimates with assumptions. Unknown input/output totals remain unknown.
Return lane, ceilings, estimated context need, metrics available and whether parallel
independent work warrants orchestration. Do not override the user's configured model.

## Mode: allocate

1. Record current totals and remaining query/open/round/worker/reading budget.
2. Reserve operations/context for coordinator review and synthesis.
3. Grant each independent worker a disjoint portion plus scoped sources and file ownership.
4. Require worker manifests to return consumed operations and remaining allocation.
5. Merge usage before any retry/re-plan; sub-admin handoff never resets the pool.

Parallelization itself does not establish lower token cost. Prefer inline work for small
or dependent tasks. Do not silently skip required acceptance criteria to fit a budget.

## Mode: track

Record actual search/open/worker counts and timestamps; token/cost metrics only when
reported by the runtime. If reuse matters, save a compact task log in the project with
lane, allocation, consumption, source-reading volume, limitations and measurement origin.
Distinguish estimates from observed values and static checks from actual model executions.
No percentage-saving claim without matched baseline measurements.

## Mode: overflow

Re-plan within the remaining allocation: compress redundant context, reuse fresh artifacts,
reduce optional depth with disclosure or perform bounded work sequentially. Preserve exact
passages needed to audit material claims. When ceilings are exhausted, stop with verified
partial results and NEI/CONTESTED gaps; no hidden budget extension.
Release tests are release gates, not a cost charged on each ordinary admin request.
