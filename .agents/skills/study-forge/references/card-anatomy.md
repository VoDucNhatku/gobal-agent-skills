# Card Anatomy — cách điền từng ô

Đọc file này khi đang thực sự viết nội dung thẻ. `SKILL.md` chỉ liệt kê 10 ô;
đây là tiêu chuẩn chất lượng cho từng ô, kèm phép thử "ô này đã đạt chưa".

---

## 01 · Việc nó làm (`job`)

Một câu. Nói **công việc**, không nói **định nghĩa**.

- ✅ "Ép toàn bộ độ tệ của mô hình trên mọi điểm dữ liệu xuống còn MỘT con số, để có thứ mà tối thiểu hoá."
- ❌ "Hàm chi phí MSE là trung bình bình phương sai số." ← đây là định nghĩa, đọc xong vẫn không biết dùng để làm gì.

**Phép thử:** che tên thẻ đi, đọc câu này — có đoán được vì sao người ta cần nó không?

---

## 02 · Công thức / Mã nguồn (`expr` / `code`)

- `expr`: TeX **không** kèm `$$`. Script tự bọc `equation` và đánh số.
- `code`: ASCII tiếng Anh (kể cả comment). Cắt đúng phần đáng học — dán cả file là lười.
  Giữ nguyên tên biến gốc của project, không đổi tên cho "đẹp": người học phải nhận ra
  code này khi quay lại repo.

---

### Thẻ khái niệm (`claim`)

Tài liệu kinh tế, luật, quản trị phần lớn KHÔNG có công thức. Ô 02 khi đó chứa một
**mệnh đề** — thứ có thể đúng hoặc sai, không phải một định nghĩa. Mọi ô sau vẫn chạy:
ô 05 mổ *giả định* thay vì *số hạng*, ô 06 chạy một tình huống thật thay vì phép tính,
ô 08 nén mệnh đề thành một dòng ký hiệu.

- ✅ "Cân bằng KHÔNG hợp tác có thể trùng khít kết quả THÔNG ĐỒNG."
- ❌ "Chi phí chuyển đổi là chi phí khách phải trả khi đổi nhà cung cấp." ← định nghĩa.

---

## 03 · Giải phẫu (`legend`)

Một dòng cho mỗi ký hiệu/biến. Cột `note` trả lời **"nó làm gì"**, không phải "nó tên là gì".

- ✅ `w` → "nút vặn ĐỘ DỐC: x tăng 1 thì đầu ra tăng w"
- ❌ `w` → "trọng số (weight)" ← chỉ dịch lại tên.

Kể cả **hằng số** cũng phải có dòng riêng nếu nó gây thắc mắc. Ví dụ số `2` trong `1/(2m)`:
"không có ý nghĩa thống kê, chỉ để khi đạo hàm số mũ 2 rơi xuống và triệt tiêu" — đây
đúng là câu hỏi mọi người học đều có mà sách hiếm khi trả lời.

`role` phải đúng luật màu. Lẫn `param` với `hyper` là lỗi nặng nhất ở ô này.

---

## 04 · Truy vết kích thước (`shapes`)

Ô có tỉ lệ giá trị/công sức cao nhất cho người học ML, và gần như luôn bị bỏ qua.

- Ghi chiều thật: `(m,n)·(n,1) → (m,1)`.
- Cột `note` dùng để cảnh báo **lỗi im lặng**: "nếu `y` là `(m,)` thì kết quả thành
  `(m,m)` — SAI mà KHÔNG báo lỗi". Loại ghi chú này cứu được hàng giờ debug.
- Với code không phải ML: dùng kiểu dữ liệu và bất biến thay cho shape
  (`list[str] → dict[str,int]`, "trả về dict rỗng chứ không phải None").

---

## 05 · Bỏ đi thì sao (`ablation`) ⭐

Với **mỗi** thành phần: xoá nó / đặt về 0 / đảo dấu → chuyện gì xảy ra?

`severity`:

| Giá trị | Nghĩa | Ví dụ |
|---|---|---|
| `breaks` | hỏng hẳn, thường thấy ngay | bỏ `X.T` → `ValueError` |
| `degrades` | vẫn chạy, kết quả kém đi | bỏ `1/m` → learning rate hỏng theo cỡ batch |
| `subtle` | vẫn chạy, vẫn *có vẻ* đúng, nhưng sai | cập nhật không đồng thời |

Ưu tiên tìm cho ra ít nhất một `subtle`. Đó là loại bug đắt nhất trong ML, và là thứ
người học không bao giờ tự nghĩ ra được.

**Phép thử:** hệ quả có nói được **cơ chế** không? "sẽ sai" là chưa đạt; "gradient tỉ lệ
với cỡ batch nên đổi batch size là phải chỉnh lại alpha" mới đạt.

---

## 06 · Chạy số thật (`trace`) ⭐

Iron Law #2 sống ở đây.

1. Chọn bộ dữ liệu nhỏ nhất còn ý nghĩa — 3 hàng là đủ, số nguyên nhỏ.
2. **Dùng lại đúng bộ đó cho mọi thẻ liên quan.** Khi thẻ cost ra `J = 1.5` và thẻ
   gradient descent xuất phát từ chính `J = 1.5` đó, người học thấy được sợi dây nối.
3. Ghi **mọi bước trung gian**, không nhảy cóc. Bước ẩn là chỗ người học rơi.
4. `result` nói ra **bài học**, không chỉ con số:
   "gradient ÂM nên `w` ĐI LÊN — dấu trừ trong công thức là thứ đảo hướng đó."

Tính bằng `python` rồi chép lại. Đừng tính nhẩm rồi ghi.

---

## 07 · Hình dung (`picture`)

Chọn `kind` theo thứ nó cần trả lời:

| Câu hỏi | `kind` |
|---|---|
| "Hàm này có hình gì? Tối ưu nằm đâu?" | `plot` |
| "Dữ liệu chảy qua đâu? Vòng lặp quay về đâu?" | `flow` |
| "Cần một hình đặc thù không rơi vào hai loại trên" | `tikz` |

Quy tắc cho `plot`:
- Chọn `xmin/xmax/ymin/ymax` sao cho **đặc trưng cần thấy chiếm phần lớn khung**. Đồ thị
  mà đường cong dẹp lét ở đáy là đồ thị vô dụng.
- Đánh dấu điểm có nghĩa (`points`): điểm tối ưu, vị trí hiện tại, các bước lặp.
- Nhãn chồng nhau thì đẩy bằng `dx`/`dy` (đơn vị pt), đừng viết nhãn dài.
- `caption` phải nói điều đồ thị **chứng minh**, không mô tả lại đồ thị.
  ✅ "Bình phương sai số biến độ tệ thành lòng chảo lồi — đúng một đáy, nên GD không thể kẹt."
  ❌ "Đồ thị hàm J theo w."

Quy tắc cho `flow`:
- `type`: `start` (đầu/cuối) · `proc` (xử lý) · `dec` (rẽ nhánh) · `io` (vào/ra).
- Text node là **text thuần**, script tự escape.
- Cạnh quay ngược: chỉ khai `from`/`to`/`label`, script tự vòng ra ngoài. Thêm `bend` sẽ
  làm cạnh cắt xuyên qua các hộp ở giữa.

---

## 08 · Viết bằng ngôn ngữ kia (`twin`) ⭐

Ô vá khoảng cách công thức ↔ code. Tiêu đề in ra tự đổi theo loại thẻ:
"Cùng công thức này, viết bằng code" hoặc "Cùng đoạn code này, viết bằng công thức" —
**không bao giờ đặt tên ẩn dụ**; người đọc phải biết ngay phải làm gì với ô.

- Thẻ **công thức** → `twin` là code (thường `python`/`numpy`), ngắn nhất có thể.
- Thẻ **code** → `twin` là công thức hoặc pseudocode (`lang: "text"`).
- `map` là phần quan trọng nhất: nối từng ký hiệu với đúng tên biến
  (`m` ↔ `X.shape[0]`, `∇_w J` ↔ `grad_w`). Thiếu bảng này thì ô mất tác dụng.

Code trong `twin` phải **chạy được nếu dán vào**, không phải mã giả trá hình.

---

## 09 · Khi nó hỏng (`failures`)

Ba cột: **triệu chứng bạn thấy** → nguyên nhân → cách sửa.

Bắt đầu bằng triệu chứng, vì đó là thứ người học gặp trước: "J = nan ngay từ epoch đầu",
"w bỗng có shape (3,3)", "loss đứng yên hoàn toàn".

Cách sửa phải **cụ thể và làm được ngay**: "assert `gw.shape == w.shape` ngay sau khi tính
gradient", không phải "kiểm tra lại code".

Với thẻ code: lỗi phải là lỗi thật của **đoạn code này**, tìm được bằng cách đọc chỗ gọi
nó trong project. Lỗi chung chung là dấu hiệu chưa đọc ngữ cảnh.

---

## 10 · Tự kiểm tra (`probes`) ⭐ — BẮT BUỘC, tối thiểu 5 câu

Năm câu, xếp theo **thang khó dần**. Script cảnh báo nếu thẻ nào dưới 5.

| # | Loại | Hỏi gì |
|---|---|---|
| 1 | Nhớ lại có suy luận | hệ quả trực tiếp của cấu trúc công thức |
| 2 | Áp dụng | thay một giá trị cụ thể vào, chuyện gì xảy ra |
| 3 | Tính chất | cận, dấu, miền giá trị — "J có âm được không?" |
| 4 | Bất biến / đổi thang | đổi đơn vị, nhân đôi dữ liệu, đổi batch size |
| 5 | Trường hợp biên hoặc liên hệ rộng | m = 0, gradient = 0, "ở deep learning thì khác gì?" |

Không phải công thức cứng — nhưng năm câu **cùng một kiểu** thì chỉ đáng một câu.
Câu 5 nên nối thẻ này với thứ người học sẽ gặp sau, đó là chỗ kiến thức bám lại.

Câu hỏi phải hỏi **hệ quả**, không hỏi **định nghĩa**:

- ✅ "Nhân đôi toàn bộ dữ liệu (mỗi điểm xuất hiện 2 lần). J thay đổi thế nào?"
- ✅ "Đang đứng đúng tại đáy. Bước cập nhật tiếp theo làm gì?"
- ❌ "MSE là gì?" ← tra lại ô 02 là xong, không tạo trí nhớ.

Đáp án phải **giải thích cơ chế**, không chỉ đúng/sai:
"Không đổi. Tử số Σe² gấp đôi, mẫu 2m cũng gấp đôi — triệt tiêu. Đó chính là lý do có
1/m: J đo độ tệ TRUNG BÌNH, không phải TỔNG."

**Phép thử:** trả lời đúng câu này có chứng minh được là đã hiểu, hay chỉ chứng minh là
đã đọc? Nếu là vế sau, viết lại câu hỏi.

---

## Thẻ mẫu đã điền

Xem `assets/example-spec.json` — bốn thẻ chạy được:

| Thẻ | Loại | Minh hoạ |
|---|---|---|
| C1 | công thức | `plot` nhiều đường, ablation `breaks` + `degrades` |
| C2 | công thức | trace 5 bước, `plot` lòng chảo có đánh dấu đáy |
| C3 | công thức | `plot` các bước lặp có mũi tên, ablation `subtle` |
| C5 | **code** | flowchart có cạnh quay ngược, `twin` ngược (code → công thức) |

Số của C2, C3, C5 dùng chung một bộ dữ liệu (`x=[1,2,3]`, `y=[2,4,5]`) nên khớp nhau
xuyên suốt — đó là mẫu cần noi theo.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| ablation slot | ô bỏ đi thì sao | Xoá/đặt 0 từng thành phần để lộ vai trò thật của nó |
| numeric trace | chạy số thật | Chạy dữ liệu thật qua công thức, ghi mọi bước trung gian |
| twin | viết bằng ngôn ngữ kia | Cùng một ý diễn đạt ở ngôn ngữ còn lại (toán ↔ code) |
| recall probe | ô tự kiểm tra | Câu hỏi hệ quả, đáp án để dưới, tạo trí nhớ chủ động |
| semantic colour law | luật màu ngữ nghĩa | Một vai trò một màu, giống nhau ở mọi nơi trong sổ tay |
| silent failure | lỗi im lặng | Sai kết quả nhưng không ném lỗi — loại bug đắt nhất |
