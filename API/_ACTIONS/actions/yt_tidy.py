"""yt_tidy: station 12 as an action. One uniform name and an Obsidian note per video (local)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 12).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "One uniform name and an Obsidian note per video (local)"
API = False
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("12", [str(folder)])
