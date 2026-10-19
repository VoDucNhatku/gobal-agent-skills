---
disable-model-invocation: true
name: "study-forge"
description: "Turns a study document (course slides, PDF, book chapter, notes) OR a code snippet pulled from a project into a print-quality study handbook — every formula/function gets a fixed 10-cell card, with a real pgfplots graph, a TikZ flowchart, meaningful symbol coloring, and a self-check cell. Exports PDF (primary), Markdown (quick read), HTML (web view). Modes — formula, code, course (whole document set), refit (redesign an existing handbook). Triggers — làm sổ tay, tạo template học, học công thức này, giải thích đoạn code này, làm tài liệu ôn tập, sổ tay toán, cheat sheet có giải thích, biến slide thành sổ tay, study handbook, explain this code as a handbook, làm cho dễ hiểu, template học tập. It GENERATES a printable artifact; it does NOT tutor interactively (use study-tutor), explain one concept in chat (use concept-explainer), analyze a paper's method (use paper-read), or fix math rendering (use latex-fix)."
allowed-tools: "Read Write Edit Glob Grep Bash PowerShell Skill"
argument-hint: "<nguồn: đường dẫn | đoạn code | chủ đề> [formula|code|course|refit] [--format pdf|md|html|all]"
---

# Study Forge

> **Nguồn gốc:** tái thiết kế từ `Summary_Math_Formulas_Notebook.tex` (mẫu 3W + 4 tầng)
> và một sổ tay LaTeX tham chiếu do người dùng cung cấp (2026-08-01).
> **Mục đích:** biến tài liệu học hoặc code thành sổ tay in được, nơi mỗi công thức và
> mỗi hàm đều bị mổ xẻ theo cùng một giao thức 10 ô.

Khi xuất file: đọc `../_shared/rules/workbench-conventions.md` (song ngữ, preview-not-dump,
script-offloading), và `../_shared/rules/latex-katex-compat.md` khi xuất Markdown. Chỉ phác
dàn ý hoặc trả lời trong chat thì không cần đọc hai file này.

**Câu mở đầu:** "Tôi dùng skill study-forge để dựng sổ tay này."

---

## Iron Law — hai điều không được vi phạm

1. **Mỗi thẻ phải bắt người học TỰ SẢN XUẤT — đủ 5 lần.** Ô 10 (Tự kiểm tra) là bắt
   buộc, tối thiểu **5 câu**, không bao giờ bỏ. Sổ tay chỉ để đọc là sổ tay vô dụng —
   đọc trôi tạo cảm giác hiểu mà không tạo trí nhớ. Script cảnh báo nếu thẻ nào thiếu.
2. **Mọi con số trong ô "Chạy số thật" phải được TÍNH THẬT, không ước lượng.** Tính ra
   nháp trước khi ghi. Một con số bịa làm hỏng toàn bộ độ tin cậy của sổ tay. Nếu không
   tính được thì bỏ ô đó, không đoán.

Vi phạm 1 → sản phẩm chỉ là bản chép lại đẹp hơn. Vi phạm 2 → tệ hơn bản gốc.

---

## Giao thức 10 ô — dùng CHUNG cho công thức và code

Đây là điểm cốt lõi: **công thức và code được mổ theo cùng một bộ ô.** Người học chỉ
phải học cách đọc một lần.

| Ô | Tên | Với công thức | Với code |
|---|---|---|---|
| 01 | Việc nó làm | công thức này giải quyết việc gì, một câu | hàm/khối này giải quyết việc gì |
| 02 | Công thức / Mã nguồn / **Ý chính** | biểu thức, đóng khung, đánh số | đoạn code, tô cú pháp, đánh số dòng |
| 03 | Giải phẫu | từng ký hiệu: vai trò + nó làm gì | từng biến/khối: vai trò + nó làm gì |
| 04 | Truy vết kích thước | chiều của từng số hạng, `(m,n)·(n,1)→(m,1)` | shape/type vào–ra từng dòng |
| 05 | **Bỏ đi thì sao** | xoá/đặt 0 từng số hạng → vỡ cái gì | xoá/ngắn mạch từng khối → vỡ cái gì |
| 06 | **Chạy số thật** | chạy 2–3 hàng số thật qua công thức | chạy một input thật, in state từng bước |
| 07 | Hình dung | đồ thị pgfplots: hình dạng, điểm tối ưu | flowchart TikZ: luồng dữ liệu |
| 08 | **Viết bằng ngôn ngữ kia** | 3 dòng code tương đương + bảng ký hiệu↔biến | công thức/pseudocode tương đương |
| 09 | Khi nó hỏng | NaN, phân kỳ, sai âm thầm + triệu chứng | bug, edge case + triệu chứng + cách phát hiện |
| 10 | **Tự kiểm tra** | **5 câu hỏi**, đáp án ở dòng dưới | **5 câu hỏi**, đáp án ở dòng dưới |

Bốn ô **in đậm** là thứ bản gốc không có, và là lý do sổ tay này dạy được:
- **05** biến công thức thụ động thành mô hình nhân quả ("bỏ `1/m` thì learning rate hỏng").
- **06** chống cái bẫy "thuộc ký hiệu nhưng chưa từng thấy nó chạy".
- **08** vá đúng khoảng cách công thức ↔ code mà sinh viên AI vấp. Tên ô phải nói VIỆC
  ("Cùng công thức này, viết bằng code"), không được đặt tên ẩn dụ.
- **10** là chỗ duy nhất tạo trí nhớ.

Chi tiết cách điền từng ô (kèm ví dụ đã điền cho cả math và code):
→ `references/card-anatomy.md`.

---

## Luật màu ngữ nghĩa

Một vai trò = một màu, **giống nhau ở công thức, ở đồ thị, và ở code**. Nhìn màu là biết
ký hiệu đó thuộc loại gì mà không cần tra.

| Vai trò | `role` | Nghĩa |
|---|---|---|
| Tham số học được | `param` | mô hình tự học ra (`w`, `b`) |
| Siêu tham số | `hyper` | BẠN chọn, không học (`alpha`, `lambda`) |
| Dữ liệu vào | `data` | `x`, `X` |
| Nhãn thật | `truth` | `y` |
| Dự đoán | `pred` | `f`, `y_hat` |
| Chỉ số / kích thước | `index` | `i`, `j`, `m`, `n` |
| Toán tử / rút gọn | `op` | `Σ`, `μ`, `σ` |

Phân biệt `param` với `hyper` là thứ sinh viên hay lẫn nhất — tách màu là cách chữa rẻ nhất.

---

## Modes

| Mode | Input | Làm gì |
|---|---|---|
| `formula` | công thức, ảnh chụp slide, chương sách | 1–5 thẻ công thức |
| `code` | đoạn code dán vào, hoặc `path/to/file.py:120-180` | 1–5 thẻ code |
| `course` | thư mục tài liệu / bộ slide / PDF nhiều tuần | trích mọi công thức+code đáng học, chia thẻ, dựng DAG phụ thuộc |
| `refit` | một sổ tay đã có (`.tex`/`.md`) | đọc, giữ nội dung đúng, tái cấu trúc về giao thức 10 ô |

Mặc định: đoán từ input. Có code → `code`. Có công thức → `formula`. Trỏ vào thư mục → `course`.

**Ba loại thẻ.** `expr` (công thức) · `code` (mã nguồn) · `claim` (mệnh đề, cho tài liệu
kinh tế/luật/khái niệm không có công thức lẫn code). Cùng bộ 10 ô; script tự đổi cách
diễn đạt của ô 05 và ô 08 theo loại thẻ.

**Ngoài ML thì đổi tên vai trò.** Bảy vai trò màu là phổ quát (thứ ta CHỌN / thứ được
CHO / chỉ số), nhưng tên mặc định là từ vựng ML. Tài liệu ngành khác phải khai
`role_labels` để đổi tên — vd kinh tế: `param` → "Hãng tự chọn", `hyper` → "Thị trường
cho sẵn". Không đổi thì sổ tay in ra chữ "Nhãn thật" giữa một bài kinh tế học.

**Mode `code` — bắt buộc đọc ngữ cảnh thật.** Không bao giờ giải thích một đoạn code
trong chân không: `Grep` chỗ gọi nó, `Read` các import và kiểu dữ liệu liên quan, rồi mới
điền ô 04 (shape) và ô 09 (khi nó hỏng). Ô 09 phải là bug THẬT có thể xảy ra với code
này, không phải bug chung chung.

---

## Quy trình

**Bước 1 — Chốt nguồn.** Phân giải `$ARGUMENTS` thành mục tiêu cụ thể (conventions §2).
Nguồn mơ hồ → hỏi **đúng một câu**, liệt kê các lựa chọn. Không đoán thầm.

**Bước 2 — Đọc có chọn lọc.** Với tài liệu dài, chỉ đọc vùng mật độ cao: công thức,
định nghĩa, caption hình, khối code (conventions §6). Trước khi đọc nguồn thô, kiểm tra
`notes/INDEX.md` xem đã có bản distill chưa (§4).

**Bước 3 — Chọn thẻ + dựng DAG.** Mỗi công thức/hàm đáng học = một thẻ. Ghi quan hệ phụ
thuộc (`C2` cần `C1`) — người học biết quay lại đâu khi tắc. Gán `tier`: 1 cốt lõi,
2 mở rộng, 3 chuyên sâu.

**Bước 4 — Tính số cho ô 06 TRƯỚC khi viết.** Chọn bộ dữ liệu nhỏ nhất còn ý nghĩa
(2–4 hàng), chạy tay hoặc bằng `python`, ghi lại từng bước trung gian. Iron Law #2.
Dùng chung một bộ dữ liệu cho các thẻ liên quan để số khớp nhau xuyên suốt — đó là thứ
làm sổ tay trở nên liền mạch.

**Bước 5 — Viết spec JSON.** Chỉ viết NỘI DUNG. Không tự viết `\begin{axis}`,
`\begin{tcolorbox}`, hay bất kỳ boilerplate LaTeX nào (conventions §9).
Ghi ra `.tmp/study-forge_<slug>.json` (hoặc thư mục scratchpad nếu harness có).
Schema đầy đủ → `references/spec-schema.md`.

**Bước 6 — Build.**

```bash
python ~/.claude/skills/study-forge/scripts/build_handbook.py .tmp/study-forge_<slug>.json --format all --out-dir notes
```

**Bước 7 — Compile PDF và TỰ XEM LẠI.**

```bash
cd notes && xelatex -interaction=nonstopmode study-<slug>.tex && xelatex -interaction=nonstopmode study-<slug>.tex
```

Chạy hai lần cho mục lục. Rồi làm **cả hai** việc sau:

1. **Quét log tìm ký tự bị nuốt.** XeLaTeX bỏ glyph font không có mà **không** báo lỗi —
   `≥ 0` in ra thành ` 0`. Bắt buộc kiểm tra:

   ```bash
   grep -c "Missing character" notes/study-<slug>.log
   ```

   Phải bằng 0. Khác 0 → bổ sung ký tự đó vào bảng `UNI` trong `scripts/tex_emitter.py`.

2. **`Read` chính file PDF và nhìn thật.** Bảng tràn khung, nhãn đồ thị đè nhau, chữ chồng
   tiêu đề ô, trang trống hoác — không lỗi nào trong số này hiện ra trong log.

Sửa spec rồi build lại. Không báo xong khi chưa nhìn.

**Bước 8 — Báo cáo.** 5–10 dòng tiếng Việt + đường dẫn. Không dump nội dung file vào chat.

---

## Hợp đồng script-offloading

Model viết **nội dung**; script viết **mọi thứ liên quan tới định dạng**.

| Script tự sinh | Model KHÔNG được viết tay |
|---|---|
| preamble LaTeX, tcolorbox, thanh tiêu đề màu | `\newtcolorbox`, `\definecolor` |
| `\begin{axis}` + style pgfplots | bất kỳ dòng pgfplots nào |
| node/edge TikZ, định tuyến cạnh quay ngược | `\node[diamond, draw=...]` |
| `lstlisting` + tô cú pháp | `\lstset` |
| bảng `booktabs`, độ rộng cột | `\begin{tabular}` |
| khung Markdown, `<details>`, HTML+CSS | HTML/CSS bằng tay |

**Hình vẽ khai báo bằng dữ liệu, không bằng code vẽ:**

```json
"picture": {"kind": "plot", "plot": {
   "xlabel":"w", "ylabel":"J(w)", "xmin":0, "xmax":3.5, "ymin":0, "ymax":8,
   "curves":[{"expr":"(14*x^2 - 50*x + 45)/6", "style":"main", "legend":"J(w)"}],
   "points":[{"x":1.79, "y":0.06, "label":"day bat", "style":"min", "dy":10}]}}

"picture": {"kind": "flow", "flow": {
   "dir":"vertical",
   "nodes":[{"id":"n1","text":"y_hat = X @ w + b","type":"proc"},
            {"id":"n5","text":"Da hoi tu?","type":"dec"}],
   "edges":[{"from":"n5","to":"n1","label":"Chua"}]}}
```

`kind`: `plot` (pgfplots) · `flow` (TikZ) · `tikz` (TikZ thô, khi thật sự cần).
Cạnh quay ngược được script tự định tuyến vòng ra ngoài — **đừng** thêm `bend`.

**Text trong node là text THUẦN.** Script tự escape. Viết `y_hat = X @ w + b`, không viết
`y\_hat` hay `$-$` — pre-escape sẽ ra `y\{\}_hat` trên bản in.

---

## Định dạng xuất

| Format | Dùng khi | Ghi chú |
|---|---|---|
| `tex` → PDF | **mặc định**, bản để học và in | XeLaTeX. Chất lượng cao nhất: đồ thị thật, hộp màu, tô cú pháp |
| `md` | đọc nhanh trong VS Code / GitHub | công thức `$$`, Mermaid, `<details>`. Tuân `latex-katex-compat.md` |
| `html` | xem trên web / publish Artifact | tự chứa, không CDN, có bộ render công thức riêng |

**Không có đường Markdown → PDF đẹp.** Markdown không có primitive cho đồ thị, hộp màu,
hay flowchart. Đường đi là `JSON → LaTeX → PDF`; `md` là nhánh song song, không phải nguồn.

Yêu cầu: XeLaTeX (MiKTeX/TeX Live) với `tcolorbox`, `pgfplots`, `tikz`, `listings`.
Thiếu → vẫn xuất được `md`/`html`, và **nói rõ là chưa có PDF**, không im lặng bỏ qua.

---

## Nội dung code phải là ASCII

Code, comment trong code, và nhãn `twin.src` viết bằng **tiếng Anh ASCII**
(conventions §1). `listings` nghẹn UTF-8 và làm hỏng cả bản compile. Mọi tiếng Việt nằm
ở văn xuôi ngoài listing.

---

## Anti-patterns

| Cám dỗ | Vì sao sai | Làm đúng |
|---|---|---|
| "Công thức rõ rồi, bỏ ô 06" | Rõ với người đã hiểu, không rõ với người đang học | Luôn chạy số thật |
| "Ô 05 nghe giống ô 03" | 03 là *nó là gì*, 05 là *bỏ đi thì vỡ gì* — khác hẳn | Giữ cả hai |
| Vẽ hình bằng ASCII art | Xấu, không in được, thua xa pgfplots | Dùng `kind:"plot"` / `"flow"` |
| Tự viết `\begin{axis}` | Vi phạm §9, dễ sai, tốn token | Khai báo dữ liệu, để script vẽ |
| Ước lượng "khoảng 1.5" | Vi phạm Iron Law #2 | Tính thật hoặc bỏ ô |
| Giải thích code không đọc project | Ô 04/09 thành vô nghĩa | `Grep` chỗ gọi trước |
| Compile xong báo luôn | Lỗi layout chỉ thấy bằng mắt | `Read` PDF rồi mới báo |
| Chỉ viết 2 câu ở ô 10 | Trang bị hụt, và 2 lần nhớ lại là quá ít | Đủ 5 câu, theo thang khó dần |
| Ép mỗi thẻ một trang riêng | Thẻ ngắn để lại 3/4 trang trắng | Để thẻ chảy tự nhiên; script đã chống mồ côi tiêu đề |
| Nhồi 20 thẻ một lần | Không ai học nổi | ≤ 8 thẻ/sổ; nhiều hơn thì chia tập |
| Đặt màu theo thẩm mỹ | Phá luật màu ngữ nghĩa | Màu theo `role`, không theo ý thích |

---

## Ranh giới

| Việc | Skill đúng |
|---|---|
| **Tài liệu LẬP LUẬN không có công thức/code** (kinh tế, khoa học xã hội, luật) | **`claim-forge`** |
| Dạy tương tác, hỏi đáp qua lại | `study-tutor` |
| Giải thích một khái niệm trong chat, không cần file | `concept-explainer` |
| Phân tích method/toán của một paper | `paper-read` |
| Ra đề kiểm tra từ knowledge graph | `knowledge-quiz` |
| Sửa công thức không render | `latex-fix` |
| Vẽ figure cho bài báo Q1 | `latex-tikz-generator` |
| Review chất lượng code | `code-senior` |

Sinh xong sổ tay, handoff hợp lý: `→ knowledge-quiz` để tự kiểm tra sâu hơn,
`→ study-tutor` nếu người học vẫn tắc ở một thẻ cụ thể.

---

## Đầu ra

| Thứ | Đường dẫn |
|---|---|
| Sổ tay | `notes/study-<slug>.{tex,pdf,md,html}` |
| Spec | `.tmp/study-forge_<slug>.json` (giữ lại để build lại/sửa) |
| Ghi vào manifest | một dòng trong `notes/INDEX.md` |

`<slug>` là kebab-case theo chủ đề (`ml-w1-3`, `attention-forward`), ổn định giữa các lần
chạy để sửa là ghi đè, không sinh file mới.

## Tham chiếu

- `references/card-anatomy.md` — cách điền từng ô, kèm thẻ mẫu đã điền (math + code)
- `references/spec-schema.md` — schema JSON đầy đủ, gồm `plot` và `flow`
- `assets/example-spec.json` — spec chạy được, cũng là smoke-test
