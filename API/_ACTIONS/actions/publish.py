"""publish: write every finished analysis of this note onto the note (deep CKG, argument grades, Fruits, YouTube CKG)."""
import importlib.util
from pathlib import Path

TOOL = next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system" / "tools" / "publish_analysis.py"
_spec = importlib.util.spec_from_file_location("publish_analysis", TOOL)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)

ABOUT = "put every finished analysis onto the note, between <!-- analysis --> markers (no API)"
API = False


def run(note: Path, text: str) -> dict:
    return {"say": pa.publish(note, False)}
