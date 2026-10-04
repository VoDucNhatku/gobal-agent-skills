# TikZ Skeletons — 4 diagram types

Compile-verified templates (pdflatex/MiKTeX, `standalone` class, exit 0, visually
inspected) for the 4 diagram types listed in `SKILL.md`. Copy the relevant skeleton,
edit the marked spots, then apply the anti-plagiarism rules (abstraction /
perspective-shift / own palette) and the compile-safety rules from `SKILL.md` before
handing code back to the user. Every skeleton uses only the standard library set:
`shapes, arrows.meta, positioning, calc, matrix, backgrounds` (skeleton 2 also needs
`fit`, listed in its own header).

---

## 1. Pipeline / Flowchart (Encoder-Decoder / sequential)

```latex
\begin{tikzpicture}[
  node distance=8mm,
  block/.style={draw, rectangle, rounded corners=1pt, minimum height=8mm,
    minimum width=20mm, align=center, font=\footnotesize, fill=blue!6},
  io/.style={draw, rectangle, minimum height=7mm, minimum width=16mm,
    align=center, font=\footnotesize, fill=gray!10},
  arr/.style={-{Stealth[length=2mm]}, thick}
]
  \node[io] (input) {Input $x$};
  \node[block, right=of input] (enc) {Encoder\\ $f_\theta$};
  \node[block, right=of enc, fill=orange!12] (latent) {Latent $z$};
  \node[block, right=of latent] (dec) {Decoder\\ $g_\phi$};
  \node[io, right=of dec] (output) {Output $\hat{x}$};

  \draw[arr] (input) -- (enc);
  \draw[arr] (enc) -- (latent);
  \draw[arr] (latent) -- (dec);
  \draw[arr] (dec) -- (output);
\end{tikzpicture}
```

**Edit:** stage count (add/remove `node[block, right=of <prev>]` in the chain), stage
labels, and the highlighted stage's fill color (`orange!12` marks the contribution).
For a vertical pipeline, swap `right=of` for `below=of` throughout.

---

## 2. Block / Component Architecture

Needs `\usetikzlibrary{..., fit}` in addition to the standard set (for the dotted
container box around the whole model).

```latex
\begin{tikzpicture}[
  node distance=6mm and 10mm,
  comp/.style={draw, rectangle, dashed, rounded corners=1pt, minimum height=8mm,
    minimum width=22mm, align=center, font=\footnotesize},
  core/.style={draw, rectangle, solid, thick, rounded corners=1pt,
    minimum height=8mm, minimum width=22mm, align=center, font=\footnotesize,
    fill=blue!8},
  arr/.style={-{Stealth[length=2mm]}, thick},
  lbl/.style={font=\scriptsize, midway, above, sloped}
]
  \node[comp] (a) {Feature\\Extractor};
  \node[core, right=of a] (b) {Fusion\\Module};
  \node[comp, right=of b] (c) {Decoder\\Head};
  \node[comp, below=of b, yshift=-4mm] (d) {Auxiliary\\Branch};

  \draw[arr] (a) -- node[lbl] {$x$} (b);
  \draw[arr] (b) -- node[lbl] {$z$} (c);
  \draw[arr] (d) -- node[lbl, sloped, above] {$x_{aux}$} (b);

  \begin{scope}[on background layer]
    \node[draw, dotted, inner sep=6mm, fit=(a) (b) (c) (d),
      label={[font=\scriptsize]above:Model $\mathcal{M}$}] {};
  \end{scope}
\end{tikzpicture}
```

**Edit:** `comp` = a peripheral/reused component (dashed border); `core` = the paper's
own contribution (solid, filled — the visual weight the reader should notice first,
per SKILL.md's "1 dominant + 1 accent" color rule). Add/remove nodes and `fit=(...)`
entries together; the `fit` list must name every node the box should enclose.

---

## 3. Attention / weight-matrix heatmap

Pure TikZ — no `pgfplots` dependency. `\pgfmathparse` only evaluates numbers, so the
numeric weight array is indexed programmatically but the row/column **labels are
zipped via `foreach i/lbl`**, never put in a `\pgfmathparse`-indexed array (that silently
prints garbage — verified by compiling the wrong version first).

```latex
\def\weights{{
  0.80,0.10,0.05,0.05,
  0.15,0.70,0.10,0.05,
  0.05,0.15,0.65,0.15,
  0.05,0.05,0.20,0.70
}}
\begin{tikzpicture}[
  cell/.style={draw, minimum size=8mm, inner sep=0},
  lbl/.style={font=\scriptsize}
]
  \foreach \i in {0,...,3} {
    \foreach \j in {0,...,3} {
      \pgfmathparse{\weights[\i*4+\j]}
      \pgfmathsetmacro{\pct}{100*\pgfmathresult}
      \node[cell, fill=blue!\pct, minimum size=8mm] at (\j*8mm, -\i*8mm) {};
    }
  }
  \foreach \j/\lbl in {0/The, 1/cat, 2/sat, 3/down}
    \node[lbl, above] at (\j*8mm, 4mm) {\lbl};
  \foreach \i/\lbl in {0/The, 1/cat, 2/sat, 3/down}
    \node[lbl, left] at (-4mm, -\i*8mm) {\lbl};
\end{tikzpicture}
```

**Edit:** `\weights` is row-major, values in `[0,1]`, size must be `N*N` for an `N`
you also change in both `\foreach \i/\j in {0,...,N-1}` loops. The two label lists
must each have exactly `N` entries and stay in the same order as the weight rows/cols
(query tokens on top, key tokens on the left — swap if your convention is reversed).
`fill=blue!\pct` needs `\pct` in `[0,100]`; `\pgfmathsetmacro{\pct}{100*\pgfmathresult}`
already does that scaling — do not multiply again.

---

## 4. Training / Convergence curves

Pure TikZ `\draw ... plot coordinates` + hand-drawn axis — no `pgfplots` dependency,
per this skill's "common libs only" rule. Coordinates are hand-placed to match the
axis scale (`\width`/`\height` mm ↔ `\xmax`/`\ymax` data range); this is a schematic,
not a data-accurate plot — if you have real numbers, compute each point's mm position
as `value/\ymax*\height` before writing the coordinate list.

```latex
\begin{tikzpicture}[
  axis/.style={-{Stealth[length=2mm]}, thick},
  curveA/.style={thick, blue},
  curveB/.style={thick, red, dashed},
  lbl/.style={font=\scriptsize}
]
  \def\xmax{50}
  \def\ymax{1.0}
  \def\width{55mm}
  \def\height{35mm}

  \draw[axis] (0,0) -- (\width+2mm,0) node[right, lbl] {epoch};
  \draw[axis] (0,0) -- (0,\height+2mm) node[above, lbl] {loss / acc};

  \foreach \x/\xl in {0/0, 10/10, 20/20, 30/30, 40/40, 50/50} {
    \pgfmathsetmacro{\xp}{\x/\xmax*\width/1mm}
    \draw (\xp mm, 0) -- ++(0,-1mm) node[below, lbl] {\xl};
  }
  \foreach \y in {0,0.25,0.5,0.75,1.0} {
    \pgfmathsetmacro{\yp}{\y/\ymax*\height/1mm}
    \draw (0,\yp mm) -- ++(-1mm,0) node[left, lbl] {\y};
  }

  % train loss: 0.9 -> 0.08 (y-values already converted to mm at \height=35mm scale)
  \draw[curveA] plot[smooth] coordinates {
    (0,31.5mm) (5mm,26.4mm) (11mm,19.6mm) (16.5mm,14.7mm) (22mm,10.85mm)
    (27.5mm,8.05mm) (33mm,6.3mm) (38.5mm,4.9mm) (44mm,4.2mm) (49.5mm,3.5mm) (55mm,2.8mm)
  };
  % val accuracy: 0.1 -> 0.82
  \draw[curveB] plot[smooth] coordinates {
    (0,3.5mm) (5mm,10.5mm) (11mm,16.1mm) (16.5mm,20.3mm) (22mm,23.8mm)
    (27.5mm,25.9mm) (33mm,27.3mm) (38.5mm,28.4mm) (44mm,28.7mm) (49.5mm,28.7mm) (55mm,28.7mm)
  };

  \draw[curveA] (\width+6mm,\height) -- ++(6mm,0) node[right, lbl] {train loss};
  \draw[curveB] (\width+6mm,\height-6mm) -- ++(6mm,0) node[right, lbl] {val acc};
\end{tikzpicture}
```

**Edit:** `\xmax`/`\ymax` set the axis range shown in the ticks; each curve's
coordinate list is `(x_mm, value/\ymax*\height)` — recompute every y if you change
`\ymax` or `\height`. Add a third `curveC` style (e.g. `thick, dashed, gray`) for a
third series (val loss, LR schedule) the same way.

---

## Known pitfalls (hit and fixed while compile-testing these)

- **`\toks` is a reserved TeX primitive** (register allocator) — never name a macro
  `\toks`; it fails with `You can't use begin-group character { after \the`. Use
  `\seqlabels` or similar instead.
- **`\pgfmathparse` is numeric-only.** Do not index a string array with it — it either
  errors or silently prints an unrelated numeric result (verified: it printed stray
  TikZ coordinate values instead of token strings). Zip strings with
  `\foreach a/b in {0/foo, 1/bar}` instead.
- **A `plot[smooth]` first point set to `(0,0)` on a curve meant to start high** (e.g.
  a loss curve) produces a spline overshoot/hump before it decays — set the first
  coordinate to the actual starting value, not the origin.
