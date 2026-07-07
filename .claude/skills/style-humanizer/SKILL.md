---
name: style-humanizer
description: "Giảm đánh dấu AI-generated text qua heuristic checklist + style calibration. Không dùng perplexity/burstiness metric loop (tool ngoài không có API chuẩn). Áp dụng: kiểm tra burstiness, em dash, throat-cleaning openers, paragraph length variance, synonym cycling, AI-typical term filter. Triggers: humanize, giảm AI, AI checker, burstiness, paragraph variance, writing quality check, qua AI detector, giấu AI, chống AI detect."
---

# Style Humanizer — Writing Quality Check + Style Calibration

Kiểm tra và điều chỉnh văn phong bài báo để giảm signature AI-generated text. Không dùng perplexity/burstiness score vì detector model bên ngoài (GPTZero, Turnitin AI) không công bố API chuẩn để interactive tune.

Tốt hơn: tập trung vào **heuristic checklist** + **style calibration** (feed past papers → cụm từ riêng → không trùng phân phối training LLM).

## Capability

- **Heuristic checklist** (rule-based): flag + suggest fix.
- **Burstiness cue** (local observation, không tính metric): phát hiện 5+ câu liên tiếp có cùng khoảng từ count → suggest lệch độ dài.
- **Style calibration pass**: khi user cung cấp 3+ past papers, generate profile rồi hướng dẫn draft theo đúng fingerprint riêng.

Binding: `~/.claude/rules/paper-writing-integrity.md` §4–5.

## LUẬT 0 — Bất biến bảo toàn nghĩa (meaning-preservation invariant)

Skill này chỉ được đổi CÁCH VIẾT. Tuyệt đối đóng băng: số liệu & đơn vị · công thức
toán · citation key và câu nó bám vào · độ mạnh của claim (shown/suggests/may) · hedge ·
chiều của mọi phép so sánh. Sau khi sửa: diff-check các bất biến trên; lệch bất kỳ →
revert đoạn đó. Sửa văn phong ≠ sửa nội dung; phát hiện câu SAI về nội dung → flag cho
user, không tự sửa nghĩa.

## Quy trình

1. **Term filter**: loại 25 flagged terms (delve, tapestry, landscape, pivotal, crucial, foster, showcase, testament, navigate, leverage, realm, embark, underscore, multifaceted, nuanced, comprehensive, robust, intricate, cornerstone, paradigm, synergy, holistic, streamline, cutting-edge, groundbreaking).
   - Có ngoại lệ: là thuật ngữ chuẩn trong ngành thì giữ.
2. **Punctuation**: em dash ≤3 tổng cộng; semicolon ≤2 / 1000 từ; tránh 2+ đoạn liên tiếp mỗi đoạn mở đầu bằng colon + list.
3. **Throat-cleaning openers**: xóa "In the realm of...", "It's important to note that...", "In this section we will discuss...", "This serves as a testament to..." — trừ roadmap sentence trong Introduction (Section 2 reviews..., Section 3 describes...).
4. **Structure pattern warnings**: không ép Rule of 3 (văn bản tự nhiên không lúc nào cũng 3 mục); đa dạng hóa độ dài paragraph (2→8 câu); synonym cycling cấm trong cùng một đoạn (1 concept = 1 thuật ngữ); binary contrast "Not X. Y." ≤2 toàn bài; mirror structure mỗi section giống hệt nhau → thay đổi theo function (Methods procedural, Discussion exploratory).
5. **Burstiness cue (qualitative)**: nếu 5 câu liên tiếp cùng ~20–25 từ → gắn cờ. Section-specific burstiness target:
   - Abstract: moderate, steady
   - Introduction: cao (mở bằng câu ngắn, kéo câu dài)
   - Lit Review: moderate
   - Methods: cho phép thấp (procedural)
   - Results: moderate
   - Discussion: cao nhất.
6. **TEEL paragraph structure**: Topic → Evidence-with-citation → Explanation → Link. Tối thiểu 120–200 từ / đoạn (EN); ít nhất 3 body paragraph/section. Mở đầu Introduction + kết Conclusion được ngoại lệ.
7. **Citation integration**: narrative + parenthetical theo đúng ngữ cảnh. "While A argued X, this study contends Y" (contrastive), "(Original, Year, as cited in Citing, Year) ≤3 secondary per paper".
8. **Style calibration** (optional, chiến lược quan trọng nhất chống AI detector): khi user cung cấp 3–5 past papers → extract fingerprint:
   - độ dài câu thường dùng, phân bố histogram
   - từ vựng thường dùng theo domain (không dùng default AI-typical)
   - pattern mở đầu đoạn, pattern chuyển đoạn, pattern dùng semicolon/em dash
   - save vào `style_profile`. Khi draft, giữ hòa theo profile (trong ngưỡng discipline convention).

## Output format

```markdown
## Style Humanizer Report

### Pass Summary
- [PASS / NEEDS_REVISION] Overall

### Issues

| # | Category | Location | Issue | Suggested Fix | Auto-fixable? |
|---|----------|----------|-------|---------------|----------------|
| 1 | Flagged term | Intro P2 | "crucial" | "essential" / domain-specific | Yes |
| 2 | Punctuation | Methods | 4 em dashes | Trả về comma hoặc tách câu | Yes |
| 3 | Throat-cleaning | ... | "In this section..." | Xóa, mở argument trực tiếp | Yes |
| ... | ... | ... | ... | ... | ... |

### Burstiness Flags (qualitative)
- Section X: 6 consecutive sentences 21–25 words → suggest breaking

### Style Calibration Summary (nếu dùng)
- Matched past style in: paragraph length distribution, register
- Diverged: over-reliance on "Furthermore" as transition → suggest alternate

### Acceptance
- [ ] Burstiness cue addressed
- [ ] All flagged term replaced OR justified as domain term
- [ ] Throat-cleaning removed
- [ ] Paragraph length varied (no uniform 150w pattern)
- [ ] Synonym cycling audited
- [ ] Binary contrast ≤2
```

##ưu tiên thực thi
1. Auto-fix deterministic issues (flagged term, em dash, throat-cleaning) cho toàn bộ paper.
2. Burstiness cue → liệt kê spot, user tự quyết fix hoặc auto suggest.
3. Style calibration optional: chỉ chạy khi user cung cấp past papers + yêu cầu.

## Lưu ý
- Không claim vượt AI detector bên ngoài — verifiable claim chỉ là "giảm AI signature dựa trên empirical heuristic", không accelerando "100% pass GPTZero".
- Chính sách khai báo AI-use của venue (IEEE v.v.) là quyết định + trách nhiệm của TÁC GIẢ — nêu policy của venue đích một lần cho user, không tự quyết thay (integrity rules §5).
- Sau mỗi pass: báo cáo kèm xác nhận "invariant §4 giữ nguyên" (đã diff số liệu/citation/công thức).
- Style Profile: tiếng Anh (machine content); các ghi chú hướng dẫn cho người dùng tiếng Việt.
