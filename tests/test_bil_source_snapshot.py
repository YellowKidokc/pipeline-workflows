import importlib.util
import json
import re
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - CI may not install jsonschema
    Draft202012Validator = None


BIL_ROOT = Path("preferences/engines/bil")
SOURCE_ROOT = BIL_ROOT / "source"
EXPECTED_SOURCE_FILES = {
    "bil/bil_api.py",
    "bil/bil_features.py",
    "bil/bil_models.py",
    "bil/bil_server.py",
    "bil/config.py",
    "bil/ingest.py",
    "bil/llm_query.py",
    "browser/background.js",
    "browser/content.js",
    "browser/config.js",
    "browser/manifest.json",
    "README.md",
}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(api[_-]?key|secret|token|credential)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
)


def load(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def import_bil_api():
    sys.path.insert(0, str(SOURCE_ROOT))
    spec = importlib.util.spec_from_file_location("bil.bil_api", SOURCE_ROOT / "bil" / "bil_api.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_bil_source_snapshot_shape_exists():
    for relative in EXPECTED_SOURCE_FILES:
        assert (SOURCE_ROOT / relative).is_file(), f"missing BIL source file: {relative}"
    assert (BIL_ROOT / "README.md").is_file()
    assert (BIL_ROOT / "requirements.txt").is_file()


def test_bil_source_snapshot_has_no_secret_assignments_or_runtime_artifacts():
    forbidden_suffixes = {".zip", ".db", ".sqlite", ".sqlite3", ".jsonl", ".log", ".safetensors", ".pt", ".bin"}
    for path in BIL_ROOT.rglob("*"):
        assert path.suffix not in forbidden_suffixes, f"runtime artifact committed: {path}"
        if path.is_file() and path.suffix in {".py", ".js", ".json", ".md", ".txt"}:
            text = path.read_text(encoding="utf-8")
            assert not SECRET_ASSIGNMENT.search(text), f"possible secret assignment in {path}"


def test_bil_event_mapping_matches_preference_event_contract():
    bil_api = import_bil_api()
    event = bil_api.build_preference_event(
        signal="bookmark",
        source="browser",
        subject="example page",
        timestamp="2026-06-12T00:00:00Z",
        metadata={"url": "https://example.test/article"},
    )

    assert event["event_type"] == "preference_event"
    assert event["source"] == "browser_extension"
    assert event["signal"] == "bookmark_save"
    assert event["weight"] == 0.7

    if Draft202012Validator is not None:
        Draft202012Validator(load("contracts/schemas/preference-event.schema.json")).validate(event)
