---
name: "paper-synthesize"
description: "Works ACROSS several papers: rank a corpus against a question, compare methods, reconcile contradictory results by their conditions, build a taxonomy, find research gaps, generalize a problem. Use when two or more papers are involved. Triggers — so sánh bài, lọc bài, xếp hạng, mâu thuẫn, khoảng trống nghiên cứu, hệ thống hóa, hướng nghiên cứu."
argument-hint: "<ids|all|topic> [triage|compare|conflicts|taxonomy|gaps|expand]"
allowed-tools: "Read Write Glob Grep"
---

# paper-synthesize — reason across papers

## 1. Scope and sources
Resolve the set: ids, `all` (every file in `papers/`), or a topic. Prefer distilled notes
(`notes/<id>-read-summary.md`, `notes/<id>-method.md`, rows of `notes/INDEX.md`) over raw
papers. Scale by size so the context stays bounded:
- ≤ 4 papers: read each note or the needed sections in full.
- 5–12: one line per paper, focus on cross-cutting structure.
- > 12: reason over `notes/INDEX.md` gists; shard into batches of ≤ 12 if more detail is needed.
A paper with no note: read its abstract, tables and conclusion only, and label it `skim`.

## 2. Modes
| Mode | Output |
|---|---|
| `triage` | relevance 0–5 per paper against the stated question, one-line reason from the abstract, action (đọc sâu / lướt / bỏ); read abstracts only |
| `compare` (default) | table rows = papers, columns = task, data, backbone, schedule, metric, headline number; then the differences that matter |
| `conflicts` | for each pair of disagreeing results, the setting differences that could explain it (backbone, schedule, data split, metric definition) before calling it a contradiction |
| `taxonomy` | organizing dimensions → named groups with a one-line rationale → matrix |
| `gaps` | recurring weaknesses and untested settings, each tied to source ids; each gap → one concrete next study |
| `expand` | the broader problem class, relaxable assumptions, neighbouring problems, open sub-problems |

## 3. Rules
- Every cross-paper statement names the ids it rests on.
- Two results conflict only if their settings match; otherwise report "khác điều kiện" and
  name the differing condition.
- Compare numbers only when the metric definition and split are the same; say when they are not.
- A gap is "not found in the papers read at depth X", never "no one has done this".
- Directions proposed from `gaps`/`expand` follow `../_shared/research-integrity.md`
  (project scope first; no venue band unless allowed). Judging one direction in depth → `research-assess`.

## 4. Output
Chat answer for `triage` and short comparisons. Write `notes/synth-<mode>-<slug>.md` for
full tables or when asked, with a ≤ 8-line preview and the path.
