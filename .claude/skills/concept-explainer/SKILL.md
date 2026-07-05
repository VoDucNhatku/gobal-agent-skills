---
name: "concept-explainer"
description: "Concept explainer for GOBAL AGENT — explains complex concepts at the right depth for the learner. Modes: eli5 (plain-language intuition with one analogy + toy example), deep-dive (technical depth with examples), analogy (find the right comparison). Source: gstack (learn) + addyosmani (context-engineering). It explains; it does NOT tutor (use study-tutor for full learning sessions)."
argument-hint: "<concept> [eli5|deep-dive|analogy]"
allowed-tools: "Read Write Bash Glob WebSearch WebFetch"
---

# Concept Explainer

> **Source:** gstack (learn) + addyosmani (context-engineering)
> **Purpose:** Explain concepts at the right depth. One concept, one explanation.

## Modes

| Mode | Depth | When to Use |
|------|-------|-------------|
| `eli5` | Plain language, one analogy + toy example | First exposure, non-expert |
| `deep-dive` | Technical with code/examples | Practitioner, needs implementation detail |
| `analogy` | Find the right comparison | Abstract concept needs concrete anchor |

---

## Mode: eli5

### Structure

1. **One-sentence gist** — What is this, in one sentence?
2. **The analogy** — One comparison from everyday life. Not "it's like a database" — be specific: "it's like a library catalog that remembers every book you've ever borrowed."
3. **Toy example** — Minimal concrete example (code, diagram, or numbers) showing the concept in action
4. **Why it matters** — One paragraph on real-world impact
5. **Common misconception** — One thing people get wrong about this
6. **Next step** — Where to go deeper (specific resource or skill)

### Rules
- **One analogy only.** Multiple analogies confuse.
- **Toy example must run** — if code, it must be copy-paste executable
- **No jargon without definition** — first use of any technical term gets `thuật ngữ tiếng Việt (English term)`
- **Active voice, user-side labels**

---

## Mode: deep-dive

### Structure

1. **Precise definition** — Formal definition with notation if applicable
2. **How it works** — Step-by-step mechanism
3. **Implementation** — Code example (real, runnable)
4. **Trade-offs** — When to use vs not use
5. **Edge cases** — Common pitfalls
6. **Related concepts** — What connects to this

### Rules
- Code examples in the project's language (infer from codebase)
- Show both "right" and "wrong" implementations
- Cite source papers/docs where the concept originated
- Preserve all quantitative details exactly

---

## Mode: analogy

### Process

1. **Identify the core mechanism** — What does the concept actually DO?
2. **Find the domain** — What world does the learner already understand?
3. **Map 1:1** — Every part of the analogy must map to a part of the concept
4. **State the limits** — Where the analogy breaks down (every analogy does)

### Rules
- Never use the first analogy that comes to mind (it's usually a cliché)
- Prefer analogies from the learner's stated domain
- Always state where the analogy breaks — false analogies cause more confusion than no analogy

---

## Triggers

- "explain X", "eli5", "deep dive", "analogy for X", "giải thích", "thuật ngữ là gì", "so sánh cho dễ hiểu".

## Integration

- `study-tutor` — full learning session following this concept
- `knowledge-quiz` — test retention after the explanation
- `paper-read` / `paper-method` — source paper context; usually invoked by `study-tutor` rather than research-orchestrator directly

## Progressive Disclosure

- First pass: gist + analogy (always)
- Second pass: toy example + why it matters
- Third pass (on request): deep-dive with implementation

---

## Cross-References

- `study-tutor` → Full learning session with this concept
- `knowledge-quiz` → Test understanding after explanation
- `paper-read` → Source paper for research concepts
- `paper-method` → Technical implementation details
