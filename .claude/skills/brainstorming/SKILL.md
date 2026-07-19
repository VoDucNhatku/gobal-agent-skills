---
name: brainstorming
description: Brainstorming for GOBAL AGENT — explores user intent, requirements, and design BEFORE any implementation. MUST be used before any creative work: creating features, building components, adding functionality, or modifying behavior. Source: superpowers (brainstorming). It designs; it does NOT write code or invoke implementation skills.
argument-hint: <project description>
allowed-tools: Read Write Bash Glob WebSearch WebFetch
---

# Brainstorming

> **Source:** superpowers (brainstorming)
> **Purpose:** Turn ideas into fully formed designs through collaborative dialogue.

## HARD GATE

**Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.** This applies to EVERY project regardless of perceived simplicity.

---

## Checklist (Complete in Order)

1. **Explore project context** — check files, docs, recent commits
2. **Offer visual companion just-in-time** — NOT upfront. First time a question would be clearer shown than described, offer it then. If no visual question ever arises, never offer it.
3. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
5. **Present design** — in sections scaled to complexity, get approval after each section
6. **Write design doc** — save to `notes/design-<slug>.md` and commit
7. **Spec self-review** — quick check for placeholders, contradictions, ambiguity, scope
8. **User reviews written spec** — ask user to review before proceeding
9. **Transition to implementation** → invoke `writing-plans` skill

---

## The Process

### Understanding the Idea

- Check current project state first (files, docs, recent commits)
- If request describes multiple independent subsystems → flag immediately, suggest decomposition
- Ask questions one at a time — never overwhelm
- Focus on: purpose, constraints, success criteria
- Prefer multiple choice questions when possible

### Exploring Approaches

- Propose 2-3 different approaches with trade-offs
- Lead with your recommended option and explain why
- Present options conversationally

### Presenting the Design

- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify

### Design for Isolation

- Break system into smaller units with one clear purpose each
- Communicate through well-defined interfaces
- Each unit should be: understandable without reading internals, changeable without breaking consumers

### Working in Existing Codebases

- Explore current structure before proposing changes
- Follow existing patterns
- Include targeted improvements for existing problems (don't propose unrelated refactoring)

---

## After the Design

### Documentation

- Write validated design to `notes/design-<slug>.md`
- Commit the design document to git

### Spec Self-Review

After writing the spec, check:
1. **Placeholder scan:** Any "TBD", "TODO", vague requirements? Fix them.
2. **Internal consistency:** Do sections contradict? Does architecture match feature descriptions?
3. **Scope check:** Focused enough for one implementation plan?
4. **Ambiguity check:** Could any requirement be interpreted two ways? Pick one, make it explicit.

Fix issues inline. No need to re-review.

### User Review Gate

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Wait for user response. Only proceed once approved.

### Transition

**The terminal state is invoking `writing-plans`.** Do NOT invoke any implementation skill.

---

## Key Principles

- **One question at a time** — Don't overwhelm
- **Multiple choice preferred** — Easier to answer
- **YAGNI ruthlessly** — Remove unnecessary features
- **Explore alternatives** — Always propose 2-3 approaches
- **Incremental validation** — Present design, get approval before moving on

---

## Triggers

- "brainstorm", "design before coding", "b brainstorming", "lên ý tưởng", "thiết kế trước khi code".

## Integration

- `writing-plans` → ONLY skill to invoke after brainstorming (terminal state per this skill)
- `design-web` → visual design direction
- `spec-writer` → formal specification writing
- `gobal-orchestrator` → orchestrates the full pipeline

## Anti-Pattern

**"This Is Too Simple To Need A Design"** — Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences), but you MUST present it and get approval.

---

## Cross-References

- `writing-plans` → ONLY skill to invoke after brainstorming
- `design-web` → Visual design direction
- `spec-writer` → Formal specification writing
- `gobal-orchestrator` → Orchestrates the full pipeline
