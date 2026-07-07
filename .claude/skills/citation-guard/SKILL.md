---
name: citation-guard
description: "Bảo vệ trích dẫn: DOI verify, orphan in-text/reference detection, citation synthesis quality, self-citation ratio, source currency, retraction screening. Auto-correction deterministic errors; flag vấn đề cần người dùng. Triggers: check citations, citation audit, verify DOI, orphan citation, trích dẫn, kiểm tra trích dẫn, review reference list, check đạo văn trích dẫn."
allowed-tools: Read Write Grep Glob Bash WebFetch WebSearch
---

# Citation Guard — Trích dẫn chuyên nghiệp + đạo văn guard

Kiểm tra và sửa toàn bộ citation trong draft bài báo. Binding:
`~/.claude/rules/paper-writing-integrity.md` §1–2 (zero fabricated references, đạo văn).

## LUẬT CỨNG — không bịa reference (đọc trước mọi việc khác)

1. **Verify thật, không verify miệng.** DOI verify = WebFetch
   `https://api.crossref.org/works/<DOI>` (hoặc `https://doi.org/<DOI>`) rồi đối chiếu
   title/authors/venue/year với entry. Không gọi được mạng → đánh dấu
   `[unverified — kiểm tra DOI trước khi nộp]`, KHÔNG được báo "verified".
2. **Cấm sinh entry từ trí nhớ model.** Entry mới chỉ được thêm từ (a) nguồn user cung
   cấp / notes có id, hoặc (b) lookup đã verify trong session. Nghi ngờ entry nào do
   LLM tự nhớ ra → flag `[nguồn gốc không rõ — có thể fabricated]` mức CRITICAL.
3. **Retraction screening** chỉ khi tra được (WebSearch "retraction <title>"); không tra
   được → ghi "chưa kiểm tra retraction", không bịa kết quả sạch.

## Capability

- **Zero orphan enforcement**: in-text ↔ reference list phải khớp 1:1.
- **DOI verification**: mọi entry có DOI phải có `https://doi.org/xxx`, format đúng ưu tiên `/doi.org/` thay `dx.doi.org`.
- **Auto-correction deterministic errors**: đổi `&`↔`and`, sắp xếp multi-source alphabetically (APA/Chicago/MLA) hay theo appearance (IEEE/Vancouver), loại bỏ period trailing DOI, chuyển Title Case → sentence case (APA article), thêm `et al.` đúng ngưỡng.
- **Metrics report**: self-citation ratio (flag >15%), source currency % (/<10yr flag), citation density / paragraph (flag 0-citation paragraph, >5 cite/sentence).
- **Retraction screening**: đối chiếu Retraction Watch; retracted paper → đề xuất remove / giữ kèm `[Retracted]`.
- **Synthesis quality scan**: phát hiện mẫu "Nguyễn Văn A nói X [1]. Trần Văn B nói Y [2].", đề xuất synthesize "các phương pháp dựa trên CNN đã giải quyết X [1,2], còn hạn chế Y — transformer [3] khắc phục".

## Supported formats
APA 7.0 (default), Chicago 17th (Author-Date / Notes-Bibliography), MLA 9th, IEEE, Vancouver. Mỗi entry kiểm tra đúng format spec của loại.

## Output format

```markdown
## Citation Audit Report

### Summary
| Metric | Count |
|--------|-------|
| Total in-text citations | N |
| Total reference list entries | N |
| DOI verified online / unverified | N / N |
| Suspected fabricated entries | N |
| Orphan in-text | N |
| Orphan reference | N |
| Format errors (auto-corrected) | N |
| Format errors (flagged) | N |
| Missing DOI | N |
| Retracted sources | N |
| Self-citation ratio | N% |
| Sources last 5 years | N% |

### Corrections Made
| # | Location | Error | Correction |
|---|----------|-------|-----------|
| 1 | Intro P2 | "(Smith and Jones, 2024)" parenthetical | "(Smith & Jones, 2024)" — APA 7 |
| 2 | Ref #7 | dx.doi.org prefix | https://doi.org/... |
| ... | ... | ... | ... |

### Flagged for Review
| # | Entry | Issue | Suggested action |
|---|-------|-------|-----------------|
| ... | ... | ... | ... |

### Synthesis Quality (optional sub-scan)
| # | Pattern observed | Location | Better formulation |
|---|------------------|----------|-------------------|
| ... | ... | ... | ... |

### Corrected Reference List (sorted by selected format)
[full list]
```

## Auto-correction vs human review phân biệt

Auto-correct: formatting-only (thiếu DOI, thiếu et al., sai case).
Flag + human review: claim misrepresented, unknown source, multi-source attributed to wrong paper, suspicious self-citation cluster.

## Chinese citation special checks (nếu địch là TE, chuyển ngữ cho người dùng)
- Chinese author: full name (không first/last split): Wang Daming (2024).
- Chinese book: angle brackets hoặc italic theo journal.
- Chinese title: full tên, không abbreviation.
- Translated work: `Original Author (Trans. Translator, Year). *Title*. Publisher. (Original work published YYYY)`.
- Chinese reference ordering: Chinese trước, English sau (Taiwan convention).

## Privacy note
- Mọi nội dung paper do user cung cấp. Không gửi ra ngoài. Tất cả xử lý nội bộ trong session.
