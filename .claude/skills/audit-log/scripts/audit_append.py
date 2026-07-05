#!/usr/bin/env python3
"""audit_append.py — append one material decision to notes/audit-log.md as a JSON
line, or print a summary, or archive+reset. Called by the `audit-log` skill
(script-offloading, workbench-conventions §9): the skill emits a decision spec and
this script auto-stamps timestamp / entry_id / session, validates the event type,
and writes the line. Timestamp/entry-id generation lives here so the model never
hand-writes them.

Usage:
    python audit_append.py /tmp/audit-log_entry.json   # append one entry
    python audit_append.py --summary                   # counts + last 10 (no write)
    python audit_append.py --clear                      # archive then reset

Log file: notes/audit-log.md (one JSON object per line).
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

EVENT_TYPES = {"scope-decision", "synthesis-framing", "cross-source-assumption"}
REQUIRED = ("actor", "event_type", "decision", "rationale")


def _now_iso() -> str:
    # NOTE: real wall-clock — these scripts run on the user's machine, not in a
    # workflow journal, so datetime is fine here.
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _today() -> str:
    return _dt.date.today().isoformat()


def read_entries(log: Path) -> list[dict]:
    if not log.exists():
        return []
    out = []
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def append_entry(spec_path: Path, log: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    for k in REQUIRED:
        if not spec.get(k):
            sys.exit(f"[audit_append] missing required field: {k!r}")
    if spec["event_type"] not in EVENT_TYPES:
        sys.exit(f"[audit_append] event_type {spec['event_type']!r} fails the materiality "
                 f"filter. Allowed: {', '.join(sorted(EVENT_TYPES))}. Refusing to log.")
    entry = {
        "entry_id": "ae_" + uuid.uuid4().hex[:10],
        "timestamp": _now_iso(),
        "session": _today(),
        "actor": spec["actor"],
        "event_type": spec["event_type"],
        "target": spec.get("target", ""),
        "decision": spec["decision"],
        "rationale": spec["rationale"],
        "alternatives_considered": spec.get("alternatives_considered", ""),
        "artifacts": spec.get("artifacts", []),
    }
    log.parent.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text("# Audit log — append-only material decisions (JSON lines)\n",
                       encoding="utf-8")
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def summarize(log: Path) -> dict:
    entries = read_entries(log)
    counts: dict[str, int] = {}
    for e in entries:
        counts[e.get("event_type", "?")] = counts.get(e.get("event_type", "?"), 0) + 1
    return {"total": len(entries), "by_type": counts, "last": entries[-10:]}


def clear(log: Path) -> dict:
    entries = read_entries(log)
    if not log.exists():
        return {"archived": None, "cleared": 0}
    archive = log.parent / f"audit-log-archive-{_today()}.md"
    archive.write_text(log.read_text(encoding="utf-8"), encoding="utf-8")
    log.write_text("# Audit log — append-only material decisions (JSON lines)\n",
                   encoding="utf-8")
    return {"archived": str(archive), "cleared": len(entries)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="?", type=Path)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--clear", action="store_true")
    ap.add_argument("--log", type=Path, default=Path("notes/audit-log.md"))
    args = ap.parse_args()

    if args.summary:
        print(json.dumps(summarize(args.log), ensure_ascii=False))
        return
    if args.clear:
        print(json.dumps(clear(args.log), ensure_ascii=False))
        return
    if not args.spec:
        sys.exit("usage: audit_append.py <spec.json> | --summary | --clear")
    entry = append_entry(args.spec, args.log)
    print(json.dumps({"appended": entry["entry_id"], "event_type": entry["event_type"],
                      "log": str(args.log)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
