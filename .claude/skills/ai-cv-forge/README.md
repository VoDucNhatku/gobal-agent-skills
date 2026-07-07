# AI CV Forge — Skill README

> Build chi tiết CV AI profile cho sinh viên mới ra trường, cập nhật mindset HR 2025–2026.
> Integrates with `career-ops` skill (same parent directory `career-ops/.claude/skills/`).

## Quickstart

```bash
# 1. Xác định profile (chỉ cần tên + ngành + 1 project)
/career-ops ai-cv-forge init

# 2. Hoặc nếu đã có profile.yml → chỉ sinh/refresh cv.md
/career-ops ai-cv-forge resume-brief

# 3. Hoặc sinh project briefs phù hợp profile
/career-ops ai-cv-forge project-brief

# 4. Hoặc sinh story-bank cho phỏng vấn
/career-ops ai-cv-forge story-bank

# 5. Hoặc tối ưu LinkedIn
/career-ops ai-cv-forge linkedin-brief
```

## Output Structure

```
project-root/
├── cv.md                       # Markdown CV (tương thích career-ops)
├── config/
│   └── profile.yml             # YAML profile (tương thích career-ops)
├── briefs/
│   ├── project-brief-01.md     # Mô tả chi tiết project 1
│   └── project-brief-02.md
├── interview-prep/
│   └── story-bank.md           # 5-8 STAR+R stories
├── linkedin-brief.md           # Optimized LinkedIn (optional)
└── README.md                   # Chiến lược + hướng dẫn bạn đọc
```

## Phối hợp với career-ops

```
ai-cv-forge init            # Build cv.md + profile.yml + README từ đầu
        ↓
ai-cv-forge linkedin-brief  # (optional) Tối ưu LinkedIn cho headhunter
ai-cv-forge story-bank      # (optional) STAR+R stories cho interview
        ↓
career-ops /career-ops {JD} # Auto-pipeline: so sánh JD → sinh CV theo JD → PDF
```

## Workflow của skill

1. **init** mode nhận form input hoặc paste file. Clarify missing fields (tối đa 3 câu).
2. Detect archetype (LLMOps/Agentic/RAG/Research/...) + market-relevant keywords 2025–2026.
3. Build cv.md với section order theo standard: Summary → Work/Internship → Projects → Education → Skills.
4. Build profile.yml + 2-3 project briefs.
5. Generate story-bank + README.
6. Optional: linkedin-brief, resume-brief refresh.

## Anti-patterns built-in

- Không generate "fake project" — nếu thiếu project → rõ ràng chỉ ra trong output.
- Không "passionate about AI" spam — replace by quantifiable actions.
- Không dài quá 1 trang với fresh grad.
- Không đặt output bên trong skill folder — theo `workbench-conventions.md`.

## Chiến lược build CV AI 2025–2026

Skill embed 3 insight chính (đọc thêm trong SKILL.md):

1. **Traits hiring managers in AI actually scan for** in 6 seconds — vs old "generic good communicator" boilerplate.
2. **Pattern "Trained → Improved → Deployed → Instrumented"** — show awareness of AI production loop.
3. **Pattern by archetype** (LLMOps vs Agentic vs RAG vs Research vs AI PM vs Solutions) — each has different keyword vocabulary + project brief style.

## Tech Notes

- Single-agent skill — NO fan-out. Output size 5-8 files fit in single pass.
- Reads references at runtime (modern_ai_market_2025_2026.md + ats_rules_2025.md) — keeps SKILL.md lean.
- Output in Vietnamese + English per `workbench-conventions.md` (human = Vietnamese, machine files = English).
- Compatible with `career-ops` format: cv.md + profile.yml feed directly into `/career-ops pdf` pipeline.

## Update Log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-07 | Initial create: SKILL.md + cv-template.md + 2 reference files |

## Credits

Template structure + cv.md/profile.yml formats derived from [career-ops](https://github.com/ferrerotomas/career-ops) (MIT).
AI market insight compiled from publicly-available JD datasets + job board analysis + interview prep guides 2025–2026.
