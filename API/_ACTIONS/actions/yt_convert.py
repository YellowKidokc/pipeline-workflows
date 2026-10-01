"""yt_convert: station 07 as an action. SRT / VTT / JSON transcripts -> ytgrab-style .md (local)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 07).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "SRT / VTT / JSON transcripts -> ytgrab-style .md (local)"
API = False
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("07", [str(folder)])
