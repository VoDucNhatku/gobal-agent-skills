---
name: "claim-forge"
description: "Turns an ARGUMENT-bearing document (economics paper, social-science paper, management/law text, policy report, book chapter) into a print-quality critical-reading handbook — every card is ONE falsifiable claim, with its source, argument chain, evidence tier, load-bearing assumptions, the strongest counter-reading, and what would refute it. Ends with a one-page claim ledger. Exports PDF. Modes — paper (single document), theme (multiple sources on one topic), audit (self-review a draft). Triggers — đọc phê phán, sổ tay lập luận, bài này lập luận thế nào, bằng chứng có đủ không, giả định nào gánh, phản biện bài báo, paper kinh tế, khoa học xã hội, làm sổ tay cho paper không có code, critical reading handbook, claim ledger. It GENERATES a printable handbook for argument-bearing documents; a document with formulas/code uses study-forge instead; a single-pass Markdown analysis note uses paper-read mode think; a harsh Q1-standard rebuttal uses ieee-q1-devil-advocate."
---

# Claim Forge

> **Vì sao tồn tại:** `study-forge` áp lên paper kinh tế thì gượng — nó bắt mọi thẻ phải
> có công thức hoặc code, nên ô "viết bằng ngôn ngữ kia" đẻ ra mã giả rởm chỉ để lấp chỗ
> (quan sát thật, 2026-08-02, sổ tay Klemperer 1987).
> **Nguyên nhân gốc:** khung của `study-forge` hỏi *"cái này tính ra gì?"*.
> Tài liệu lập luận phải hỏi *"cái này có thể sai ở đâu?"*.

Đọc `../_shared/rules/workbench-conventions.md` (song ngữ, preview-not-dump,
script-offloading), `../_shared/rules/paper-writing-integrity.md` (§1 không bịa trích dẫn,
§4 bảo toàn độ mạnh khẳng định) và `../_shared/research-integrity.md`
(§4 nhãn nguồn gốc, §6 khẳng định đánh giá là khẳng định quét được).

**Câu mở đầu:** "Tôi dùng skill claim-forge để dựng sổ tay đọc phê phán này."

---

## Iron Law — ba điều không được vi phạm

1. **Đơn vị là KHẲNG ĐỊNH, không phải chủ đề.** Ô 01 phải nêu một mệnh đề **có thể sai**.
   "Chi phí chuyển đổi trong B2B" là chủ đề — hỏng. "Cân bằng không hợp tác có thể trùng
   khít kết quả thông đồng" là khẳng định — đúng.
2. **Không bao giờ đẩy độ mạnh lên cao hơn nguồn.** Nguồn viết "the presumption is that
   welfare is reduced" thì thẻ mang mức `goi-y`, không phải `chung-minh`. Đây là bất biến
   bảo toàn nghĩa của `paper-writing-integrity` §4.
3. **Mỗi dòng phải truy được về nguồn.** Ô 02 gắn nhãn `nguon` (nguồn nói) ·
   `suy-ra` (tôi suy ra) · `chua-kiem`. Trộn lẫn ba thứ này là lỗi nặng nhất của skill này.

Vi phạm 1 → thẻ thành bài tóm tắt. Vi phạm 2 → sổ tay nguy hiểm hơn không đọc.
Vi phạm 3 → không phân biệt được đâu là bài báo nói, đâu là mô hình bịa.

---

## Giao thức 11 ô

| Ô | Tên | Nó ép người đọc làm gì |
|---|---|---|
| 01 | Khẳng định | phát biểu sao cho có thể sai; kèm huy hiệu độ mạnh |
| 02 | **Ai nói, ở đâu** | truy nguồn tới mục/trang + nhãn `nguon`/`suy-ra`/`chua-kiem` |
| 03 | **Đường lập luận** | tiền đề → tiền đề → kết luận, và **chỗ hở** nếu có |
| 04 | **Bằng chứng đỡ ở đâu** | mỗi bằng chứng gắn hạng: số liệu / mô hình / ca cụ thể / suy luận |
| 05 | **Giả định gánh** | nới từng giả định → kết luận còn đứng không; đánh dấu GÁNH / PHỤ |
| 06 | **Cách giải thích khác** | lời giải thích đối thủ cũng khớp bằng chứng + cách phân biệt |
| 07 | **Cái gì bác được nó** | quan sát nào sẽ giết khẳng định này |
| 08 | Một ca cụ thể | chạy một tình huống thật; có số thì phải tính thật |
| 09 | Hình dung | đồ thị hoặc sơ đồ lập luận (tuỳ chọn — không có thì bỏ) |
| 10 | Dùng được tới đâu | áp dụng được khi nào, hỏng khi nào |
| 11 | **Tự kiểm tra** | 5 câu hỏi hệ quả, đáp án ở dòng dưới |

Ô **02, 03, 04, 06, 07** là thứ `study-forge` không có ô nào tương ứng — và là toàn bộ
khác biệt giữa đọc xuôi và đọc phê phán.

Ô **05** trông giống "Bỏ đi thì sao" nhưng khác trục: ở đó là *xoá số hạng*, ở đây là
*nới giả định*. Đừng dịch cơ học từ skill kia sang.

Chi tiết cách điền, kèm phép thử đạt/chưa đạt → `references/claim-anatomy.md`.

---

## Ba hệ thống nhãn

**Hạng bằng chứng** (ô 04) — dán cho từng dòng bằng chứng:

| Hạng | Nghĩa |
|---|---|
| `so-lieu` | đo đạc / thống kê / thực nghiệm — mạnh nhất |
| `mo-hinh` | suy ra từ mô hình hình thức, chỉ đúng trong phạm vi giả định của nó |
| `ca-cu-the` | một ví dụ hoặc ca lịch sử — minh hoạ, **không** chứng minh |
| `suy-luan` | chỉ là lập luận hợp lý, không có gì bên ngoài đỡ |

**Độ mạnh khẳng định** (huy hiệu ở đầu thẻ): `chung-minh` · `cho-thay` · `goi-y` ·
`gia-thuyet`. Chọn theo **cách nguồn tự phát biểu**, không theo cảm nhận của bạn về
tính thuyết phục.

**Nhãn nguồn gốc** (ô 02): `nguon` · `suy-ra` · `chua-kiem`.

> Một thẻ mức `chung-minh` mà bằng chứng cao nhất chỉ hạng `suy-luan` là **mâu thuẫn nội
> tại** — sửa độ mạnh xuống, đừng nâng bằng chứng lên.

---

## Modes

| Mode | Input | Làm gì |
|---|---|---|
| `paper` *(mặc định)* | một bài báo / chương sách / báo cáo | 3–6 thẻ, mỗi thẻ một khẳng định trung tâm |
| `theme` | nhiều nguồn cùng chủ đề | mỗi thẻ là một khẳng định **có tranh cãi**, ô 06 chứa quan điểm đối lập của nguồn khác |
| `audit` | bản thảo của chính người dùng | soi khẳng định của chính mình: chỗ nào chưa có bằng chứng, chỗ nào phát biểu quá tay |

Mode `audit` là chỗ skill này đắt giá nhất — nó bắt tác giả tự đối diện ô 06 và ô 07
trước khi người phản biện làm việc đó.

---

## Quy trình

**Bước 1 — Chốt nguồn và đọc có chọn lọc.** Tóm tắt, phần đóng góp, kết luận, và mọi câu
dạng "we show / we find / chúng tôi cho thấy" (conventions §6). PDF quét thì rút text
bằng PyMuPDF trước, rẻ hơn render trang thành ảnh nhiều lần.

**Bước 2 — Trích khẳng định.** Tìm 3–6 mệnh đề trung tâm. Với mỗi cái, **chép lại cách
nguồn tự phát biểu** rồi mới quyết mức độ mạnh. Đừng đọc lướt rồi tự diễn đạt — đó là chỗ
độ mạnh bị trôi.

**Bước 3 — Kiểm chất lượng nguồn.** OCR hỏng, công thức vỡ, số liệu không đọc được → ghi
`nguồn không đọc được ở chỗ này`, **không dựng lại từ OCR hỏng**. Với trích dẫn cần kiểm,
theo `paper-writing-integrity` §1.

**Bước 4 — Điền ô 06 và 07 TRƯỚC ô 04.** Nghĩ ra cách giải thích ngược lại và phép bác bỏ
trước, rồi mới liệt kê bằng chứng. Làm ngược lại thì bạn chỉ đi tìm bằng chứng ủng hộ —
đúng định nghĩa của thiên kiến xác nhận.

**Bước 5 — Tính số cho ô 08.** Có số thì chạy thật bằng `python`. Không có số thì kể một
ca cụ thể có thật trong nguồn.

**Bước 6 — Viết spec JSON** (`profile: "argument"`), ghi ra
`.tmp/claim-forge_<slug>.json`. Schema → `references/claim-anatomy.md`.

**Bước 7 — Build và compile.** Dùng chung builder với `study-forge` (không nhân đôi
hạ tầng):

```bash
python ../study-forge/scripts/build_handbook.py .tmp/claim-forge_<slug>.json --format tex --out-dir notes
```

```bash
cd notes && xelatex -interaction=nonstopmode study-<slug>.tex && xelatex -interaction=nonstopmode study-<slug>.tex
```

**Bước 8 — Kiểm bằng mắt và bằng log.** Bắt buộc cả hai:

```bash
grep -c "Missing character" notes/study-<slug>.log
```

Phải bằng 0. Rồi `file reading capability` chính file PDF và nhìn — bảng tràn khung, chữ chồng tiêu đề,
trang trống không bao giờ hiện ra trong log.

**Bước 9 — Tự soát mâu thuẫn nội tại.** Với mỗi thẻ: độ mạnh có khớp hạng bằng chứng
cao nhất không? Ô 06 có trống không (thẻ không có cách giải thích khác nào là thẻ đáng
ngờ)? Ô 07 có phải là quan sát thật kiểm được không, hay chỉ là câu chữ?

---

## Anti-patterns

| Cám dỗ | Vì sao sai | Làm đúng |
|---|---|---|
| Thẻ đặt tên theo chủ đề | thành mục lục, không phải khẳng định | Nêu mệnh đề có thể sai |
| Bỏ trống ô 06 vì "không nghĩ ra" | thường là chưa nghĩ, không phải không có | Ít nhất một cách giải thích khác, hoặc ghi rõ vì sao không có |
| Ô 07 viết "nếu bằng chứng ngược lại" | nói suông, không kiểm được | Nêu **quan sát cụ thể** đo được |
| Nâng độ mạnh cho thẻ nghe thuyết phục | vi phạm Iron Law 2 | Bám cách nguồn tự phát biểu |
| Dựng lại công thức từ OCR vỡ | bịa | Ghi "nguồn không đọc được", bỏ qua |
| Trộn ý nguồn với suy luận của mình | không truy được | Nhãn ô 02, và nói rõ trong ô 03 chỗ nào là suy ra |
| Ép mỗi thẻ đủ 11 ô | quay lại đúng lỗi của study-forge | Ô 09 và 10 bỏ được; ô 01–07 và 11 thì không |
| Dùng skill này cho paper có code | sai công cụ | `→ study-forge` |

---

## Ranh giới

| Việc | Skill đúng |
|---|---|
| Tài liệu có công thức/code cần học cách vận hành | `study-forge` |
| Ghi chú phân tích lập luận, Markdown, một lượt, cho người nghiên cứu | `paper-read` mode `think` |
| Phản biện gắt theo chuẩn Q1, novelty + ablation | `ieee-q1-devil-advocate` |
| So sánh nhiều bài, dựng taxonomy, tìm khoảng trống | `paper-synthesize` |
| Kiểm trích dẫn, DOI, đạo văn | `citation-guard` |
| Quét khẳng định bịa trong output | `evidence-check` |

Khác biệt với `paper-read think`: bên kia là **ghi chú phân tích Markdown một lượt** cho
người nghiên cứu quyết định. Bên này là **sổ tay in để học lâu dài**, có máy móc ghi nhớ
(5 câu tự kiểm tra mỗi thẻ) và sổ khẳng định để ôn. Cùng quan hệ như `paper-read` với
`study-forge`: một bên mổ xẻ, một bên dạy.

---

## Hạn chế đã biết

- **Chỉ xuất `tex`/PDF.** Bản `md`/`html` chưa hỗ trợ profile `argument`; builder sẽ báo
  và bỏ qua chứ không xuất file hỏng.
- Mode `theme` và `audit` **chưa chạy thực tế lần nào** (tính tới 2026-08-02). Chỉ mode
  `paper` đã kiểm trên Klemperer (1987).
- Chưa thử tài liệu tiếng Anh, chưa thử tài liệu định tính thuần (dân tộc học, luật án lệ).

## Đầu ra

| Thứ | Đường dẫn |
|---|---|
| Sổ tay | `notes/study-<slug>.{tex,pdf}` |
| Spec | `.tmp/claim-forge_<slug>.json` |
| Manifest | một dòng trong `notes/INDEX.md` |

## Tham chiếu

- `references/claim-anatomy.md` — cách điền từng ô + schema JSON đầy đủ
- Builder dùng chung: `../study-forge/scripts` (`build_handbook.py`,
  `tex_emitter.py` — hàm `emit_tex_argument`)


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
