---
name: "token-budget"
description: "Token budget manager for GOBAL AGENT — estimates, allocates, and tracks token usage per task and per session. Invoked before any fan-out dispatch or large operation. Enforces progressive disclosure tiers (Tier 1 ~100 token metadata, Tier 2 <5k token body, Tier 3 on-demand). Modes — estimate (calculate cost for a task), allocate (distribute budget across sub-tasks), track (log actual usage), overflow (handle budget exceeded: compress/shard/skip). It manages budgets; it does NOT execute tasks."
argument-hint: "<task description> [estimate|allocate|track|overflow]"
allowed-tools: "Read Bash"
---

# Token Budget

Manage token economy for GOBAL AGENT. Every task has a budget. Stay within it.

## Token Estimation Rules

| Task Type | Input Tokens | Output Tokens |
|-----------|-------------|---------------|
| Simple Q&A | 1-2k | 0.5-1k |
| Single skill invoke | 2-5k | 1-3k |
| Multi-skill (solo) | 5-15k | 3-10k |
| Fan-out (2-3 agents) | 10-30k | 10-30k |
| Fan-out (4+ agents) | 20-50k | 20-50k |
| Full research pipeline | 30-80k | 20-60k |

## Progressive Disclosure Tiers

```
Tier 1 (always loaded, ~100 token): name + description only
Tier 2 (on trigger, <5k token): SKILL.md body
Tier 3 (on demand): references/ + scripts/
```

**Rule:** Never load Tier 2 unless the skill is actively being invoked. Never load Tier 3 unless Tier 2 references it.

## Budget Allocation (fan-out)

When orchestrator decides fan-out:

1. **Estimate total budget** = sum of sub-task estimates + 20% overhead for synthesis
2. **Per-agent budget** = total / N agents
3. **Per-agent context spec** = only include what fits in budget
4. **If overflow** → apply overflow strategy (see below)

## Overflow Strategies

| Strategy | When | Action |
|----------|------|--------|
| Compress | Context too large | Summarize prior artifacts, drop redundant context |
| Shard | Too many sub-tasks | Split into batches, run sequentially |
| Skip | Low-value sub-task | Drop it, note in synthesis |
| Reduce depth | Output too large | Switch to lighter mode (e.g., gist instead of summary) |

## Session Budget

```
Total session: 200k tokens (Claude Opus default)
├── System prompt: 10k (5%)
├── Skill metadata (Tier 1): 5k (2.5%)
├── Active skill body (Tier 2): 5k (2.5%)
├── Conversation history: 50k (25%)
├── Artifacts (Tier 3, on demand): 30k (15%)
└── Working buffer: 100k (50%)
```

**Red flag:** If working buffer drops below 30%, trigger context-compressor.

## Mode: estimate

Input: task description + context size
Output: `{input_tokens, output_tokens, total, tier_required, fan_out_worthy}`

## Mode: allocate

Input: N sub-tasks + total budget
Output: per-task budget allocation + overflow plan

## Mode: track

Log actual token usage per skill invocation. Write to `logs/token-usage-<date>.md`.

## Mode: overflow

When budget exceeded: apply strategy, re-estimate, retry.
