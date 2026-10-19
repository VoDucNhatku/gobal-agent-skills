---
language: en / vi
---

<div align="center">

# GOBAL Agent Skills — v2 research core

**9 always-on research skills, 48 specialty skills on demand, one shared evidence policy.**
Built for reading papers, running training code and deep multi-domain research.

[Install](#install) · [How it works](#how-it-works) · [Measured results](#measured-results) · [Improvement loop](#improvement-loop) · [Tiếng Việt](#tiếng-việt) · [v1 README](docs/README-v1.md)

</div>

---

## How it works

| Layer | What | Cost per turn |
|---|---|---|
| **Core** (model-visible) | `admin` · `paper-read` · `paper-synthesize` · `research-assess` · `evidence-check` · `experiment` · `code-senior` · `research-memory` · `research-write` | ~1k tokens of descriptions |
| **Packs** (hidden) | writing & LaTeX · learning · code process · web · ops · career — 48 skills with `disable-model-invocation: true` | 0 until used |
| **Shared policy** | `.claude/skills/_shared/`: evidence, reasoning check, research integrity, conventions | 0 until a skill points to it |

You talk to it the same way as before. A request covered by a core skill loads that skill
directly. Anything else — "admin, làm sổ tay ôn tập", "admin, dựng landing page" — goes
through `admin`, which keeps a table of the hidden skills and reads the right `SKILL.md`
from disk. Hidden skills can also be called by name (`/study-forge`).

Design and the old→new mapping: [notes/design-v2-research-core.md](notes/design-v2-research-core.md).

## Install

Requires Node.js 18+. The installer backs up everything it replaces.

```bash
git clone https://github.com/VoDucNhatku/gobal-agent-skills.git
cd gobal-agent-skills
node scripts/install_v2.mjs --dry-run
node scripts/install_v2.mjs --retire-rules ~/.claude/rules
```

`--retire-rules` moves the v1 rule files out of `~/.claude/rules`, where Claude Code loads
them into every conversation; v2 reads them on demand from `_shared/`. Keep
`evidence-first.md` there if you want the short always-on evidence rule.

- **DeepSeek Harness:** run the same installer with `--target <dsh skills dir>`, or re-run
  the lab's `sync-skills.ps1` after installing into `~/.claude/skills`.
- **Antigravity IDE:** `python scripts/build_antigravity.py` regenerates `skills/` and
  `rules/`; see [docs/ANTIGRAVITY.md](docs/ANTIGRAVITY.md). The Antigravity build keeps
  only `name` and `description` in frontmatter, so all 57 skills are listed there.

Validate the structure (Python 3.11+, pinned PyYAML):

```bash
python -m pip install -r ~/.claude/skills/test-framework/requirements.txt
python .claude/skills/test-framework/scripts/test_skills.py --skills-root .claude/skills --host canonical
```

## Measured results

See [notes/eval-v2-2026-10-20.md](notes/eval-v2-2026-10-20.md) for the full table, method
and limits. The eval runs 30 cases headless on DeepSeek Harness:

```bash
node evals/v2/build-arm.mjs --src .claude/skills --out .tmp/arms/v2
node evals/v2/run.mjs --arm-dir .tmp/arms/v2 --arm v2 --label my-run
```

## Improvement loop

1. A confirmed mistake goes into the project's `notes/lessons.md` (`research-memory lesson`).
2. Research skills read the top of `lessons.md` before research work.
3. A mistake that would recur in other projects becomes a case in `evals/v2/cases.mjs`.
4. A skill change is kept only if the eval does not regress.

---

# Tiếng Việt

## Bộ này làm gì

Bộ skill cho nghiên cứu: đọc paper, chạy code huấn luyện AI, thẩm định ý tưởng và viết bài.
Chỉ 9 skill lõi luôn hiện với model (khoảng 1k token mỗi lượt). 48 skill chuyên môn khác
(viết bài, LaTeX, sổ tay học tập, web, deploy, CV…) được ẩn để không tốn token, nhưng vẫn
dùng được: cứ mô tả việc cho `admin`, nó tra bảng và tự đọc skill phù hợp; hoặc gọi thẳng
`/tên-skill`.

| Skill lõi | Dùng khi |
|---|---|
| `paper-read` | hỏi về một bài: con số, công thức, phương pháp, tái lập |
| `paper-synthesize` | nhiều bài: lọc, so sánh, mâu thuẫn, khoảng trống |
| `research-assess` | thẩm định đề xuất hoặc lập luận trước khi bỏ công làm |
| `evidence-check` | kiểm số liệu, trích dẫn, phiên bản, suy luận trước khi tin |
| `experiment` | tái lập bài, chạy GPU, đọc log và seed cho đúng |
| `code-senior` | viết, sửa, debug code (cả code train) |
| `research-memory` | ledger, đính chính, bài học, nhật ký thí nghiệm |
| `research-write` | chuỗi viết bản thảo |
| `admin` | việc nhiều bước, hoặc chuyên môn ngoài danh sách trên |

## Điểm khác so với v1

- Chỉ còn 1 file quy tắc luôn nạp (`evidence-first.md`, khoảng 20 dòng); các quy tắc khác nằm
  trong `_shared/` và chỉ được đọc khi một skill cần.

- Câu hỏi hẹp được trả lời ngay kèm vị trí trong nguồn, không tạo file.
- Phạm vi do dự án quy định (`SCOPE` trong `notes/claims-ledger.md`) đứng trên rubric venue chung.
- Kiểm suy luận bằng 6 câu hỏi cố định, vì phần lớn lỗi cũ là suy luận sai chứ không phải thiếu đọc.
- Bài học từ lỗi đã xác nhận được ghi lại và đọc lại ở lần sau; lỗi chung trở thành ca eval.

Kết quả đo: [notes/eval-v2-2026-10-20.md](notes/eval-v2-2026-10-20.md).
