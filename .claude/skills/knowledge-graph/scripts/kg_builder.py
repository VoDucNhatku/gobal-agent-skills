#!/usr/bin/env python3
"""kg_builder.py — render a per-paper knowledge-graph note and merge it into the
cumulative master graph. Called by the `knowledge-graph` skill (script-offloading,
workbench-conventions §9): the skill emits a compact JSON spec, this script writes
every byte of the Markdown/Mermaid boilerplate and performs the merge.

Usage:
    python kg_builder.py .tmp/knowledge-graph_<id>.json [--notes-dir notes]

Spec schema (see references/kg-schema.md):
    {
      "paper_id": "003",
      "title": "...",
      "entities": [{"id": "e1", "type": "Method", "label": "Hyper-Ray sampling"}, ...],
      "triples":  [{"s": "e1", "r": "evaluated-on", "o": "e2"}, ...]
    }

Outputs:
    notes/<id>-kg.md            per-paper triples table + Mermaid graph
    notes/knowledge-graph.md    cumulative master graph (merged, de-duplicated)
    notes/knowledge-graph.json  machine-readable master state (drives the merge)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

# Windows consoles default to cp1252; force UTF-8 so Vietnamese labels in the
# JSON output never crash the process (UnicodeEncodeError).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ENTITY_TYPES = [
    "Method", "Model", "Dataset", "Metric", "Concept",
    "Task", "Problem", "Component", "PriorWork",
]
RELATION_TYPES = [
    "proposes", "addresses", "uses", "part-of", "based-on", "evaluated-on",
    "measured-by", "improves-over", "compared-with", "trained-on",
]
# Edge strength vocabulary (added 2026-07-20). Ordered weakest → strongest so
# max() during merge keeps the strongest evidence across papers.
STRENGTH_RANK = {"inferred": 1, "secondary": 2, "primary": 3}
DEFAULT_STRENGTH = "secondary"
# Distinct Mermaid classDef colours, one per entity type.
TYPE_COLOURS = {
    "Method": "#2563eb", "Model": "#7c3aed", "Dataset": "#059669",
    "Metric": "#d97706", "Concept": "#0891b2", "Task": "#dc2626",
    "Problem": "#db2777", "Component": "#65a30d", "PriorWork": "#6b7280",
}


def _norm(label: str) -> str:
    """Normalized node key fragment: lowercase, whitespace-collapsed."""
    return re.sub(r"\s+", " ", label.strip().lower())


def node_key(etype: str, label: str) -> str:
    return f"{etype}::{_norm(label)}"


def _sanitize_mermaid(text: str) -> str:
    """Strip characters that break Mermaid node labels."""
    return re.sub(r'["\(\)\[\]{};|]', " ", text).strip()


def load_spec(path: Path) -> dict:
    spec = json.loads(path.read_text(encoding="utf-8"))
    for key in ("paper_id", "entities", "triples"):
        if key not in spec:
            sys.exit(f"[kg_builder] spec missing required key: {key!r}")
    return spec


def validate(spec: dict) -> None:
    ids = {e["id"] for e in spec["entities"]}
    for e in spec["entities"]:
        if e.get("type") not in ENTITY_TYPES:
            sys.exit(f"[kg_builder] unknown entity type {e.get('type')!r} "
                     f"(allowed: {', '.join(ENTITY_TYPES)})")
    for t in spec["triples"]:
        if t.get("r") not in RELATION_TYPES:
            sys.exit(f"[kg_builder] unknown relation {t.get('r')!r} "
                     f"(allowed: {', '.join(RELATION_TYPES)})")
        if t.get("s") not in ids or t.get("o") not in ids:
            sys.exit(f"[kg_builder] triple references unknown entity id: {t}")
        if t.get("strength") and t["strength"] not in STRENGTH_RANK:
            sys.exit(f"[kg_builder] unknown strength {t.get('strength')!r} "
                     f"(allowed: {', '.join(STRENGTH_RANK)})")


def _strength(t: dict) -> str:
    """Default + normalize. Missing strength → DEFAULT_STRENGTH."""
    return t.get("strength") or DEFAULT_STRENGTH


def render_mermaid(entities_by_key: dict, edges: list[tuple]) -> str:
    """edges: list of (subj_key, relation, obj_key, [tags])."""
    lines = ["```mermaid", "flowchart LR"]
    # classDefs
    for etype, colour in TYPE_COLOURS.items():
        lines.append(f"  classDef {etype} fill:{colour},color:#fff,stroke:#0f172a;")
    # nodes (deterministic id = n<index>)
    keys = list(entities_by_key.keys())
    nid = {k: f"n{i}" for i, k in enumerate(keys)}
    for k in keys:
        ent = entities_by_key[k]
        label = _sanitize_mermaid(ent["label"])
        lines.append(f'  {nid[k]}["{label}"]:::{ent["type"]}')
    # edges
    seen = set()
    for s, r, o, tags in edges:
        if s not in nid or o not in nid:
            continue
        tagstr = " ".join(sorted(set(tags)))
        edge_label = f"{r} {tagstr}".strip()
        sig = (nid[s], r, nid[o])
        if sig in seen:
            continue
        seen.add(sig)
        lines.append(f"  {nid[s]} -->|{_sanitize_mermaid(edge_label)}| {nid[o]}")
    lines.append("```")
    return "\n".join(lines)


def write_per_paper(spec: dict, notes_dir: Path) -> Path:
    pid = spec["paper_id"]
    title = spec.get("title", "")
    today = _dt.date.today().isoformat()
    by_id = {e["id"]: e for e in spec["entities"]}
    entities_by_key = {}
    for e in spec["entities"]:
        entities_by_key.setdefault(node_key(e["type"], e["label"]), e)

    rows = []
    edges = []
    for t in spec["triples"]:
        s, o = by_id[t["s"]], by_id[t["o"]]
        strength = _strength(t)
        # Inferred edges get a visible tag on the relation text so downstream
        # consumers (paper-synthesize) can see them at a glance.
        r_display = f"{t['r']} (inferred)" if strength == "inferred" else t["r"]
        rows.append((s["label"], r_display, o["label"], strength))
        edges.append((node_key(s["type"], s["label"]), t["r"],
                      node_key(o["type"], o["label"]),
                      [f"[{pid}]", strength]))

    out = [
        f"# Knowledge graph — paper {pid}",
        "",
        f"- paper id: **{pid}**",
        f"- title: {title}",
        f"- worker: knowledge-graph",
        f"- date: {today}",
        "",
        f"## Triples ({len(rows)})",
        "",
        "| Subject | Relation | Object | Strength |",
        "|---------|----------|--------|----------|",
    ]
    out += [f"| {s} | {r} | {o} | {st} |" for s, r, o, st in rows]
    out += ["", "## Mermaid graph", "", render_mermaid(entities_by_key, edges), ""]
    path = notes_dir / f"{pid}-kg.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def merge_master(spec: dict, notes_dir: Path) -> tuple[Path, int, int]:
    """Merge this paper into notes/knowledge-graph.json + render .md. Returns
    (md_path, total_nodes, total_edges)."""
    state_path = notes_dir / "knowledge-graph.json"
    state = {"nodes": {}, "edges": {}}
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))

    pid = spec["paper_id"]
    by_id = {e["id"]: e for e in spec["entities"]}

    for e in spec["entities"]:
        k = node_key(e["type"], e["label"])
        node = state["nodes"].setdefault(k, {"type": e["type"], "label": e["label"], "papers": []})
        if pid not in node["papers"]:
            node["papers"].append(pid)

    for t in spec["triples"]:
        s, o = by_id[t["s"]], by_id[t["o"]]
        sk, ok = node_key(s["type"], s["label"]), node_key(o["type"], o["label"])
        ek = f"{sk}|{t['r']}|{ok}"
        strength = _strength(t)
        # First time we see this edge → seed with this triple's strength; later
        # papers can only UPGRADE it (primary > secondary > inferred).
        edge = state["edges"].setdefault(
            ek, {"s": sk, "r": t["r"], "o": ok, "papers": [], "strength": strength})
        if pid not in edge["papers"]:
            edge["papers"].append(pid)
        if STRENGTH_RANK[strength] > STRENGTH_RANK[edge["strength"]]:
            edge["strength"] = strength

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    # render master .md
    entities_by_key = {k: {"type": v["type"], "label": v["label"]}
                       for k, v in state["nodes"].items()}
    edges = [(v["s"], v["r"], v["o"],
              [f"[{p}]" for p in v["papers"]] + [v["strength"]])
             for v in state["edges"].values()]
    today = _dt.date.today().isoformat()
    out = [
        "# Knowledge graph — master (cumulative)",
        "",
        f"- worker: knowledge-graph (merge)",
        f"- updated: {today}",
        f"- papers merged: {sorted({p for v in state['nodes'].values() for p in v['papers']})}",
        f"- nodes: {len(state['nodes'])} · edges: {len(state['edges'])}",
        "",
        "## All triples (source ids + strength in brackets)",
        "",
        "| Subject | Relation | Object | Papers | Strength |",
        "|---------|----------|--------|--------|----------|",
    ]
    for v in state["edges"].values():
        sl = state["nodes"][v["s"]]["label"]
        ol = state["nodes"][v["o"]]["label"]
        papers = ' '.join('['+p+']' for p in v["papers"])
        r_display = f"{v['r']} (inferred)" if v["strength"] == "inferred" else v["r"]
        out.append(f"| {sl} | {r_display} | {ol} | {papers} | {v['strength']} |")
    out += ["", "## Mermaid master graph", "", render_mermaid(entities_by_key, edges), ""]
    md_path = notes_dir / "knowledge-graph.md"
    md_path.write_text("\n".join(out), encoding="utf-8")
    return md_path, len(state["nodes"]), len(state["edges"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path)
    ap.add_argument("--notes-dir", type=Path, default=Path("notes"))
    args = ap.parse_args()
    args.notes_dir.mkdir(parents=True, exist_ok=True)

    spec = load_spec(args.spec)
    validate(spec)
    per = write_per_paper(spec, args.notes_dir)
    master, nodes, edges = merge_master(spec, args.notes_dir)
    print(json.dumps({
        "per_paper": str(per),
        "master": str(master),
        "master_nodes": nodes,
        "master_edges": edges,
        "paper_entities": len(spec["entities"]),
        "paper_triples": len(spec["triples"]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
