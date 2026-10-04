#!/usr/bin/env python3
"""Validate ledger structure and review records, never semantic truth.

Developer tool: requires the repository's pinned PyYAML and bundled strict loader.
No source is fetched and no local source existence or model behavior is verified.
"""

import argparse
from datetime import date, datetime
from graphlib import CycleError, TopologicalSorter
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

import yaml

if __package__:
    from .skill_manifest import ManifestError, UniqueKeyLoader
else:
    from skill_manifest import ManifestError, UniqueKeyLoader


DISCLAIMER = (
    "Structural validation only: semantic entailment, logical validity, source truth, "
    "source existence/access and actual reviewer actions are not verified. "
    "No network or source-content checks were performed."
)
CLAIM_STATUSES = {"SUPPORTED", "REFUTED", "CONTESTED", "NEI"}
REVIEW_STATUSES = {"accepted", "pending"}
STANCES = {"support", "contradict"}


def _report(errors):
    return {"valid": not errors, "errors": errors,
            "semantic_verified": False, "disclaimer": DISCLAIMER}


def _nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _date_valid(value):
    if isinstance(value, (datetime, date)):
        return True
    if not _nonempty_string(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _source_identity_valid(value, source_type):
    if not _nonempty_string(value) or any(ord(c) < 32 for c in value):
        return False
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() in {"http", "https"}:
            return bool(parsed.hostname) and not any(c.isspace() for c in value) and (
                parsed.port is None or 0 < parsed.port < 65536
            )
        if source_type != "local_file":
            return False
        if parsed.scheme.lower() == "file":
            return bool(parsed.path) and PurePosixPath(parsed.path).is_absolute() and (
                not parsed.query and not parsed.fragment and not any(c.isspace() for c in value)
            )
        return PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute()
    except ValueError:
        return False


def validate_ledger(data):
    """Return a JSON-serializable report for deterministic provenance checks."""
    errors = []

    def fail(code, path, message):
        errors.append({"code": code, "path": path, "message": message})

    def required(record, keys, path):
        for key in keys:
            if key not in record:
                fail("missing_field", f"{path}.{key}", "Required field is missing")

    def string_fields(record, keys, path):
        for key in keys:
            if not _nonempty_string(record.get(key)):
                fail("invalid_type", f"{path}.{key}", "Expected a nonempty string")

    def records(key):
        value = data.get(key)
        if not isinstance(value, list):
            fail("invalid_type", key, "Expected a list")
            return []
        result = []
        for index, record in enumerate(value):
            path = f"{key}[{index}]"
            if not isinstance(record, dict):
                fail("invalid_type", path, "Expected a mapping")
            else:
                result.append((path, record))
        return result

    def string_list(record, key, path):
        value = record.get(key)
        if not isinstance(value, list) or any(not _nonempty_string(x) for x in value):
            fail("invalid_type", f"{path}.{key}", "Expected a list of nonempty strings")
            return []
        return value

    def check_review(value, path):
        start = len(errors)
        if not isinstance(value, dict):
            fail("invalid_review", path, "Expected a review mapping")
            return False
        required(value, ("method", "reviewer", "status", "reviewed_at"), path)
        string_fields(value, ("method", "reviewer"), path)
        status = value.get("status")
        if not isinstance(status, str) or status not in REVIEW_STATUSES:
            fail("invalid_review", f"{path}.status", "Expected accepted or pending")
        reviewed_at = value.get("reviewed_at")
        if not (status == "pending" and reviewed_at is None) and not _date_valid(reviewed_at):
            fail("invalid_date", f"{path}.reviewed_at", "Expected an ISO date/timestamp; pending may use null")
        return len(errors) == start and status == "accepted"

    if not isinstance(data, dict):
        fail("invalid_type", "$", "Ledger must be a mapping")
        return _report(errors)
    required(data, ("schema_version", "sources", "claims", "output"), "$")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        fail("invalid_schema_version", "schema_version", "Expected integer 1")
    source_records, claim_records, output_records = (records(key) for key in ("sources", "claims", "output"))
    if all(data.get(key) == [] for key in ("sources", "claims", "output")):
        fail("empty_ledger", "$", "An entirely empty ledger is not evidence validation")

    sources = {}
    for path, record in source_records:
        required(record, ("source_id", "canonical_url", "title", "origin_id", "source_type", "accessed_at"), path)
        string_fields(record, ("source_id", "canonical_url", "title", "origin_id", "source_type"), path)
        if not _source_identity_valid(record.get("canonical_url"), record.get("source_type")):
            fail("invalid_source_identity", f"{path}.canonical_url", "Expected http(s) URL, or absolute identity for local_file")
        if not _date_valid(record.get("accessed_at")):
            fail("invalid_date", f"{path}.accessed_at", "Expected an ISO date/timestamp")
        source_id = record.get("source_id")
        if _nonempty_string(source_id):
            if source_id in sources:
                fail("duplicate_id", f"{path}.source_id", f"Duplicate source ID: {source_id}")
            else:
                sources[source_id] = record

    claims = {}
    metadata = {}
    provenance = {}
    for path, record in claim_records:
        claim_start = len(errors)
        required(record, ("claim_id", "text_atomic", "status", "risk", "evidence", "derived_from_claim_ids",
                          "fatal_flags", "corroboration_required", "conflicts"), path)
        string_fields(record, ("claim_id", "text_atomic", "risk"), path)
        status = record.get("status")
        if not isinstance(status, str) or status not in CLAIM_STATUSES:
            fail("invalid_status", f"{path}.status", "Unknown claim status")
        parents = string_list(record, "derived_from_claim_ids", path)
        fatal_flags = string_list(record, "fatal_flags", path)
        if type(record.get("corroboration_required")) is not bool:
            fail("invalid_type", f"{path}.corroboration_required", "Expected a boolean")
        conflicts = record.get("conflicts")
        unresolved_conflict = False
        if not isinstance(conflicts, list):
            fail("invalid_type", f"{path}.conflicts", "Expected a list")
            conflicts = []
        for index, conflict in enumerate(conflicts):
            conflict_path = f"{path}.conflicts[{index}]"
            if _nonempty_string(conflict):
                unresolved_conflict = True
            elif isinstance(conflict, dict) and _nonempty_string(conflict.get("reason")):
                if "resolution" in conflict and not isinstance(conflict["resolution"], str):
                    fail("invalid_conflict", conflict_path, "Resolution must be a string when provided")
                unresolved_conflict |= not _nonempty_string(conflict.get("resolution"))
            else:
                fail("invalid_conflict", conflict_path, "Expected a reason string or a mapping with nonempty reason")
        evidence = record.get("evidence")
        if not isinstance(evidence, list):
            fail("invalid_type", f"{path}.evidence", "Expected a list")
            evidence = []
        accepted = {"support": set(), "contradict": set()}
        recorded_sources = set()
        for index, item in enumerate(evidence):
            edge_path = f"{path}.evidence[{index}]"
            start = len(errors)
            if not isinstance(item, dict):
                fail("invalid_type", edge_path, "Expected an evidence mapping")
                continue
            required(item, ("source_id", "locator", "passage", "stance", "review"), edge_path)
            string_fields(item, ("source_id", "locator", "passage"), edge_path)
            stance = item.get("stance")
            if not isinstance(stance, str) or stance not in STANCES:
                fail("invalid_stance", f"{edge_path}.stance", "Expected support or contradict")
            source_id = item.get("source_id")
            if _nonempty_string(source_id):
                if source_id not in sources:
                    fail("unknown_source", f"{edge_path}.source_id", f"Source does not exist: {source_id}")
                else:
                    recorded_sources.add(source_id)
            reviewed = check_review(item.get("review"), f"{edge_path}.review")
            if len(errors) == start and reviewed:
                accepted[stance].add(source_id)
        claim_id = record.get("claim_id")
        if _nonempty_string(claim_id):
            if claim_id in claims:
                fail("duplicate_id", f"{path}.claim_id", f"Duplicate claim ID: {claim_id}")
            else:
                claims[claim_id] = record
                provenance[claim_id] = recorded_sources
                metadata[claim_id] = {
                    "path": path, "parents": parents, "accepted": accepted,
                    "fatal_flags": fatal_flags, "conflicts": conflicts,
                    "unresolved_conflict": unresolved_conflict,
                    "fields_valid": len(errors) == claim_start,
                }

    graph = {}
    for claim_id, record in claims.items():
        info = metadata[claim_id]
        graph[claim_id] = []
        for parent in info["parents"]:
            if parent == claim_id:
                fail("self_dependency", f"{info['path']}.derived_from_claim_ids", "A claim cannot depend on itself")
            if parent not in claims:
                fail("unknown_derivation", f"{info['path']}.derived_from_claim_ids", f"Parent does not exist: {parent}")
            else:
                graph[claim_id].append(parent)
                if claims[parent].get("status") != "SUPPORTED":
                    fail("unsupported_dependency", f"{info['path']}.derived_from_claim_ids", f"Parent is not SUPPORTED: {parent}")
    try:
        # Parents precede children, so provenance propagation never uses recursion.
        # O(V+E) graph work, plus source-set unions (worst O((V+E)*S)).
        order = list(TopologicalSorter(graph).static_order())
    except CycleError as exc:
        fail("cyclic_derivation", "claims", f"Derivation graph is cyclic: {exc.args[1]}")
        order = list(claims)  # Keep checking records; the graph can no longer pass.

    valid_supported = {}
    for claim_id in order:
        record = claims[claim_id]
        info = metadata[claim_id]
        path = info["path"]
        start = len(errors)
        accepted = info["accepted"]
        parents = info["parents"]
        raw_status = record.get("status")
        status = raw_status if isinstance(raw_status, str) else None
        parents_valid = bool(parents) and all(valid_supported.get(parent, False) for parent in parents)
        inherited_support = set()
        for parent in parents:
            if valid_supported.get(parent, False):
                inherited_support.update(metadata[parent]["accepted"]["support"])
                provenance[claim_id].update(metadata[parent]["accepted"]["support"])
        needs_derivation = bool(parents) and not accepted["support"] and status in {"SUPPORTED", "CONTESTED"}
        derivation_accepted = False
        if needs_derivation or "derivation_review" in record:
            if not _nonempty_string(record.get("derivation_rationale")):
                fail("invalid_derivation", f"{path}.derivation_rationale", "A logical review needs a nonempty derivation rationale")
            if "derivation_review" not in record:
                fail("invalid_derivation", f"{path}.derivation_review", "A deduction needs a separate logical review record")
            derivation_accepted = check_review(record.get("derivation_review"), f"{path}.derivation_review")
        if needs_derivation and parents_valid and derivation_accepted and _nonempty_string(record.get("derivation_rationale")):
            accepted["support"].update(inherited_support)
        if status in {"SUPPORTED", "CONTESTED"} and not accepted["support"]:
            fail("unsupported_status", f"{path}.status", "Status requires accepted support or a reviewed supported deduction with source provenance")
        if status in {"REFUTED", "CONTESTED"} and not accepted["contradict"]:
            fail("unsupported_status", f"{path}.status", "Status requires accepted contradiction")
        both_stances = bool(accepted["support"] and accepted["contradict"])
        if (both_stances and status != "CONTESTED") or (
            status == "SUPPORTED" and accepted["contradict"]
        ) or (status == "REFUTED" and accepted["support"]):
            fail("status_conflict", f"{path}.status", "Accepted opposing evidence cannot be silently ignored")
        if status == "CONTESTED" and not info["conflicts"]:
            fail("missing_conflict", f"{path}.conflicts", "CONTESTED must preserve a conflict record")
        if status in {"SUPPORTED", "REFUTED"} and info["unresolved_conflict"]:
            fail("unresolved_conflict", f"{path}.conflicts", "Unresolved credible conflict blocks a settled status")
        if status == "SUPPORTED" and info["fatal_flags"]:
            fail("fatal_supported", f"{path}.fatal_flags", "Fatal flags block SUPPORTED")
        if record.get("corroboration_required") is True:
            relevant = {"SUPPORTED": ("support",), "REFUTED": ("contradict",),
                        "CONTESTED": ("support", "contradict")}.get(status, ()) if isinstance(status, str) else ()
            for stance in relevant:
                origins = {sources[source_id]["origin_id"] for source_id in accepted[stance]
                           if _nonempty_string(sources[source_id].get("origin_id"))}
                if len(origins) < 2:
                    fail("insufficient_origins", f"{path}.corroboration_required", f"{stance} requires at least two independent origin IDs")
        if parents and not parents_valid and status == "SUPPORTED":
            fail("unsupported_dependency", f"{path}.derived_from_claim_ids", "Every deduction parent must be structurally SUPPORTED")
        valid_supported[claim_id] = status == "SUPPORTED" and info["fields_valid"] and len(errors) == start

    statement_ids = set()
    for path, record in output_records:
        required(record, ("statement_id", "claim_ids", "cited_source_ids"), path)
        string_fields(record, ("statement_id",), path)
        statement_id = record.get("statement_id")
        if _nonempty_string(statement_id):
            if statement_id in statement_ids:
                fail("duplicate_id", f"{path}.statement_id", f"Duplicate statement ID: {statement_id}")
            statement_ids.add(statement_id)
        claim_ids = string_list(record, "claim_ids", path)
        cited_sources = string_list(record, "cited_source_ids", path)
        allowed = set()
        for claim_id in claim_ids:
            if claim_id not in claims:
                fail("unknown_claim", f"{path}.claim_ids", f"Claim does not exist: {claim_id}")
            else:
                allowed.update(provenance.get(claim_id, set()))
        for source_id in cited_sources:
            if source_id not in sources:
                fail("unknown_source", f"{path}.cited_source_ids", f"Source does not exist: {source_id}")
            elif source_id not in allowed:
                fail("unrelated_citation", f"{path}.cited_source_ids", f"Source is not on a mapped claim: {source_id}")
        for claim_id in claim_ids:
            if claim_id not in claims:
                continue
            status = claims[claim_id].get("status")
            relevant = {"SUPPORTED": ("support",), "REFUTED": ("contradict",),
                        "CONTESTED": ("support", "contradict")}.get(status, ()) if isinstance(status, str) else ()
            for stance in relevant:
                if not metadata[claim_id]["accepted"][stance].intersection(cited_sources):
                    fail("missing_citation", f"{path}.cited_source_ids", f"Mapped claim {claim_id} needs a citation for {stance}")
    return _report(errors)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="YAML ledger path")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report")
    args = parser.parse_args(argv)
    try:
        data = yaml.load(args.path.read_text(encoding="utf-8-sig"), Loader=UniqueKeyLoader)
        report = validate_ledger(data)
    except (OSError, UnicodeError, yaml.YAMLError, ManifestError, ValueError, TypeError, RecursionError) as exc:
        report = _report([{"code": "invalid_input", "path": str(args.path), "message": str(exc)}])
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("VALID (structure only)" if report["valid"] else "INVALID")
        for error in report["errors"]:
            print(f"{error['code']}: {error['path']}: {error['message']}")
        print(report["disclaimer"])
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
