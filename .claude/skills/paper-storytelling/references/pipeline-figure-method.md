# Pipeline Figure Method — Từ method notes ra figure "gánh được bài"

Đọc runtime bởi `paper-storytelling` (mode nào có figure). Style nền + luật chống đạo
văn hình thuộc `latex-tikz-generator` (≤8–10 node, 1 dominant + 1 accent, không copy
cấu trúc figure bài khác) — file này KHÔNG lặp lại, chỉ thêm tầng thiết kế & verify.
Skeleton dưới đây đã compile thật (IEEEtran + MiKTeX, 2026-07-20, paper 034).

---

## Pha 1 — Trích figure spec từ method notes (7 câu hỏi)

Trả lời 7 câu này TRƯỚC khi viết bất kỳ dòng TikZ nào (ghi nháp dạng list):

1. **Cái gì chảy?** (tensor/feature/message nào đi qua pipeline — đặt tên ký hiệu đúng như prose: $z_i$, $u_i$...)
2. **Các stage tuần tự?** (encoder → neck → ... → output; gộp bước chuẩn thành 1 block đại diện — luật abstraction)
3. **Phần nào MỚI vs KẾ THỪA?** (đóng góp của bài nằm ở block nào — đây là thứ figure phải làm nổi)
4. **Điểm chèn (insertion point) ở đâu?** (nếu đóng góp là recipe/module gắn vào 1 chỗ — highlight đúng 1 chỗ đó)
5. **Cái gì CHỈ CHẠY LÚC TRAIN?** (teacher, EMA branch, loss, target precomputed — tách hẳn khỏi đường inference)
6. **Loss nào đọc cái gì?** (mũi tên vào loss phải đúng nguồn — ví dụ loss đọc $z$ thô chứ không phải $u$ đã gate: chi tiết này NÓI được trong caption)
7. **Có vòng lặp/feedback không?** (iterative/closed-loop → cần cung dashed quay ngược)

Spec hoàn chỉnh = danh sách node (tên + 1–2 dòng text + phân loại base/new/loss) +
danh sách cạnh (từ→đến + solid/dashed + label nếu có) + câu trả lời 3/4/5.

## Pha 2 — Văn phạm thị giác (visual grammar)

| Ngữ nghĩa | Kiểu vẽ | TikZ style |
|---|---|---|
| Đường inference (chạy lúc deploy) | hàng TRÊN, mũi tên solid | `arr` |
| Train-only (teacher/EMA/loss) | hàng DƯỚI, mũi tên dashed xám | `tarr` |
| Block kế thừa (baseline) | xám nhạt | `base` (fill=gray!10) |
| Block ĐÓNG GÓP MỚI | màu accent + viền dày | `new` (fill=orange!25, thick) |
| Loss/objective | dashed viền, fill xanh rất nhạt | `loss` (fill=blue!8, dashed) |
| Legend | 1 node text dưới cùng, giải nghĩa dashed + 2 màu | `lbl` |

- Chỉ 1 màu accent cho phần mới — người đọc lướt 2 giây phải thấy ngay đóng góp nằm đâu.
- Text trong node: ký hiệu toán đúng như prose ($a_i{=}H_{aes}(z_i)$) — figure và text
  dùng CHUNG ký hiệu, không đặt tên mới.
- Không emoji, không icon, không drop-shadow.

## Pha 3 — Chọn layout (3 biến thể)

| Layout | Khi nào | Bố cục |
|---|---|---|
| **Two-row** (mặc định) | Method có train/inference khác nhau (distillation, EMA, self-supervision) | Hàng trên = inference solid; hàng dưới = targets + losses dashed; mũi tên thả từ node trên xuống loss dưới |
| **Single-row + inset** | Đóng góp là 1 module nội bộ | 1 hàng chính; module mới phóng to thành khung zoom bên dưới nối bằng 2 đường chéo mảnh |
| **Loop** | Method iterative / closed-loop / performative | Chuỗi ngang + cung dashed từ output vòng về input, label số vòng/điều kiện dừng |

Perspective-shift (luật `latex-tikz-generator`): nếu figure bài gốc/bài mẫu vẽ data-flow
thì cân nhắc vẽ theo insertion-point view hoặc train-vs-inference view — vừa tránh đạo
văn thiết kế vừa thường kể chuyện tốt hơn.

## Pha 3b — Thích ứng canvas theo venue (số ĐO THẬT, không ước lượng)

Canvas đo bằng probe `\typeout{\the\textwidth}` (MiKTeX, 2026-07-20):

| Venue class | Canvas cho figure | Ghi chú |
|---|---|---|
| `IEEEtran` conference, `figure*` | **516pt ≈ 18.1cm** | tràn 2 cột — canvas rộng nhất, skeleton Pha 4 vẽ thẳng cho cỡ này |
| `IEEEtran` conference, `figure` 1 cột | 252pt ≈ 8.9cm | chỉ cho hình phụ nhỏ; pipeline KHÔNG nhét vào đây |
| `llncs` (Springer LNCS, 1 cột) | **347pt ≈ 12.2cm** | = 67% canvas IEEE `figure*` |

Đo lại khi gặp class mới: tạo probe 5 dòng, KHÔNG viết bề rộng từ trí nhớ.

Luật thích ứng (rút từ lỗi thật 2026-07-20 — bản LNCS đầu tiên bị co pipeline
2 hàng thành 1 hàng vì thiếu các luật này):

| # | Luật | Vì sao |
|---|---|---|
| V1 | **Two-row là BẤT BIẾN kể chuyện — không format nào được co thành 1 hàng.** Thứ được phép co: chữ trong node, khoảng cách, font | 1 hàng đánh mất phân tách inference/train-only — chính là thứ figure phải kể |
| V2 | Tính `scale = canvas / natural width` (natural width lấy từ overfull message hoặc render). `scale ≥ 0.85` → cho phép `\resizebox`; `scale < 0.85` → **RE-LAYOUT compact**, cấm resizebox | font 8pt co 0.67 còn 5.4pt — không đọc được trên bản in |
| V3 | Re-layout compact cho canvas 347pt (LNCS): node `text width` 20→15–16mm · chữ node ≤2 từ/dòng (bỏ chữ thừa, giữ ký hiệu) · `node distance` ngang 5→4mm · font `\footnotesize`→`\scriptsize` · inner sep 3→1.5pt. Đủ cho hàng 5 box + nhãn output (~300pt) | co THÔNG SỐ giữ SƠ ĐỒ, thay vì co sơ đồ giữ thông số |
| V4 | **Float 1 cột trôi theo vị trí source.** Muốn pipeline nổi trang 2–3 (độ nổi ngang bài mẫu IEEE): đặt `\begin{figure}[t]` NGAY SAU đoạn đầu Introduction trong source, không đợi đến Method. Sau compile: hình đổ trang X, `\ref` đầu tiên trang Y — lệch >1 trang → dời source | LNCS bản đầu: figure source nằm ở Method → hình trôi tuốt trang 5/7, user tưởng "không có hình" |
| V5 | `figure*` của IEEE không bao giờ hiện trên trang đang gõ — trễ ít nhất sang trang sau. Muốn hiện trang N → source phải nằm trong text của trang N−1 | float mechanics của twocolumn |
| V6 | Headline 2 panel: canvas ≥500pt → 2 axis NGANG (mỗi cái ~8.4cm, skeleton §G). Canvas 347pt → 2 axis ngang chỉ khi ≤5 nhóm cột + nhãn ngắn (mỗi axis `width=0.48\textwidth`); ngược lại XẾP DỌC 2 axis (`at={(ax1.south west)}, yshift=-14mm`) | 2 panel ngang nhét 347pt với nhãn dài = chữ trục đè nhau |

## Pha 4 — TikZ skeleton (two-row, đã compile thật — thay text, giữ khung)

Preamble cần: `\usepackage{tikz}` + `\usetikzlibrary{positioning,arrows.meta,fit,backgrounds}`.

```latex
\begin{figure*}[t]
\centering
\begin{tikzpicture}[
  font=\footnotesize,
  node distance=3.5mm and 5mm,
  box/.style={draw, rounded corners=1.5pt, align=center, inner sep=3pt,
              minimum height=6.5mm},
  base/.style={box, fill=gray!10},
  new/.style={box, fill=orange!25, thick},
  loss/.style={box, fill=blue!8, dashed},
  lbl/.style={align=center, inner sep=1pt},
  arr/.style={-{Stealth[length=2mm]}, semithick},
  tarr/.style={arr, dashed, gray!70!black},
]
% ---- top row: inference path (solid) ----
\node[base] (in)    {input};
\node[base, right=of in]   (enc)  {stage A};
\node[base, right=of enc]  (mid)  {stage B\\$z_i$};
\node[new,  right=of mid]  (contrib) {NEW block\\$a_i, s_i$};
\node[base, right=of contrib] (dec) {stage C};
\node[base, right=of dec]  (out)  {output};
\draw[arr] (in) -- (enc);  \draw[arr] (enc) -- (mid);
\draw[arr] (mid) -- (contrib); \draw[arr] (contrib) -- (dec);
\draw[arr] (dec) -- (out);
% ---- bottom row: training-only (dashed), >=13mm below ----
\node[base, below=13mm of enc] (tgt1) {target source 1};
\node[base, right=of tgt1]     (tgt2) {targets $t_i$};
\node[base, right=of tgt2]     (teach){aux target\\(precomputed)};
\node[loss, right=of teach]    (l1)   {$\mathcal{L}_{main}$};
\node[loss, right=of l1]       (l2)   {$\mathcal{L}_{aux}$};
\draw[tarr] (tgt1) -- (tgt2);
% non-adjacent same-row edge: MUST detour below (rule R1)
\draw[tarr] (tgt2.south) -- ++(0,-3mm) -| ([xshift=-2.5mm]l1.south);
\draw[tarr] (teach) -- (l1);
% top->bottom drops: orthogonal, offset targets (rules R2, R3)
\draw[tarr] (mid.south) -- ++(0,-2mm)
  -| node[lbl, pos=0.22, above, font=\tiny]{raw $z_i$} ([xshift=-3mm]l1.north);
\draw[tarr] (contrib.south) -- ++(0,-1.5mm)
  -| node[lbl, pos=0.3, above, font=\tiny]{$a_i,\ s_i$} ([xshift=3mm]l1.north);
\draw[tarr] (dec.south) to[out=-90,in=90] (l2.north);
% ---- legend: >=7mm below bottom row (rule R4) ----
\node[lbl, below=7mm of tgt1, xshift=-2mm, anchor=north west]
  {\textcolor{gray!70!black}{dashed = training only}\quad
   \colorbox{orange!25}{\strut new (ours)}\quad
   \colorbox{gray!10}{\strut unchanged baseline}};
\end{tikzpicture}
\caption{«PHÁT HIỆN/thông điệp của figure, không phải "overview of the method": nêu
điểm chèn, cái gì train-only, và chi tiết chống-misread quan trọng nhất (ví dụ: loss
đọc raw $z_i$, không đọc gated $u_i$)».}
\label{fig:pipeline}
\end{figure*}
```

## Pha 5 — Luật chống va chạm (rút từ lỗi thật, mỗi luật từng cứu 1 bug render)

| # | Luật | Vì sao |
|---|---|---|
| R1 | **Cấm mũi tên thẳng giữa 2 node KHÔNG kề nhau cùng hàng** — luôn detour: `(a.south) -- ++(0,-3mm) -| ([xshift=..]b.south)` | Đường thẳng sẽ XUYÊN mọi box nằm giữa |
| R2 | Mũi tên thả hàng trên→hàng dưới đi ORTHOGONAL (`-- ++(0,-2mm) -|`), không `to[out=..,in=..]` khi giữa 2 hàng có box | Curve tự do dễ liếm qua góc box hàng dưới |
| R3 | Nhiều mũi tên cùng vào 1 node → target anchor LỆCH nhau: `([xshift=-3mm]l1.north)` vs `([xshift=3mm]l1.north)` | Trùng anchor = đè nhau, không đọc được nguồn |
| R4 | Legend đặt `below=7mm` trở xuống so với hàng cuối | Đường detour âm 3mm sẽ xuyên legend nếu để 1.5mm |
| R5 | Khoảng cách 2 hàng ≥13mm khi box 2+ dòng text; box nào 3 dòng → rút còn 2 (gộp text) | Hành lang giữa 2 hàng là nơi mọi đường ngang đi qua — box cao chiếm mất hành lang |
| R6 | Label trên cạnh: `font=\tiny`, đặt `above` đoạn NGANG của detour (pos 0.2–0.35), không đặt trên đoạn dọc | Đoạn dọc ngắn, label sẽ đè vào box |

## Pha 6 — Vòng compile → render → inspect (BẮT BUỘC, lặp đến sạch)

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex   # x2 (+bibtex neu doi cite)
python -c "import fitz; d=fitz.open('main.pdf'); d[PAGE].get_pixmap(dpi=160, clip=fitz.Rect(0,40,612,240)).save('fig_zoom.png')"
# -> Read fig_zoom.png va TU NHIN — khong claim "hinh dep" khi chua nhin
```

(pymupdf: `pip install pymupdf`; chỉnh `PAGE` 0-based và `clip` theo vị trí figure.
Không có pdflatex/pymupdf → ghi rõ "chưa compile-test".)

Bảng symptom → fix khi inspect:

| Triệu chứng nhìn thấy | Nguyên nhân | Fix |
|---|---|---|
| Đường dashed xuyên chữ trong box | vi phạm R1/R2 | detour orthogonal |
| Label cạnh đè lên box | vi phạm R6 hoặc hành lang hẹp | tăng khoảng hàng (R5) + label lên đoạn ngang |
| Legend bị đường gạch ngang xuyên | vi phạm R4 | hạ legend xuống ≥7mm |
| 2 mũi tên vào node đè nhau | vi phạm R3 | xshift target anchors |
| Trục pgfplots hiện `8·10⁻²` | scaled ticks mặc định | `scaled y ticks=false` + `yticklabel style={/pgf/number format/.cd, fixed, precision=2}` |
| Box tràn cột | node text quá dài | ≤20 từ/node (luật latex-tikz-generator), gộp dòng |

## Pha 7 (§G) — Headline figure + Algorithm (bộ đi kèm pipeline)

### §G.0 — Chọn LOẠI biểu đồ theo loại phát hiện (trước khi viết pgfplots)

Chart không phải trang trí — nó là CÂU CLAIM vẽ ra. Đọc results note, xác định
loại phát hiện, rồi tra bảng; không mặc định ybar cho mọi thứ:

| Phát hiện trong results note | Loại chart | Yếu tố bắt buộc |
|---|---|---|
| So sánh N model/variant trên 1 metric | `ybar` | đường **baseline dashed** + nhãn giá trị baseline; ymin đặt tại mức chance/floor có nghĩa, KHÔNG cắt trục để phóng đại gap |
| 2 metric cùng thang cho N variant | grouped `ybar` (2 `\addplot`) | legend gọn; 2 màu = 2 token của pipeline |
| Sweep 1 tham số (N, epochs, λ...) | line + marks | trục x là tham số; có vùng CI (`fill between`) CHỈ khi results note có số CI thật |
| Trade-off 2 chiều (metric A tăng, B giảm) | 2 panel (a)/(b) — panel (b) là chiều XẤU | trung thực bằng hình: không normalize/smooth giấu chiều xấu |
| Chất lượng phân loại theo ngưỡng | ROC/PR line | CHỈ vẽ từ điểm dữ liệu thật trong log; cấm vẽ đường cong minh họa |
| Sai lầm theo lớp | confusion matrix (`matrix plot`, colormap 1 màu) | số trong ô; colormap đơn sắc từ màu token |
| Phân bố per-sample/per-class | boxplot (pgfplots `statistics`) | chỉ khi có dữ liệu phân bố thật, không suy từ mean±std bịa |

Luật chung mọi chart: (1) số verbatim từ results note — thiếu số thì KHÔNG vẽ chart
đó, ghi `\TODO`; (2) màu dùng lại đúng token của pipeline (base/new/cls) — cả bài
1 bảng màu; (3) `scaled y ticks=false` + fixed precision; (4) caption nêu PHÁT HIỆN;
(5) mỗi chart trả lời đúng 1 research question — chart không map về question nào là
chart thừa.

### Headline pgfplots (đầu Results — 2 panel, số THẬT verbatim)

Preamble: `\usepackage{pgfplots}` + `\pgfplotsset{compat=1.15}`.

```latex
\begin{figure*}[t]
\centering
\begin{tikzpicture}
\begin{axis}[name=ax1, width=0.44\textwidth, height=4.6cm,
  ybar, bar width=5.5pt,
  title={(a) «metric family 1» (lower is better)}, title style={font=\footnotesize},
  symbolic x coords={R0,R1,R2,R3,R4}, xtick=data,
  ymin=0, scaled y ticks=false,
  yticklabel style={/pgf/number format/.cd, fixed, precision=2},
  tick label style={font=\footnotesize}, ymajorgrids, grid style={gray!20},
  legend style={font=\scriptsize, at={(0.98,0.98)}, anchor=north east, draw=none, fill=none}]
\addplot+[fill=blue!45, draw=blue!60!black] coordinates {(R0,..) (R1,..) ...};
\addplot+[fill=teal!45, draw=teal!60!black] coordinates {(R0,..) ...};
\legend{metric\_1, metric\_2}
\end{axis}
\begin{axis}[at={(ax1.outer east)}, anchor=outer west, xshift=8mm, ... ]
\addplot+[fill=orange!55, draw=orange!70!black] coordinates {...};
% baseline reference line — bat buoc khi co negative finding:
\draw[dashed, gray!60!black] (axis cs:R0,«baseline») -- (axis cs:R4,«baseline»);
\end{axis}
\end{tikzpicture}
\caption{«Nêu 2 phát hiện: (a) claim 1; (b) claim 2 + "the dashed line marks the
baseline"». }
\label{fig:headline}
\end{figure*}
```

- Panel (a) = phát hiện dương, panel (b) = phát hiện âm/trade-off KÈM đường baseline
  dashed — trung thực bằng hình.
- Số copy verbatim từ results note; không smooth, không normalize giấu chiều xấu.

### Algorithm (trong Method)

Preamble: `\usepackage{algorithm}` + `\usepackage{algorithmic}`.

```latex
\begin{algorithm}[t]
\caption{«Tên method» training with «safety property»}
\label{alg:main}
\begin{algorithmic}[1]
\REQUIRE «data; precomputed targets; switches; epochs»
\ENSURE «checkpoint contents (đủ để resume: model, optimiser, scheduler, RNG)»
\STATE «init — DÒNG QUYẾT ĐỊNH, kèm comment» \ \ $\triangleright$ «vì sao = baseline»
\FOR{...}\FORALL{batches}
  \STATE ... (mỗi dòng map 1-1 với 1 công thức Eq.~\eqref{..} trong prose)
\ENDFOR
\STATE «persist/commit» \ \ $\triangleright$ «tính chất vận hành»
\ENDFOR
\end{algorithmic}
\end{algorithm}
```

Ngay sau algorithm: đoạn walkthrough (mẫu câu ở `structure-template.md` §6.4). Mỗi
`\STATE` phải trỏ được về đúng công thức/đoạn prose — algorithm là MỤC LỤC của Method,
không phải pseudocode mới.

## Checklist nghiệm thu figure (trước khi handoff)

- [ ] Trả lời đủ 7 câu Pha 1; block mới nổi bằng đúng 1 màu accent
- [ ] Train-only tách hẳn (dashed + hàng riêng hoặc cung riêng); legend giải nghĩa
- [ ] Không vi phạm R1–R6 (đã NHÌN bản render, không đoán)
- [ ] Caption nêu phát hiện/chi tiết chống-misread, không mô tả suông
- [ ] Ký hiệu trong figure = ký hiệu trong prose, 1-1
- [ ] Không mirror cấu trúc figure của bài khác (nếu adapted → caption "adapted from [x]")
- [ ] Headline: số verbatim + baseline dashed line ở panel negative
- [ ] Algorithm: mỗi dòng trỏ về 1 Eq/đoạn prose; walkthrough gọi tên decisive step
