"""scripture: every Bible reference the note uses, found in code (written or spoken forms), into its YAML."""
import sys
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine import scripture  # noqa: E402

ABOUT = "every Bible reference used (cited or mentioned), found in code -> YAML scriptures: [...]"
API = False


def run(note: Path, text: str) -> dict:
    hits = scripture.find(text)
    cited = [h["ref"] for h in hits if h["chapter"]]
    return {"yaml": {"scriptures": cited, "scripture_books": sorted({h["book"] for h in hits})},
            "say": f"{len(cited)} reference(s), {len({h['book'] for h in hits})} book(s)"}
