---
name: "study-tutor"
description: "Study tutor for GOBAL AGENT — adaptive learning assistant. Modes: explain (concept explanation), practice (guided exercises), quiz (test knowledge), summarize (condense material). It tutors; it does NOT replace domain expertise (use domain-specific skills for actual work). Triggers — học, dạy tôi, ôn bài, luyện tập, gia sư, giảng lại, kiểm tra trình độ."
---

# Study Tutor

> **Source:** gstack (learn) + addyosmani (teaching patterns) + superpowers (brainstorming)
> **Purpose:** Adaptive learning — explain, practice, quiz, summarize at the right depth.

## Level Assessment

Before any mode, assess the learner's level:

| Level | Indicators | Approach |
|-------|-----------|----------|
| Beginner | No prior knowledge, asks basic questions | Fundamentals, analogies, ELI5 |
| Intermediate | Knows basics, asks "how" and "why" | Depth + connections to known concepts |
| Advanced | Asks about edge cases, latest research | Nuance, trade-offs, open problems |

**Assessment method:** Ask ONE diagnostic question if level is unclear. Never assume.

---

## Mode: explain

### Process

1. **Assess level** (see above)
2. **Start with analogy** — One relatable comparison from everyday life
3. **Core definition** — Precise, with notation if applicable
4. **How it works** — Step by step
5. **Why it matters** — Real-world impact, one paragraph
6. **Common misconception** — One thing people get wrong
7. **Further learning** — Specific next step (paper, skill, resource)

### Delegation
- Beginner → `concept-explainer` (eli5 mode)
- Intermediate → `concept-explainer` (deep-dive mode)
- Advanced → `paper-read` + `paper-method`

**Reuse-before-read:** trước khi delegate Advanced, check `notes/INDEX.md`
(artifact-manager mode `reuse`) — topic đã có distillate trong `notes/` → ground giải
thích vào note đó thay vì đọc lại paper (rẻ hơn + có nguồn cụ thể để cite).
**Fast-moving claims:** khẳng định kiểu "SOTA hiện tại / mới nhất" trong topic thay đổi
nhanh → 1 web search capability verify trước, không nói từ trí nhớ.

---

## Mode: practice

### Process

1. **Generate exercise** — Start easy, increase difficulty
2. **Each exercise:** Problem → Hint → Solution → Explanation
3. **Track progress** — What's mastered, what needs more practice
4. **Adapt next exercise** based on performance

### Exercise Template

```markdown
### Exercise N: <topic>

**Problem:** <description>

**Hint:** <gradual hint — don't give the answer>

**Solution:** <step-by-step solution>

**Explanation:** <why this works, common pitfalls>
```

### Adaptive Rules
- 2+ correct → increase difficulty
- 2+ incorrect → decrease difficulty, review fundamentals
- Mastery (3 consecutive correct at current level) → advance to next concept

---

## Mode: quiz

Delegate to `knowledge-quiz` for KG-based questions.
See knowledge-quiz SKILL.md for full quiz generation and administration protocol.

---

## Mode: summarize

Condense learning material:

1. **Key concepts** — Bullet list, one line each
2. **Key formulas/definitions** — With notation
3. **Connections** — How concepts relate to each other
4. **Quick reference** — One-page cheat sheet format

---

## Learning Principles

- **Spaced repetition:** Review earlier concepts when relevant in new contexts
- **Active recall:** Test before explaining (retrieval practice)
- **Concrete before abstract:** Examples before theory
- **Connect to known:** Relate new concepts to existing knowledge
- **Socratic questioning:** Ask guiding questions instead of giving answers (from brainstorming)
- **Error as learning:** Wrong answers are learning opportunities, not failures

---

## Cross-References

- `concept-explainer` → Deep concept explanations
- `knowledge-quiz` → Quiz generation and administration
- `paper-read` → Source material for advanced topics
- `paper-method` → Technical implementation details
- `knowledge-graph` → Entity/relation map for structured learning


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
