---
name: vi-translate
description: Faithful, complete academic translation of a passage, section, or whole paper — preserves technical terms inline and appends a glossary. Default target is Vietnamese; --to <lang> overrides the target language. Translates the source fully and accurately; it does NOT summarize, condense, or critique. Triggers — translate, dịch, dịch bài báo, dịch sang tiếng Việt, dịch đoạn này, translate paper to Vietnamese, translate this passage, translate section, dịch toàn bộ, dịch nguyên văn, or any pasted block of foreign-language text the user wants rendered in another language. Use when the user wants the actual text in another language (full fidelity, nothing dropped). For a condensed read or section-by-section gist use paper-read; for deep method analysis use paper-method.
argument-hint: <id|file|path|pasted text> [--to <lang>]
allowed-tools: Skill Agent Read Write Glob Bash
---

# vi-translate — faithful academic translation (dịch học thuật trung thành)

Translate a passage, a section, or an entire paper **completely and faithfully**
into a target language (default Vietnamese), keeping every technical term
recoverable and the original structure intact. This skill **translates, it does not
summarize** — nothing in the source is dropped, merged, or paraphrased away.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual
policy §1, input resolution §2, PREVIEW-NOT-DUMP §3, reuse §4, stable naming §5,
strategic/ranged reading §6, single-pass scope §10). It pulls no satellite rules
file. One deviation from the master §1 bilingual policy: here the **target language
is a parameter** — the body of the translation is rendered in `--to <lang>`
(default `vi`), while skill instructions, the chat preview, and the artifact header
stay Vietnamese.

## Inputs
- `$ARGUMENTS` first token resolves a **source** per §2:
  - a 3-digit paper id (`003`) → file under `./papers/`,
  - a filename / partial title, an absolute or relative path,
  - or **pasted text** (the argument is itself the foreign-language block to
    translate — no file lookup).
- `--to <lang>` sets the **target language** (ISO-ish name or code: `vi`, `en`,
  `ja`, `zh`, `fr`, …). Default `vi` (Vietnamese).
- Resolve to a concrete source before working. If a paper id is ambiguous, list
  candidates and ask **once** (§2); never guess silently.

## Procedure

### Phase 0 — Resolve source & target
1. Parse `--to <lang>`; default `vi`. Parse the source token.
2. Decide the **unit**:
   - pasted text → translate that block, write **no file**, print to chat (this is
     a digest-style / inline mode under §3); still preserve terms inline.
   - a paper id / file / path → **whole-paper** translation to a file (below).
   - if the user named a single section ("dịch phần Method của 003"), translate only
     that section but still write the file (named for the paper + lang).
3. Consult `notes/INDEX.md` and check for an existing `notes/<id>-<lang>.md` (§4). If
   present and fresh, offer to reuse it instead of re-translating.

### Phase 1 — Read the source (strategic, ranged)
- Read the **actual** source with the Read tool — never translate from a title (§8).
- For long PDFs, use **ranged reads** (page ranges), translating in order; do not
  load the whole PDF into context at once (§6). Translate each range fully before
  moving to the next so no passage is skipped.
- Skip pure layout artifacts (page numbers, running headers, line-break hyphenation)
  but keep all substantive content: body text, captions, table contents, footnotes,
  equation surrounding prose. Mathematical formulae are copied **verbatim** (do not
  "translate" LaTeX/symbols).

### Phase 2 — Translate faithfully
- **Completeness:** render every sentence of the source. Do not summarize, reorder,
  or omit. If a sentence is genuinely untranslatable as-is, translate literally and
  add a short translator note in brackets `[ghi chú người dịch: …]`.
- **Term preservation (§1):** on first use of each technical term, write
  `bản dịch (Original term)` — e.g. `học tương phản (contrastive learning)`,
  `hàm mất mát (loss function)`. Afterwards the translated form may stand alone, but
  the original must remain recoverable. **Never translate** API / library / function
  / dataset / model / metric names — keep them verbatim (`PyTorch`, `ImageNet`,
  `BLEU`, `AdamW`).
- **Structure parity:** preserve heading hierarchy, lists, numbering, table layout,
  and equation placement so the translation maps 1:1 onto the source. Keep citation
  markers (`[12]`, `(He et al., 2016)`) as-is.
- **Register:** academic / formal in the target language (for `vi`, văn phong học
  thuật).
- This is a faithful translation, **not** an interpretation — do not insert analysis,
  opinions, or "in other words" expansions beyond bracketed translator notes.

### Phase 3 — Glossary
Append a `## Thuật ngữ (Glossary)` table collecting the technical terms encountered
(per master §1): `| Original | Bản dịch | Giải thích ngắn |`. One row per distinct
term; short gloss in the target language.

### Phase 4 — Write & preview (PREVIEW-NOT-DUMP, §3)
- **Whole-paper / section → file.** Write the full translation to
  **`notes/<id>-<lang>.md`** (e.g. `notes/003-vi.md`, `notes/003-en.md`) with the
  standard research header block (paper id · title · source filename · worker
  `vi-translate` · target lang · date `YYYY-MM-DD`), then the translated body, then
  the glossary.
- Print to chat **only**: a **5–8 line** Vietnamese preview — what was translated
  (source + unit), target language, term count in the glossary, the title/abstract
  rendered as a taste — **plus the absolute saved path**. **Never echo the full
  translation into chat.**
- **Pasted text / inline mode → chat-only.** Print the translation directly (no
  file), still preserving terms inline. For a long pasted block, keep the preview
  discipline: lead with the translation, do not add commentary.

## Output template (file modes)
```markdown
# <Paper title> — Bản dịch (<lang>)
> id: <id> · nguồn: <source filename> · worker: vi-translate · ngôn ngữ đích: <lang> · ngày: YYYY-MM-DD

> Bản dịch trung thành, đầy đủ. Thuật ngữ kỹ thuật giữ kèm nguyên gốc; xem Glossary.

## <Heading 1 đã dịch>
<full translated text — every sentence>

## <Heading 2 đã dịch>
…

## Thuật ngữ (Glossary)
| Original | Bản dịch | Giải thích ngắn |
|---|---|---|
| contrastive learning | học tương phản | … |
```

## Chat preview shape (file modes)
```
Đã dịch: <id> — <title> (<unit>) → <lang>
Glossary: <N> thuật ngữ.
Trích (tiêu đề/abstract đã dịch): "<1–2 câu>"
Đã lưu: <absolute path to notes/<id>-<lang>.md>
→ Muốn bản tóm tắt thay vì dịch nguyên văn? dùng skill paper-read.
```

## Gotchas
- **This is translation, not summarization.** If the user wants a condensed,
  section-by-section read or an intuition pass, hand off: `→ dùng skill paper-read`
  (`gist`/`summary`/`eli5`). Do not silently shorten the source here.
- **Single-pass, single source (§10).** Translate one source per invocation. Do not
  wander into method critique (`→ paper-method`) or cross-paper comparison
  (`→ paper-synthesize`).
- **Don't translate code-y identifiers.** Library / API / function / dataset / model
  / metric names and CLI flags stay verbatim; only natural-language prose is
  translated. Math stays verbatim.
- **Don't dump.** Whole-paper translations always go to file with a short preview;
  only short pasted text prints inline (§3).
- **Ranged reads for long PDFs (§6).** Never pull a whole large PDF into context;
  translate page-range by page-range, in order, so nothing is skipped or duplicated.
- **Target language is a parameter.** Respect `--to <lang>` — the body is in that
  language, but the chat preview and the artifact header stay Vietnamese (skill UX
  language).
- **Term-first fidelity (§1).** First occurrence always carries the original in
  parentheses; never invent a target-language coinage for a term with no settled
  translation — keep the original and gloss it.
