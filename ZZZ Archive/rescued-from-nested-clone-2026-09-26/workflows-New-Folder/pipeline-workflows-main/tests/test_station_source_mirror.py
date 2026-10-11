import json
from pathlib import Path


FORBIDDEN_DIR_NAMES = {
    "OUTPUT",
    "REVIEW",
    "ARCHIVE",
    "ERROR",
    "LOGS",
    "logs",
    "exports",
    "qdrant",
    "chroma",
    "vector_db",
    "databases",
    "node_modules",
    "__pycache__",
}

FORBIDDEN_SUFFIXES = {
    ".db",
    ".sqlite",
    ".sqlite3",
    ".db-wal",
    ".db-shm",
    ".faiss",
    ".hnsw",
    ".qdrant",
    ".chroma",
    ".pickle",
    ".pkl",
    ".pt",
    ".pth",
    ".bin",
    ".onnx",
    ".safetensors",
    ".log",
    ".jsonl",
    ".parquet",
    ".arrow",
}

FORBIDDEN_NAME_PARTS = ("secret", "token")
ALLOWED_ROOT_FILES = {"README.md", "AUDIT.md", "AUDIT.json", ".gitignore"}


def load(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_station_source_audit_matches_registry_and_snapshot_dirs():
    registry = load("stations/STATION_REGISTRY.json")["stations"]
    audit = load("stations/source/AUDIT.json")
    source_root = Path("stations/source")

    snapshot_dirs = sorted(p.name for p in source_root.iterdir() if p.is_dir())

    assert audit["live_registry"] == "stations/STATION_REGISTRY.json"
    assert audit["registry_count"] == len(registry)
    assert audit["present_snapshots"] == sorted(name for name in snapshot_dirs if name in registry)
    assert audit["missing_snapshots"] == sorted(set(registry) - set(audit["present_snapshots"]))


def test_station_source_root_contains_only_docs_or_station_snapshot_dirs():
    registry = load("stations/STATION_REGISTRY.json")["stations"]
    for path in Path("stations/source").iterdir():
        if path.is_file():
            assert path.name in ALLOWED_ROOT_FILES
        elif path.is_dir():
            assert path.name in registry


def test_station_source_mirror_excludes_runtime_artifact_patterns():
    for path in Path("stations/source").rglob("*"):
        relative_parts = set(path.relative_to("stations/source").parts)
        assert not (relative_parts & FORBIDDEN_DIR_NAMES), f"forbidden runtime directory in {path}"
        assert path.suffix not in FORBIDDEN_SUFFIXES, f"forbidden runtime artifact suffix in {path}"
        lowered = path.name.lower()
        assert not any(part in lowered for part in FORBIDDEN_NAME_PARTS), f"possible secret/token artifact in {path}"
