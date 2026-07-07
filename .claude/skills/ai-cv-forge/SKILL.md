---
name: ai-cv-forge
description: "CV & career profile builder dành riêng cho sinh viên ngành AI mới ra trường. Từ input tối thiểu (khóa học, project, internship) → sinh cv.md + profile.yml + README theo format career-ops, cập nhật mindset tuyển dụng AI thực tế 2025–2026 (agentic, eval, RAG, MLOps, LLM infra), bỏ lối mòn template. Output feed thẳng vào career-ops pdf/apply. Triggers: init cv, build cv AI, cv scratch, xây cv, ai cv, profile AI mới ra trường, prepare AI resume."
user_invocable: true
args: mode
argument-hint: "[init | resume-brief | project-brief | story-bank | linkedin-brief | profile]"
---

# AI CV Forge — CV builder cho AI graduate theo insight thị trường thực tế

Từ thông tin tối thiểu (tên, trường, khóa học, project nhỏ, internship, kỹ năng) → sinh **cv.md, profile.yml, README, cover letter** theo format tương thích `career-ops`. Cập nhật mindset HR / hiring manager AI 2025–2026: không còn "làm chatbot đơn giản", đang cần agentic pipelines, eval harness, RAG production, MLOps, LLMOps, observability — bulleting quantifiably từng project nhỏ. Không bắt template, không PR fluff.

## Mục tiêu của skill này (khác gì career-ops)

| career-ops `pdf` | ai-cv-forge |
|---|---|
| Input: **đã có `cv.md`** rồi → rewrite theo JD | Input: **không có CV** → sinh từ đầu |
| Target: senior/mid có kinh nghiệm | Target: sinh viên mới ra trường AI, 0–1 yr, có thể có internship/project |
| JD-driven keyword injection | JD-driven + **market-aware role archetypes + project briefs** dựa trên trend 2025–2026 |
| Template fill theo format sẵn | **Template minimal** + agent gợi ý chi tiết phù hợp từng profile |
| Portrait | Portrait + **Onboarding flow** |

## Phạm vi output

- Root output: **cv.md** (Markdown, career-ops format)
- **profile.yml** (YAML, career-ops format)
- **README.md** (giải thích chiến lược, narrative bridge)
- **FULL COVERAGE OUTPUT cho từng mode**:
  - `init`: cv.md + profile.yml + README.md + brief.md (project briefs) + story-bank.md (STAR+R stories)
  - `resume-brief`: cv.md chỉ (dành cho người đã có profile sẵn)
  - `project-brief`: 2–3 project briefs phù hợp profile + JD pattern
  - `story-bank`: 5–8 STAR+R stories từ experience thực tế
  - `linkedin-brief`: optimized Vietnamese/EN LinkedIn About + Featured + Skills SEO
  - `profile`: chỉ profile.yml + brief justification

Mỗi file được **viết đầy đủ**, không để placeholder `{{fill_me}}` mà không giải thích cách điền.

## Shared context (loaded cho mọi mode)

Đọc trước khi chạy bất kỳ mode nào:

- `templates/cv-template.md` (layout / section order reference)
- `references/modern_ai_market_2025_2026.md` (keyword bag, role archetypes, employer signals — đọc mỗi lần)
- `references/ats_rules_2025.md` (ATS do/don't 2025)

### Ngữ cảnh UI / built-in này

Gọi tool `read` (built-in) để đọc td các file reference khi cần. Workflow này chỉ đọc khi cần.

---

## Mục tiêu của mode

Khi user gọi skill này, nếu không chỉ rõ mode → có 2 fallback hợp lý:
1. Có profile.yml hiện có → chạy `resume-brief` để sinh/refresh cv.md.
2. Không có profile.yml → chạy `init` (mặc định).

---

# Mode List

## Mode 1: `init` (mặc định) — Tạo profile + CV + README từ đầu

### Input format (1 trong 2)

**A. Structured form** (khuyến nghị gọi `gobal-orchestrator` phân tích structured input qua file):

Người dùng cung cấp dạng form sau (ít nhất phải có 3 trường có data, nếu thiếu agent hỏi 1 câu):

```markdown
## Form ai-cv-forge init

### Identity
- Full name:
- Email:
- Phone (optional):
- Location (city, country):
- LinkedIn URL:
- GitHub URL:
- Portfolio / demo URL (nếu có):

### Education
- Trường, ngành, GPA (nếu > 3.5/4.0), năm tốt nghiệp / dự kiến
- Liên quan: course AI/ML notable (deep learning, NLP, LLM, CV, RL, MLOps...)

### Projects (mỗi mục: tên + mô tả ngắn + kết quả số nếu có)
1. 
2. 
3. 

### Internship / Work experience (nếu có)
- Vị trí, công ty, mô tả công việc

### Awards / Competitions / Publications (nếu có)
...

### Kỹ năng chính (liệt kê tự nhiên, không phân loại)
- Ngôn ngữ: Python (có thể nói framework), SQL, etc.
- Framework: PyTorch/TensorFlow, LangChain, Hugging Face, etc.
- Tools: Docker, Git, cloud provider, etc.

### Target role mong muốn (có thể mơ hồ, agent sẽ clarify)
- ví dụ: "AI Engineer", "ML Engineer", "Data Scientist", "AI PM", v.v.

### Điểm mạnh / đặc điểm cá nhân muốn nhấn (tự nguyện)
 ví dụ: thích giảng dạy, từng bán product, từng thi đấu Kaggle, v.v.
```

**B. Paste file** — người dùng đưa link file hoặc nội dung cv.md hiện có → agent đọc rồi refactor.

### Output form

```
cv.md
profile.yml
README.md
briefs/
  project-brief-01.md
  project-brief-02.md (nếu có đủ project)
  project-brief-03.md (nếu đủ)
interview-prep/
  story-bank.md
```

### Workflow chi tiết

#### Step 1 — Clarify missing (agent tự chủ)

Nếu input thiếu điểm mấu chốt (học thuật kém rõ, không có project / internship, không rõ target), agent hỏi **tối đa 3 câu** để đủ sinh được CV chất lượng tốt nhất:

Ví dụ câu hỏi:
- "Bạn có muốn hướng đến kỹ sư kỹ thuật (software engineer, MLOps) hay hướng sản phẩm / nghiên cứu AI?"
- "Project nào của bạn bạn tự hào nhất? Có link GitHub / demo không?"
- "Bạn có quan tâm đến khía cạnh nào của AI hơn — xây model, deploy pipeline, build product, nghiên cứu?"

Sau khi đủ info → chuyển sang step 2.

#### Step 2 — Archetype detection + North Star selection

Dựa trên target role + kỹ năng + project → chọn 1–2 archetype chính, 1–2 adjacent.

Primary archetypes (2025–2026, dựa trên trend tuyển dụng thực tế):

| Archetype | Signals trong JD 2025-2026 | What they BUY |
|---|---|---|
| **AI/ML Engineer (General)** | PyTorch, scikit-learn, model training, experiment tracking | Có thể train + evaluate model end-to-end |
| **LLMOps / AI Platform Engineer** | LangSmith, Prometheus, model registry, deployment, pipelines, evals | AI system đi vào production có reliability, cost control |
| **Agentic / Multi-Agent Engineer** | LangChain/LangGraph, function calling, tool use, orchestration, HITL | Build agentic workflow đáng tin cậy, có guardrails |
| **RAG / Retrieval Engineer** | vector DB (Chroma/Pinecone/Qdrant), embedding, chunking, hybrid search, reranking | Retrieval pipeline production-grade |
| **MLOps / Data Engineer (AI)** | Airflow, Feast, model monitoring, retraining pipeline, data quality | Infrastructure cho AI, vòng đời model |
| **AI Product Manager (Technical)** | PRD, roadmap, discovery, experiments, stakeholder | Có technical depth để lead AI product |
| **AI Solutions Architect / Forward Deployed** | enterprise integration, design, customer-facing, fast prototype | Chuyển AI research thành giải pháp khách hàng dùng được |
| **AI Research Engineer (Applied)** | fine-tune, RLHF, preference optimization, SFT, evaluation | Có tay nghề research + engineering cho cutting-edge model |

**Giải thích cho người dùng (Việt):** "Theo thị trường tuyển dụng AI 2025–2026, đây là các vai trò phổ biến nhất. Mình sẽ gợi ý role phù hợp với background của bạn để CV mạnh nhất."

#### Step 3 — Hiểu role archetype để build content

Dựa trên archetype detection, mở `references/modern_ai_market_2025_2026.md` → đọc phần keyword bag + proof-point templates cho archetype đó.

**Mapping keyword "bắt buộc" 2025–2026 theo archetype** (dùng để craft achievement bullet):

- **LLMOps / AI Platform Engineer**: agent observability, model registry, deployment pipeline, evals, cost-per-query, p99 latency, Grafana/MLflow/LangSmith, retraining trigger, A/B testing, sharding, rate-limiting, token tracking
- **Agentic Engineer**: multi-agent orchestration, HITL, tool use, function calling, planner/executor, checkpointer, state machine, idempotency, timeout handling, fallback chain, human-in-the-loop review
- **RAG Engineer**: chunking strategy, hybrid search, reranker, context window optimization, hallucination rate, citation accuracy, retrieval precision/recall, metadata enrichment, multi-tenant vector store
- **MLOps**: feature store, drift detection, data quality, retraining triggers, experiment tracking, CI/CD for model, deployment orchestration, Airflow/Kubeflow
- **Applied Research Engineer**: SFT, RLHF, DPO/ORPO/KTO, preference data, reward modeling, evaluation harness, ablation study, hyperparameter sweep, LoRA/QLoRA
- **AI Solutions Architect / Forward Deployed**: enterprise integration (API gateway, SSO, RBAC), customer POC, cost estimation, playbook, SLA, on-prem deployment
- **AI PM (Technical)**: PRD, discovery sprints, experiment design, A/B tests, stakeholder alignment, roadmap, OKR/KPI, user research with AI

Skill đọc archetype → chọn **4–6 keyword phrase chính** để inject vào triết lý viết bullet, không hardcode.

#### Step 4 — Build cv.md từ dữ liệu thô

Thứ tự section (theo format career-ops, "6-second recruiter scan"):

```
Header (tên, liên hệ)  ← bắt buộc
Professional Summary  ← 3–4 dòng, keyword-rich, "exit narrative" bridge từ background hiện tại sang role mong muốn
Work Experience / Internship / Teaching (nếu có)  ← bullets 4–6/công việc, mỗi bullet dạng [ACTION] + [TOOL] + [RESULT số]
Projects  ← top 3–4 project, mỗi cái 2–3 bullet quantifiable
Education & Certifications  ← trường, GPA nếu >3.5, 2–4 relevant certs
Skills  ← chia nhóm: AI/ML, MLOps/LLMOps, Language, Tools/Infra
Portfolio / Repos (nếu có)  ← link + mô tả ngắn 1 dòng
```

**Quy tắc viết bullet (bắt buộc tuân theo để pass ATS + ATS không bắt bắt template):**

- Format chính: `[Action verb] [WHAT] using [TOOL/FRAMEWORK], achieving [RESULT]`
- ABSOLUTELY không bắt đầu bằng "responsible for", "assisted with", "helped" → bắt đầu bằng động từ mạnh (trained, built, engineered, architected, optimized, evaluated, deployed, instrumented, led)
- Mỗi bullet phải có **ít nhất 1 số** (nếu project quá nhỏ không có metric → dùng "delivered", "reduced" với kết quả định tính rõ)
- Không "improved performance" không số → thay bằng "reduced p95 latency from 2.1s to 380ms" hoặc "improved throughput by 40% (180 → 252 doc/min)"

VD quy tắc đúng/sai:
| ❌ Lối mòn (cũ) | ✅ Mới (hiện đại 2025-2026) |
|---|---|
| "Developed a chatbot using RAG" | "Built RAG pipeline (LlamaIndex + Qdrant) for 12K-doc knowledge base; retrieved passages in 180ms p95" |
| "Worked on LLM fine-tuning" | "Fine-tuned Llama-3-8B with LoRA on 40K industry corpus; F1 +8.4 pts over base; deployed via vLLM on 1× A10G" |
| "Built an AI web app" | "Shipped FastAPI + Streamlit demo of multi-agent orchestrator; 5 tools, HITL approval gate, Redis checkpointer; served 20 devs internally" |
| "Responsible for model evaluation" | "Built eval harness with 17 custom metrics; caught 2 regressions in CI before they reached production" |

**Anti-fluff vocabulary (bắt buộc tránh):**
"passionate about", "results-oriented", "proven track record", "leverage[d]", "spearheaded", "best practices", "innovative solution", "cutting-edge", "fast-paced environment", "synergy", "seamless", "demonstrated ability to"

Agent **tự động thay** bằng ngôn ngữ cụ thể, sát thực tế công việc.

#### Step 5 — Build profile.yml

```yaml
candidate:
  full_name: "..."
  email: "..."
  phone: "..."          # optional
  location: "..."
  linkedin: "..."
  github: "..."
  portfolio_url: "..."

target_roles:
  primary:
    - "..."
  archetypes:
    - name: "..."
      level: "Entry / Junior / Mid"
      fit: "primary"
      keywords: [...]   # keyword auto-lifted từ JD pattern

narrative:
  headline: "..."
  exit_story: "..."                    # 1 câu: context hiện tại → muốn hướng tới đâu
  why_this_track: "..."                # lý do chọn con đường này — cá nhân, tự nhiên

superpowers:
  - "..."

proof_points:
  - name: "..."
    url: "..."
    hero_metric: "..."
    track: "..."                       # archetype liên quan

compensation:
  target_range: "..."                 # per JD của region, agent WebSearch để gợi ý range
  currency: "..."
  minimum: "..."

location:
  country: "..."
  city: "..."
  visa_status: "..."                   # no sponsorship needed / needs
```

Agent điền mọi trường. Nếu thiếu (ví dụ không có portfolio URL), ghi chú trong output `README.md` gợi ý cách lấy / tạo.

#### Step 6 — Build briefs (project-brief-NN.md)

Với mỗi project lớn trong CV, tạo file bổ sung chứa:

```markdown
# Project Brief: <tên project>

## Context / Problem statement (2–3 câu)
--Giải thích vấn đề đang muốn giải quyết (không nói "học", nói "cần có giải pháp cho...")--

## Input / Approach (2–3 câu)
--Tóm tắt kiến thức nền + phương pháp + tool stack sử dụng--

## Output / Result (số/dạng có thể đo)
- **Metric 1**: 
- **Metric 2**:
- **Deliverable**: (notebook, repo, demo link, PDF, presentation, etc.)

## Hardware / Environment (nếu có)
- GPU used: (RTX 3060 12GB / Kaggle / Google Colab / CPU-only)
- Data source: (kaggle, personal collect, open-source dataset)

## CV Bullets (đã chốt, copy-paste vào cv.md)
1. Động từ + công việc + tool + kết quả
2. ...

## Giải thích lý do chọn project brief này (ballpark)
--Giúp người đọc CV hiểu "tại sao là cái này?"--
```

Agent nên đóng gói vài nguồn thông tin về how to write strong project descriptions for AI engineering roles (bằng research qua WebFetch với nguồn đáng tin, hoặc template nội bộ). Nhưng ở đây mình sẽ extract vài pattern từ các role description thực tế của các công ty tuyển dụng AI hiện tại (đọc từ các file đã có trong career-ops).

#### Step 7 — Build story-bank.md (STAR+R format)

Mỗi story là 1 project/internship → 1 câu chuyện 5 câu (STAR+R):

- **S**ituation: ngữ cảnh (khóa học, internship, competition)
- **T**ask: nhiệm vụ cụ thể
- **A**ction: bạn đã làm gì — WITH evidence
- **R**esult: kết quả định lượng / định tính
- **R**eflection: điều gì bạn học được, nếu apply lại sẽ làm khác

Ví dụ (template):
```markdown
## Story 1: Llama-3 fine-tune cho Legal Doc Classification

- **Situation**: Cuối khóa NLP, được giao bài classify legal contracts bằng model thuật toán
- **Task**: Đạt F1 >= 82% trên imbalanced dataset 12K docs, 47 lớp
- **Action**: (1) LoRA QLoRA 4-bit trên Llama-3-8B + LoRA rank 16; (2) augment minority với back-translation vi→en; (3) threshold sweep; (4) eval trên 3 folds
- **Result**: F1 = 85.3 (vs base 76.1), +9.2 pts, repo có 180 stars
- **Reflection**: Nếu làm lại sẽ dùng DPO thay cross-entropy thuần để giảm hallucination trên class hiếm
```

Agent cung cấp **5–8 stories** phù hợp profile nhận được.

#### Step 8 — Build linkedin-brief.md (optional theo ngữ cảnh)

```
- Tiêu đề headline (tối ưu search): headline + 4 keyword
- About section (~150–200 từ): câu chuyện sự nghiệp tóm tắt, "I'm choosing" ngụ ý
- Featured: 3 item (repo, project, article)
- Skills SEO: list skills priority theo archetype
```

#### Step 9 — README.md chiến lược / narrative guide

Dành cho người dùng (human-readable):

```markdown
# CV của bạn — Chiến lược & Cách dùng

## Lý do chọn archetype này (viết thêm các lý do phù hợp với profile của bạn)
## Narrative: câu chuyện sự nghiệp của bạn tóm tắt 1 dòng
## Điểm mạnh chính (3–5)
## Đề xuất bổ sung để nâng cấp (nếu muốn đạt mức cao hơn)
## Cách dùng skills này + career-ops phối hợp:
1. Chạy ai-cv-forge `init` → có cv.md + profile.yml
2. Chạy career-ops `/career-ops {JD_URL}` → auto-pipeline sinh PDF + draft answers
3. Chạy ai-cv-forge `linkedin-brief` để tối ưu hồ sơ LinkedIn
```

---

## Cấu trúc quản lý subagent khi xử lý lớn

Skill này **tự viết trực tiếp output** (single-agent) — không cần fan-out vì:
- Output vừa đủ lớn (5–8 file) cho 1 agent
- Mỗi file phụ thuộc file trước (cv.md dùng input profile)
- Hiệu quả hơn 1 agent cố định hành vi

**Tuy nhiên**, mode `init` có thể async background:
1. Agent chính sinh cv.md, profile.yml, README
2. In parallel: sinh `briefs/` và `story-bank.md`

---

# Mode 2: `resume-brief` — Refresh cv.md từ profile hiện có

## Input

`profile.yml` tồn tại + JD (nếu có) hoặc mô tả target role mới.

## Output

Chỉ 1 file: **cv.md** mới, override cũ.

## Đặc trưng "modern AI" cập nhật vào cv.md refresh

- Đảm bảo có **header section "LLM / GenAI Capabilities"** nếu role liên quan (Hiện tại các công ty cho AI muốn xem được ngay bạn có kinh nghiệm gì với LLM — phải có section Riêng hoặc Skills section có LLM keyword)
- Đảm bảo JG các bullet dạng "trained → improved → deployed → instrumented" loop — đây là pattern quan trọng nhất trong JD 2025–2026
- Đảm bảo có **Phần GitHub / Open Source nếu có** (repo + số sao + used-by note)
- Đảm bảo có ít nhất 1 project có deployment / prod exposure (không chỉ notebook sandbox)

## Quy tắc bổ sung cho fresh graduate (0–2 năm)

Vì chưa có kinh nghiệm production thực tế:
1. **Internship / Tết linh hoạt**: mô tả internship như kinh nghiệm production — dùng động từ mạnh, encode số (processed X, delivered Y, saved Z hours)
2. **Course project lên production**: uni course project nếu có metrics (F1, throughput, latency) thì ghi như project thật (project card)
3. **Hackathon / Competition**: nếu có kết quả (rank, prize) → ghi dạng achievement, có thể dùng "Award" section
4. **Open Source contribution**: PR merged, issue triaged → tính như "work experience", nhiều công ty trân trọng này (Đặc biệt là công ty software)
5. **Blog / Paper / Speaking**: ghi dạng "Publications & Speaking" — không cần ấn tượng cũng ghi (kèm blog link + topic)

---

# Mode 3: `project-brief` — Sinh project briefs phù hợp profile

## Input
- profile.yml hoặc text mô tả background user
- Tùy chọn: JD (để recommand project cụ thể theo role)

## Output
- 2–3 file `briefs/project-brief-NN.md`
- Mỗi brief có: problem statement → approach → result template → cv bullets → justifications

## Project categories hiện đại AI 2025–2026 (skill gợi ý theo profile)

| Category | Level phù hợp fresh-grad | Why quan trọng |
|---|---|---|
| RAG / Knowledge Base Builder | Beginner–Mid | 90%+ JD cho AI Engineer có từ "RAG", "retrieval", "vector DB" |
| Multi-Agent Orchestration Demo | Mid | "Multi-agent", "tool use" là keyword hot 2025–2026 |
| LLM Evaluation Harness | Beginner–Mid | "Eval-driven" đang trở thành yêu cầu phổ biến — kỹ năng đáng giá |
| LLM fine-tuning (SFT/DPO/LoRA) | Mid | Đặc biệt cho role Applied Research — không quá khó với fresh grad nếu có resource |
| MLOps / CI-CD Pipeline cho LLM | Beginner | Gắn với automation mindset, employer thích |
| Production Chatbot with Guardrails | Beginner | Cũ nhưng vẫn keyword ĐẦU — phải có guardrails mới khác template: HITL, content filter, rate limiter |
| AI Product BMI / Cost Tracker | Mid | Cost-of-AI quant là skill 2025 mới nổi — ít người có, đáng highlight |
| RAG + Fine-tune Hybrid | Mid | Show bạn hiểu hiệu năng RAG có giới hạn → fine-tune để nâng cao |

**Skill không GENERATE full code** — sinh brief (problem → approach → expected result → tech stack → metrics) — người dùng tự triển khai trên colab/local, tuy mô tả chi tiết.

---

# Mode 4: `story-bank` — STAR+R Interview Prep từ cv.md

## Output
- `interview-prep/story-bank.md`

## Workflow
1. Đọc cv.md + profile.yml
2. Select 5–8 strongest evidence items (project, internship, award)
3. Mỗi item → 1 story STAR+R
4. Optional: Story có thể mở rộng thành cover letter paragraph

## Format trong file
```markdown
# Project 1: ... 

**Note:** Học từ AI hiring thực tế: interviewers frequently hỏi "Tell me about a time X", story bank này chuẩn bị.

## Story A: <tên scenario>
- **Situation**:
- **Task**:
- **Action** (3–5 bước cụ thể):
  1. 
  2. 
  3. 
- **Result** (định lượng):
- **Reflection**:
- **JD mapping**: nếu JD có keywords náy, story này match vào đâu?

## Story B: ...
```

---

# Mode 5: `linkedin-brief` — Tối ưu LinkedIn profile cho AI roles

## Output
- `linkedin-brief.md` (or `README.md` khi combine với init)

## Section cần cover
- Headline (tối ưu keyword cho recruiters)
- About (~200 từ, narrative-driven, không copy-paste CV)
- Featured (3 item chọn lọc)
- Skills (top 10 structured, theo archetype)
- Experience rewrite (câu mô tả ngắn → viết lại chuyên nghiệp, quantifiable)

---

# Mode 6: `profile` — Chỉ sinh profile.yml + justification

## Output
- `profile.yml`
- `PROFILE_JUSTIFICATION.md` (giải thích từng trường)

---

# Gợi ý chiến lược build CV hay & hiện đại 2025–2026 (đi vào output README.md)

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

# Errors / Edge Cases

**NGHIÊM CẤM:**
- Không generate cv.md mà bỏ SECTION quan trọng (Skills, Education, Projects)
- Không sinh phải có section header / content vượt ATS quy định (ATS doc không đọc section quá mờ)
- Không nhắc "Passionate about AI" — spam phrase, auto-remove
- Không đặt output **inside the skill folder** — theo `workbench-conventions.md` §3a, output vào project cwd: `output/cv-init-{candidate-slug}-{date}.md` etc.

**Edge**
- Không có project → bắt user nhập, không generated "fake project" — nếu thiếu, ghi rõ trong output + gợi ý khởi tạo 1 project
- Không có GitHub/portfolio → gợi ý bước tạo (1 repo public tối thiểu)
- Ngôn ngữ output: mặc định tiếng Việt (vn) cho README/mô tả, tiếng Anh cho machine-facing (YAML keys, code comments, file content)
- `candidate-slug` từ `candidate: full_name` lowercase + replace space → {nguyen-van-a}
- ISO-range date: `YYYY-MM-DD`

**If running inside career-ops**, skill sẽ đọc danh sách các file cần thay thế / ghi đè lên artifact để không lặp quá nhiều.
