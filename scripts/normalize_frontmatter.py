#!/usr/bin/env python3
"""Safely normalize scalar-only SKILL.md frontmatter.

The canonical manifests predate strict YAML validation, so this module first
extracts their one-field-per-line representation as text.  It deliberately
does not parse the complete, potentially invalid YAML document.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


class NormalizeError(ValueError):
    """Raised when legacy frontmatter cannot be normalized without guessing."""


FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]*(.*))?$")
INTEGER_RE = re.compile(
    r"^[+-]?(?:0|[1-9][0-9_]*|0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+)$"
)
FLOAT_RE = re.compile(
    r"^[+-]?(?:(?:[0-9][0-9_]*)?\.[0-9_]+(?:[eE][+-]?[0-9]+)?|"
    r"[0-9][0-9_]*\.(?:[eE][+-]?[0-9]+)?|"
    r"[0-9][0-9_]*[eE][+-]?[0-9]+|\.inf|\.nan)$",
    re.IGNORECASE,
)
BOOLEAN_VALUES = {"true", "false"}
NULL_VALUES = {"null", "~"}
CANONICAL_FIRST_KEYS = ("name", "description")
STRING_FIELDS = {"name", "description", "argument-hint", "allowed-tools", "args"}


def _split_legacy_frontmatter(text: str) -> tuple[list[str], str]:
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0].strip() != "---":
        raise NormalizeError("SKILL.md must start with a frontmatter delimiter")

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        raise NormalizeError("SKILL.md is missing the closing frontmatter delimiter")

    return lines[1:closing_index], "\n".join(lines[closing_index + 1 :])


def _decode_quoted_string(raw_value: str, key: str) -> str:
    quote = raw_value[0]
    if raw_value[-1:] != quote:
        raise NormalizeError(f"{key}: quoted scalar must end on the same line")
    try:
        scalars = [token for token in yaml.scan(raw_value) if isinstance(token, yaml.tokens.ScalarToken)]
        if len(scalars) != 1 or scalars[0].end_mark.index != len(raw_value):
            raise NormalizeError(f"{key}: quoted scalar must be the only value on the line")
        value = yaml.safe_load(raw_value)
    except yaml.YAMLError as exc:
        raise NormalizeError(f"{key}: invalid quoted scalar: {exc}") from exc
    if not isinstance(value, str):
        raise NormalizeError(f"{key}: quoted value must be a string")
    return value


def _render_value(key: str, raw_value: str) -> str:
    value = raw_value.strip()
    if not value:
        raise NormalizeError(f"{key}: empty values require explicit quotes or null")
    if value.startswith((">", "|")):
        raise NormalizeError(f"{key}: multiline block scalars are not supported")

    if value.startswith(("'", '"')):
        return json.dumps(
            _decode_quoted_string(value, key),
            ensure_ascii=False,
            separators=(",", ":"),
        )

    if re.search(r"(?:^|\s)#", value):
        raise NormalizeError(f"{key}: inline comments are ambiguous; quote the literal value")
    if value.startswith(("&", "*", "!")):
        raise NormalizeError(f"{key}: YAML anchors, aliases, and tags are not supported")

    # Legacy argument hints were intended as literal command syntax even when
    # YAML interpreted a bracket-only hint as a flow sequence.
    if key == "argument-hint":
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    if value.startswith(("[", "{")):
        raise NormalizeError(f"{key}: collection values are not supported")

    if key in STRING_FIELDS:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    lower_value = value.lower()
    if lower_value in BOOLEAN_VALUES:
        return lower_value
    if lower_value in NULL_VALUES:
        return "null"
    if INTEGER_RE.fullmatch(value) or FLOAT_RE.fullmatch(value):
        return value

    try:
        parsed = yaml.safe_load(value)
    except yaml.YAMLError as exc:
        raise NormalizeError(f"{key}: ambiguous legacy scalar; quote the literal value") from exc
    if not isinstance(parsed, str):
        raise NormalizeError(f"{key}: unsupported legacy scalar; quote the literal value")

    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def normalize_text(text: str) -> str:
    """Return deterministic UTF-8-ready text for one scalar-only SKILL.md."""
    frontmatter_lines, body = _split_legacy_frontmatter(text)
    fields: dict[str, str] = {}

    for line_number, line in enumerate(frontmatter_lines, start=2):
        if not line.strip():
            continue
        if line[:1].isspace():
            raise NormalizeError(
                f"line {line_number}: indented or multiline frontmatter is not supported"
            )
        match = FIELD_RE.fullmatch(line)
        if not match:
            raise NormalizeError(
                f"line {line_number}: expected one frontmatter field per line"
            )
        key, raw_value = match.groups()
        if key in fields:
            raise NormalizeError(f"duplicate frontmatter key: {key}")
        fields[key] = _render_value(key, raw_value or "")

    if not fields:
        raise NormalizeError("frontmatter must contain at least one field")

    ordered_keys = [key for key in CANONICAL_FIRST_KEYS if key in fields]
    ordered_keys.extend(sorted(key for key in fields if key not in ordered_keys))
    yaml_lines = [f"{key}: {fields[key]}" for key in ordered_keys]

    yaml_text = "\n".join(yaml_lines)
    return f"---\n{yaml_text}\n---\n{body}"


def _skill_paths(skills_root: Path) -> list[Path]:
    if not skills_root.is_dir():
        raise NormalizeError(f"skills root is not a directory: {skills_root}")
    paths = sorted(skills_root.rglob("SKILL.md"), key=lambda path: path.as_posix())
    if not paths:
        raise NormalizeError(f"no SKILL.md files found below: {skills_root}")
    return paths


def run(skills_root: Path, *, write: bool) -> int:
    changed: list[Path] = []
    pending: list[tuple[Path, bytes]] = []
    paths = _skill_paths(skills_root)
    for path in paths:
        source_bytes = path.read_bytes()
        source = source_bytes.decode("utf-8-sig")
        try:
            normalized = normalize_text(source)
        except NormalizeError as exc:
            raise NormalizeError(f"{path}: {exc}") from exc
        normalized_bytes = normalized.encode("utf-8")
        if normalized_bytes == source_bytes:
            continue
        changed.append(path)
        pending.append((path, normalized_bytes))

    if write:
        for path, normalized_bytes in pending:
            path.write_bytes(normalized_bytes)

    action = "normalized" if write else "would normalize"
    for path in changed:
        print(f"{action}: {path.relative_to(skills_root).as_posix()}")
    if not changed:
        print(f"{len(paths)} skill manifests already normalized")
    elif write:
        print(f"normalized {len(changed)} of {len(paths)} skill manifests")
    else:
        print(f"{len(changed)} of {len(paths)} skill manifests require normalization")
    return 0 if write or not changed else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize scalar-only canonical SKILL.md frontmatter safely."
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        required=True,
        help="Explicit root containing canonical skill directories.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Report drift without writing.")
    mode.add_argument("--write", action="store_true", help="Rewrite changed manifests.")
    args = parser.parse_args(argv)

    try:
        return run(args.skills_root, write=args.write)
    except (NormalizeError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
