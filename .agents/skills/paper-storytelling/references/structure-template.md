# Structure Template — Bản đồ cấu trúc storytelling (chưng cất từ SARD + AUFE-Q4)

Đọc runtime bởi `paper-storytelling`. Mọi ví dụ tiếng Anh là MẪU CÂU (sentence formula)
— thay nội dung, giữ chức năng. Không copy nguyên văn câu của bài mẫu nào vào bản thảo.

---

## 0. Thứ tự VIẾT (khác thứ tự ĐỌC)

Viết theo thứ tự results-first của advisor:
`①Results → ②Discussion(gộp vào Results) → ③Method → ④Conclusion → ⑤Related → ⑥Intro → ⑦Abstract → ⑧Title → ⑨References`.
Lý do: mọi claim ở Intro/Abstract phải trỏ về số đã viết ở Results — viết ngược để
không bao giờ hứa thứ chưa có.

## 1. Title — công thức 3 vế

```
«Tên phương pháp/framework» for «Bài toán»: «Finding A», «Finding B», and «Tính chất C»
```

- 3 vế là **kết quả/tính chất đã chứng minh trong bài**, không phải buzzword.
  Vế C thường là tính chất engineering/honesty (ví dụ: "Safety-by-Construction
  Training", "a Conformal Certification").
- Viết CUỐI CÙNG, sau khi biết chính xác bài chứng minh được gì.
- Test: đọc riêng title phải đoán được cả 3 phát hiện chính của bài.

## 2. Abstract — 4 khối, ~10 câu, 1 đoạn đặc

| Khối | Số câu | Chức năng | Mẫu câu |
|---|---|---|---|
| Scene + reframe | 2–3 | Mở bằng cảnh CỤ THỂ của bài toán, rồi reframe thành vấn đề mô hình chưa giải | "A photograph often frames its subject badly only because..." — cấm "In recent years" |
| Approach + safety property | 2–3 | Nêu N tín hiệu/thành phần + tính chất làm so sánh đáng tin | "...all inserted at a single point, with every new parameter identity-initialised so that training starts bit-for-bit at the baseline" |
| Numbers | 2–3 | Số THẬT verbatim, nêu cả chiều xấu | "...box loss down 12.7%..., while classification error improves only for..." |
| Honesty closer | 1–2 | Câu chốt trung thực | "Every number comes from executed runs; measurements not yet performed are explicitly marked as pending." |

- Kết quả partial/negative nêu THẲNG trong abstract — không giấu đến Results.

## 3. Introduction — tỷ lệ 10/40/40/10, có research questions

Cấu trúc đoạn:
1. **Opening scene** (~10%): 1 đoạn, cảnh cụ thể → định nghĩa bài toán → tên framework
   nền + cách nó hoạt động trong 2–3 câu.
2. **Gap** (~40% cùng đoạn 2): chỉ ra thiếu sót bằng một CÂU CHÂN DUNG dễ nhớ
   ("This design, however, is *uniform in confidence*.") + 1 so sánh đời thường
   (a human editor...).
3. **Research questions** — bắt buộc, mẫu:
   ```
   «N» questions organise this paper. First, does «tín hiệu 1» ...?
   Second, does «tín hiệu 2» ...? Third, can «tín hiệu 3» ...?
   ```
   Mỗi section sau phải trả lời đúng các câu này; Results subsection ↔ question 1-1.
4. **Contributions as prose** (~40%): MỘT đoạn văn liền mạch (không bullet), mỗi đóng
   góp dính ngay con số của nó:
   ```
   Our contributions are as follows. We show that «X»: «số cụ thể». We identify and
   quantify «trade-off/negative finding»..., a negative result we report as a finding
   in its own right. We make the comparison honest by construction: «safety property».
   Finally, we document «mechanism/engineering contribution».
   ```
5. Câu chốt (~10%): điều bài KHÔNG làm / phạm vi (giữ claim ≤ tier ledger).

## 4. Related Work — mỗi đoạn kết bằng positioning

- 3–4 đoạn CHỦ ĐỀ (không phải theo paper). Mỗi đoạn: mở bằng dòng văn liệu → 2–3 nguồn
  đan thành lập luận (synthesis, không "A said X. B said Y.") → **câu kết định vị**:
  ```
  What separates our study is «khác biệt component-level»...
  ```
- Nguồn nào bị dùng off-design → nói thẳng tại đây ("We adopt the loss form unchanged
  but apply it to a residual it was not designed for... a design choice to be validated
  empirically") — đây là mồi cho ablation.

## 5. Preliminaries / Threat Model — định nghĩa thước đo TẠI ĐÂY

- Mô tả setting bằng VĂN XUÔI trước, ký hiệu sau; chỉ công thức nào Results cần.
- **Mọi metric mà Results dùng để so sánh phải được định nghĩa ở đây**, kèm cảnh báo
  non-comparability nếu có (ví dụ: vì sao total loss không so được giữa các run) —
  KHÔNG để người đọc gặp cảnh báo lần đầu ở Results.

## 6. Method — insertion point + crux + Algorithm walkthrough

1. Mở bằng 1 câu định vị: mọi thay đổi nằm Ở ĐÂU trong pipeline (trỏ Fig 1) và vì sao
   thiết kế đó làm ablation đáng tin ("a set of switches over one code path").
2. Mỗi thành phần = 1 `\paragraph`; mỗi công thức mang đúng 1 tag provenance
   ([cited]/[derived]/[design]) — luật research-proposal-integrity §4.
3. **Gọi tên crux**: một câu tường minh "The crux is «X»" / "the decisive step is
   line «N»".
4. **Algorithm 1** (env `algorithm`+`algorithmic`, `\REQUIRE/\ENSURE`, comment
   `$\triangleright$`) + đoạn **walkthrough** ngay sau, mẫu:
   ```
   Algorithm 1 reads as follows. The decisive step is line «N»: «vì sao». Lines
   «A–B» are one ordinary «unit»: «tóm tắt». Line «C» is the operational half of
   the design: «cơ chế engineering + bằng chứng nó đã chạy thật».
   ```
5. Safety property (identity-init, invariant, v.v.) tách thành subsection riêng nếu nó
   là lý do tin được ablation.

## 7. Experimental Setup — gọn + trung thực dữ liệu

- 1 đoạn: dataset (số CHÍNH XÁC, nêu rõ subset và vì sao — "the constraint is upstream
  design, not our filtering"), init, epochs, GPU, batch, LR, các preset ablation gắn
  với switches của Algorithm.
- Câu tái lập: chỉ claim những gì THẬT ("logs and checkpoints are retained on ...");
  cấm claim "code released" khi chưa release.

## 8. Results AND Discussion — GỘP, chia theo phát hiện

Khung chuẩn (map 1-1 với research questions):

```
\section{Results and Discussion}
  [đoạn dẫn: Fig 2 headline tóm 2 phát hiện chính + trỏ Table đầy đủ]
  \subsection{«Finding 1 — claim khẳng định»}      % ví dụ: "Localisation improves under every variant"
  \subsection{«Finding 2 — trade-off/negative»}     % kể như phát hiện đáng giá nhất
  \subsection{Why «hiện tượng», and what «module» learns}   % mục CƠ CHẾ
  \subsection{Caveats and pending measurements}     % đoạn văn, KHÔNG mục rỗng
```

Luật viết trong Results:
- **Number-narration**: mỗi số nằm trong câu có nghĩa nhân quả + so sánh tương đối
  ("R3 the best values of 0.0740/0.0406 --- reductions of 12.7% and 12.3%"). Bảng chỉ
  để tra cứu.
- Đặt tên PATTERN của kết quả ("The pattern is informative in two ways. It is
  *additive*: ... And it is *unconditional*: ...").
- **Negative result**: mở bằng câu nâng tầm ("The second finding is the one a
  leaderboard would hide, and we consider it the more instructive of the two."),
  nêu nghi phạm cơ chế + bằng chứng chiều hướng, kết bằng lời khuyên practitioner.
- **Mục cơ chế**: giải thích hiện tượng gây hiểu lầm (loss âm...) + điều module học
  được; mọi phép suy ra mang tag [derived].
- **Caveats**: 1 đoạn "Several caveats bound our claims. First... (\TODO{...}).
  Second... Third..." — mỗi caveat kèm hướng khắc phục; \TODO đỏ hiển thị, không giấu.

## 9. Conclusion — 1 đoạn

Reframe lại bằng ngôn ngữ mới → những gì ĐÃ chứng minh (kèm số) → trade-off thẳng thắn
→ future work = chính danh sách \TODO còn lại (nhất quán, không hứa thêm).

## 10. Bộ figure tối thiểu

| Figure | Vị trí | Chức năng | Nguồn quy trình |
|---|---|---|---|
| Fig 1 pipeline | đầu Method | kiến trúc + điểm chèn + train/inference split | `pipeline-figure-method.md` pha 1–6 |
| Algorithm 1 | trong Method | training loop + safety property | `pipeline-figure-method.md` §G |
| Fig 2 headline | NGAY ĐẦU Results | 2 phát hiện chính từ số thật | `pipeline-figure-method.md` §G |
| Table ablation | Results | tra cứu đầy đủ, best-per-column bold, chú thích non-comparability | số verbatim từ results note |

Caption luật: caption NÊU PHÁT HIỆN ("Both box-regression losses improve for *every*
augmented variant"), không mô tả suông ("Results of the ablation").

## 11. Diagnosis checklist — 10 lỗi khiến bản thảo "đọc dở" (dùng cho mode rewrite)

| # | Lỗi | Sửa bằng |
|---|---|---|
| 1 | 0 figure | §10 |
| 2 | Không có Algorithm + walkthrough | §6 |
| 3 | Không có research questions | §3 |
| 4 | Số đứng trơ trong bảng, prose không kể | §8 number-narration |
| 5 | Experiments/Discussion tách rời, lặp nhau | §8 gộp |
| 6 | Subsection rỗng chứa \TODO | §8 caveats-as-paragraph |
| 7 | Kết quả âm kể như điểm trừ/limitation | §8 negative-as-finding |
| 8 | Thiếu mục cơ chế "why" | §8 mechanism subsection |
| 9 | Đoạn mỏng, không TEEL 120–200 từ | style-humanizer §TEEL (handoff) |
| 10 | Title/Abstract không phản ánh finding | §1–§2 |

## 12. Tỷ lệ trang tham khảo (theo định dạng — cùng cấu trúc, khác lớp trình bày)

| Định dạng | Độ dài điển hình | Ghi chú trình bày |
|---|---|---|
| IEEE 2 cột (`IEEEtran` conference) | ~5–8 trang | figure/chart chủ đạo dùng `figure*` tràn 2 cột; nhớ độ trễ 1 trang của `figure*` (luật V5) |
| Springer LNCS (`llncs`, 1 cột) | ~10–16 trang | canvas hẹp 347pt → pipeline re-layout compact (luật V3); float đặt source sớm để hình nổi trang 2–3 (luật V4) |

Tỷ lệ mục GIỮ NGUYÊN cho cả hai: Intro ~15% · Related ~10% · Prelim ~8% · Method
(kèm Fig1+Alg) ~25% · Setup ~7% · Results+Discussion (kèm Fig2+Table) ~30% ·
Conclusion ~5%. Results+Discussion là mục DÀI NHẤT — nếu Method dài hơn Results,
bài đang kể sai trọng tâm. Cùng một bài đổi định dạng: prose/số/bib giữ nguyên,
chỉ làm lại lớp figure theo Pha 3b của `pipeline-figure-method.md`.
