---
name: latex-tikz-generator
description: "Sinh code TikZ/Latex để vẽ diagram chuẩn Q1 (pipeline, block, attention, architecture, flow). Output là code LaTeX .tex inline, có thể compile trực tiếp. Tránh đạo văn hình ảnh vì TikZ là vector code, không có metadata. Triggers: vẽ pipeline, TikZ, system diagram, architecture diagram, flowchart, vẽ sơ đồ LaTeX, figure cho bài báo."
---

# LaTeX TikZ Generator — Hình học học thuật chuẩn Q1

Sinh code TikZ/Latex để vẽ figure cho bài báo Q1 IEEE. Output là `.tex` inline, compile trong LaTeX trực tiếp, không cần file ngoài.

Binding: `~/.claude/rules/paper-writing-integrity.md` §2 (figures — chuẩn là ORIGINALITY,
không phải detectability).

## Tại sao TikZ thay vì hình raster/GUI tool
- Hình TikZ sinh từ code → vector vô hạn, tự vẽ nguyên bản nên không dính bản quyền ảnh của bài khác. **Lưu ý:** vẽ lại CẤU TRÚC figure của bài khác bằng TikZ vẫn là đạo văn thiết kế — hoặc redesign thật (abstraction/perspective-shift bên dưới), hoặc caption "adapted from [x]"
- Nằm trong `.tex` cùng document, đồng nhất font + palette với paper
- Kích thước compile theo dpi, qua-peer-review không bị mờ
- Dễ version control (text-based, diff hữu ích)

## Thiết kế TikZ để tránh đạo văn hình
Áp dụng 3-quy tắc:

1. Abstraction (trừu tượng hóa): gộp các bước chuẩn thành block đại diện (ví dụ: "Preprocessing" thay vì liệt kê từng sub-step). Giữ chi tiết ở module đóng góp chính.
2. Perspective shift (đổi góc nhìn): nếu bài liên quan vẽ data-flow → bạn vẽ component-based hoặc control-flow → narrator view.
3. Màu nhận diện (theo domain): không copy màu của bài tham khảo. Mỗi block type có palette riêng do bạn định nghĩa.

## Phong cách đồ họa Q1 (IEEE / ACM / Springer)
- Số node ≤ 8 trong một diagram (nếu nhiều hơn → chia thành 2 figures).
- Đường nối → thẳng, không curve fancy (academic style).
- Font: \footnotesize hoặc \small (không quá nhỏ).
- Khoảng cách node: khép vừa, không rời rạc.
- Màu: dominant 1 màu, accent 1 màu cho output, rest neutral gray.
- Label: text bên trong node rõ, không icon/phông tượng (emoji → cấm).

## 4 Loại diagram (trigger patterns)

Mỗi loại có 1 skeleton TikZ đã compile-verify (pdflatex, exit 0, visually inspected)
trong `references/tikz-skeletons.md` — đọc file đó để lấy code khởi điểm, đừng viết
lại từ đầu. Copy skeleton đúng loại, sửa theo phần "Edit:" của nó, rồi mới áp 3 quy
tắc tránh đạo văn ở trên.

### 1. Pipeline / Flowchart (Encoder-Decoder / Sequential)
Input: user mô tả luồng dữ liệu từ đầu vào đầu ra. Skeleton: node chain ngang,
`right=of` giữa các stage, 1 stage highlight màu accent (đóng góp chính).

### 2. Block / Component Architecture
Input: các thành phần + mối liên kết (aggregation/composition). Skeleton: block nét
đứt (module tái dùng) vs block liền nét tô màu (đóng góp chính), khung `fit` bao quanh
toàn model.

### 3. Attention / Attention-head / Matrix visualization
Input: số class, số head, label trục. Skeleton: heatmap N×N thuần TikZ (không cần
pgfplots), fill theo `\pgfmathparse` trên mảng số; label hàng/cột dùng
`foreach i/lbl` — KHÔNG index mảng chuỗi bằng `\pgfmathparse` (silent garbage, xem
"Known pitfalls" trong file skeleton).

### 4. Training / Convergence / Curves
Input: data points (epoch, loss/acc) hoặc trend. Skeleton: `\draw plot coordinates`
thuần TikZ + trục vẽ tay (không pgfplots), 2 series minh họa (loss giảm, acc tăng) +
legend.

## Output format

Khi viết TikZ cho user, luôn trả về:

1. Code TikZ đầy đủ trong môi trường `tikzpicture`
2. Giải thích ngắn 2–3 dòng cách đọc figure
3. Lưu ý compile: `pdflatex` cần `\usepackage{tikz}` + libs phụ trợ.

Không bao giờ sinh code copy từ bài khác. Diagram mô phỏng cấu trúc figure nguồn →
bắt buộc "adapted from [x]" trong caption (integrity rules §2).

## Quy tắc compile an toàn
- Chỉ dùng libs phổ biến: `\usetikzlibrary{shapes,arrows.meta,positioning,calc,matrix,backgrounds}` (+ `fit` riêng cho skeleton #2) — không dùng lib hiếm gây lỗi compile. Dùng `arrows.meta` (không phải `arrows` cũ) cho cú pháp `{Stealth[length=2mm]}` hiện đại.
- **Compile-verify khi có thể:** nếu `pdflatex`/`tectonic` có trên máy (check `where pdflatex`), compile thử bản `standalone` của figure trước khi trả; không có → ghi rõ "code chưa compile-test" thay vì claim chạy được.
- Giữ node text trong English (machine content).
- Giới hạn chiều dài mỗi node ≤ 20 từ để không tràn khi render.

## Kích thước paper chuẩn
- single-column figure: width ≤ 0.9\columnwidth
- two-column figure: width = \columnwidth
- caption dưới figure, label TikZ node nên tạo label đúng convention `\label{fig:...}`.

## Cách dùng từ skill khác
Skill khác gọi: "Vẽ pipeline", "TikZ figure", "LaTeX diagram", "System architecture diagram". Khi đó skill gọi tool chuyên này. Skill này không write prose (không caption dài), chỉ sinh code + giải thích. Prose + caption do skill gọi viết.
