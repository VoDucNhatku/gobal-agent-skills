---
name: latex-tikz-generator
description: "Sinh code TikZ/Latex để vẽ diagram chuẩn Q1 (pipeline, block, attention, architecture, flow). Output là code LaTeX .tex inline, có thể compile trực tiếp. Tránh đạo văn hình ảnh vì TikZ là vector code, không có metadata. Triggers: vẽ pipeline, TikZ, system diagram, architecture diagram, flowchart, vẽ sơ đồ LaTeX, figure cho bài báo."
---

# LaTeX TikZ Generator — Hình học học thuật chuẩn Q1

Sinh code TikZ/Latex để vẽ figure cho bài báo Q1 IEEE. Output là `.tex` inline, compile trong LaTeX trực tiếp, không cần file ngoài.

## Tại sao TikZ thay vì hình raster/GUI tool
- Hình TikZ sinh từ code → vector vô hạn, không bị đạo văn ảnh (image plagiarism scanner chỉ quét pixels/metadata, không quét TikZ code)
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

### 1. Pipeline / Flowchart (Encoder-Decoder / Sequential)
Input: user mô tả luồng dữ liệu từ đầu vào đầu ra.
Output: \begin{tikzpicture} \node chain xuôi hoặc ngang.

### 2. Block / Component Architecture
Input: các thành phần + mối liên kết (aggregation/composition).
Output: block chữ nhật có nét đứt, mũi tên gán nhãn.

### 3. Attention / Attention-head / Matrix visualization
Input: số class, số head, label trục.
Output: heatmap grid hoặc attention weight matrix.

### 4. Training / Convergence / Curves
Input: data points (epoch, loss/acc) hoặc trend.
Output: \draw + plot coordinates + axis node.

## Output format

Khi viết TikZ cho user, luôn trả về:

1. Code TikZ đầy đủ trong môi trường `tikzpicture`
2. Giải thích ngắn 2–3 dòng cách đọc figure
3. Lưu ý compile: `pdflatex` cần `\usepackage{tikz}` + libs phụ trợ.

Không bao giờ sinh code có copyright/copy từ bài khác. TikZ tự sinh — không đạo văn khái niệm được.

## Quy tắc compile an toàn
- Chỉ dùng libs phổ biến: `\usetikzlibrary{shapes,arrows,positioning,calc,matrix,backgrounds}` — không dùng lib hiếm gây lỗi compile.
- Giữ node text trong English (machine content).
- Giới hạn chiều dài mỗi node ≤ 20 từ để không tràn khi render.

## Kích thước paper chuẩn
- single-column figure: width ≤ 0.9\columnwidth
- two-column figure: width = \columnwidth
- caption dưới figure, label TikZ node nên tạo label đúng convention `\label{fig:...}`.

## Cách dùng từ skill khác
Skill khác gọi: "Vẽ pipeline", "TikZ figure", "LaTeX diagram", "System architecture diagram". Khi đó skill gọi tool chuyên này. Skill này không write prose (không caption dài), chỉ sinh code + giải thích. Prose + caption do skill gọi viết.
