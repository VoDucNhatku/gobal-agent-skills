#!/usr/bin/env python3
"""build_handbook.py — render a study handbook from a compact JSON card spec.

Called by the `study-forge` skill (script-offloading, workbench-conventions §9):
the skill emits ONLY pedagogical content as JSON; this script writes every byte of
format boilerplate — Markdown scaffolding, the LaTeX preamble + tcolorbox envelopes,
and a fully self-contained HTML page (no CDN, no external font, no JS dependency,
CSP-safe) including a dependency-free TeX renderer for the formula subset used by
ML/DL study material.

Usage:
    python build_handbook.py <spec.json> [--format md|tex|html|all] [--out-dir notes]

Output: <out-dir>/study-<slug>.{md,tex,html}

Spec schema (all fields optional except slug/title/cards):
{
  "slug": "ml-w1-3",
  "title": "...",
  "subtitle": "...",
  "source": "Summary_Math_Formulas_Notebook.tex",
  "domain": "math" | "code" | "mixed",
  "palette": "blueprint",
  "notation": [{"sym":"m","role":"index","read":"em","means":"số điểm dữ liệu"}],
  "dag": [{"from":"C1","to":"C2","label":"dùng trong"}],
  "cards": [{
    "id": "C1", "title": "...", "tier": 1,
    "job": "một dòng: công thức/hàm này làm việc gì",
    "expr": "f_{w,b}(x) = w \\cdot x + b",          # math card (TeX, no $$)
    "code": {"lang":"python","src":"..."},           # code card
    "legend": [{"key":"w","role":"param","note":"trọng số"}],
    "shapes": [{"expr":"X @ w","in":"(m,n)·(n,1)","out":"(m,1)","note":""}],
    "ablation": [{"remove":"b","effect":"...","severity":"breaks"}],
    "trace": {"given":"...","steps":[{"step":"...","value":"..."}],"result":"..."},
    "picture": {"kind":"plot","plot":{...},"caption":"..."}    # pgfplots / mpl SVG
             | {"kind":"flow","flow":{...},"caption":"..."}    # TikZ / mermaid
             | {"kind":"tikz","src":"...","caption":"..."},    # raw TikZ (tex only)
    "twin": {"lang":"python","src":"...","map":[{"sym":"w","var":"w"}]},
    "failures": [{"symptom":"...","cause":"...","fix":"..."}],
    "probes": [{"q":"...","a":"..."}]
  }]
}
"""
from __future__ import annotations

import argparse
import html as _html
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# ---------------------------------------------------------------------------
# Semantic role law — the SAME role has the SAME colour in formula, diagram, code.
# Light / dark values are both pinned at >= 4.5:1 on their own surface.
# ---------------------------------------------------------------------------
ROLES = {
    "param":  ("Tham số học được",   "#B45309", "#F0B357"),
    "data":   ("Dữ liệu vào",        "#0E7490", "#5FD0E6"),
    "pred":   ("Dự đoán của mô hình", "#1D4ED8", "#8AB4FF"),
    "truth":  ("Nhãn thật",          "#047857", "#5BD6A4"),
    "hyper":  ("Siêu tham số",       "#A21CAF", "#E88CF0"),
    "index":  ("Chỉ số / kích thước", "#64748B", "#9AA6B8"),
    "op":     ("Toán tử / rút gọn",  "#334155", "#C3CDDB"),
}
SEVERITY = {
    "breaks":   ("VỠ NGAY",     "#B42318", "#FF8A7A"),
    "degrades": ("KÉM ĐI",      "#B45309", "#F0B357"),
    "subtle":   ("SAI ÂM THẦM", "#64748B", "#9AA6B8"),
}
# A chip is useless without a legend. This text is printed once at the front of
# every handbook, and again as a lead line inside slot 05.
SEVERITY_WHY = {
    "breaks":   "chương trình báo lỗi ngay — không thể bỏ sót",
    "degrades": "vẫn chạy, nhưng kết quả tệ đi thấy rõ",
    "subtle":   "vẫn chạy, kết quả trông vẫn hợp lý, nhưng SAI — loại nguy hiểm nhất",
}
TIER_LABEL = {1: "Cốt lõi", 2: "Mở rộng", 3: "Chuyên sâu"}

# Card-type-dependent wording. A concept card has no formula, so it must never
# be told to "xoá từng mảnh của công thức".
TWIN_TITLE = {
    "math":  "Cùng công thức này, viết bằng code",
    "code":  "Cùng đoạn code này, viết bằng công thức",
    "claim": "Cùng ý này, viết gọn thành công thức",
}
TWIN_LEAD = {
    "math":  "Công thức ở trên dịch sang code chạy được.",
    "code":  "Đoạn code ở trên viết lại thành công thức toán.",
    "claim": "Ý chính ở trên nén lại thành một dòng ký hiệu.",
}
ABLATE_WHAT = {
    "math": "từng mảnh của công thức", "code": "từng khối của đoạn code",
    "claim": "từng giả định của lập luận",
}

SLOTS = [
    ("job",      "Việc nó làm"),
    ("anatomy",  "Giải phẫu"),
    ("shapes",   "Truy vết kích thước"),
    ("ablation", "Bỏ đi thì sao"),
    ("trace",    "Chạy số thật"),
    ("picture",  "Hình dung"),
    ("twin",     "Viết bằng ngôn ngữ kia"),
    ("failures", "Khi nó hỏng"),
    ("probes",   "Tự kiểm tra"),
]

# ===========================================================================
# Dependency-free TeX -> HTML renderer (subset used by ML/DL study material)
# ===========================================================================
SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "ϑ",
    "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ",
    "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π",
    "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
    "cdot": "·", "times": "×", "div": "÷", "pm": "±", "mp": "∓",
    "leq": "≤", "geq": "≥", "neq": "≠", "approx": "≈", "equiv": "≡", "sim": "∼",
    "to": "→", "rightarrow": "→", "leftarrow": "←", "Rightarrow": "⇒",
    "Leftarrow": "⇐", "Leftrightarrow": "⇔", "leftrightarrow": "↔",
    "mapsto": "↦", "longrightarrow": "⟶",
    "partial": "∂", "nabla": "∇", "infty": "∞", "forall": "∀", "exists": "∃",
    "in": "∈", "notin": "∉", "subset": "⊂", "subseteq": "⊆", "cup": "∪",
    "cap": "∩", "emptyset": "∅", "mid": "∣", "ldots": "…", "dots": "…",
    "cdots": "⋯", "vdots": "⋮", "circ": "∘", "propto": "∝", "perp": "⊥",
    "quad": " ", "qquad": "  ", ",": " ", ";": " ",
    "!": "", " ": " ", "%": "%", "&": "&", "#": "#", "_": "_", "{": "{", "}": "}",
    "langle": "⟨", "rangle": "⟩", "star": "⋆", "ast": "∗", "prime": "′",
}
BIGOPS = {"sum": "∑", "prod": "∏", "int": "∫", "bigcup": "⋃", "bigcap": "⋂",
          "lim": "lim", "max": "max", "min": "min", "argmax": "arg max",
          "argmin": "arg min"}
FUNCS = {"log", "ln", "exp", "sin", "cos", "tan", "det", "dim", "deg", "gcd",
         "sup", "inf", "arg", "Pr", "softmax", "sigmoid", "relu"}
FONTS = {"mathbf": "mb", "mathbb": "bb", "mathcal": "cal", "mathrm": "rm",
         "mathit": "it", "boldsymbol": "mb", "mathsf": "sf", "text": "txt",
         "textbf": "txtb", "textit": "txti", "operatorname": "rm"}
ACCENTS = {"hat": "^", "bar": "‾", "tilde": "~", "vec": "→", "dot": "·"}


def _tokenize(s: str):
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            out.append(("cmd", m.group(1)))
            i += m.end()
        elif s.startswith(":=", i):
            out.append(("bin", "≔"))
            i += 2
        elif c in "{}_^":
            out.append(("ctl", c))
            i += 1
        elif c.isspace():
            i += 1
        elif c.isdigit():
            m = re.match(r"[0-9]+(\.[0-9]+)?", s[i:])
            out.append(("num", m.group(0)))
            i += m.end()
        elif c.isalpha():
            out.append(("var", c))
            i += 1
        else:
            out.append(("op", c))
            i += 1
    return out


class _P:
    """Recursive-descent parser -> HTML string. Small by design: it covers the
    formula subset that appears in ML/DL coursework, not all of TeX."""

    def __init__(self, toks, roles):
        self.t, self.i, self.roles = toks, 0, roles

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def next(self):
        tok = self.peek()
        self.i += 1
        return tok

    def group(self, stop_brace=False):
        parts = []
        while self.i < len(self.t):
            k, v = self.peek()
            if k == "ctl" and v == "}":
                if stop_brace:
                    self.next()
                    return "".join(parts)
                self.next()
                continue
            parts.append(self.atom_with_scripts())
        return "".join(parts)

    def arg(self):
        k, v = self.peek()
        if k == "ctl" and v == "{":
            self.next()
            return self.group(stop_brace=True)
        return self.atom()

    def atom_with_scripts(self):
        base = self.atom()
        sub = sup = None
        for _ in range(2):
            k, v = self.peek()
            if k == "ctl" and v == "_":
                self.next()
                sub = self.arg()
            elif k == "ctl" and v == "^":
                self.next()
                sup = self.arg()
            else:
                break
        if sub is None and sup is None:
            return base
        if sub is not None and sup is not None:
            return (f'<span class="sf-b">{base}</span>'
                    f'<span class="sf-ss"><span class="sf-u">{sup}</span>'
                    f'<span class="sf-l">{sub}</span></span>')
        if sup is not None:
            return f'{base}<sup class="sf-sup">{sup}</sup>'
        return f'{base}<sub class="sf-sub">{sub}</sub>'

    def _role_wrap(self, sym, rendered):
        role = self.roles.get(sym)
        if role:
            return f'<span class="sf-r sf-{role}" data-sym="{_html.escape(sym)}">{rendered}</span>'
        return rendered

    def atom(self):
        k, v = self.next()
        if k is None:
            return ""
        if k == "bin":
            return f'<span class="sf-bin">{v}</span>'
        if k == "num":
            return f'<span class="sf-num">{v}</span>'
        if k == "var":
            return self._role_wrap(v, f'<i class="sf-var">{v}</i>')
        if k == "op":
            if v in "()[]|":
                return f'<span class="sf-fence">{_html.escape(v)}</span>'
            if v in "+-=<>":
                ch = {"-": "−", "<": "&lt;", ">": "&gt;"}.get(v, v)
                return f'<span class="sf-bin">{ch}</span>'
            return f'<span class="sf-op">{_html.escape(v)}</span>'
        if k == "ctl":
            if v == "{":
                return f'<span class="sf-grp">{self.group(stop_brace=True)}</span>'
            return ""
        # --- commands ---
        if v == "frac" or v == "dfrac" or v == "tfrac":
            num, den = self.arg(), self.arg()
            return (f'<span class="sf-frac"><span class="sf-n">{num}</span>'
                    f'<span class="sf-d">{den}</span></span>')
        if v == "sqrt":
            return f'<span class="sf-sqrt">{self.arg()}</span>'
        if v in ACCENTS:
            inner = self.arg()
            return (f'<span class="sf-acc" data-a="{ACCENTS[v]}">{inner}'
                    f'<span class="sf-accm">{ACCENTS[v]}</span></span>')
        if v in FONTS:
            inner = self.arg()
            plain = re.sub(r"<[^>]+>", "", inner)
            return self._role_wrap(plain, f'<span class="sf-{FONTS[v]}">{inner}</span>')
        if v in BIGOPS:
            sub = sup = None
            for _ in range(2):
                k2, v2 = self.peek()
                if k2 == "ctl" and v2 == "_":
                    self.next()
                    sub = self.arg()
                elif k2 == "ctl" and v2 == "^":
                    self.next()
                    sup = self.arg()
                else:
                    break
            top = f'<span class="sf-lt">{sup}</span>' if sup else ""
            bot = f'<span class="sf-lb">{sub}</span>' if sub else ""
            return (f'<span class="sf-big">{top}'
                    f'<span class="sf-bigop">{BIGOPS[v]}</span>{bot}</span>')
        if v in FUNCS:
            return f'<span class="sf-fn">{v}</span>'
        if v in ("left", "right", "big", "Big", "bigg", "Bigg"):
            k2, v2 = self.peek()
            if k2 in ("op", "cmd"):
                self.next()
                ch = SYMBOLS.get(v2, v2)
                if ch == ".":
                    return ""
                return f'<span class="sf-fence sf-tall">{_html.escape(ch)}</span>'
            return ""
        if v in SYMBOLS:
            ch = SYMBOLS[v]
            return self._role_wrap(v, f'<span class="sf-sym">{_html.escape(ch)}</span>') if ch else ""
        if v == "\\":
            return '<span class="sf-br"></span>'
        return f'<span class="sf-unk">{_html.escape(v)}</span>'


def tex_html(expr: str, roles: dict) -> str:
    try:
        return _P(_tokenize(expr), roles).group()
    except Exception:                                    # never break the build
        return f'<code class="sf-raw">{_html.escape(expr)}</code>'


# ===========================================================================
# helpers
# ===========================================================================
def roles_of(card, spec):
    r = {}
    for n in spec.get("notation", []):
        if n.get("role"):
            r[n["sym"]] = n["role"]
    for l in card.get("legend", []):
        if l.get("role"):
            r[l["key"]] = l["role"]
    return r


def esc(s):
    return _html.escape(str(s), quote=False)


def tex_esc(s):
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    return s


def used_slots(card):
    return [k for k, _ in SLOTS if card.get(k if k != "anatomy" else
                                            ("expr" if card.get("expr") else "code"))]


# ===========================================================================
# Figures for the md / html targets.
#   plot -> matplotlib SVG   (tex uses pgfplots; same spec, two renderers)
#   flow -> Mermaid          (GitHub, VS Code and Artifacts all render it)
# ===========================================================================
MPL_CURVE = {"main":  ("#1D4ED8", "-", 2.1),
             "alt":   ("#B4442A", "--", 1.7),
             "ghost": ("#5A6878", ":", 1.5)}
MPL_POINT = {"min":  ("#B4442A", "o", 7),
             "step": ("#1D4ED8", "o", 6),
             "note": ("#1F6B45", "^", 7)}
_AXC = "#5A6878"          # readable on both light and dark grounds


def _tex_to_py(e: str) -> str:
    return e.replace("^", "**")


def plot_svg(p: dict) -> str | None:
    """Render a plot spec to a standalone SVG string. None if matplotlib is absent."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return None
    import io as _io

    fig, ax = plt.subplots(figsize=(6.4, 3.5), dpi=100)
    ns = {"np": np, "exp": np.exp, "log": np.log, "ln": np.log, "sqrt": np.sqrt,
          "sin": np.sin, "cos": np.cos, "tan": np.tan, "abs": np.abs, "pi": np.pi}
    x0 = float(p.get("xmin", -5))
    x1 = float(p.get("xmax", 5))

    for c in p.get("curves", []):
        d = c.get("domain")
        a, b = (float(v) for v in d.split(":")) if d else (x0, x1)
        xs = np.linspace(a, b, 400)
        try:
            ys = eval(_tex_to_py(c["expr"]), {"__builtins__": {}}, dict(ns, x=xs))
        except Exception:
            continue
        ys = np.broadcast_to(np.asarray(ys, dtype=float), xs.shape)
        col, ls, lw = MPL_CURVE.get(c.get("style", "main"), MPL_CURVE["main"])
        ax.plot(xs, ys, color=col, linestyle=ls, linewidth=lw,
                label=(f"${c['legend']}$" if c.get("legend") else None))

    for pt in p.get("points", []):
        col, mk, ms = MPL_POINT.get(pt.get("style", "step"), MPL_POINT["step"])
        ax.plot([pt["x"]], [pt["y"]], marker=mk, color=col, markersize=ms,
                linestyle="none", zorder=5)
        if pt.get("label"):
            ax.annotate(pt["label"], (pt["x"], pt["y"]),
                        textcoords="offset points",
                        xytext=(pt.get("dx", 6), pt.get("dy", 7)),
                        fontsize=8, color="#131A24",
                        bbox=dict(boxstyle="round,pad=0.18", fc="white",
                                  ec="none", alpha=0.8))

    for a_ in p.get("arrows", []):
        ax.annotate("", xy=tuple(a_["to"]), xytext=tuple(a_["from"]),
                    arrowprops=dict(arrowstyle="-|>", color="#B4442A", lw=1.6))
        if a_.get("label"):
            mx = (a_["from"][0] + a_["to"][0]) / 2
            my = (a_["from"][1] + a_["to"][1]) / 2
            ax.annotate(a_["label"], (mx, my), fontsize=8, color="#B4442A")

    if p.get("xmin") is not None or p.get("xmax") is not None:
        ax.set_xlim(p.get("xmin"), p.get("xmax"))
    if p.get("ymin") is not None or p.get("ymax") is not None:
        ax.set_ylim(p.get("ymin"), p.get("ymax"))
    if p.get("xlabel"):
        ax.set_xlabel(f"${p['xlabel']}$", color=_AXC, fontsize=10)
    if p.get("ylabel"):
        ax.set_ylabel(f"${p['ylabel']}$", color=_AXC, fontsize=10)
    ax.grid(True, color="#C7D0DD", linewidth=0.6, alpha=0.8)
    ax.tick_params(colors=_AXC, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(_AXC)
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    if any(c.get("legend") for c in p.get("curves", [])):
        lg = ax.legend(fontsize=8, framealpha=0.9)
        lg.get_frame().set_edgecolor("#C7D0DD")
    fig.tight_layout()

    buf = _io.StringIO()
    fig.savefig(buf, format="svg", transparent=True)
    plt.close(fig)
    svg = buf.getvalue()
    return svg[svg.index("<svg"):]                # strip XML decl + DOCTYPE


MERMAID_SHAPE = {"start": ("([", "])"), "proc": ("[", "]"),
                 "dec": ("{", "}"), "io": ("[/", "/]")}


def flow_mermaid(f: dict) -> str:
    head = "graph TD" if f.get("dir", "vertical") == "vertical" else "graph LR"
    out = [head]
    for n in f.get("nodes", []):
        o, c = MERMAID_SHAPE.get(n.get("type", "proc"), MERMAID_SHAPE["proc"])
        txt = str(n["text"]).replace('"', "'")
        out.append(f'  {n["id"]}{o}"{txt}"{c}')
    for e in f.get("edges", []):
        lab = f'|"{e["label"]}"|' if e.get("label") else ""
        out.append(f'  {e["from"]} -->{lab} {e["to"]}')
    return "\n".join(out)


# ===========================================================================
# MARKDOWN emitter  (dual-safe: VS Code/KaTeX + GitHub/MathJax)
# ===========================================================================
def emit_md(spec, out_dir=None) -> str:
    out_dir = Path(out_dir or ".")
    L = []
    A = L.append
    A(f"# {spec['title']}")
    if spec.get("subtitle"):
        A(f"\n> {spec['subtitle']}")
    meta = []
    if spec.get("source"):
        meta.append(f"nguồn: `{spec['source']}`")
    meta.append(f"{len(spec['cards'])} thẻ")
    A(f"\n<sub>{' · '.join(meta)}</sub>\n")

    A("## Cách đọc sổ tay\n")
    A("| Đường đọc | Đọc những mục | Dùng khi |")
    A("|---|---|---|")
    A("| **60 giây** | Việc nó làm → Giải phẫu → ô 08 viết bằng ngôn ngữ kia | ôn nhanh trước buổi học |")
    A("| **Hiểu sâu** | thêm Bỏ đi thì sao → Chạy số thật → Hình dung | học lần đầu |")
    A("| **Chốt kiến thức** | thêm Khi nó hỏng → Tự kiểm tra | trước khi thi / trước khi code |")
    A("\n> Mục **Tự kiểm tra** gập lại — hãy tự trả lời TRƯỚC khi bấm mở.\n")
    A("### Ba nhãn trong ô \"Bỏ đi thì sao\"\n")
    A("| Nhãn | Nghĩa |")
    A("|---|---|")
    for _k in ("breaks", "degrades", "subtle"):
        A(f"| **{SEVERITY[_k][0]}** | {SEVERITY_WHY[_k]} |")
    A("\n> Nhãn **SAI ÂM THẦM** đáng sợ hơn nhãn đỏ: lỗi đỏ thì máy báo, lỗi này chỉ có bạn tự phát hiện.\n")

    if spec.get("notation"):
        A("## Quy ước ký hiệu\n")
        A("| Ký hiệu | Đọc là | Nghĩa | Vai trò |")
        A("|---|---|---|---|")
        for n in spec["notation"]:
            role = ROLES.get(n.get("role", ""), ("—",))[0]
            A(f"| ${n['sym']}$ | {n.get('read','')} | {n.get('means','')} | {role} |")
        A("")

    if spec.get("dag"):
        A("## Bản đồ phụ thuộc\n")
        A("```mermaid")
        A("graph LR")
        titles = {c["id"]: c["title"] for c in spec["cards"]}
        for c in spec["cards"]:
            A(f'  {c["id"]}["{c["id"]} · {c["title"]}"]')
        for e in spec["dag"]:
            lab = f'|{e["label"]}|' if e.get("label") else ""
            A(f'  {e["from"]} -->{lab} {e["to"]}')
        A("```\n")
        del titles

    for c in spec["cards"]:
        A("\n---\n")
        tier = TIER_LABEL.get(c.get("tier", 1), "")
        A(f"## {c['id']} · {c['title']}")
        A(f"\n<sub>{tier}</sub>\n")

        A(f"**Việc nó làm.** {c['job']}\n")

        if c.get("expr"):
            A("\n$$")
            A(c["expr"])
            A("$$\n")
        if c.get("code"):
            A(f"```{c['code'].get('lang','')}")
            A(c["code"]["src"])
            A("```\n")
        if c.get("claim"):
            A(f"> **Ý chính.** {c['claim']}\n")

        if c.get("legend"):
            A("**Giải phẫu — từng mảnh làm gì**\n")
            A("| Mảnh | Vai trò | Nó làm gì |")
            A("|---|---|---|")
            for l in c["legend"]:
                role = ROLES.get(l.get("role", ""), ("—",))[0]
                A(f"| `{l['key']}` | {role} | {l.get('note','')} |")
            A("")

        if c.get("shapes"):
            A("**Truy vết kích thước**\n")
            A("| Phép | Vào | Ra | Ghi chú |")
            A("|---|---|---|---|")
            for s in c["shapes"]:
                A(f"| `{s['expr']}` | `{s.get('in','')}` | `{s.get('out','')}` | {s.get('note','')} |")
            A("")

        if c.get("ablation"):
            _what = ABLATE_WHAT[kind_of(c)]
            A(f"**Bỏ đi thì sao** — xoá hoặc vô hiệu hoá {_what}, rồi hỏi: hỏng cái gì?\n")
            A("| Bỏ đi | Mức | Hệ quả |")
            A("|---|---|---|")
            for a in c["ablation"]:
                sev = SEVERITY.get(a.get("severity", "subtle"), ("—",))[0]
                A(f"| `{a['remove']}` | **{sev}** | {a['effect']} |")
            A("")

        if c.get("trace"):
            t = c["trace"]
            A("**Chạy số thật**\n")
            A(f"*Cho:* {t.get('given','')}\n")
            A("| Bước | Giá trị |")
            A("|---|---|")
            for s in t.get("steps", []):
                A(f"| {s['step']} | `{s['value']}` |")
            A("")
            if t.get("result"):
                A(f"*Kết quả:* **{t['result']}**\n")

        if c.get("picture"):
            p = c["picture"]
            k = p.get("kind")
            A("**Hình dung**\n")
            if k == "plot":
                svg = plot_svg(p["plot"])
                if svg:
                    name = f"study-{spec['slug']}-{c['id']}.svg"
                    (out_dir / name).write_text(svg, encoding="utf-8")
                    A(f"![{p.get('caption','')}]({name})")
                else:
                    A("> *(cần matplotlib để dựng đồ thị — xem bản PDF)*")
            elif k == "flow":
                A("```mermaid")
                A(flow_mermaid(p["flow"]))
                A("```")
            elif k == "mermaid":
                A("```mermaid")
                A(p["src"])
                A("```")
            elif k == "ascii":
                A("```text")
                A(p["src"])
                A("```")
            else:
                A("```latex")
                A(p.get("src", ""))
                A("```")
            if p.get("caption"):
                A(f"\n<sub>{p['caption']}</sub>")
            A("")

        if c.get("twin"):
            t = c["twin"]
            _k = kind_of(c)
            A(f"**{TWIN_TITLE[_k]}**\n")
            A(TWIN_LEAD[_k] + " Bảng bên dưới nối từng ký hiệu với đúng tên biến.\n")
            A(f"```{t.get('lang','python')}")
            A(t["src"])
            A("```\n")
            if t.get("map"):
                A("| Ký hiệu trong công thức | Là biến này trong code |")
                A("|---|---|")
                for m in t["map"]:
                    A(f"| ${m['sym']}$ | `{m['var']}` |")
                A("")

        if c.get("failures"):
            A("**Khi nó hỏng**\n")
            A("| Triệu chứng bạn thấy | Nguyên nhân | Cách sửa |")
            A("|---|---|---|")
            for f in c["failures"]:
                A(f"| {f['symptom']} | {f['cause']} | {f['fix']} |")
            A("")

        if c.get("probes"):
            A("**Tự kiểm tra** — trả lời trước, mở sau\n")
            for i, p in enumerate(c["probes"], 1):
                A(f"<details>\n<summary><b>Hỏi {i}.</b> {p['q']}</summary>\n")
                A(f"\n{p['a']}\n")
                A("</details>\n")
    return "\n".join(L) + "\n"


# ===========================================================================
# LATEX emitter -- delegated to tex_emitter.py (pgfplots + TikZ + tcolorbox)
# ===========================================================================
from tex_emitter import emit_tex as _emit_tex_impl


def emit_tex(spec) -> str:
    return _emit_tex_impl(spec, ROLES, SEVERITY, TIER_LABEL, SEVERITY_WHY)


# ===========================================================================
# HTML emitter — fully self-contained, no external host, no JS dependency
# ===========================================================================
def _css() -> str:
    light = "\n".join(f"    --r-{k}: {v[1]};" for k, v in ROLES.items())
    dark = "\n".join(f"    --r-{k}: {v[2]};" for k, v in ROLES.items())
    slight = "\n".join(f"    --sev-{k}: {v[1]};" for k, v in SEVERITY.items())
    sdark = "\n".join(f"    --sev-{k}: {v[2]};" for k, v in SEVERITY.items())
    return f"""
:root {{
  --ink:#131A24; --ink-2:#5A6878; --paper:#EBEFF5; --card:#FFFFFF;
  --rule:#C7D0DD; --accent:#131A24; --cool:#44536A; --shadow:rgba(19,26,36,.10);
{light}
{slight}
  --disp:"IBM Plex Sans Condensed","IBM Plex Sans","Segoe UI Variable Display",
         "Segoe UI",Avenir,sans-serif;
  --body:"IBM Plex Serif","Source Serif 4",Cambria,"Palatino Linotype",Georgia,serif;
  --mono:"IBM Plex Mono","Cascadia Mono",Consolas,ui-monospace,monospace;
  --gut:138px;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --ink:#E4EAF2; --ink-2:#93A2B6; --paper:#0D1219; --card:#151C25;
    --rule:#293441; --accent:#E4EAF2; --cool:#93A2B6; --shadow:rgba(0,0,0,.45);
{dark}
{sdark}
  }}
}}
:root[data-theme="dark"] {{
  --ink:#E8EDF4; --ink-2:#A3B1C4; --paper:#10151D; --card:#171E28;
  --rule:#2B3644; --accent:#F0B357; --cool:#5FD0E6; --shadow:rgba(0,0,0,.4);
{dark}
{sdark}
}}
:root[data-theme="light"] {{
  --ink:#131A24; --ink-2:#5A6878; --paper:#EBEFF5; --card:#FFFFFF;
  --rule:#C7D0DD; --accent:#131A24; --cool:#44536A; --shadow:rgba(19,26,36,.10);
{light}
{slight}
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; padding:0; background:var(--paper); color:var(--ink);
  font-family:var(--body); font-size:17px; line-height:1.62;
  background-image:
    linear-gradient(var(--rule) 1px, transparent 1px),
    linear-gradient(90deg, var(--rule) 1px, transparent 1px);
  background-size:28px 28px, 28px 28px;
  background-attachment:fixed;
}}
body::before {{
  content:""; position:fixed; inset:0; pointer-events:none;
  background:radial-gradient(120% 80% at 50% 0%, transparent 30%, var(--paper) 92%);
}}
.wrap {{ position:relative; max-width:920px; margin:0 auto; padding:44px 20px 96px; }}
h1,h2,h3,.slot-h,.kicker {{ font-family:var(--disp); }}
h1 {{ font-size:clamp(2.1rem,6vw,3.5rem); font-weight:600; line-height:1.02;
     letter-spacing:-.032em; margin:0 0 .3em; text-wrap:balance; }}
.pill,.slot-h,th,.kicker {{ text-wrap:balance; }}
.sub {{ color:var(--ink-2); font-size:1.05rem; max-width:62ch; margin:0 0 1.4em; }}
.kicker {{ font-size:.72rem; font-weight:600; letter-spacing:.16em;
          text-transform:uppercase; color:var(--ink-2); }}
.meta {{ font-family:var(--mono); font-size:.74rem; color:var(--ink-2);
        letter-spacing:.04em; margin-bottom:2.4em; }}
.card {{ background:var(--card); border:1px solid var(--rule); border-top:2.5px solid var(--ink);
        margin:0 0 34px; box-shadow:0 1px 0 var(--shadow); }}
.card > header {{ display:grid; grid-template-columns:var(--gut) 1fr; gap:0 22px;
                 padding:18px 22px 16px; border-bottom:1px solid var(--rule); }}
.card > header > .gut {{ padding-top:.3em; }}
.card h2 {{ font-size:1.5rem; margin:0 0 .4em; letter-spacing:-.02em;
           text-wrap:balance; line-height:1.15; }}
.job {{ margin:0; color:var(--ink); max-width:62ch; }}
.slot {{ display:grid; grid-template-columns:var(--gut) 1fr; gap:0 22px;
        border-top:1px solid var(--rule); padding:15px 22px 17px; }}
.slot > .body {{ min-width:0; }}
.slot-h {{ font-size:.7rem; font-weight:600; letter-spacing:.1em;
          text-transform:uppercase; color:var(--ink-2); margin:0;
          padding-top:.25em; text-wrap:balance; }}
.slot-n {{ font-family:var(--mono); font-size:.62rem; color:var(--ink-2);
          opacity:.7; display:block; margin-bottom:2px; }}
table {{ border-collapse:collapse; width:100%; font-size:.9rem;
        font-variant-numeric:tabular-nums; }}
.scroll {{ overflow-x:auto; }}
th,td {{ text-align:left; padding:7px 10px; border-bottom:1px solid var(--rule);
        vertical-align:top; }}
th {{ font-family:var(--disp); font-size:.68rem; letter-spacing:.1em;
     text-transform:uppercase; color:var(--ink-2); font-weight:600;
     border-bottom:1.5px solid var(--rule); white-space:nowrap; }}
tr:last-child td {{ border-bottom:none; }}
code,pre,.mono {{ font-family:var(--mono); font-size:.85em; }}
pre {{ background:color-mix(in srgb, var(--rule) 28%, transparent);
      border:1px solid var(--rule); border-radius:4px; padding:12px 14px;
      overflow-x:auto; line-height:1.5; margin:0; }}
.eq {{ padding:20px 16px; overflow-x:auto;
      background:color-mix(in srgb, var(--rule) 20%, transparent);
      border:1px solid var(--rule); }}
.pill {{ display:inline-block; font-family:var(--mono); font-size:.68rem;
        font-weight:700; letter-spacing:.06em; padding:2px 7px; border-radius:3px;
        border:1px solid currentColor; white-space:nowrap; }}
.role-key {{ display:flex; flex-wrap:wrap; gap:6px 14px; margin:0 0 14px;
            font-family:var(--mono); font-size:.72rem; }}
.role-key span {{ display:inline-flex; align-items:center; gap:5px; }}
.role-key i {{ width:9px; height:9px; border-radius:2px; display:inline-block; }}
details {{ border:1px solid var(--ink); margin:0 0 10px; background:transparent; }}
summary {{ cursor:pointer; padding:10px 13px; font-weight:600; list-style:none;
          display:flex; gap:11px; align-items:baseline; }}
summary::-webkit-details-marker {{ display:none; }}
summary::before {{ content:""; width:9px; height:9px; background:var(--ink);
                  flex:none; transform:translateY(-1px); }}
details[open] summary::before {{ background:transparent;
                                box-shadow:inset 0 0 0 1.5px var(--ink); }}
details[open] summary {{ border-bottom:1px solid var(--rule); }}
details > div {{ padding:12px 13px 14px 33px; color:var(--ink-2); max-width:66ch; }}
.tracks {{ display:grid; gap:10px; grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
          margin:0 0 34px; }}
.track {{ border:1px solid var(--rule); border-top:2px solid var(--ink);
         padding:12px 15px 14px; background:var(--card); }}
.track b {{ font-family:var(--disp); display:block; font-size:.95rem; margin-bottom:3px; }}
.track span {{ font-size:.82rem; color:var(--ink-2); }}
.dagbox {{ background:var(--card); border:1px solid var(--rule);
          border-top:2px solid var(--ink); padding:15px 18px 17px; margin:0 0 30px; }}
.dagbox .slot-h {{ margin-bottom:10px; }}
.fig {{ margin:0; overflow-x:auto; }}
.claim {{ font-size:1.12rem; line-height:1.55; margin:0; max-width:60ch;
         border-left:3px solid var(--ink); padding-left:14px; }}
.fig svg {{ max-width:100%; height:auto; display:block; }}
a {{ color:var(--cool); }}
a:focus-visible, summary:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
hr.sep {{ border:none; border-top:1px solid var(--rule); margin:34px 0; }}
/* ---- formula rendering ---- */
.sf {{ font-family:var(--body); font-size:1.32rem; line-height:2.1;
      white-space:nowrap; display:inline-block; }}
.sf-var {{ font-style:italic; }}
.sf-num,.sf-fn,.sf-rm {{ font-style:normal; }}
.sf-fn {{ margin:0 .18em; }}
.sf-mb {{ font-weight:800; }}
.sf-cal {{ font-style:italic; font-family:Georgia,serif; }}
.sf-bb {{ font-weight:600; letter-spacing:-.04em; }}
.sf-bin {{ margin:0 .26em; }}
.sf-op,.sf-sym {{ margin:0 .1em; }}
.sf-fence {{ margin:0 .04em; }}
.sf-tall {{ font-size:1.25em; }}
.sf-sub,.sf-sup {{ font-size:.66em; }}
.sf-sub {{ vertical-align:-.28em; }}
.sf-sup {{ vertical-align:.52em; }}
.sf-b {{ display:inline-block; }}
.sf-ss {{ display:inline-flex; flex-direction:column; font-size:.62em;
         vertical-align:middle; line-height:1.05; text-align:left; }}
.sf-frac {{ display:inline-flex; flex-direction:column; vertical-align:middle;
           text-align:center; margin:0 .2em; font-size:.96em; }}
.sf-frac > .sf-n {{ padding:0 .35em .1em; border-bottom:1.4px solid currentColor; }}
.sf-frac > .sf-d {{ padding:.1em .35em 0; }}
.sf-big {{ display:inline-flex; flex-direction:column; align-items:center;
          vertical-align:middle; margin:0 .18em; line-height:1; }}
.sf-bigop {{ font-size:1.55em; font-style:normal; }}
.sf-lt,.sf-lb {{ font-size:.52em; line-height:1.3; }}
.sf-sqrt::before {{ content:"√"; }}
.sf-sqrt {{ border-top:1.2px solid currentColor; padding:0 .18em; }}
.sf-acc {{ position:relative; display:inline-block; }}
.sf-accm {{ position:absolute; top:-.62em; left:0; right:0; text-align:center;
           font-size:.8em; line-height:1; }}
.sf-r {{ font-weight:600; }}
{"".join(f'.sf-{k}{{color:var(--r-{k});}}' for k in ROLES)}
{"".join(f'.sev-{k}{{color:var(--sev-{k});}}' for k in SEVERITY)}
@media (prefers-reduced-motion: reduce) {{
  * {{ animation:none !important; transition:none !important; }}
}}
@media print {{
  body {{ background:#fff; }} body::before {{ display:none; }}
  .card {{ break-inside:avoid; box-shadow:none; }}
  details[open] > div, details > div {{ display:block; }}
  details {{ break-inside:avoid; }}
}}
@media (max-width:720px) {{
  :root {{ --gut:0px; }}
  .slot, .card > header {{ grid-template-columns:1fr; gap:8px; }}
  .slot-h {{ padding-top:0; border-bottom:1px solid var(--rule); padding-bottom:5px; }}
}}
@media (max-width:560px) {{
  body {{ font-size:16px; background-size:22px 22px, 22px 22px; }}
  .slot,.card > header {{ padding-left:14px; padding-right:14px; }}
  .eq {{ font-size:.86em; padding:14px 10px; }}
}}
"""


def kind_of(c) -> str:
    """math | code | claim — drives every card-type-dependent label."""
    if c.get("code"):
        return "code"
    if c.get("expr"):
        return "math"
    return "claim"


def _h_table(headers, rows, cls=""):
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def _slot(title, inner, num=None):
    n = f'<span class="slot-n">{num}</span>' if num else ""
    return (f'<section class="slot"><div class="gut">'
            f'<h3 class="slot-h">{n}{esc(title)}</h3></div>'
            f'<div class="body">{inner}</div></section>')


def emit_html(spec) -> str:
    P = []
    A = P.append
    A(f'<title>{esc(spec["title"])}</title>')
    A(f"<style>{_css()}</style>")
    A('<div class="wrap">')
    A(f'<p class="kicker">Sổ tay học tập · study-forge</p>')
    A(f'<h1>{esc(spec["title"])}</h1>')
    if spec.get("subtitle"):
        A(f'<p class="sub">{esc(spec["subtitle"])}</p>')
    m = []
    if spec.get("source"):
        m.append("nguồn: " + esc(spec["source"]))
    m.append(f'{len(spec["cards"])} thẻ')
    A(f'<p class="meta">{" · ".join(m)}</p>')

    A('<div class="tracks">')
    for b, s in [("60 giây", "Việc nó làm → Giải phẫu → ô 08 viết bằng ngôn ngữ kia"),
                 ("Hiểu sâu", "thêm Bỏ đi thì sao → Chạy số thật → Hình dung"),
                 ("Chốt kiến thức", "thêm Khi nó hỏng → Tự kiểm tra")]:
        A(f'<div class="track"><b>{esc(b)}</b><span>{esc(s)}</span></div>')
    A("</div>")

    A('<div class="dagbox"><h3 class="slot-h">Ba nhãn trong ô "Bỏ đi thì sao"</h3>')
    A(_h_table(["Nhãn", "Nghĩa"],
               [[f'<span class="pill sev-{k}">{SEVERITY[k][0]}</span>',
                 esc(SEVERITY_WHY[k])] for k in ("breaks", "degrades", "subtle")]))
    A('<p class="meta" style="margin:10px 0 0">Nhãn <b>SAI \u00c2M TH\u1ea6M</b> \u0111\u00e1ng s\u1ee3 h\u01a1n nh\u00e3n \u0111\u1ecf: '
      'l\u1ed7i \u0111\u1ecf th\u00ec m\u00e1y b\u00e1o, l\u1ed7i n\u00e0y ch\u1ec9 c\u00f3 b\u1ea1n t\u1ef1 ph\u00e1t hi\u1ec7n.</p></div>')
    A('<div class="role-key">')
    for k, (label, _l, _d) in ROLES.items():
        A(f'<span><i style="background:var(--r-{k})"></i>{esc(label)}</span>')
    A("</div>")

    if spec.get("notation"):
        rows = []
        for n in spec["notation"]:
            r = n.get("role", "index")
            rows.append([f'<span class="sf sf-r sf-{r}" style="font-size:1.05rem">'
                         f'{tex_html(n["sym"], {})}</span>',
                         esc(n.get("read", "")), esc(n.get("means", "")),
                         f'<span class="sf-{r}">{esc(ROLES.get(r,("—",))[0])}</span>'])
        A('<div class="dagbox"><h3 class="slot-h">Quy ước ký hiệu</h3>'
          + _h_table(["Ký hiệu", "Đọc là", "Nghĩa", "Vai trò"], rows) + "</div>")

    if spec.get("dag"):
        A('<div class="dagbox"><h3 class="slot-h">Bản đồ phụ thuộc</h3><pre class="mermaid">')
        A("graph LR")
        for c in spec["cards"]:
            A(f'  {c["id"]}["{c["id"]} · {c["title"]}"]')
        for e in spec["dag"]:
            lab = f'|{e["label"]}|' if e.get("label") else ""
            A(f'  {e["from"]} -->{lab} {e["to"]}')
        A("</pre></div>")

    for c in spec["cards"]:
        roles = roles_of(c, spec)
        A('<article class="card">')
        A("<header>")
        A(f'<div class="gut"><p class="kicker">{esc(c["id"])}<br>'
          f'{esc(TIER_LABEL.get(c.get("tier",1),""))}</p></div>')
        A(f'<div class="body"><h2>{esc(c["title"])}</h2>'
          f'<p class="job">{esc(c["job"])}</p></div>')
        A("</header>")

        if c.get("expr"):
            A(_slot("Công thức",
                    f'<div class="eq"><span class="sf">{tex_html(c["expr"], roles)}</span></div>',
                    "01"))
        if c.get("code"):
            A(_slot("Mã nguồn", f'<pre><code>{esc(c["code"]["src"])}</code></pre>', "01"))
        if c.get("claim"):
            A(_slot("Ý chính", f'<p class="claim">{esc(c["claim"])}</p>', "01"))

        if c.get("legend"):
            rows = []
            for l in c["legend"]:
                r = l.get("role", "index")
                rows.append([f'<span class="sf sf-{r}" style="font-size:1rem">{tex_html(l["key"], {})}</span>',
                             f'<span class="sf-{r}">{esc(ROLES.get(r,("—",))[0])}</span>',
                             esc(l.get("note", ""))])
            A(_slot("Giải phẫu — từng mảnh làm gì",
                    _h_table(["Mảnh", "Vai trò", "Nó làm gì"], rows), "02"))

        if c.get("shapes"):
            rows = [[f"<code>{esc(s['expr'])}</code>", f"<code>{esc(s.get('in',''))}</code>",
                     f"<code>{esc(s.get('out',''))}</code>", esc(s.get("note", ""))]
                    for s in c["shapes"]]
            A(_slot("Truy vết kích thước", _h_table(["Phép", "Vào", "Ra", "Ghi chú"], rows), "03"))

        if c.get("ablation"):
            rows = []
            for a in c["ablation"]:
                sv = a.get("severity", "subtle")
                rows.append([f"<code>{esc(a['remove'])}</code>",
                             f'<span class="pill sev-{sv}">{SEVERITY.get(sv,("—",))[0]}</span>',
                             esc(a["effect"])])
            A(_slot("Bỏ đi thì sao — xoá/đặt về 0 từng mảnh, rồi hỏi: hỏng cái gì?",
                    _h_table(["Bỏ đi", "Mức", "Hệ quả"], rows), "04"))

        if c.get("trace"):
            t = c["trace"]
            rows = [[esc(s["step"]), f"<code>{esc(s['value'])}</code>"] for s in t.get("steps", [])]
            inner = f'<p><i>Cho:</i> {esc(t.get("given",""))}</p>' + _h_table(["Bước", "Giá trị"], rows)
            if t.get("result"):
                inner += f'<p><i>Kết quả:</i> <b>{esc(t["result"])}</b></p>'
            A(_slot("Chạy số thật", inner, "05"))

        if c.get("picture"):
            p = c["picture"]
            k = p.get("kind")
            if k == "plot":
                svg = plot_svg(p["plot"])
                inner = (f'<figure class="fig">{svg}</figure>' if svg
                         else '<p class="meta">(cần matplotlib — xem bản PDF)</p>')
            elif k in ("flow", "mermaid"):
                src = flow_mermaid(p["flow"]) if k == "flow" else p["src"]
                inner = f'<pre class="mermaid">{esc(src)}</pre>'
            else:
                inner = f'<pre>{esc(p.get("src",""))}</pre>'
            if p.get("caption"):
                inner += f'<p class="meta" style="margin:8px 0 0">{esc(p["caption"])}</p>'
            A(_slot("Hình dung", inner, "06"))

        if c.get("twin"):
            t = c["twin"]
            _k = kind_of(c)
            lead = TWIN_LEAD[_k]
            inner = (f'<p class="meta" style="margin:-2px 0 10px">{esc(lead)} '
                     'Bảng bên dưới nối từng ký hiệu với đúng tên biến.</p>'
                     f'<pre><code>{esc(t["src"])}</code></pre>')
            if t.get("map"):
                rows = [[f'<span class="sf" style="font-size:1rem">'
                         f'{tex_html(m["sym"], roles)}</span>', f"<code>{esc(m['var'])}</code>"]
                        for m in t["map"]]
                inner += _h_table(["Ký hiệu trong công thức", "Là biến này trong code"], rows)
            A(_slot(TWIN_TITLE[_k], inner, "07"))

        if c.get("failures"):
            rows = [[esc(f["symptom"]), esc(f["cause"]), esc(f["fix"])] for f in c["failures"]]
            A(_slot("Khi nó hỏng", _h_table(["Triệu chứng bạn thấy", "Nguyên nhân", "Cách sửa"], rows), "08"))

        if c.get("probes"):
            inner = ['<p class="meta" style="margin:-4px 0 10px">Tự trả lời TRƯỚC khi mở.</p>']
            for i, p in enumerate(c["probes"], 1):
                inner.append(f"<details><summary><b>Hỏi {i}.</b>&nbsp;{esc(p['q'])}</summary>"
                             f"<div>{esc(p['a'])}</div></details>")
            A(_slot("Tự kiểm tra", "".join(inner), "09"))
        A("</article>")

    A("</div>")
    return "\n".join(P)


# ===========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--format", default="md", choices=["md", "tex", "html", "all"])
    ap.add_argument("--out-dir", default="notes")
    a = ap.parse_args()

    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    for req in ("slug", "title", "cards"):
        if req not in spec:
            sys.exit(f"spec thiếu trường bắt buộc: {req}")
    # The seven role SLOTS are universal (a thing you choose vs a thing given to
    # you vs an index), but their default NAMES are ML vocabulary. A handbook on
    # economics, law or biology renames them without touching the colour law.
    for _k, _lab in spec.get("role_labels", {}).items():
        if _k in ROLES:
            ROLES[_k] = (_lab, ROLES[_k][1], ROLES[_k][2])

    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    fmts = ["md", "tex", "html"] if a.format == "all" else [a.format]
    if spec.get("profile") == "argument":
        # The md/html emitters still assume the formula slot set. Refuse loudly
        # rather than write a half-rendered file.
        dropped = [f for f in fmts if f != "tex"]
        if dropped:
            print(f"  profile=argument: bỏ qua {', '.join(dropped)} "
                  f"(mới hỗ trợ tex/PDF)")
        fmts = ["tex"]
    written = []
    for f in fmts:
        p = out / f"study-{spec['slug']}.{f}"
        body = (emit_md(spec, out) if f == "md"
                else emit_tex(spec) if f == "tex" else emit_html(spec))
        p.write_text(body, encoding="utf-8")
        written.append(p)

    n = len(spec["cards"])
    if spec.get("profile") == "argument":
        ARG = ["provenance", "chain", "evidence", "assumptions", "rival",
               "falsify", "case", "picture", "scope", "probes"]
        filled = sum(len([k for k in ARG if c.get(k)]) for c in spec["cards"])
        print(f"OK — {n} thẻ · {filled}/{n * len(ARG)} ô đã điền")
    else:
        filled = sum(len([k for k, _ in SLOTS if c.get(k)]) for c in spec["cards"])
        print(f"OK — {n} thẻ · {filled}/{n * len(SLOTS)} ô đã điền")
    for p in written:
        print(f"  {p.resolve()}")

    # Iron Law #1: every card must force the reader to produce something.
    PROBE_MIN = 5
    thin = [(c["id"], len(c.get("probes", []))) for c in spec["cards"]
            if len(c.get("probes", [])) < PROBE_MIN]
    if thin:
        print(f"\n  CẢNH BÁO — ô 10 (Tự kiểm tra) cần >= {PROBE_MIN} câu:")
        for cid, k in thin:
            print(f"    {cid}: mới có {k} câu")
        print("  Ít câu hỏi => trang bị hụt và người học không đủ lần tự sản xuất.")


if __name__ == "__main__":
    main()
