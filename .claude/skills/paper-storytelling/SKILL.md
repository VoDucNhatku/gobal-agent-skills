---
name: paper-storytelling
description: "Viết/viết lại bản thảo theo cấu trúc storytelling chuẩn IEEE/Springer (mẫu SARD): title 3 vế, research questions tổ chức bài, contributions viết thành văn xuôi gắn số, Results+Discussion GỘP theo phát hiện, negative result kể như finding, kèm QUY TRÌNH thiết kế pipeline figure TikZ 2 hàng (inference/train-only) + Algorithm walkthrough + headline pgfplots + vòng compile→render→inspect. Triggers: viết theo cấu trúc storytelling, narrative paper, SARD structure, viết lại paper theo bài mẫu, vẽ pipeline đẹp, storytelling rewrite, cấu trúc bài chi tiết."
argument-hint: "<paper id | main.tex path> [rewrite|draft|figure-only|analyze <exemplar.pdf>]"
allowed-tools: Read Write Edit Glob Bash
---

# Paper Storytelling — Cấu trúc kể chuyện + Pipeline figure chuẩn IEEE/Springer

> **Role:** Tầng CẤU TRÚC & KỂ CHUYỆN đặt lên trên khâu draft của `paper-submission`.
> Biến notes/kết quả thật thành bản thảo đọc như một câu chuyện có bằng chứng — và
> thiết kế bộ figure gánh phần kể chuyện (pipeline 2 hàng, Algorithm walkthrough,
> headline chart).
>
> **Provenance:** chưng cất 2026-07-20 từ bài mẫu SARD (Springer sn-jnl) + lần rewrite
> AUFE-Q4 (paper 034) đã chạy end-to-end thành công (compile sạch, figure không lỗi).

Binding (đọc runtime, mỗi file 1 dòng):
- `~/.claude/rules/paper-writing-integrity.md` — §1 zero fabricated refs, §3 [TODO] thay vì bịa số, §6 vị trí pipeline.
- `~/.claude/rules/research-proposal-integrity.md` — claim ≤ tier trong `notes/claims-ledger.md`; venue = band + điều kiện.
- `~/.claude/rules/workbench-conventions.md` — bilingual, preview-not-dump, reuse-before-read.
- `~/.claude/rules/latex-katex-compat.md` — chỉ khi emit math vào notes markdown (file .tex dùng LaTeX đầy đủ).

## Vị trí trong chuỗi sản xuất (§6 paper-writing-integrity)

Skill này là **chuyên biệt hóa của khâu đầu** — thay cho `paper-submission draft/format`
khi user muốn cấu trúc storytelling. Chuỗi sau GIỮ NGUYÊN:

```
paper-storytelling (structure + narrative + figures)   ← khâu này
   → citation-guard → style-humanizer → latex-fix + compile
   → ieee-q1-devil-advocate → self-evaluator
```

Kết thúc mode `rewrite`/`draft`: ghi `paper/reports/paper-storytelling.md` và nêu
handoff `citation-guard`. Figure có thể làm SONG SONG với prose (khâu duy nhất được
parallel).

## Phân vai với skill cũ — dung hợp tài nguyên (KHÔNG lặp lại)

| Tài sản | Chủ sở hữu | Skill này làm gì |
|---|---|---|
| Venue template mechanics (IEEEtran/cvpr/sn-jnl), mode `format`/`rebuttal`, TODO discipline, no-fabrication | `paper-submission` | THAM CHIẾU — không chép lại; cần format/rebuttal → gọi skill đó |
| Style TikZ Q1 (≤8 node, màu dominant+accent, font, kích thước), 3 quy tắc chống đạo văn hình (abstraction / perspective-shift / màu riêng) | `latex-tikz-generator` | Figure spec của skill này RÀNG theo các quy tắc đó; skill này thêm tầng THIẾT KẾ (đọc method → spec → layout → verify) |
| DOI verify, orphan check | `citation-guard` | Handoff sau khi draft xong |
| Văn phong, chống AI-signature, bất biến bảo toàn nghĩa §4 | `style-humanizer` | Handoff — skill này viết CẤU TRÚC, không tự nhận đã calibrate văn phong |
| Math 2-engine, compile repair | `latex-fix` | Handoff; skill này chỉ compile-verify figure |
| Phản biện, cổng cuối | `ieee-q1-devil-advocate`, `self-evaluator` | Handoff |

**Tài sản riêng của skill này (chỉ 2):**
1. `references/structure-template.md` — bản đồ cấu trúc storytelling từng section, công thức câu, tỷ lệ trang, 8 luật kể chuyện + checklist.
2. `references/pipeline-figure-method.md` — quy trình 7 pha: đọc method → figure spec → văn phạm thị giác → layout → **Pha 3b thích ứng canvas venue (IEEE 516pt / LNCS 347pt, luật V1–V6)** → TikZ skeleton đã chạy thật → luật chống va chạm → vòng compile→render→inspect; kèm **§G.0 chọn loại chart theo loại phát hiện** + skeleton headline pgfplots + Algorithm walkthrough.

## Luật số 0 — CHỐT ĐỊNH DẠNG VENUE trước khi viết/vẽ (thêm 2026-07-20)

Trước mọi việc khác: xác định documentclass đích (`IEEEtran` 2 cột / `llncs` 1 cột /
khác). User không nói → **hỏi 1 câu** (kèm gợi ý: bài mẫu gần nhất dùng gì); không tự
chọn ngầm. Hệ quả trực tiếp của định dạng:
- Canvas figure khác nhau 33% (Pha 3b) → pipeline 2 hàng phải re-layout compact cho
  LNCS, **không bao giờ co thành 1 hàng** (luật V1/V2).
- Float 1 cột trôi theo source (luật V4) → pipeline figure đặt source sớm ngay sau
  đoạn đầu Intro để nổi trang 2–3, không đợi đến Method.
- Cả 2 định dạng dùng CHUNG cấu trúc storytelling, chung số, chung bib — chỉ lớp
  trình bày khác. Đổi định dạng = giữ nguyên prose, làm lại lớp figure theo Pha 3b.

*Nguồn luật: sự cố 2026-07-20 — bản LNCS đầu tiên bị co pipeline thành 1 hàng + hình
trôi trang 5/7 vì skill chưa chốt các luật này; bản IEEE cùng nội dung đạt chuẩn ngay.*

## Modes

| Mode | Mục đích | Khi dùng |
|------|----------|----------|
| `rewrite` | Tái cấu trúc main.tex có sẵn theo template storytelling | Bản thảo "đọc dở" nhưng số liệu/công thức đã có |
| `draft` | Viết mới từ notes theo template | Bắt đầu viết; grounding rules kế thừa `paper-submission draft` |
| `figure-only` | Chỉ sinh pipeline figure + headline figure + Algorithm từ method notes | Paper đã ổn, thiếu hình |
| `analyze <exemplar.pdf>` | Mổ xẻ 1 bài mẫu mới thành structure map (như đã làm với SARD) → lưu `notes/<id>-structure-analysis.md` | User quăng bài mẫu mới muốn học cấu trúc |

## Procedure

### Mode `rewrite` (mặc định khi input là main.tex có sẵn)
1. **Reuse-before-read**: đọc `notes/INDEX.md`, results note, mechanism note, claims-ledger. KHÔNG đọc lại PDF gốc nếu notes đã có.
2. Đọc main.tex hiện tại — kiểm kê phần GIỮ (công thức đã tag provenance, bảng số verbatim, Related Work đã pass synthesis) và phần VIẾT LẠI.
3. Chẩn đoán theo checklist 10 lỗi trong `references/structure-template.md` §Diagnosis.
4. Viết lại theo bản đồ section trong `references/structure-template.md` — thứ tự VIẾT vẫn là results-first (Results→Discussion→Method→Conclusion→Related→Intro→Abstract→Title→Refs).
5. Sinh figure theo `references/pipeline-figure-method.md` (pha 1→7, bắt buộc vòng verify).
6. Compile 3 pass + bibtex; render PNG từng trang; tự inspect; sửa đến khi sạch.
7. Report + audit-log + handoff `citation-guard`.

### Mode `draft`
Như `rewrite` nhưng bước 2 thay bằng: dựng khung section trống theo template rồi điền
từ notes; mọi số chưa có = `\TODO{...}` hiển thị đỏ (định nghĩa macro trong preamble).

### Mode `figure-only`
Chạy riêng pha 1→7 của `references/pipeline-figure-method.md`; trả về block TikZ/pgfplots
+ 2–3 dòng giải thích cách đọc (quy ước output của `latex-tikz-generator`).

### Mode `analyze`
1. Extract text bài mẫu (pypdf nếu Read PDF fail).
2. Lập bản đồ: mỗi section → CHỨC NĂNG THẬT (không phải tên mục) + độ dài + kỹ thuật kể chuyện.
3. So khung với `references/structure-template.md` — điểm nào bài mẫu làm KHÁC/hay hơn → đề xuất cập nhật template (hỏi user trước khi sửa file references).
4. Lưu `notes/<id>-structure-analysis.md` theo format của bản phân tích SARD.

## Luật cứng khi viết (tóm tắt — chi tiết trong references)

1. **Số nào cũng nằm trong câu có nghĩa nhân quả** — bảng chỉ để tra cứu, câu chuyện nằm trong prose.
2. **2–3 research questions tường minh** ở Intro; mọi section sau trả lời đúng các câu đó.
3. **Contributions = văn xuôi**, mỗi đóng góp dính liền con số/bằng chứng của nó.
4. **Results + Discussion GỘP**; subsection đặt tên theo PHÁT HIỆN (tiêu đề gần như claim).
5. **Kết quả âm = finding**, kể trước cả khi bị hỏi ("the one a leaderboard would hide").
6. **Có mục cơ chế "Why X"** — không dừng ở cái-gì-tốt-hơn.
7. **Caveats nằm TRONG Results** thành 1 đoạn văn (không tạo subsection rỗng chứa TODO).
8. **Figure gánh kể chuyện**: caption nêu PHÁT HIỆN, không nêu "Results of experiments".

Mọi luật integrity vẫn đứng trên: số verbatim từ results note; thiếu → `\TODO` đỏ; claim
≤ tier ledger; công thức mang tag [cited]/[derived]/[design]; figure mô phỏng cấu trúc
bài khác = đạo văn thiết kế (luật của `latex-tikz-generator`).

## Vòng verify bắt buộc (không claim "hình đẹp" khi chưa nhìn)

```
pdflatex x2 (+bibtex nếu đổi cite) → render PNG (pymupdf, dpi 110–160)
→ Read PNG tự inspect: mũi tên cắt box? label đè chữ? legend bị đường vòng xuyên?
→ sửa theo bảng symptom→fix trong references/pipeline-figure-method.md §F → lặp
→ pagination QA: python <skills>/latex-fix/scripts/pdf_pagination_check.py main.pdf
  (orphan heading / widow / trang thưa — exit 0 hoặc waive có lý do)
```

Không có pdflatex/pymupdf → ghi rõ "code chưa compile-test", không claim chạy được
(quy ước `latex-tikz-generator`).

## Output & Report

- Bản thảo: `paper/main.tex` (+ `paper/main.pdf` nếu compile được).
- Report: `paper/reports/paper-storytelling.md` — phần giữ/phần viết lại, danh sách
  \TODO còn lại, kết quả vòng verify figure, handoff citation-guard.
- Mode analyze: `notes/<id>-structure-analysis.md`.
- Chat: 5–10 dòng tiếng Việt + paths (preview-not-dump).

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| finding-titled subsection | subsection mang tên phát hiện | Tiêu đề subsection là claim, không phải loại thí nghiệm |
| headline figure | hình chủ đạo | Figure tổng kết phát hiện chính, đặt ngay đầu Results |
| insertion point | điểm chèn | Vị trí duy nhất trong pipeline nơi đóng góp mới được gắn vào |
| walkthrough | diễn giải từng dòng | Đoạn văn giải thích Algorithm theo số dòng, gọi tên "decisive step" |
| visual grammar | văn phạm thị giác | Quy ước ngữ nghĩa→kiểu vẽ: solid=inference, dashed=train-only, cam=mới, xám=kế thừa |
