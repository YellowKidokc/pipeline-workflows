"""title: the standard name  <Author> <date> · <Title> · <Keyword>, <Keyword> · <Move>  (renames the note)."""
import importlib.util
from pathlib import Path

TOOL = next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system" / "tools" / "standard_title.py"
_spec = importlib.util.spec_from_file_location("standard_title", TOOL)
st = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(st)

ABOUT = "standard title, 2-3 specific keywords and the move; renames the note (~1.5k tokens)"
API = True
SERIAL = True          # each note sees the keywords the previous one added to the master record


def run(note: Path, text: str) -> dict:
    result = st.process(note, True)
    if result.startswith("CLASH"):
        return {"say": result}
    return {"note": str(note.parent / result), "say": result}      # result may include a new series folder
