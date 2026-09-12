# Spec Schema — hợp đồng JSON của study-forge

Model viết file này. `scripts/build_handbook.py` đọc nó và sinh toàn bộ LaTeX/Markdown/HTML.
Ghi ra `.tmp/study-forge_<slug>.json`.

```bash
python ~/.claude/skills/study-forge/scripts/build_handbook.py <spec.json> \
       --format all --out-dir notes
```

`--format`: `md` (mặc định) · `tex` · `html` · `all`.

---

## Cấp tài liệu

| Trường | Bắt buộc | Kiểu | Ghi chú |
|---|---|---|---|
| `slug` | ✅ | string | kebab-case, ổn định giữa các lần chạy → tên file `study-<slug>.*` |
| `title` | ✅ | string | tiêu đề sổ tay (tiếng Việt) |
| `cards` | ✅ | array | 1–8 thẻ. Nhiều hơn thì tách thành nhiều sổ |
| `subtitle` | | string | 1–2 câu mô tả phạm vi |
| `source` | | string | nguồn gốc tài liệu, hiện ở trang bìa |
| `domain` | | `math`\|`code`\|`mixed` | chỉ để ghi chú |
| `notation` | | array | bảng ký hiệu dùng chung, in một lần ở đầu |
| `dag` | | array | quan hệ phụ thuộc giữa các thẻ |
| `role_labels` | | object | đổi tên 7 vai trò cho ngành khác ML (giữ nguyên màu) |

```json
"notation": [
  {"sym": "m", "role": "index", "read": "em", "means": "số điểm dữ liệu (số hàng)"},
  {"sym": "alpha", "role": "hyper", "read": "an-pha", "means": "learning rate — BẠN chọn"}
]
"dag": [{"from": "C1", "to": "C2", "label": "đo sai số của"}]
```

`sym` viết **không kèm dấu `\`**: `alpha`, `sigma`, `mu`. Chữ Hy Lạp được nhận diện tự động.

---

## Cấp thẻ

| Trường | Bắt buộc | Ô | Kiểu |
|---|---|---|---|
| `id` | ✅ | — | `C1`, `C2`… dùng trong `dag` |
| `title` | ✅ | — | tên thẻ |
| `job` | ✅ | 01 | một câu: việc nó làm |
| `tier` | | — | `1` cốt lõi · `2` mở rộng · `3` chuyên sâu |
| `expr` | ✳ | 02 | TeX, **không** kèm `$$` |
| `claim` | ✳ | 02 | một mệnh đề — thẻ khái niệm, không công thức không code |
| `code` | ✳ | 02 | `{"lang":"python","src":"..."}` — ASCII |
| `legend` | | 03 | giải phẫu từng mảnh |
| `shapes` | | 04 | truy vết kích thước |
| `ablation` | | 05 | bỏ đi thì sao |
| `trace` | | 06 | chạy số thật |
| `picture` | | 07 | hình dung |
| `twin` | | 08 | cùng ý đó viết bằng ngôn ngữ kia (toán ↔ code) |
| `failures` | | 09 | khi nó hỏng |
| `probes` | ✅ | 10 | tự kiểm tra — **tối thiểu 5 câu**, Iron Law #1 |

✳ mỗi thẻ cần đúng một trong `expr` · `code` · `claim`. Loại thẻ quyết định cách diễn
đạt của ô 05 ("từng mảnh của công thức" vs "từng giả định của lập luận") và ô 08.

```json
"legend":   [{"key":"w", "role":"param", "note":"nút vặn ĐỘ DỐC: x tăng 1 thì đầu ra tăng w"}],
"shapes":   [{"expr":"X @ w", "in":"(m,n)·(n,1)", "out":"(m,1)", "note":"n phải khớp"}],
"ablation": [{"remove":"b", "severity":"degrades", "effect":"đường buộc đi qua gốc..."}],
"trace":    {"given":"m = 3 điểm: x = [1,2,3], y = [2,4,5]; w = 1, b = 0",
             "steps":[{"step":"1. Dự đoán f = 1·x + 0", "value":"[1, 2, 3]"}],
             "result":"J = 1.5"},
"twin":     {"lang":"python", "src":"...", "map":[{"sym":"m","var":"len(y)"}]},
"failures": [{"symptom":"J = nan ngay từ epoch đầu", "cause":"...", "fix":"..."}],
"probes":   [{"q":"...", "a":"..."}]
```

`role`: `param` · `hyper` · `data` · `truth` · `pred` · `index` · `op`
`severity`: `breaks` · `degrades` · `subtle`

---

## `picture` — hình vẽ khai báo bằng dữ liệu

### `kind: "plot"` → pgfplots

```json
{"kind":"plot", "caption":"...", "plot":{
  "xlabel":"w", "ylabel":"J(w)",
  "xmin":0, "xmax":3.5, "ymin":0, "ymax":8,
  "curves":[{"expr":"(14*x^2 - 50*x + 45)/6", "domain":"0:3.5",
             "style":"main", "legend":"J(w)"}],
  "points":[{"x":1.79, "y":0.06, "label":"day bat", "style":"min",
             "anchor":"south west", "dx":6, "dy":10}],
  "arrows":[{"from":[1,1.5], "to":[1.37,0.47], "label":"mot buoc"}]}}
```

| Trường | Giá trị |
|---|---|
| `curves[].expr` | biểu thức pgfplots, biến là `x`: `x^2`, `exp(-x)`, `1/(1+exp(-x))` |
| `curves[].style` | `main` (đậm, xanh) · `alt` (đỏ, nét đứt) · `ghost` (xám, chấm) |
| `curves[].legend` | TeX không kèm `$`. Bỏ trống → đường không vào chú giải |
| `points[].style` | `min` (đỏ, tròn) · `step` (xanh, tròn) · `note` (xanh lá, tam giác) |
| `points[].anchor` | `north west`, `south east`, `west`… vị trí nhãn so với điểm |
| `points[].dx/dy` | đẩy nhãn thêm, đơn vị pt — dùng khi nhãn chồng nhau |

Nhãn trong `label`/`caption` là **text thuần**, script tự escape.
`expr` là cú pháp pgfplots, **không** escape — viết `x^2`, không `x\^2`.

### `kind: "flow"` → TikZ

```json
{"kind":"flow", "caption":"...", "flow":{
  "dir":"vertical",
  "nodes":[{"id":"n0", "text":"Khởi tạo w, b", "type":"start", "width":"38mm"},
           {"id":"n1", "text":"y_hat = X @ w + b", "type":"proc"},
           {"id":"n5", "text":"Đã hội tụ?", "type":"dec", "width":"24mm"}],
  "edges":[{"from":"n0","to":"n1"},
           {"from":"n5","to":"n1","label":"Chưa","offset":3.2}]}}
```

| Trường | Giá trị |
|---|---|
| `dir` | `vertical` (mặc định) · `horizontal` |
| `type` | `start` (bo góc, xanh lá) · `proc` (chữ nhật, xanh) · `dec` (thoi, đỏ) · `io` (hình thang, xám) |
| `width` | bề rộng text, mặc định `30mm` — nới ra khi chữ dài |
| `offset` | chỉ cho **cạnh quay ngược**: khoảng vòng ra ngoài, đơn vị cm (mặc định 3.0) |

Node xếp tuần tự theo thứ tự trong `nodes`. Cạnh **quay ngược** (đích đứng trước nguồn)
được script tự định tuyến vòng ra ngoài cột — **đừng** thêm `bend`, nó sẽ cắt xuyên qua
các hộp ở giữa.

`text` là **text thuần**: viết `y_hat = X @ w + b`, không viết `y\_hat` hay `$-$`.

### `kind: "tikz"` → TikZ thô

```json
{"kind":"tikz", "src":"\\begin{tikzpicture}...\\end{tikzpicture}", "caption":"..."}
```

Chỉ dùng khi `plot` và `flow` thật sự không diễn đạt được. Không có lưới an toàn ở đây:
sai cú pháp là hỏng cả bản compile.

---

## Sau khi build

```bash
cd notes
xelatex -interaction=nonstopmode study-<slug>.tex
xelatex -interaction=nonstopmode study-<slug>.tex   # lần 2 cho mục lục
```

Rồi **`Read` file PDF và nhìn thật.** Lỗi hay gặp mà log không báo:

| Thấy gì | Nguyên nhân | Sửa ở đâu |
|---|---|---|
| Bảng tràn ra khỏi khung màu | cột `p{}` quá rộng | rút gọn `note`/`effect` trong spec |
| Nhãn đồ thị đè lên nhau | hai điểm quá gần | thêm `dx`/`dy`, rút ngắn `label` |
| Đường cong dẹp sát đáy | khung trục quá rộng | siết `ymin`/`ymax` |
| Chữ lạ kiểu `y\{\}_hat` | đã escape sẵn trong spec | bỏ escape, viết text thuần |
| Mũi tên cắt xuyên hộp | có `bend` ở cạnh quay ngược | bỏ `bend`, dùng `offset` |
| Compile chết ở `lstlisting` | code có ký tự UTF-8 | code phải ASCII tiếng Anh |
| Ký hiệu biến mất (`≥ 0` → ` 0`) | font không có glyph, XeLaTeX nuốt im lặng | thêm ký tự vào `UNI` trong `tex_emitter.py` |
| Trang trắng lớn cuối thẻ | ô 10 dưới 5 câu | viết đủ 5 câu (script có cảnh báo) |

**Bắt buộc quét log sau khi compile** — số này phải bằng 0:

```bash
grep -c "Missing character" study-<slug>.log
```
