# CV Template — ai-cv-forge (Fresh AI Graduate)

Sử dụng template này làm skeleton. Điền content vào `{{...}}` hoặc để agent auto-fill khi _SKILL.md mode.
Format: Markdown tương thích `career-ops` (cite bằng path trong cv.md cho PDF generation).

---

# CV -- {{FULL_NAME}}

**Location:** {{LOCATION}}  **Email:** {{EMAIL}}  **LinkedIn:** {{LINKEDIN}}  **Portfolio:** {{PORTFOLIO}}  **GitHub:** {{GITHUB}}

## Professional Summary

{{3-4 dòng tóm tắt: background hiện tại (sinh viên mới ra trường AI) + project chính + skill nổi bật + mục tiêu role mong muốn. Viết ở present tense, không có "passionate about".}}

Ví dụ pattern: "Recent AI/ML graduate from [University] with hands-on experience building [types of systems]. Built [project] achieving [metric]. Proficient in [tools]. Looking for [target role] to apply [strength] to [domain]."

## Work Experience / Internship / Research

### {{COMPANY}} -- {{LOCATION}}
**{{ROLE_TITLE}}**  {{DATE_RANGE}}

{{4-5 bullets, mỗi bullet: Action + Tool + Result (có số). Với fresh grad, mô tả internship như production work — dynamic verb, quantifiable.}}

- {{Action verb}} {{WHAT}} using {{TOOL}}, {{RESULT with metric}}
- ...

### Nếu có Teaching / TA / Research Assistant:
{{Mô tả tương tự — teaching experience được nhiều công ty AI đánh giá cao}}

## Projects (Most Important Section for Fresh Grad)

{{3-4 project cards. Mỗi project ~3-5 lines tổng cộng: tên bold + description → bullets. Project phải có link GitHub/demo.}}

### {{PROJECT_NAME}} ({{STATUS: production / demo / research}})
{{1-2 dòng mô tả: problem → approach → result}}

- {{Bullet 1: Tool + Action + Metric}}
- {{Bullet 2: Result / impact}}
- **GitHub:** {{URL}}  **Demo:** {{URL nếu có}}

### {{PROJECT_NAME_2}} -- ...
...

## Education

- {{DEGREE}}, {{UNIVERSITY}} ({{DATES}})
- GPA: {{GPA nếu > 3.5/4.0 hoặc theo scale}}
- Relevant coursework: {{2-4 môn chính: Deep Learning, NLP, Computer Vision, MLOps, ...}}
- Thesis / capstone (nếu có): {{1 dòng}}

## Certifications (nếu có)

- {{Certification name}} -- {{Issuer}} ({{Date}})
- ...

## Skills

Chia nhóm để ATS nhận diện tốt:

- **LLM / GenAI:** {{LLaMA, GPT, LangChain, LlamaIndex, Prompt Engineering, ...}}
- **ML/AI Fundamentals:** {{PyTorch, TensorFlow, scikit-learn, Hugging Face, ...}}
- **MLOps / Deployment:** {{Docker, FastAPI, MLflow, model monitoring, CI/CD, ...}}
- **Data & Retrieval:** {{RAG, vector DB (Chroma/Pinecone/Qdrant), embedding, ...}}
- **Languages:** {{Python (daily), SQL, ...}}
- **Tools & Infra:** {{Git, Linux, AWS/GCP/Azure basics, ...}}

## Open Source / Community (nếu có)

- **{{REPO_NAME}}** -- {{Mô tả ngắn}}, {{stars/forks/downloads}}, {{link}}
- Blog posts, talks, contributions: ...

## Awards / Competitions (nếu có)

- {{Tên giải}}, {{Rank}}, {{Năm}}

---

## Tips khi điền template:

1. **Projects section là quan trọng nhất** với fresh grad — không công ty nào tuyển fresh grad mà không xem project
2. Mỗi bullet phải có ít nhất 1 số hoặc link demo; "trained model" không đủ — "fine-tuned LLaMA-3-8B, F1 +8.4 pts over base" đủ
3. Educational projects vẫn được ghi như project thật nếu có metrics — không cần production deployment mới được liệt kê
4. Links phải clickable (Markdown `[text](url)`) — ATS đọc được, recruiter cũng đọc được
5. Không để quá 1 trang; nếu dài → cắt Educational details phụ, giữ lại bullets quan trọng nhất
6. Skills section theo nhóm giúp ATS keyword matching tốt hơn list phẳng
