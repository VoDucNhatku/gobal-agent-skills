#!/usr/bin/env python3
"""Build the deterministic Antigravity distribution from canonical skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import stat
import sys
from pathlib import Path

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.skill_manifest import ManifestError, load_frontmatter


class BuildError(ValueError):
    """A distribution cannot be built without guessing or losing user files."""


TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".json", ".yml", ".yaml", ".csv", ".tsv",
    ".ps1", ".sh", ".toml", ".tex", ".js", ".ts", ".css", ".html",
    ".svg", ".ipynb", ".gitignore", ".gitattributes",
}
HOME_PATH = re.compile(r"~[/\\]\.claude[^\s`\"'<>()[\]{};,]*")
SKILLS_PLACEHOLDER = re.compile(r"<skills>(?:/[A-Za-z0-9_.-]+)*")
RESOURCE_ROOTS = {"scripts", "references", "assets", "templates", "resources"}
INLINE_PATH = re.compile(r"`([^`\n]+)`|\[[^\]\n]*\]\(([^)\n]+)\)")
PLUGIN = {
    "$schema": "https://antigravity.google/schemas/v1/plugin.json",
    "name": "gobal-agent-skills",
    "description": "Evidence-grounded GOBAL AGENT skills for Antigravity IDE.",
}
PILOT_NAME = "admin-evidence-pilot"
PILOT_BASE = f"pilot/skills/{PILOT_NAME}"
RESOURCE_EXECUTION = (
    "\n\n## Antigravity resource execution\n"
    "Resolve relative skill/resource paths against the containing loaded file's observed location.\n"
    "Before invoking a bundled command from the project working directory, resolve its entrypoint\n"
    "to an absolute quoted path; resolve bundled imports/resources from their own containing file.\n"
    "Do not change the working directory into the installed skill. Inputs and outputs such as\n"
    "`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.\n"
    "Do not invent the installed location; if the host does not expose it, discover the actual file\n"
    "using available file capabilities or ask for its location before running the command.\n"
)
PILOT_MARKER = (
    "\n\n## Temporary pilot canary\n"
    "When this skill is explicitly invoked, include `Protocol: AG-EF-PILOT-1` in the response.\n"
    "The marker is instruction-following evidence only; discovery and activation need an activity trace.\n"
)
RULE_MARKER = (
    "\n\nWhile this temporary global rule is active, include `Rule Canary: AG-EF-RULE-1`\n"
    "in the first response. It affects all chats while installed; remove it after the bounded canary.\n"
)


def _is_text_resource(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.lower() in TEXT_SUFFIXES


def _copy_bytes(path: Path) -> bytes:
    content = path.read_bytes()
    if _is_text_resource(path):
        text = content.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        return text.encode("utf-8")
    return content


def _manifest(data: dict, body: str) -> bytes:
    _reject_metadata_home({key: data[key] for key in ("name", "description")})
    header = "\n".join(
        f"{key}: {json.dumps(data[key], ensure_ascii=False)}"
        for key in ("name", "description")
    )
    return f"---\n{header}\n---\n{body}".encode("utf-8")


def _relative(target: str, output: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(output))


def _rewrite_paths(text: str, output: str, root: Path, names: list[str], compatibility: dict, *, pilot: bool = False, rule: bool = False) -> str:
    paths = compatibility["paths"]
    rules_target = f"{PILOT_BASE}/references/shared-rules" if pilot else paths["generated_rules"]

    def target_path(value: str) -> str:
        value = value.replace("\\", "/").rstrip("/")
        rules_prefix = paths["canonical_rules"]
        skills_prefix = paths["canonical_skills"]
        if value == rules_prefix:
            return _relative(rules_target, output)
        if value.startswith(rules_prefix + "/"):
            name = value[len(rules_prefix) + 1:]
            if name not in compatibility["rules"] or not (root / ".claude/rules" / name).is_file():
                raise BuildError(f"{output}: unsupported or missing rule: {value}")
            return _relative(f"{rules_target}/{name}", output)
        if value.startswith(skills_prefix + "/"):
            suffix = value[len(skills_prefix) + 1:]
            parts = suffix.split("/")
            if len(parts) < 2 or parts[0] not in names or ".." in parts:
                raise BuildError(f"{output}: unsupported skill resource: {value}")
            if not (root / ".claude/skills" / suffix).exists():
                raise BuildError(f"{output}: missing skill resource: {value}")
            if pilot:
                if parts[0] != "admin":
                    raise BuildError(f"{output}: pilot would depend on an uninstalled peer resource: {value}")
                destination = f'{PILOT_BASE}/{"/".join(parts[1:])}'
            else:
                destination = f'{paths["generated_skills"]}/{suffix}'
            return _relative(destination, output)
        raise BuildError(f"{output}: unsupported canonical path: {value}")

    def home(match):
        raw = match.group()
        value = raw.rstrip(".")
        return target_path(value) + raw[len(value):]

    def placeholder(match):
        value = match.group()
        if value in compatibility.get("literal_path_examples", []) or value == "<skills>":
            return value.replace("<skills>", paths["documented_global_skills"])
        return target_path(value.replace("<skills>", paths["canonical_skills"]))

    if output.endswith(".md"):
        output_parts = output.split("/")
        if not rule and (output_parts[0] == "skills" or pilot):
            skill = "admin" if pilot else output_parts[1]
            relative_file = output.removeprefix(PILOT_BASE + "/") if pilot else "/".join(output_parts[2:])
            source_parent = posixpath.dirname(f"{skill}/{relative_file}")
            literal_examples = compatibility.get("literal_resource_examples", {}).get(f"{skill}/{relative_file}", [])

            def resource(match):
                value = match[1] or match[2]
                if value in literal_examples or value in {f"{directory}/" for directory in RESOURCE_ROOTS} or re.search(r"[\s*?\[\]{}<>]", value):
                    return match[0]
                parts = value.split("/")
                if parts[0] in RESOURCE_ROOTS:
                    suffix = f"{skill}/{value}"
                elif parts[0] == "..":
                    if not any(part in RESOURCE_ROOTS for part in parts):
                        return match[0]
                    suffix = posixpath.normpath(posixpath.join(source_parent, value))
                elif len(parts) > 1 and parts[1] in RESOURCE_ROOTS:
                    suffix = value
                else:
                    return match[0]
                replacement = target_path(f'{paths["canonical_skills"]}/{suffix}')
                return match[0].replace(value, replacement, 1)

            text = INLINE_PATH.sub(resource, text)
    text = HOME_PATH.sub(home, text)
    if output.endswith(".md"):
        text = SKILLS_PLACEHOLDER.sub(placeholder, text)
    if "~/.claude" in text or "~\\.claude" in text:
        raise BuildError(f"{output}: unresolved canonical home path")
    return text


def _rule(metadata: dict, body: str) -> bytes:
    _reject_metadata_home(metadata)
    header = "\n".join(f"{key}: {json.dumps(metadata[key])}" for key in ("trigger", "description"))
    return f"---\n{header}\n---\n{body}".encode("utf-8")


def _reject_metadata_home(metadata: dict) -> None:
    for key, value in metadata.items():
        if isinstance(value, str) and HOME_PATH.search(value):
            raise BuildError(f"portable metadata contains a canonical home path: {key}")


def _json(data: dict) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _hash_manifest(files: dict[str, bytes]) -> bytes:
    return _json({
        "schema_version": 1,
        "files": {path: hashlib.sha256(content).hexdigest() for path, content in sorted(files.items())},
    })


def _safe_target(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or "\\" in relative or ":" in relative or any(
        part in ("", ".", "..") for part in relative.split("/")
    ):
        raise BuildError(f"unsafe generated relative path: {relative}")
    target = root / relative
    _assert_unlinked(target)
    try:
        target.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise BuildError(f"generated path escapes distribution root: {relative}") from exc
    return target


def _assert_unlinked(path: Path) -> None:
    """Inspect lexical ancestors without following a link, including missing leaves."""
    path = path.absolute()
    for candidate in (path, *path.parents):
        try:
            metadata = candidate.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024):
            raise BuildError(f"symlink or reparse point is not supported: {candidate}")
        if candidate != path and not stat.S_ISDIR(metadata.st_mode):
            raise BuildError(f"required directory ancestor is not a directory: {candidate}")


def _check_tree(path: Path) -> None:
    """Preflight every entry without traversing symlinks or Windows junctions."""
    _assert_unlinked(path)
    if not path.is_dir():
        if path.exists():
            raise BuildError(f"required tree root is not a directory: {path}")
        return
    pending = [path]
    while pending:
        directory = pending.pop()
        for entry in directory.iterdir():
            _assert_unlinked(entry)
            if entry.is_dir():
                pending.append(entry)


def _ownership(root: Path) -> dict[str, str]:
    owned = {}
    for filename, prefix in (("distribution-manifest.json", ""), ("pilot/manifest.json", "pilot/")):
        path = _safe_target(root, filename)
        if not path.exists():
            continue
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            if manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), dict):
                raise ValueError("unsupported schema")
            for name, digest in manifest["files"].items():
                if not isinstance(name, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise ValueError("invalid file hash")
                owned[prefix + name] = digest
            canonical = _json({"schema_version": 1, "files": dict(sorted(manifest["files"].items()))})
            if path.read_bytes() != canonical:
                raise ValueError("ownership metadata was modified or is not canonical")
            owned[filename] = hashlib.sha256(canonical).hexdigest()
        except (ValueError, TypeError, AttributeError) as exc:
            raise BuildError(f"invalid generation ownership manifest: {filename}") from exc
    return owned


def _synchronize(root: Path, expected: dict[str, bytes], check: bool) -> int:
    actual = {
        path.relative_to(root).as_posix()
        for directory in ("skills", "rules", "pilot")
        for path in (root / directory).rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }
    for output in actual | expected.keys():
        _safe_target(root, output)
    stale = actual - expected.keys()
    drift = stale | {
        output for output, content in expected.items()
        if not (root / output).is_file() or (root / output).read_bytes() != content
    }
    if check:
        for output in sorted(drift):
            print(f"drift: {output}")
        return 1 if drift else 0
    owned = _ownership(root)
    for output, content in sorted(expected.items()):
        target = _safe_target(root, output)
        if target.exists() and (not target.is_file() or (
            target.read_bytes() != content
            and owned.get(output) != hashlib.sha256(target.read_bytes()).hexdigest()
        )):
            raise BuildError(f"refusing unowned or modified generated output: {output}")
    for output in sorted(stale):
        if owned.get(output) != hashlib.sha256((root / output).read_bytes()).hexdigest():
            raise BuildError(f"refusing unowned or modified unexpected generated file: {output}")
    for output in sorted(stale):
        _safe_target(root, output).unlink()
    for output, content in sorted(expected.items()):
        target = _safe_target(root, output)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.is_file() or target.read_bytes() != content:
            target.write_bytes(content)
    return 0


def _rewrite_tools(text: str, source: str, compatibility: dict) -> str:
    tools = compatibility["tools"]
    literals = compatibility.get("literal_tool_tokens", {}).get(source, [])
    result = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            fence = None if fence == marker[1][0] else marker[1][0]
            result.append(line)
            continue
        if fence:
            result.append(line)
            continue

        def inline(match):
            token = match[1]
            if token not in tools and (
                token in compatibility.get("unsupported_tools", [])
                or token.endswith("Tool")
                or re.match(r"\s+tool\b", match.string[match.end():])
            ):
                raise BuildError(f"{source}: unsupported tool: {token}")
            if token in literals or token not in tools:
                return match[0]
            return f"`{tools[token]}`"

        line = re.sub(r"`([A-Z][A-Za-z0-9]+)`", inline, line)
        for token in ("WebSearch", "WebFetch", "AskUserQuestion", "TodoWrite"):
            line = re.sub(rf"\b{token}\b", lambda match: tools[token], line)
        known_tools = "|".join(re.escape(token) for token in tools)
        line = re.sub(
            rf"\b({known_tools})(?=\s+(?:calls?|tool)\b)",
            lambda match: tools[match[1]], line,
        )
        line = re.sub(
            r"\b(Task|Agent|Skill)(?=\s+(?:calls?|tool)\b|\()",
            lambda match: tools[match[1]], line,
        )
        result.append(line)
    return "".join(result)


def _inputs(repo_root: Path) -> tuple[list[str], dict]:
    names = (repo_root / "config/antigravity-skills.txt").read_text(encoding="utf-8-sig").splitlines()
    if not names or names != sorted(set(names)) or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) for name in names):
        raise BuildError("skill inventory must be nonempty, sorted, unique kebab-case names")
    source_root = repo_root / ".claude/skills"
    discovered = sorted(path.name for path in source_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    if discovered != names:
        raise BuildError(f"skill inventory mismatch: expected {names}; discovered {discovered}")
    compatibility = yaml.safe_load((repo_root / "config/antigravity-compatibility.yml").read_text(encoding="utf-8"))
    if not isinstance(compatibility, dict) or compatibility.get("schema_version") != 1:
        raise BuildError("unsupported compatibility schema")
    for key in ("paths", "tools", "rules"):
        if not isinstance(compatibility.get(key), dict):
            raise BuildError(f"compatibility requires a {key} mapping")
    if compatibility["paths"].get("generated_skills") != "skills" or compatibility["paths"].get("generated_rules") != "rules":
        raise BuildError("generated roots must be skills and rules")
    rules = compatibility["rules"]
    actual_rules = {path.name for path in (repo_root / ".claude/rules").glob("*.md")}
    if actual_rules != rules.keys() or "evidence-first.md" not in rules:
        raise BuildError("canonical rule inventory does not match compatibility table")
    for name, metadata in rules.items():
        expected_trigger = "always_on" if name == "evidence-first.md" else "model_decision"
        if not re.fullmatch(r"[a-z0-9-]+\.md", name) or metadata.get("trigger") != expected_trigger or not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            raise BuildError(f"invalid rule compatibility metadata: {name}")
    return names, compatibility


def _skill_files(root: Path, name: str, names: list[str], compatibility: dict, *, pilot: bool = False) -> dict[str, bytes]:
    source_dir = root / ".claude/skills" / name
    source = source_dir / "SKILL.md"
    data, body = load_frontmatter(source, canonical=True)
    if data["name"] != name or len(data["description"]) > 1024:
        raise BuildError(f"{source}: invalid directory name or description length")
    unknown_tools = set(re.split(r"[\s,]+", data["allowed-tools"].strip())) - compatibility["tools"].keys()
    if unknown_tools:
        raise BuildError(f"{source}: unsupported tools: {', '.join(sorted(unknown_tools))}")
    destination = PILOT_BASE if pilot else f"skills/{name}"
    output = f"{destination}/SKILL.md"
    body = _rewrite_paths(body, output, root, names, compatibility, pilot=pilot)
    body = _rewrite_tools(body, f"{name}/SKILL.md", compatibility)
    body += RESOURCE_EXECUTION
    if pilot:
        data = {**data, "name": PILOT_NAME}
        body += PILOT_MARKER
    files = {output: _manifest(data, body)}
    for companion in sorted(source_dir.rglob("*")):
        if not companion.is_file() or companion == source:
            continue
        if "__pycache__" in companion.parts or companion.suffix == ".pyc":
            continue
        suffix = companion.relative_to(source_dir).as_posix()
        output = f"{destination}/{suffix}"
        content = _copy_bytes(companion)
        if _is_text_resource(companion):
            text = _rewrite_paths(content.decode("utf-8"), output, root, names, compatibility, pilot=pilot)
            if companion.suffix.lower() == ".md":
                text = _rewrite_tools(text, f"{name}/{suffix}", compatibility)
            content = text.encode("utf-8")
        files[output] = content
    return files


def _pilot_rules(root: Path, compatibility: dict) -> list[str]:
    """Return reachable rule dependencies, processing each rule once even in cycles."""
    prefix = compatibility["paths"]["canonical_rules"]

    def dependencies(text: str) -> set[str]:
        result = set()
        for match in HOME_PATH.finditer(text):
            value = match.group().replace("\\", "/").rstrip(".").rstrip("/")
            if value == prefix:
                result.update(compatibility["rules"])
            elif value.startswith(prefix + "/"):
                name = value[len(prefix) + 1:]
                if name not in compatibility["rules"]:
                    raise BuildError(f"unsupported pilot rule dependency: {value}")
                result.add(name)
        return result

    pending = set()
    for source in (root / ".claude/skills/admin").rglob("*"):
        if source.is_file() and _is_text_resource(source) and "__pycache__" not in source.parts:
            pending.update(dependencies(_copy_bytes(source).decode("utf-8")))
    pending.update(dependencies(_copy_bytes(root / ".claude/rules/evidence-first.md").decode("utf-8")))
    visited = set()
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        pending.update(dependencies(_copy_bytes(root / ".claude/rules" / name).decode("utf-8")) - visited)
    return sorted(visited)


def build(repo_root: Path, *, check: bool = False) -> int:
    repo_root = Path(repo_root)
    _assert_unlinked(repo_root)
    repo_root = Path(os.path.abspath(repo_root))
    for directory in ("config", ".claude/skills", ".claude/rules", "skills", "rules", "pilot"):
        _check_tree(repo_root / directory)
    for filename in ("plugin.json", "distribution-manifest.json", "pilot/manifest.json"):
        _safe_target(repo_root, filename)
    names, compatibility = _inputs(repo_root)
    expected: dict[str, bytes] = {}
    for name in names:
        expected.update(_skill_files(repo_root, name, names, compatibility))
    shared_root = repo_root / ".claude/skills/_shared"
    if shared_root.is_dir():
        # Shared policy files are referenced by relative paths (../_shared/...) and ship as-is.
        for source in sorted(shared_root.rglob("*")):
            if not source.is_file() or "__pycache__" in source.parts:
                continue
            output = f"skills/_shared/{source.relative_to(shared_root).as_posix()}"
            content = _copy_bytes(source)
            if _is_text_resource(source):
                content = _rewrite_paths(content.decode("utf-8"), output, repo_root, names, compatibility).encode("utf-8")
            expected[output] = content
    for name, metadata in compatibility["rules"].items():
        source = repo_root / ".claude/rules" / name
        output = f"rules/{name}"
        body = _rewrite_paths(_copy_bytes(source).decode("utf-8"), output, repo_root, names, compatibility)
        body = _rewrite_tools(body, f"rules/{name}", compatibility)
        expected[output] = _rule(metadata, body)
    expected["plugin.json"] = _json(PLUGIN)
    expected["distribution-manifest.json"] = _hash_manifest(expected)
    if "admin" not in names:
        raise BuildError("canonical inventory must include admin for the pilot")
    pilot_files = _skill_files(repo_root, "admin", names, compatibility, pilot=True)
    for name in _pilot_rules(repo_root, compatibility):
        output = f"{PILOT_BASE}/references/shared-rules/{name}"
        body = _rewrite_paths(_copy_bytes(repo_root / ".claude/rules" / name).decode("utf-8"), output, repo_root, names, compatibility, pilot=True, rule=True)
        pilot_files[output] = _rewrite_tools(body, f"rules/{name}", compatibility).encode("utf-8")
    body = _copy_bytes(repo_root / ".claude/rules/evidence-first.md").decode("utf-8")
    output = "pilot/rules/admin-evidence-pilot.md"
    body = _rewrite_paths(body, output, repo_root, names, compatibility, pilot=True, rule=True)
    pilot_files[output] = _rule({
        "trigger": "always_on",
        "description": "Temporary global evidence policy canary; affects all chats while installed.",
    }, body + RULE_MARKER)
    expected.update(pilot_files)
    expected["pilot/manifest.json"] = _hash_manifest({path.removeprefix("pilot/"): content for path, content in pilot_files.items()})
    return _synchronize(repo_root, expected, check)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        result = build(args.repo_root, check=args.check)
        if result == 0:
            print("distribution already matches" if args.check else "generated distribution updated")
        return result
    except (BuildError, ManifestError, OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
