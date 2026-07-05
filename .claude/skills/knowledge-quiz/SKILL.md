---
name: "knowledge-quiz"
description: "Knowledge quiz for GOBAL AGENT — generates and administers rigorous quizzes from knowledge graph, notes, or any source material. Tests understanding, not rote memorization. Modes — generate (create quiz), administer (one question at a time), review (analyze results). Source: gstack (learn, benchmark) + addyosmani (testing-patterns). It quizzes; it does NOT tutor (use study-tutor for guided learning)."
argument-hint: "<topic | kg-id> [generate|administer|review]"
allowed-tools: "Read Write Bash Glob"
---

# Knowledge Quiz

> **Source:** gstack (learn, benchmark) + addyosmani (testing-patterns)
> **Purpose:** Generate rigorous quizzes that test understanding, not just memorization.

## Mode: generate

### Process

1. **Read source material** — Load knowledge graph, notes, or specified source
2. **Extract key entities** — Identify 5-10 key facts, concepts, or relations
3. **Generate questions** — Use templates below, mix difficulty levels
4. **Write distractors** — Plausible wrong answers based on common misconceptions
5. **Write explanations** — Why correct AND why distractors are wrong

### Question Templates

| Type | Difficulty | Template |
|------|-----------|----------|
| Conceptual Application | Hard | "Given [Scenario involving X], what is the expected outcome?" |
| Comparison | Medium | "What is the primary difference between [A] and [B] in [context]?" |
| Procedural | Medium | "What is the correct sequence to achieve [Goal]?" |
| Factual Identification | Easy | "Which best describes [Entity]?" |
| Edge Case | Hard | "What happens when [edge condition] in [system]?" |

### Anti-Slop Distractor Rules

- **Plausible:** Based on common misconceptions, not random wrong answers
- **No length bias:** Correct answer must NOT be obviously longer or more detailed
- **No lazy patterns:** Avoid "All of the above" / "None of the above" unless genuinely correct
- **No giveaway patterns:** Don't always put correct answer at position B

### Output Format

```markdown
## Quiz: <topic> (N questions)

### Q1: [question text]
A) [distractor — plausible misconception]
B) [correct answer]
C) [distractor — plausible misconception]
D) [distractor — plausible misconception]

**Correct Answer:** B
**Explanation:** [Why B is correct + why A/C/D are wrong]
**Source:** [KG path or notes path]
**Difficulty:** Easy/Medium/Hard
```

---

## Mode: administer

1. Present ONE question at a time
2. Wait for user answer (do not auto-advance)
3. Reveal correct answer + explanation
4. Track score: correct/incorrect per concept
5. After all questions: summary of strengths, gaps, recommendations

### Adaptive Rules
- If user gets 2+ questions on same concept wrong → suggest re-reading that section
- If user gets all easy questions right → skip to medium/hard
- Mix concepts — don't cluster all questions on one topic

---

## Mode: review

Analyze quiz results:
1. **Strengths** — Concepts user mastered (all questions correct)
2. **Gaps** — Concepts user missed (identify specific misconceptions from wrong answers)
3. **Recommendations** — Specific sections to re-read, specific skills to invoke
4. **Progress tracking** — Score trend if multiple quizzes taken

---

## Cross-References

- `study-tutor` → Guided learning based on quiz results
- `knowledge-graph` → Source entities for quiz generation
- `concept-explainer` → Explain concepts user missed
- `paper-read` → Source material for paper-based quizzes
