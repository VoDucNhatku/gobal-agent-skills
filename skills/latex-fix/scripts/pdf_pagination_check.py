#!/usr/bin/env python3
"""Pagination-budget checker for compiled papers (PyMuPDF).

Flags layout problems that prose-level edits can fix:
  - last_page_sparse:   last page fill < 15% (tighten prose / pull content back)
  - sparse_mid_page:    a non-final page fill < 50% (bad float placement or forced break)
  - orphan_heading:     a heading sitting in the bottom 12% of a page (its body starts overleaf)
  - widow_line:         a lone short line at the very top of a page (paragraph tail)

Usage:
    python pdf_pagination_check.py <paper.pdf> [--json]

Exit code 0 = no findings, 1 = findings present (so it can gate a verify loop).
All findings are heuristics on text-block geometry — confirm visually before editing.
"""

import sys
import json
import statistics

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed (pip install pymupdf)", file=sys.stderr)
    sys.exit(2)

# Fill ratios are relative to the document's TYPE AREA (estimated from block
# bboxes), not the raw page area — otherwise wide-margin classes (llncs) look
# uniformly "sparse" and the check is useless.
LAST_PAGE_MIN_FILL = 0.25
MID_PAGE_MIN_FILL = 0.60
HEADING_BOTTOM_ZONE = 0.88   # heading with y0 beyond this fraction = orphan
HEADING_SIZE_RATIO = 1.15    # span size >= ratio * body median size = heading candidate
WIDOW_MAX_CHARS = 65


def page_metrics(page):
    """Return (covered_area, blocks) where blocks carry text + bbox + span size."""
    raw = page.get_text("dict")
    blocks = []
    covered = 0.0
    for b in raw["blocks"]:
        if b.get("type") != 0:
            # image/drawing block still occupies layout space
            x0, y0, x1, y1 = b["bbox"]
            covered += max(0.0, (x1 - x0)) * max(0.0, (y1 - y0))
            continue
        text = " ".join(
            s["text"] for line in b["lines"] for s in line["spans"]).strip()
        if not text:
            continue
        sizes = [s["size"] for line in b["lines"] for s in line["spans"]]
        x0, y0, x1, y1 = b["bbox"]
        covered += (x1 - x0) * (y1 - y0)
        blocks.append({
            "text": text, "bbox": b["bbox"],
            "max_size": max(sizes), "n_lines": len(b["lines"]),
        })
    # Vector figures (TikZ/pgfplots) are invisible to get_text — count the
    # union bbox of all drawings so figure pages are not misread as sparse.
    drawings = page.get_drawings()
    if drawings:
        union = fitz.Rect()
        for d in drawings:
            union |= d["rect"]
        covered += union.get_area()
    return covered, blocks


def type_area(doc, per_page_blocks):
    """Estimate the document's type area from median per-page block extents."""
    ext = {"x0": [], "y0": [], "x1": [], "y1": []}
    for blocks in per_page_blocks:
        if not blocks:
            continue
        ext["x0"].append(min(b["bbox"][0] for b in blocks))
        ext["y0"].append(min(b["bbox"][1] for b in blocks))
        ext["x1"].append(max(b["bbox"][2] for b in blocks))
        ext["y1"].append(max(b["bbox"][3] for b in blocks))
    if not ext["x0"]:
        return doc[0].rect.width * doc[0].rect.height
    w = statistics.median(ext["x1"]) - statistics.median(ext["x0"])
    h = statistics.median(ext["y1"]) - statistics.median(ext["y0"])
    return max(1.0, w * h)


def body_font_size(all_blocks):
    sizes = []
    for blocks in all_blocks:
        for b in blocks:
            sizes.extend([b["max_size"]] * b["n_lines"])
    return statistics.median(sizes) if sizes else 10.0


def check(pdf_path):
    doc = fitz.open(pdf_path)
    covered_areas, per_page_blocks = [], []
    for page in doc:
        covered, blocks = page_metrics(page)
        covered_areas.append(covered)
        per_page_blocks.append(blocks)

    ta = type_area(doc, per_page_blocks)
    fills = [min(1.2, c / ta) for c in covered_areas]
    body_size = body_font_size(per_page_blocks)
    findings = []

    for i, (fill, blocks) in enumerate(zip(fills, per_page_blocks), start=1):
        ph = doc[i - 1].rect.height
        is_last = i == len(fills)

        if is_last and fill < LAST_PAGE_MIN_FILL and len(fills) > 1:
            findings.append({
                "type": "last_page_sparse", "page": i,
                "detail": f"fill {fill:.0%} < {LAST_PAGE_MIN_FILL:.0%}",
                "prose_fix": "tighten preceding sections or pull a paragraph back"})
        elif not is_last and fill < MID_PAGE_MIN_FILL:
            findings.append({
                "type": "sparse_mid_page", "page": i,
                "detail": f"fill {fill:.0%} < {MID_PAGE_MIN_FILL:.0%}",
                "prose_fix": "check float placement ([tb] options) / forced breaks"})

        for b in blocks:
            y0 = b["bbox"][1]
            is_heading = (b["max_size"] >= HEADING_SIZE_RATIO * body_size
                          and len(b["text"]) < 80 and b["n_lines"] <= 2)
            if is_heading and y0 / ph > HEADING_BOTTOM_ZONE and not is_last:
                findings.append({
                    "type": "orphan_heading", "page": i,
                    "detail": f"heading '{b['text'][:50]}' at {y0/ph:.0%} page height",
                    "prose_fix": "lengthen/shorten the paragraph above so the "
                                 "heading crosses the break naturally"})

        if blocks and not is_last:
            nxt = per_page_blocks[i] if i < len(per_page_blocks) else []
            if nxt:
                first = nxt[0]
                if (first["n_lines"] == 1 and len(first["text"]) < WIDOW_MAX_CHARS
                        and first["max_size"] < HEADING_SIZE_RATIO * body_size):
                    findings.append({
                        "type": "widow_line", "page": i + 1,
                        "detail": f"lone line at top: '{first['text'][:50]}'",
                        "prose_fix": "add/remove a few words in that paragraph "
                                     "so it does not break one line over"})

    return {
        "pdf": str(pdf_path), "pages": len(fills),
        "fill_per_page": [round(f, 2) for f in fills],
        "body_font_size": round(body_size, 1),
        "findings": findings,
    }


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    report = check(args[0])
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"{report['pdf']}: {report['pages']} pages, "
              f"body font ~{report['body_font_size']}pt")
        print("fill/page:", " ".join(f"{f:.0%}" for f in report["fill_per_page"]))
        if not report["findings"]:
            print("OK — no pagination findings")
        for f in report["findings"]:
            print(f"  [{f['type']}] p.{f['page']}: {f['detail']}"
                  f"\n      fix: {f['prose_fix']}")
    sys.exit(1 if report["findings"] else 0)
