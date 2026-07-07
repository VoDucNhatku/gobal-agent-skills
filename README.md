---
language: en / vi
---

# GOBAL Agent Skills

A curated collection of **62 specialist skills** for [Claude Code](https://claude.ai/claude-code) — covering academic research, software engineering, UI/UX design, and operations. Each skill is a self-contained playbook that teaches Claude how to do one thing well.

Built on the **GOBAL Orchestrator** pattern: one master router receives your request, classifies it, routes to a domain orchestrator, which dispatches worker skills in parallel where helpful, then synthesizes a single bilingual deliverable (Vietnamese + English code).

[Browse Skills](#skills) · [Phiên bản Tiếng Việt](#tiếng-việt)

---

## Table of Contents

- [How It Works](#how-it-works)
- [Skills](#skills)
- [Tiếng Việt](#tiếng-việt)
- [Architecture Decisions](#architecture-decisions)

---

## How It Works

```
YOU: "Read paper 003 and summarize its method"
  │
  ▼
GOBAL ORCHESTRATOR  (your entry point)
  • Classifies intent + domain
  • Estimates token cost
  • Routes to domain orchestrator
  │
  ▼
DOMAIN ORCHESTRATOR  (e.g., Research Orchestrator)
  • Reads INDEX.md, memory, existing artifacts
  • Decides: solo / fan-out / ask-first
  • Dispatches worker skills
  │
  ├─ Worker A: paper-read    ─┐
  └─ Worker B: kg-extract    ─┤  ← parallel, isolated
                               │  each returns path + ≤2k summary
  ▼
GOBAL ORCHESTRATOR  ← synthesizes
  • Combines all findings
  • Runs hallucination-guard + self-evaluator
  • Writes to notes/ + updates INDEX.md
  │
  ▼
FINAL DELIVERABLE  ← Vietnamese + file paths in chat
```

**Key principles:** Orchestrator sees only summaries. Raw PDFs never enter the orchestrator context. Workers handle them in isolation.

---

## Skills

### Orchestrators

| Skill | Description |
|-------|-------------|
| `gobal-orchestrator` | Main entry point — classifies, routes, synthesizes |
| `workbench-orchestrator` | Legacy orchestrator, aliased to gobal |
| `skill-router` | Standalone routing — classify + suggest skill |

### Research & Academic (15)

| Skill | Description |
|-------|-------------|
| `paper-triage` | Rank N papers by relevance → 0-5 score + action plan |
| `paper-read` | Read ONE paper: gist / summary / eli5 / mindmap |
| `paper-method` | Deep method: critique + recipe + reproducibility A-F |
| `paper-synthesize` | Cross-paper: compare / taxonomy / gaps / expand |
| `knowledge-graph` | Typed entities + relations → master graph |
| `latex-fix` | Batch LaTeX repair (KaTeX/MathJax) |
| `latex-math-renderer` | LaTeX → HTML (KaTeX/MathJax) |
| `latex-tikz-generator` | TikZ vector diagrams — pipeline/architecture figures, plagiarism-safe |
| `vi-translate` | Faithful Vietnamese translation + glossary |
| `paper-submission` | Draft/format (IEEE, CVPR, NeurIPS) — head of the sequential write pipeline |
| `citation-guard` | DOI verify (CrossRef), orphan-citation detect, synthesis-quality scan |
| `style-humanizer` | AI-text humanizer — heuristic checklist + style calibration under a meaning-preservation invariant |
| `ieee-q1-devil-advocate` | IEEE Q1 reviewer simulation — novelty tier + ablation + rejection-pattern analysis |
| `paper-to-notebook` | Paper → runnable Jupyter notebook |
| `run-on-modal` | Paper → Modal GPU. VRAM profile + cost estimate |

### Code & Development (12)

| Skill | Description |
|-------|-------------|
| `code-senior` | Senior-grade: infer stack, minimal diff, surgical edits, verify |
| `understand-codebase` | Map repo into token-bounded knowledge graph |
| `code-reviewer` | 5-axis review: correctness, readability, arch, security, perf |
| `debug-investigator` | Investigate → pattern → hypothesis → fix |
| `spec-writer` | Structured specs with gated review |
| `writing-plans` | Bite-sized implementation steps |
| `executing-plans` | Run plan with verification checkpoints |
| `finishing-a-dev-branch` | Merge / PR / keep / discard |
| `tdd-enforcer` | Strict TDD: RED → GREEN → REFACTOR |
| `brainstorming` | Explore intent before implementation |
| `domain-modeling` | DDD: entities, value objects, aggregates |
| `using-git-worktrees` | Isolated worktrees for parallel dev |

### Web & UI (6)

| Skill | Description |
|-------|-------------|
| `design-web` | Anti-slop tokens → HTML preview → design-record |
| `build-ui` | Accessible components from design-record |
| `build-admin-dashboard` | CRUD admin + role-gated + analytics |
| `review-frontend` | 8-dim slop + a11y + token audit |
| `fullstack-builder` | Scaffold + implement fullstack features |

### Backend & Security (2)

| Skill | Description |
|-------|-------------|
| `backend-engineer` | Contract-first API + threat model |
| `security-review` | STRIDE + OWASP rubric |

### Deploy & Ops (5)

| Skill | Description |
|-------|-------------|
| `deploy-orchestrator` | Coordinate: validate → ship → monitor → rollback |
| `ship-validator` | Pre-ship gate (lint, types, tests, security) |
| `monitor-setup` | Observability: RED/USE metrics, logs, alerts |
| `rollback-manager` | Decision matrix → assess → execute → verify |

### Study & Learning (3)

| Skill | Description |
|-------|-------------|
| `study-tutor` | Adaptive: assess → explain → practice → quiz |
| `concept-explainer` | eli5 / deep-dive / analogy |
| `knowledge-quiz` | Rigorous quiz from KG/notes |

### Career (1)

| Skill | Description |
|-------|-------------|
| `ai-cv-forge` | CV/career-profile builder for new-grad AI students — minimal input → cv.md + profile.yml, 2025–2026 hiring mindset (agentic, eval, RAG, MLOps, LLM infra) |

### Governance (10)

| Skill | Description |
|-------|-------------|
| `artifact-manager` | Index + track file artifacts |
| `audit-log` | Append-only log of material decisions |
| `project-memory` | Persist project context |
| `learnings-db` | Capture + query lessons |
| `token-budget` | Estimate/allocate/track tokens |
| `context-compressor` | Compress when context grows large |
| `reuse-checker` | Verify artifact exists before re-creating |
| `hallucination-guard` | Catch fabricated content |
| `verification-before-completion` | No "done" without fresh verify |
| `self-evaluator` | 4-dim quality gate |

---

## Architecture Decisions

### Why orchestrators?

```
Single big skill   → hard to maintain, low token efficiency
Many flat skills   → hard to route, no context sharing

Solution: Hierarchical orchestrators
  GOBAL → domain orchestrator → worker skills
```

### Token economy (5 principles)

1. **Progressive disclosure** — metadata (~100tok) → body (<500 lines) → references/ on demand
2. **Fan-out judiciously** — parallel costs ~10x tokens. Gate on: independence + value ≥ 2k tokens + clear scope
3. **Preview-not-dump** — chat = 5-10 lines + file paths. Full content in files
4. **Reuse-before-read** — check INDEX.md + existing artifacts before ingesting sources
5. **Context isolation** — each worker gets ONLY its spec. Orchestrator never sees raw PDF text

### Hallucination defense (tiered, not one mega-skill)

| Gate | Trigger | Domain |
|------|---------|--------|
| `hallucination-guard` | Always — scan for fabrications | Research, general |
| `verification-before-completion` | Before claiming "done" | All |
| `self-evaluator` | Before delivery | All |
| `reuse-checker` | Before creating new artifact | All |
| `stop-regain protocol` | When hallucination detected | All |

**Why tiered?** Different domains have different risks. Research has cross-source risk → hallucination-guard + audit-log. Code has API risk → verify before apply. Tiered = cheaper, more precise.

---

## Quick Start

```bash
git clone https://github.com/VoDucNhatku/gobal-agent-skills.git
# Skills auto-load from ~/.claude/skills/
claude
```

**Requirements:** Claude Code, Node.js (MCP servers), Python 3.12+, Git.  
**License:** MIT

---

<br>

---

# Tiếng Việt

## Giới thiệu

GOBAL Agent Skills là **bộ công cụ "siêu trợ lý"** cho Claude Code — think của nó là 66 "chuyên gia" nhỏ, mỗi người giỏi một việc riêng. Bạn chỉ cần **nói tiếng Việt** — nó tự hiểu, tự gọi đúng chuyên gia và trả về kết quả bằng tiếng Việt.

## Cách hoạt động — cho người không biết code

### Tương tự công ty nhỏ

```
Bạn (Giám đốc)
    │
    ▼
GOBAL Orchestrator (Trợ lý điều phối)
    ├── "Cần đọc bài báo?"      → Phòng Nghiên cứu
    ├── "Cần code?"              → Phòng Kỹ thuật
    ├── "Cần thiết kế web?"      → Phòng Thiết kế
    ├── "Cần deploy?"            → Phòng Vận hành
    └── "Cần học tập?"           → Phòng Học tập
```

Mỗi "phòng ban" có Trưởng phòng (orchestrator) và hàng loạt chuyên gia (worker skill). Khi bạn nói *"nghiên cứu các bài báo về AI, so sánh phương pháp, tìm khoảng trống"*:

```
┌───────────────────────────────────────────────────────────┐
│  Bạn: "Hiểu hết các bài báo, so sánh phương pháp"         │
└───────────────────────┬───────────────────────────────────┘
                        │
          ┌─────────────▼─────────────┐
          │  GOBAL ORCHESTRATOR        │
          │  Phân loại: Research       │
          │  Route: Research Orchestrator                     │
          └─────────────┬─────────────┘
                        │
              ┌─────────▼─────────┐
              │ TRIAGE (1 lần)    │
              │ Chỉ đọc: title +  │
              │ abstract mỗi bài │
              │ Kết quả: 5 bài   │
              │ liên quan nhất   │
              └─────────┬─────────┘
                        │
         ┌──────┬──────┬──────┐
         │Batch1│Batch2│Batch3│  (song song, mỗi cái "phòng riêng")
         │003   │007   │018   │
         │+2 bài│+2 bài│+2 bài│
         └───┬──┴───┬──┴───┬──┘
             │      │      │
             │  Mỗi batch chỉ trả về:
             │  ≤2k ký tự summary + file path
             │  (không trả nguyên PDF về)
             ▼
              ┌─────────────────┐
              │ GOM + KIỂM TRA  │
              │ • Gom vào INDEX │
              │ • Hallucination │
              │   guard         │
              │ • Self-evaluate │
              └────────┬────────┘
                       │
          ┌────────────▼─────────────┐
          │  Trả về kết quả          │
          │  "5 bài liên quan nhất:  │
          │  003, 007, 018, 021, 031 │
          │  Phương pháp chính: ...  │
          │  Khoảng trống: ...       │
          │  Files: notes/003-...,   │
          │  notes/007-... "         │
          └──────────────────────────┘
```

### Sơ đồ cây skill

```
gobal-agent-skills/
├── orchestration/         ← Điều phối (3 skills)
├── research/              ← Nghiên cứu (15 skills)
├── code/                  ← Kỹ thuật (12 skills)
├── web-ui/                ← Thiết kế web (5 skills)
├── backend/               ← Backend & bảo mật (2 skills)
├── deploy/                ← Vận hành (4 skills)
├── study/                 ← Học tập (3 skills)
├── career/                ← Sự nghiệp (1 skill)
├── governance/            ← Kiểm soát chất lượng (10 skills)
└── writing-planning/      ← Viết & lập kế hoạch (3 skills)
```

### Mỗi skill làm gì — giải thích đời thường

**Điều phối:**
- **gobal-orchestrator:** Trợ lý trưởng — bạn nói mục tiêu lớn, nó hiểu và gọi đúng người
- **workbench-orchestrator:** Phiên bản cũ, giữ tương thích
- **skill-router:** Chỉ gợi ý skill nào phù hợp, không chạy

**Nghiên cứu (15 skills):**
- **paper-triage:** "Cho tôi xem đống sách/bài báo này — cái nào đáng đọc, cái nào bỏ?" (Quét abstract → cho điểm 0-5)
- **paper-read:** "Đọc bài báo số 003, tóm tắt ra sao? chi tiết hay gọn?" (4 mức độ: gist/summary/eli5/mindmap)
- **paper-method:** "Phân tích sâu — có tái lập được không? điểm mới gì?" (critique + recipe + reproducibility A-F)
- **paper-synthesize:** "Đọc nhiều bài rồi so sánh — còn chỗ nào chưa ai giải?"
- **knowledge-graph:** "Vẽ khái niệm + mối quanệ vào đồ thị chung"
- **vi-translate:** "Dịch bài báo sang tiếng Việt, giữ thuật ngữ chuyên ngành"
- **latex-fix:** "Sửa công thức toán bị lỗi hiển thị"
- **latex-tikz-generator:** "Vẽ hình pipeline/kiến trúc chuẩn Q1 bằng TikZ — vector, không dính đạo văn ảnh"
- **paper-submission:** "Viết bài báo theo chuẩn IEEE/CVPR — mở đầu chuỗi viết bản thảo"
- **citation-guard:** "Kiểm trích dẫn — DOI có thật không, có câu nào mồ côi không, Related Work có tổng hợp thật hay chỉ liệt kê?"
- **style-humanizer:** "Giảm dấu hiệu văn AI, giữ nguyên số liệu/công thức/trích dẫn"
- **ieee-q1-devil-advocate:** "Đóng vai reviewer Q1 khó tính nhất — điểm mới thật không, ablation đủ chưa?"
- **paper-to-notebook:** "Lấy code bài báo chạy thành Jupyter notebook"
- **run-on-modal:** "Chạy mô hình lên GPU cloud — tốn bao nhiêu?"

**Sự nghiệp (1 skill):**
- **ai-cv-forge:** "Sinh viên AI mới ra trường — dựng CV/profile từ project, khóa học, internship theo tư duy tuyển dụng AI 2025–2026"

**Kỹ thuật (12 skills):**
- **code-senior:** "Code giúp — viết đúng, sạch, có test"
- **understand-codebase:** "Giải thích dự án cũ cho tôi"
- **code-reviewer:** "Review code — có bug? security OK không?"
- **debug-investigator:** "Có cái gì đó sai — tìm nguyên nhân trước khi sửa"
- **spec-writer:** "Viết tài liệu yêu cầu trước khi code"
- **writing-plans:** "Chia nhỏ công việc thành bước 2-5 phút"
- **executing-plans:** "Chạy theo kế hoạch, từng bước kiểm tra"
- **finishing-a-dev-branch:** "Xong rồi — merge hay PR hay giữ?"
- **tdd-enforcer:** "Test trước rồi code — đúng chuẩn TDD"
- **brainstorming:** "Suy nghĩ trước khi code: mục tiêu gì, giải pháp nào?"
- **domain-modeling:** "Thiết kế cấu trúc dữ liệu cho business"
- **using-git-worktrees:** "Chạy nhiều feature song song, không rối git"

**Thiết kế Web (6 skills):**
- **design-web:** "Thiết kế giao diện — chọn màu, font, bố cục"
- **build-ui:** "Dựng component thật từ bản thiết kế"
- **build-admin-dashboard:** "Trang quản trị — bảng, CRUD, phân quyền"
- **review-frontend:** "Chấm giao diện — đẹp? dễ dùng? chuẩn accessibility?"
- **fullstack-builder:** "Dựng cả frontend + backend + DB cho 1 feature"

**Vận hành (Deploy, 4 skills):**
- **deploy-orchestrator:** "Đưa lên production — an toàn, có rollback"
- **ship-validator:** "Kiểm tra toàn bộ trước khi ship"
- **monitor-setup:** "Giám sát — metric, log, alert, dashboard"
- **rollback-manager:** "Có lỗi sau deploy — rollback an toàn"

**Học tập (3 skills):**
- **study-tutor:** "Gia sư AI — điều chỉnh cấp độ phù hợp"
- **concept-explainer:** "Giải thích khái niệm phức tạp đơn giản"
- **knowledge-quiz:** "Test kiến thức thật — không phải học thuộc"

**Kiểm soát chất lượng (10 skills):**
- **artifact-manager:** Quản lý file output — đừng đọc lại cái cũ
- **audit-log:** Ghi lại quyết định quan trọng
- **project-memory:** Nhớ ngữ cảnh giữa các phiên
- **learnings-db:** Lưu bài học — đúng gì, sai gì
- **token-budget:** Đừng phí token vô ích (200k total, 50% buffer)
- **context-compressor:** Nén ngữ cảnh khi gặp giới hạn
- **reuse-checker:** Kiểm tra đã làm chưa trước khi làm lại
- **hallucination-guard:** Phát hiện "bịa" — claim không có nguồn bị bắt
- **verification-before-completion:** Không nói "xong" nếu chưa chạy thật
- **self-evaluator:** Tự chấm điểm trước khi giao

### Tiết kiệm Token — 5 quy tắc vàng

| Quy tắc | Giải thích |
|---------|-----------|
| Preview-not-dump | Chat chỉ in 5-10 dòng + đường dẫn. File đầy đủ ở `notes/` |
| Reuse-before-read | Trước khi mở PDF → kiểm tra `notes/INDEX.md`. Có rồi → đọc lại |
| Mode-scaling | 1 bài → chi tiết. 10 bài → 1 dòng/bài. Tổng output tuyến tính |
| Fan-out judiciously | Parallel ≈ 10x tokens. Chỉ khi independence + value ≥ 2k tokens |
| Script-offloading | Phát JSON spec → gọi script dựng. Không tự viết boilerplate |

### Chống "Bịa" (Hallucination) — 5 lớp phòng thủ

- **Lớp 1 — hallucination-guard:** Mọi claim cần nguồn. Không nguồn = bị bắt
- **Lớp 2 — verification-before:** Không nói "xong" nếu chưa verify thật
- **Lớp 3 — self-evaluator:** Tự chấm 4 chiều (hoàn thành, đúng, tiết kiệm, không bịa)
- **Lớp 4 — reuse-checker:** Cái này đã làm rồi → không làm lại, không claim mới
- **Lớp 5 — stop-regain:** Phát hiện bịa → DỪNG NGAY → Thú nhận → Verify → Sửa

### Scope rõ ràng

Mỗi skill làm **đúng 1 việc**. Nếu cần API → `backend-engineer`. Nếu cần UI → `design-web` → `build-ui`. Không dùng 1 skill làm 5 việc.

---

## Questions?

- **GitHub:** [@VoDucNhatku](https://github.com/VoDucNhatku)
- **Issues:** [github.com/VoDucNhatku/gobal-agent-skills/issues](https://github.com/VoDucNhatku/gobal-agent-skills/issues)

**License:** MIT
