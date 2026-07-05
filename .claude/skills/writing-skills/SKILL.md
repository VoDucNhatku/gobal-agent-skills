---
name: "writing-skills"
description: "Writing skills for GOBAL AGENT — meta skill for creating new GOBAL skills following progressive disclosure, token economy, and provenance rules. Source: superpowers (writing-skills). Use when creating a new skill for the GOBAL ecosystem."
argument-hint: "<skill-name> <source-repo>"
allowed-tools: "Read Write Bash Glob WebSearch WebFetch"
---

# Writing Skills

> **Source:** superpowers (writing-skills)
> **Purpose:** Create new GOBAL skills that follow progressive disclosure, token economy, and provenance rules.

## Overview

A GOBAL skill is a single `SKILL.md` file with YAML frontmatter + markdown body. It must be token-optimized, source-attributed, and structurally consistent.

**Announce at start:** "I'm using the writing-skills skill to create this new skill."

## Skill Anatomy

```
gobal-skills/<skill-name>/
├── SKILL.md              # The skill itself (required)
└── references/           # Optional: on-demand content
    └── <topic>.md
```

**Single file rule:** Keep everything in `SKILL.md` unless content exceeds token budget. Use `references/` only for large lookup tables or examples that are rarely needed.

## SKILL.md Structure

### 1. Frontmatter (YAML, ~5 lines)

```yaml
---
name: skill-name-kebab-case
description: One-line trigger description. Use when [specific condition]. Source: <repo> (<section>). It [verb]; it does NOT [anti-verb].
argument-hint: <required | [optional]>
allowed-tools: Read Write Bash Glob [others as needed]
---
```

**Frontmatter rules:**
- `name`: kebab-case, matches directory name
- `description`: Third person, trigger-focused, "Use when..." format. Never summarize the workflow.
- `argument-hint`: Required args in `<>`, optional in `[]`. Multiple with `|`.
- `allowed-tools`: Minimum needed. Don't list everything.

### 2. Header Block (3-4 lines)

```markdown
> **Source:** superpowers (brainstorming)
> **Purpose:** One sentence: what this skill does and why it exists.
```

### 3. Body (progressive disclosure)

Organize in this order:
1. Iron Law / Hard Gate (if applicable)
2. Process / Steps (numbered or headed)
3. Rules / Constraints (tables, lists)
4. Anti-patterns (rationalization table)
5. Modes (if skill has multiple modes)
6. Integration (cross-references)

## Token Economy Rules

| Rule | Requirement |
|------|-------------|
| SKILL.md body | < 500 lines |
| Frontmatter | ~5 lines, ~100 tokens |
| Tables over prose | Tables compress information |
| Progressive disclosure | Tier 3 content in `references/` |
| No duplication | Don't repeat what other skills cover |
| Script offloading | Emit JSON spec, call script |

## Progressive Disclosure Tiers

| Tier | Content | When Loaded |
|------|---------|-------------|
| 1 — Metadata | Frontmatter only | Always (skill registry) |
| 2 — Body | SKILL.md full body | On trigger (skill invocation) |
| 3 — References | `references/*.md` | On demand (skill reads them) |

**Rule:** If a section is rarely needed (< 20% of invocations), move it to `references/`.

## Source Attribution

Every skill MUST cite its source:

```markdown
> **Source:** superpowers (brainstorming)
> **Extracted from:** Section 3 (Design Process), Section 7 (Anti-Patterns)
```

**Provenance requirements:**
- Source repo name (superpowers, gstack, etc.)
- Section/topic extracted from
- Key content extracted (bullet list)
- Link to provenance/INDEX.md

## Anti-Pattern: Skill Slop

| Anti-Pattern | Fix |
|-------------|-----|
| Generic description | Specific trigger condition |
| No source attribution | Cite source repo + section |
| No Iron Law | Add if skill has a hard constraint |
| No anti-patterns | Add rationalization table |
| Everything in SKILL.md | Move rare content to references/ |
| No cross-references | Link to related skills |
| Duplicate content | Reference the other skill |
| No allowed-tools | Specify minimum needed |
| Verbose overview | 2-3 sentences max |
| No announce line | Add "I'm using..." |

## Quality Checklist

Before saving a new skill:

- [ ] Frontmatter: name, description, argument-hint, allowed-tools
- [ ] Description: third person, trigger-focused, "Use when..."
- [ ] Source attribution in header block
- [ ] Overview: 2-3 sentences + announce line
- [ ] Iron Law or Hard Gate (if applicable)
- [ ] Process: clear numbered steps or headed sections
- [ ] Rules: tables over prose
- [ ] Anti-patterns: rationalization table
- [ ] Modes: if skill has multiple modes
- [ ] Integration: cross-references to related skills
- [ ] SKILL.md body < 500 lines
- [ ] No duplicated content from other skills
- [ ] Naming: kebab-case, matches directory

## Integration

**This skill creates:** All other GOBAL skills.

**Required by:**
- `gobal-orchestrator` → Skill creation requests
- `brainstorming` → Design phase may identify need for new skill
- `spec-writer` → Spec may require new capability

## Cross-References

- `brainstorming` → Design before creating skill
- `writing-plans` → Plan skill implementation
- `artifact-manager` → Register new skill in INDEX.md
- `provenance` → Track skill sources
