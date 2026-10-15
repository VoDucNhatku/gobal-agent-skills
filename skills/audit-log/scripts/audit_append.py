#!/usr/bin/env python3
"""audit_append.py — append one material decision to notes/audit-log.md as a
markdown entry block, or print a summary, or archive+reset.

Usage:
    python audit_append.py <spec.json>   # append one entry
    python audit_append.py --summary     # counts by type + last 5 entries
    python audit_append.py --clear        # archive then reset

Log file: notes/audit-log.md (append-only, one ### block per entry).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import uuid
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

EVENT_TYPES = {"DESIGN", "TROUBLE", "VERIFY"}
REQUIRED = ("event_type", "decision", "why", "delta")


def _now_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="minutes")


def _today() -> str:
    return _dt.date.today().isoformat()


def _entry_id() -> str:
    return "ae_" + uuid.uuid4().hex[:7]


# ---------------------------------------------------------------------------
# Read / write helpers
# ---------------------------------------------------------------------------

def read_entries(log: Path) -> list[dict]:
    """Parse existing markdown entries back into dicts."""
    if not log.exists():
        return []
    entries: list[dict] = []
    lines = log.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("### ae_"):
            entry: dict = {}
            entry["header"] = line
            # Extract event_type from header: ### ae_xxx · timestamp · TYPE
            parts = line.split(" · ")
            if len(parts) >= 3:
                entry["event_type"] = parts[-1].strip()
            i += 1
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith("**Decision:**"):
                    entry["decision"] = l[len("**Decision:**"):].strip()
                elif l.startswith("**Why:**"):
                    entry["why"] = l[len("**Why:**"):].strip()
                elif l.startswith("**Delta:**"):
                    entry["delta"] = l[len("**Delta:**"):].strip()
                elif l.startswith("**Evidence:**"):
                    entry["evidence"] = l[len("**Evidence:**"):].strip()
                elif l.startswith("### "):
                    break
                i += 1
            entries.append(entry)
            continue
        i += 1
    return entries


def format_entry(entry: dict) -> str:
    """Build a markdown block for one entry."""
    eid = entry.get("entry_id", _entry_id())
    ts = entry.get("timestamp", _now_iso())
    etype = entry.get("event_type", "?")
    lines = [
        f"### {eid} · {ts} · {etype}",
        f"**Decision:** {entry.get('decision', '')}",
        f"**Why:** {entry.get('why', '')}",
        f"**Delta:** {entry.get('delta', '')}",
    ]
    ev = entry.get("evidence", "")
    if ev:
        lines.append(f"**Evidence:** {ev}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def append_entry(spec_path: Path, log: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    # Validate required fields
    for k in REQUIRED:
        if not spec.get(k):
            sys.exit(f"[audit] missing required field: {k!r}")
    if spec["event_type"] not in EVENT_TYPES:
        sys.exit(f"[audit] event_type {spec['event_type']!r} not allowed. "
                 f"Allowed: {', '.join(sorted(EVENT_TYPES))}")

    entry = {
        "entry_id": _entry_id(),
        "timestamp": _now_iso(),
        "event_type": spec["event_type"],
        "decision": spec["decision"],
        "why": spec["why"],
        "delta": spec["delta"],
        "evidence": spec.get("evidence", ""),
    }

    block = format_entry(entry)

    log.parent.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text("# AI Audit Log — Decision Moments\n\n", encoding="utf-8")

    with log.open("a", encoding="utf-8") as fh:
        fh.write(block + "\n\n")

    return entry


def summarize(log: Path) -> dict:
    entries = read_entries(log)
    counts: dict[str, int] = {}
    for e in entries:
        t = e.get("event_type", "?")
        counts[t] = counts.get(t, 0) + 1
    return {
        "total": len(entries),
        "by_type": counts,
        "last_5": entries[-5:] if entries else [],
    }


def clear(log: Path) -> dict:
    if not log.exists():
        return {"archived": None, "cleared": 0}
    archive = log.parent / f"audit-log-archive-{_today()}.md"
    archive.write_text(log.read_text(encoding="utf-8"), encoding="utf-8")
    log.write_text("# AI Audit Log — Decision Moments\n\n", encoding="utf-8")
    return {"archived": str(archive), "cleared": len(read_entries(archive))}


def main() -> None:
    ap = argparse.ArgumentParser(description="AI Audit Log — decision moment capture")
    ap.add_argument("spec", nargs="?", type=Path)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--clear", action="store_true")
    ap.add_argument("--log", type=Path, default=Path("notes/audit-log.md"))
    args = ap.parse_args()

    if args.summary:
        result = summarize(args.log)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.clear:
        result = clear(args.log)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not args.spec:
        sys.exit("usage: audit_append.py <spec.json> | --summary | --clear")

    entry = append_entry(args.spec, args.log)
    print(json.dumps({
        "appended": entry["entry_id"],
        "event_type": entry["event_type"],
        "log": str(args.log),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
