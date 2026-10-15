"""Repository facade for the parser shipped inside the test-framework skill."""

import importlib.util
from pathlib import Path


_PARSER_PATH = (
    Path(__file__).resolve().parents[1]
    / ".claude" / "skills" / "test-framework" / "scripts" / "skill_manifest.py"
)
_SPEC = importlib.util.spec_from_file_location("_gobal_skill_manifest", _PARSER_PATH)
_PARSER = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_PARSER)

ManifestError = _PARSER.ManifestError
UniqueKeyLoader = _PARSER.UniqueKeyLoader
split_frontmatter = _PARSER.split_frontmatter
load_frontmatter = _PARSER.load_frontmatter
dump_skill = _PARSER.dump_skill

__all__ = ["ManifestError", "UniqueKeyLoader", "split_frontmatter", "load_frontmatter", "dump_skill"]
