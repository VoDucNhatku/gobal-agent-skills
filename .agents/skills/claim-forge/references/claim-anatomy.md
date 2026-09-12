# Claim Anatomy — cách điền từng ô + schema

Đọc khi đang thực sự viết thẻ. `SKILL.md` liệt kê 11 ô; đây là tiêu chuẩn chất lượng và
hợp đồng JSON.

---

## Schema

```json
{
  "profile": "argument",
  "slug": "arg-<chu-de>", "title": "...", "subtitle": "...", "source": "...",
  "cards": [{
    "id": "K1", "title": "...",
    "strength": "chung-minh | cho-thay | goi-y | gia-thuyet",
    "claim": "mệnh đề nêu sao cho CÓ THỂ SAI",
    "provenance": {"tag":"nguon|suy-ra|chua-kiem", "who":"...", "where":"§II, tr.377",
                   "note":"..."},
    "chain": {"steps":["tiền đề 1","tiền đề 2"], "conclusion":"...", "gap":"..."},
    "evidence":    [{"kind":"so-lieu|mo-hinh|ca-cu-the|suy-luan","what":"...","note":"..."}],
    "assumptions": [{"assume":"...","load":"ganh|phu","if_false":"..."}],
    "rival":       [{"alt":"...","how_to_tell":"..."}],
    "falsify":     [{"observe":"...","would_mean":"..."}],
    "case":  {"given":"...","steps":[{"step":"...","value":"..."}],"result":"..."},
    "picture": { … giống study-forge: kind plot | flow | tikz … },
    "scope": {"applies":["..."], "breaks":["..."]},
    "probes": [{"q":"...","a":"..."}]
  }]
}
```

Bắt buộc: `id` · `title` · `strength` · `claim` · `probes` (≥5).
Bỏ được: `picture` · `scope` · `case` khi nguồn thật sự không có.
**Không bỏ được:** `provenance` · `chain` · `evidence` · `assumptions` · `rival` ·
`falsify` — thiếu bất kỳ ô nào trong sáu ô đó thì đây không còn là đọc phê phán.

---

## 01 · Khẳng định (`claim`)

Phép thử: **thêm chữ "sai" vào trước câu này, nó có thành một mệnh đề có nghĩa không?**

- ✅ "Cân bằng không hợp tác có thể trùng khít kết quả thông đồng." → phủ định được.
- ❌ "Bài báo bàn về chi phí chuyển đổi." → phủ định thành vô nghĩa. Đó là chủ đề.

`strength` chọn theo **cách nguồn tự phát biểu**:

| Nguồn viết | `strength` |
|---|---|
| "we prove", "định lý", có chứng minh | `chung-minh` |
| "we show", "our results indicate" | `cho-thay` |
| "suggests", "the presumption is", "may" | `goi-y` |
| "we conjecture", "future work should test" | `gia-thuyet` |

Nâng một bậc vì thấy lập luận thuyết phục = vi phạm bất biến bảo toàn nghĩa.

---

## 02 · Ai nói, ở đâu (`provenance`)

`where` phải đủ để người đọc tự mở nguồn kiểm lại: mục, số phương trình, số trang.
"Trong bài báo" là chưa đạt.

`tag`:
- `nguon` — nguồn nói đúng ý này.
- `suy-ra` — **bạn** ghép từ nhiều chỗ. Hợp lệ, nhưng phải khai.
- `chua-kiem` — chưa xác minh được (OCR hỏng, không tiếp cận được nguồn gốc).

Một thẻ `suy-ra` mà mức là `chung-minh` gần như luôn sai: bạn đang gán độ chắc của nguồn
cho suy luận của chính mình.

---

## 03 · Đường lập luận (`chain`)

Mỗi bước là **một** bước. Nếu một bước cần người đọc tự nhảy hai nấc, tách đôi ra.

`gap` là ô quý nhất và hay bị bỏ trống nhất: chỗ nào chuỗi lập luận cần thêm một giả định
chưa nói ra? Ví dụ đạt: *"Chuỗi này chỉ chạy khi hãng KHÔNG phân biệt giá được. Đó là giả
định, không phải kết quả."*

Không có chỗ hở thật thì ghi rõ là không, đừng bịa một chỗ hở cho đủ ô.

---

## 04 · Bằng chứng đỡ ở đâu (`evidence`)

Xếp hạng theo **thứ đỡ nó**, không theo mức độ thuyết phục khi đọc.

| `kind` | Dấu hiệu nhận ra |
|---|---|
| `so-lieu` | có bảng số, cỡ mẫu, khoảng tin cậy, dữ liệu thật |
| `mo-hinh` | có định lý / điều kiện bậc nhất / mô phỏng — đúng trong phạm vi giả định |
| `ca-cu-the` | một ví dụ, ca lịch sử, giai thoại ngành |
| `suy-luan` | chỉ có chữ, "rõ ràng là", "hiển nhiên" |

Cột `note` phải nêu **giới hạn** của bằng chứng đó, không lặp lại nội dung:
✅ "chỉ một bộ tham số a=100, c=10" · ❌ "ví dụ về hai hãng hàng không".

Một mô hình toán chặt vẫn chỉ là hạng `mo-hinh`, không phải `so-lieu`. Đây là chỗ nhầm
phổ biến nhất khi đọc kinh tế lý thuyết.

---

## 05 · Giả định gánh (`assumptions`)

`load`:
- `ganh` — bỏ nó thì **kết luận sụp**.
- `phu` — bỏ nó thì kết luận yếu đi hoặc đổi độ lớn, nhưng vẫn đứng.

`if_false` phải nói **cơ chế**, không nói "sẽ sai":
✅ "Cho phép phân biệt giá thì mỗi hãng có động cơ phá rào ngay, lợi nhuận chung giảm."
❌ "Nếu giả định này sai thì kết quả không còn đúng."

Thẻ nào cũng nên có **ít nhất một** `ganh`. Không tìm ra cái nào gánh nghĩa là bạn chưa
tìm, hoặc khẳng định đó tầm thường.

---

## 06 · Cách giải thích khác (`rival`)

Ô này quyết định sổ tay có dạy được tư duy phê phán hay không.

Câu hỏi để nghĩ ra: **cùng bằng chứng đó, còn nguyên nhân nào khác cũng tạo ra được
không?** Với dữ liệu quan sát, gần như luôn có.

`how_to_tell` bắt buộc phải là **phép phân biệt thực hiện được**:
✅ "Đo chênh lệch giá gia hạn so với giá khách mới. Khác biệt sản phẩm nâng cả hai;
lock-in chỉ nâng giá gia hạn."
❌ "Cần nghiên cứu thêm."

Nếu chính nguồn đã nêu và bác bỏ một cách giải thích khác, ghi vào đây kèm cách họ bác.

---

## 07 · Cái gì bác được nó (`falsify`)

`observe` là **quan sát cụ thể, đo được**. `would_mean` nói nó giết phần nào của khẳng
định — đôi khi chỉ giết một giả định chứ không giết cả kết luận, ghi đúng như vậy.

Không nghĩ ra được phép bác bỏ nào → đó là phát hiện quan trọng, ghi thẳng: *"khẳng định
ở dạng hiện tại không bác bỏ được bằng quan sát"*. Đừng bịa một phép bác bỏ giả.

---

## 08 · Một ca cụ thể (`case`)

Có số thì tính thật bằng `python` rồi chép lại — cùng luật với `study-forge`.
Không có số thì kể một tình huống **có trong nguồn**, không tự sáng tác ví dụ.

`result` phải nói bài học, và nếu ca đó chỉ minh hoạ chứ không chứng minh thì nói rõ.

---

## 10 · Dùng được tới đâu (`scope`)

`applies` và `breaks` là hai danh sách song song, đọc theo cặp. Đây là chỗ chuyển từ
"hiểu bài báo" sang "biết khi nào được dùng nó" — cũng là chỗ người đọc hay áp bừa kết
luận sang bối cảnh khác.

---

## 11 · Tự kiểm tra (`probes`) — tối thiểu 5

Khác với `study-forge`, câu hỏi ở đây nên nhắm vào **kết cấu lập luận**, không phải vào
cơ chế tính toán. Thang gợi ý:

| # | Nhắm vào |
|---|---|
| 1 | phân biệt khẳng định với thứ dễ nhầm với nó |
| 2 | giả định nào gánh, bỏ đi thì sụp thế nào |
| 3 | hạng bằng chứng cao nhất là gì và điều đó giới hạn ta ra sao |
| 4 | cách giải thích khác mạnh nhất |
| 5 | trích dẫn khẳng định này thế nào cho đúng độ mạnh |

Câu 5 là câu đặc trưng của skill này — nó dạy người đọc **không trích dẫn quá tay**, thứ
mà đọc bao nhiêu lần cũng không tự hình thành.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| falsifiability | tính bác bỏ được | Có quan sát nào có thể chứng minh khẳng định sai không |
| rival explanation | cách giải thích khác | Nguyên nhân khác cũng tạo ra đúng bằng chứng đó |
| load-bearing assumption | giả định gánh | Bỏ nó thì kết luận sụp, không chỉ yếu đi |
| scope condition | điều kiện áp dụng | Ranh giới mà ngoài đó kết luận không còn đúng |
| provenance tag | nhãn nguồn gốc | nguồn nói / tôi suy ra / chưa kiểm |
| claim ledger | sổ khẳng định | Bảng một dòng mỗi khẳng định + độ mạnh + phép bác bỏ |
