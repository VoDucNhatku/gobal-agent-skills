"""Strict skill manifest parser bundled with the portable validator."""

from pathlib import Path
import re

import yaml


class ManifestError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ManifestError("YAML mapping keys must be strings")
        if key in mapping:
            raise ManifestError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ManifestError("SKILL.md must start with a YAML frontmatter delimiter")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    raise ManifestError("SKILL.md is missing the closing frontmatter delimiter")


def load_frontmatter(path: Path, canonical: bool = False, *, host: str | None = None) -> tuple[dict, str]:
    if host not in (None, "canonical", "antigravity"):
        raise ManifestError(f"unsupported manifest host: {host}")
    canonical = canonical if host is None else host == "canonical"
    frontmatter_text, body = split_frontmatter(path.read_text(encoding="utf-8-sig"))
    try:
        data = yaml.load(frontmatter_text, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, ManifestError) as exc:
        raise ManifestError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"{path}: frontmatter must be a mapping")
    if host == "antigravity":
        unexpected = data.keys() - {"name", "description"}
        if unexpected:
            raise ManifestError(f"{path}: unsupported antigravity keys: {', '.join(sorted(map(str, unexpected)))}")
    for required in ("name", "description"):
        if not isinstance(data.get(required), str) or not data[required].strip():
            raise ManifestError(f"{path}: {required} must be a non-empty string")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["name"]):
        raise ManifestError(f"{path}: name must be kebab-case: {data['name']}")
    if canonical:
        missing = {"argument-hint", "allowed-tools"} - data.keys()
        if missing:
            raise ManifestError(f"{path}: missing required keys: {', '.join(sorted(missing))}")
        for field in ("argument-hint", "allowed-tools"):
            if field in data and not isinstance(data[field], str):
                raise ManifestError(f"{path}: {field} must be a string")
    return data, body


def dump_skill(frontmatter: dict, body: str) -> str:
    ordered = {key: frontmatter[key] for key in ("name", "description") if key in frontmatter}
    for key in sorted(key for key in frontmatter if key not in ordered):
        ordered[key] = frontmatter[key]
    yaml_text = yaml.safe_dump(
        ordered,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n").lstrip("\n")
    return f"---\n{yaml_text}\n---\n\n{normalized_body.rstrip()}\n"
