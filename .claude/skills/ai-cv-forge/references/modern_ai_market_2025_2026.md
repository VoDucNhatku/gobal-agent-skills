# Modern AI Market — Hiring Trends & Keywords 2025–2026

> Skill-internal reference. Loaded by ai-cv-forge modes to inject market-relevant language into cv.md, profile.yml, story-bank. Do NOT dump into user output.

---

## 1. Hiring Reality Check 2025–2026

### What companies ACTUALLY hire for (not what job boards copy-paste)

| Tier | Reality | Implications for fresh-grad CV |
|---|---|---|
| LLM product companies (Anthropic, OpenAI, Mistral, Cohere) | Looking for applied researchers + infra engineers. Fresh grad needs strong math + systems + reproducible code | Emphasize: paper reproduction, eval rigor, benchmark results, code quality |
| AI-native startups (mid stage, Series A–B) | Need full-stack AI engineers who ship POCs fast, convert research to product | Emphasize: deployment, customer-facing demo, end-to-end ownership |
| Enterprise AI teams (FAANG, banks, consulting) | Need AI platform engineers (LLMOps/evals), need AI PMs who can navigate bureaucracy | Emphasize: productionization, tooling, process, documentation |
| Consulting / System integrators | Need generalist AI engineers who can demo anywhere + solutions architects | Emphasize: breadth, client communication, POC speed |
| AI-first SaaS (newer mid-stage) | Need domain-AI engineers who ship features, not just experiments | Emphasize: shipped product, user-facing quality, A/B testing |

### What is DECLINING in demand (2025→2026 shift)

- "I trained a model in a course project" — no longer a signal unless you can point at a metric
- "I know Machine Learning" (generic) — too vague, must anchor to specific techniques
- Single-tool specialists ("I know PyTorch") without deployment story
- "Passionate about AI" phrases — spam filter level 1
- 2-page CV for fresh grad — 1 page hard ceiling
- LinkedIn endorsements / "open to work" banner as primary signal — portfolio > banner

### What is RISING in demand (what to put on CV)

- **Agentic systems fluency** — even junior roles mention "agent", "tool use", "multi-step reasoning", "orchestration". Having LangChain/LangGraph project on CV is a differentiator.
- **Evaluation mindset** — "I built eval harnesses", "I measure hallucination rate", "CI for LLM regression". This shows you think like an AI engineer, not just an AI researcher.
- **Cost consciousness** — "Optimized token usage", "Reduced inference cost by X%", "Quantized model to fit Y-context". AI teams care about burn rate.
- **RAG / Retrieval knowledge** — still universally needed. Not just "RAG chatbot" but understanding chunking, reranking, hybrid search, metadata.
- **LLMOps familiarity** — model registry, deployment pipeline, observability even if minimal. Using MLflow, Weights & Biases, LangSmith.
- **Production-grade code** — tests, typing, Docker, API design. Huge gap among fresh grads; closing it signals engineering maturity.
- **Communication + Teaching** — ability to explain AI decisions to non-technical stakeholders. Blog, talks, mentorship = signal.

---

## 2. Keyword Bag by Archetype (for ATS + human scanning)

> Use these to naturally inject into bullet language. Don't keyword-stuff — weave into real achievement description.

### AI/ML Engineer (General)
PyTorch, TensorFlow, scikit-learn, HuggingFace Transformers/Trainer, experiment tracking, MLflow/W&B, model training, fine-tuning (LoRA/QLoRA/ full fine-tune), hyperparameter sweep, evaluation metrics (F1, precision/recall, BLEU, ROUGE, mAP, mIoU, etc.), data pipeline, feature engineering, cross-validation

### LLMOps / AI Platform Engineer
LangSmith, prompt evaluation, model registry, deployment pipeline, A/B testing (cannary), CI/CD for models, observability (Grafana, Prometheus), cost-per-query tracking, token usage monitoring, p95/p99 latency, retraining triggers, data drift detection, sharding, rate limiting, caching, containerization (Docker/K8s), API gateway

### Agentic / Multi-Agent Engineer
LangChain/LangGraph, function calling, tool use, orchestration, multi-agent, planner/executor, HITL (human-in-the-loop), checkpointer (Redis/Postgres), state machine, idempotency, timeout handling, fallback chain, approval gates, agent observability

### RAG / Retrieval Engineer
vector DB (Chroma/Pinecone/Qdrant/Weaviate/Milvus), embedding model (OpenAI/text-embedding-3, Cohere, BGE, GTE), chunking strategy (semantic/recursive/fixed), hybrid search (BM25 + dense), reranker (Cohere Rerank, BGE Cross-Encoder), metadata filtering, context window optimization, retrieval precision/recall, hallucination rate, citation accuracy, multi-tenant vector store

### MLOps / Data Engineer (AI)
Feast/Tecton (feature store), Airflow/Prefect, model monitoring, data quality, Great Expectations, retraining pipeline, CI/CD for ML, deployment orchestration (SageMaker/Vertex/Kubeflow), experiment tracking, data versioning (DVC), model versioning, Kubernetes

### Applied Research / Fine-Tuning
SFT (Supervised Fine-Tuning), RLHF, PPO, DPO/ORPO/KTO, preference data, reward modeling, evaluation harness, ablation study, hyperparameter sweep, LoRA/QLoRA/QLoRA, quantization (GPTQ/AWQ), vLLM/TGI, inference optimization

### AI Product Manager (Technical)
PRD, discovery sprints, experiment design, A/B tests, stakeholder alignment, roadmap, OKR/KPI, user research with AI, ML/AI briefings, cost estimation, incident response, change management

### AI Solutions Architect / Forward Deployed
enterprise integration (API gateway, SSO, RBAC), customer POC, cost estimation, playbook, SLA, on-prem deployment, security review (SOC2, GDPR), multi-provider LLM switching, SDK design, sandbox environment

---

## 3. Employer "Signals to Look For" (fresh-grad guide)

### Green Flags (put these on CV if real)
- [ ] Project has **README.md** với 3 sections: Problem → Approach → Result
- [ ] Repo public, linked in CV
- [ ] At least 1 metric per project (accuracy, latency, cost, throughput, user count)
- [ ] Tech stack mentioned (not just "AI project" — name PyTorch/LangChain/etc.)
- [ ] Demo link works (not placeholder)
- [ ] You can explain "why this approach" not just "what I did"
- [ ] Tests / lint / CI exists in repo (even minimal)
- [ ] You contributed to someone else's project (PR merged, not self-starred)
- [ ] You can articulate trade-offs you made

### Red Flags (what recruiters/eng dismiss instantly)
- [ ] "Chatbot" without specifying RAG, tools, guardrails — too generic
- [ ] "Trained model" without architecture, dataset size, metric
- [ ] Course project claims to be production-grade — it isn't
- [ ] No README / README is just copy of assignment description
- [ ] "Passionate about AI" in every sentence
- [ ] Listing 30 tools at "proficient" level — nobody is
- [ ] Project doesn't run / broken demo link — worse than not having one
- [ ] Code is 90% copied from tutorial without attribution in README
- [ ] "Team project" where you can't describe YOUR specific contribution

### The 3-Tier Project Stack for Fresh Grad CV

| Tier | Description | CV Treatment |
|---|---|---|
| T1: Shipped | Live endpoint, real users, metrics collected | Lead with, position as "production exposure" |
| T2: Demo-ready | Repo runs end-to-end, demo link, reasonable README | 2nd position, "built and validated" |
| T3: Notebook/Sandbox | Colab notebook, tutorial-following, learning artifact | Mention in Education section or omit if space tight |

Recruiters prefer T1 + T2 variety over 4× T3.

---

## 4. CV Language Patterns That Work (2025 vetted)

### Good verbs (start bullets)
Engineered, built, shipped, instrumented, evaluated, optimized, reduced, automated, architected, designed, fine-tuned, validated, deployed, instrumented, prototyped, benchmarked, scaled, refactored, integrated, implemented, maintained, mentored

### Good result shapes (quantifiable)
- "Reduced p95 latency from X to Y (Z% improvement)"
- "Improved F1/precision/recall from X to Y on Z dataset"
- "Processed N documents / records / requests per day"
- "Deployed to N internal users / customers"
- "Saved N hours per week through automation"
- "Ranked top X% in Y competition"
- "Achieved Z-star repo, W contributors"
- "Cut inference cost by X% via quantization / batching / caching"

### Good paragraph shapes (Professional Summary)
```
[Who you are + where from] + [what you built + one metric] + [what stack you used] + [where you're going]
```

Example: "AI/ML graduate from HUST with hands-on experience building production-flavored RAG and multi-agent systems. Built retrieval pipeline over 12K-doc knowledge base (p95 180ms) and fine-tuned LLaMA-3-8B for legal doc classification (+8.4 F1 pts). Proficient in Python, PyTorch, LangChain, LangGraph, Chroma, Docker. Seeking entry-level AI Engineer role to ship LLM-powered features end-to-end."

### Pattern: Trained → Improved → Deployed → Instrumented loop (shown on CV)

Best AI CVs demonstrate awareness of this loop:
- Trained: what model, what data, what objective
- Improved: metric gain, ablation showing what worked
- Deployed: where, how, to whom
- Instrumented: monitoring, evals, cost tracking

Example showing loop: "Fine-tuned LLaMA-3-8B with LoRA on 40K legal corpus (Trained → +8.4 F1). Deployed via vLLM on 1× A10G; p95 latency 220ms (Deployed). Added latency + cost-per-query dashboards in Grafana; auto-alert when p95 > 500ms (Instrumented)."

---

## 5. Sector-Specific CV Tips

### LLM / GenAI focused roles (most common 2025–2026)
- Every bullet must contain OR imply at least 1 of: LLM, RAG, agent, eval, fine-tuning, prompt, deployment
- Section "LLM Capabilities" or "GenAI Projects" is a plus — hiring manager scanning at 2s
- Be ready to discuss: context window limits, temperature vs. top-p, hallucination mitigation strategies, when to fine-tune vs. when to RAG

### ML / Classic roles (computer vision, tabular, time series)
- CV/NLP projects still heavily valued — but to be "modern" pair with LLM/RAG skill
- Show data engineering discipline (data versioning, pipeline, experiment tracking)
- Embeddings, vector search increasingly relevant even for CV (CLIP, multi-modal)

### Data / MLOps / Platform
- Show CI/CD, infra-as-code, monitoring — these beat "model accuracy"
- GitHub history / contribution to infra tools (MLflow, Airflow, K8s operators) big signal
- Mention cost optimization story if you have one (rare for fresh grad but stands out)

### AI Research (academic-to-industry)
- Papers, reproducible experiments, benchmark comparisons, ablation studies
- GitHub should mirror paper's claims (code + data + README matching paper table)
- Blog / Medium post explaining paper in plain language adds signal

---

## 6. Cover Letter / Short-Form Writing Tips (included in apply mode output)

- Direct: "I built X achieving Y" not "I am a self-starter who is passionate about..."
- Phrase as "I'm choosing you" — show you evaluated them specifically
- Quote something concrete from JD/company and connect to YOUR proof point
- Max 1 page; in Vietnam context keep 3–4 short paragraphs max
- Always close with: "Được phỏng vấn để thảo luận cách tôi có thể đóng góp cho [team/dự án cụ thể]"

---

## 7. Anti-Patterns 2025–2026 specific (what's "cringe" now)

- "I'm a recent graduate eager to learn" — every fresh grad says this. Replace with "hands-on experience with X and Y, seeking to deepen Z at your team"
- "Hard worker", "fast learner" — credentials must show these, not claim them
- Listing 20 "skills" without any metric — pick 8–12 key skills and show depth with tools they mean
- "Utilized", "leveraged", "spearheaded" — overused AI-slop verbs
- "AI/ML enthusiast" — get specific or drop the phrase
- "Seeking opportunities to grow" — show what you bring, not what you want to take
- Generic project descriptions — "A chatbot for X" with no architecture or metric
- LinkedIn headline "Open to work" with banner — ditch the banner, fill the headline with keywords

---

## 8. Vietnam-specific notes (if target market is Vietnam / SEA)

- CV gửi qua email: PDF duy nhất, không chèn vào body + không zip nhiều file
- Ở VN recruitment context: ghi rõ "Kỹ năng: Python (5 năm học + project PyTorch)" — rõ thời gian
- Nộp qua các trang tuyển dụng VN (TopCV, VietnamWorks): chú ý điền đúng field "Kỹ năng", "Mô tả bản thân" — parsing engine của VN còn yếu kém hơn US ATS
- GitHub profile: ít nhất 1 repo public có README hoàn chỉnh — hiring manager VN hay check
- Portfolio: nếu không có domain riêng → dùng GitHub Pages / Notion public page / hiệp với career-ops deploy ra domain
