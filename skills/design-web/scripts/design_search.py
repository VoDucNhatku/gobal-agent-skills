#!/usr/bin/env python3
"""design_search.py — query the design corpus (palettes / type-pairings / style-archetypes /
anti-slop-bans) and return the top-3 matching rows. Called by the `design-web` skill
(script-offloading / progressive disclosure): the heavy design knowledge lives in on-disk
pipe-delimited CSVs, NOT in the SKILL.md body, so deep coverage costs ~0 always-loaded tokens.
Only the top matches enter context per query.

Usage:
    python design_search.py "<keywords>" [--kind palette|type|archetype|bans] [--top 3]
    python design_search.py --add archetype "id|name|layout_grammar|type_logic|color_strategy|motion_language|fits|learned"
      (append a row learned in `learn` mode; appends to style-archetypes.csv)

Ranking: simple token-overlap score (BM25-ish: term frequency over the row, normalized by row
length, with a small bonus for matches in the name/mood columns). No external deps.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

REF = Path(__file__).resolve().parent.parent / "references"
FILES = {
    "palette": REF / "palettes.csv",
    "type": REF / "type-pairings.csv",
    "archetype": REF / "style-archetypes.csv",
    "bans": REF / "anti-slop-bans.csv",
}


def load(path: Path):
    if not path.exists():
        return [], []
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        return [], []
    header = lines[0].split("|")
    rows = [dict(zip(header, l.split("|"))) for l in lines[1:]]
    return header, rows


def tokenize(s: str):
    return re.findall(r"[a-z0-9#]+", (s or "").lower())


def score(query_terms, row: dict, weight_cols=("name", "mood", "vertical", "fits")):
    text = " ".join(str(v) for v in row.values())
    toks = tokenize(text)
    if not toks:
        return 0.0
    tf = {}
    for t in toks:
        tf[t] = tf.get(t, 0) + 1
    s = 0.0
    weight_text = " ".join(str(row.get(c, "")) for c in weight_cols).lower()
    for q in query_terms:
        if q in tf:
            s += (1 + math.log(tf[q])) / math.sqrt(len(toks))
        if q in weight_text:
            s += 0.6  # bonus for hitting a salient column
    return s


def search(kinds, query, top):
    qterms = tokenize(query)
    results = []
    for kind in kinds:
        header, rows = load(FILES[kind])
        for r in rows:
            sc = score(qterms, r)
            if sc > 0:
                results.append((sc, kind, r))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top]


def fmt(row: dict, cap=300):
    out = []
    for k, v in row.items():
        v = str(v)
        if len(v) > cap:
            v = v[:cap] + "…"
        out.append(f"  {k}: {v}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--kind", choices=list(FILES), default=None)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--add", nargs=2, metavar=("KIND", "ROW"),
                    help="append a pipe-delimited row to a CSV (learn mode)")
    args = ap.parse_args()

    if args.add:
        kind, row = args.add
        if kind not in FILES:
            sys.exit(f"[design_search] unknown kind {kind!r}")
        path = FILES[kind]
        with path.open("a", encoding="utf-8") as fh:
            fh.write(("" if path.read_text(encoding="utf-8").endswith("\n") else "\n") + row.strip() + "\n")
        print(f"[design_search] appended 1 row to {path.name}")
        return

    if not args.query:
        sys.exit("usage: design_search.py \"<keywords>\" [--kind ...] [--top N]")
    kinds = [args.kind] if args.kind else list(FILES)
    hits = search(kinds, args.query, args.top)
    if not hits:
        print("[design_search] no matching rows — broaden the query or check --kind")
        return
    for sc, kind, row in hits:
        print(f"# [{kind}] score={sc:.2f}")
        print(fmt(row))
        print()


if __name__ == "__main__":
    main()
