# CV Strategy 2025–2026 — thị trường, lối mòn, glossary

> Tách khỏi `SKILL.md` (2026-08-01) để body về dưới ngưỡng 500 dòng. Đọc on-demand khi
> mode `init`/`profile` cần dựng phần chiến lược trong README output.


Đây là phần giá trị lớn nhất cho người dùng mới ra trường — skill embed mindset thị trường hiện tại:

## 1. Công ty AI tuyển fresh grad 2025–2026 cần ghi
- **Shipping taste**: họ muốn thấy bạn đã build cái gì hoàn chỉnh, deploy được, dùng được (not just notebook sandbox)
- **LLM fluency**: khả năng sử dụng API, parameter tuning, prompt engineering, chain-of-thought, evaluation
- **Agentic mindset**: hiểu orchestrator, planner/executor, tool use, HITL — không cần build architecture phức tạp, cần hiểu pattern
- **Engineering discipline**: các kỹ năng engineering cơ bản cho AI — version data, experiment tracking, reproducibility, CI cho model
- **Communication**: AI ngày càng cần người giải thích model decision cho data scientist / business — evidence: writing, teaching, presentation là soft skill đánh giá cao
- **Generic engineering depth**: họ vẫn cần Python, Git, Docker, API design — những cái fresh grad phổ thông thường yếu kém (đương nhiên)
- **Portfolio signal 2025**: repo public > private; README có 3 phần bắt buộc (problem, approach, result); demo link; metrics cụ thể

## 2. Những "lối mòn" mới 2025–2026 (tránh)

| Lối mòn CŨ | ThAY BẰNG (2025 patterns) |
|---|---|
| "Built chatbot with RAG" | "Built RAG pipeline (Qdrant + LlamaIndex), chunked 12K docs, retrieval p95 180ms, 15% improvement in citation recall" |
| "Worked on LLM fine-tuning" | "Fine-tuned Llama-3-8B via LoRA on 40K legal corpus; F1 +9.2 pts; deployed via vLLM on A10G" |
| "Production-grade system" | "Shipped multi-agent orchestrator in production (LangGraph + Redis + HITL); 4M+ events/month | gọi số thực trong project mockup |
| "Passionate about AI" (đã cũ) | **BỎ** — chuyển sang thể hiện qua action + metric |
| Header bullet "Software Engineer AI" | Header bullet quantifiable: "AI Engineer — production LLM systems, 4M+ events/month" |
| Dài 2 trang cho fresh grad | 1 trang tối đa; priority lên top 4–6 bullet quan trọng nhất |
| Nhiều từ khóa keyword stuffing | Skill section rõ ràng, summary 3–4 keyword dạng entity nhận dạng (llm, rag, evals, mcp) |

## 3. Hiểu vị trí hiện đại: 5 vòng đánh giá qua CV trong 6 giây

Một hiring manager quét CV fresh-grad AI engineer mất ~6 giây. 5 pass:

1. **Keyword scan** ( đầu tiên): "LangChain?" "Chroma?" "LlamaIndex?" "vLLM?" "evals?" — nếu không có ít nhất 3 keyword từ JD, bỏ qua
2. **Metric check**: có số không? "trained" không đủ, cần "reduced latency X%", "improved F1 from Y to Z"
3. **Production signal**: có deploy endpoint không? có link demo / repo public không? các company có AI team muốn xem code public
4. **Engineering discipline**: Git history, README, data versioning, experiment tracking cho thấy bạn biết chơi như engineer, không chỉ chơi như researcher + engineer đau đầu không đều
5. **Signal của cv.md format**: ứng với format (chữ - bullets - links - metric) → tin bạn hiểu cách trình bày professional content

## 4. Tại sao không dùng /career-ops pdf từ đầu (skipped)

**career-ops pdf** mode giả định **đã có cv.md**. Nếu sinh viên mới không có cv.md → phải tự build từ đầu. `ai-cv-forge init` chính là bước "kịch bản chuyển vào cv.md". Sau khi có cv.md → chuyển sang `career-ops` để chạy auto-pipeline, scan offers, apply.

**Phối hợp:**
```
ai-cv-forge init  →  cv.md + profile.yml + README
      ↓
ai-cv-forge linkedin-brief / story-bank  →  (nếu muốn)
      ↓
career-ops {JD_URL}  →  auto-pipeline (đánh giá offer + sinh CV theo JD + tracker)
```

## 5. Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| cv.md | CV dạng markdown | Career-ops format; source of truth cho PDF |
| profile.yml | Profile cấu hình | YAML config candidate info |
| archetype | Vai trò/khuôn mẫu vai trò | Loại vai trò AI trong hiring |
| brief | Project brief | Mô tả chi tiết 1 project phù hợp profile |
| STAR+R | Khuôn mẫu câu chuyện phỏng vấn | Situation → Task → Action → Result → Reflection |
| ATS | Hệ thống đọc CV | Applicant Tracking System — quét CV tự động |
| p95 / p99 | Phân vị độ trễ | 95th/99th percentile latency — metric latency phổ biến |
| HITL | Human-in-the-loop | Người dùng/người giám sát ở giữa pipeline |
| evals | Đánh giá | Đánh giá LLM/app chất lượng bằng metrics automation |
| LLMOps | LLM operations | Pipeline production cho LLM (observability, cost, evals, deployment) |
| vector DB | Cơ sở dữ liệu vector | Lưu embedding cho RAG |
| lod | ...

---
