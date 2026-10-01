"""yt_grab: station 01 as an action. Download YouTube transcripts: URLs listed in <folder>/URLS.txt (one per line)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 01).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Download YouTube transcripts: URLs listed in <folder>/URLS.txt (one per line)"
API = False
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    urls = folder / "URLS.txt"
    links = [l.strip() for l in urls.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if urls.is_file() else []
    if not links:
        return {"say": f"put the channel / playlist / video links in {urls} (one per line)"}
    return run_station("01", links)
