"""yt_catalog: station 05 as an action. Channel overviews, debate pages, catalog.xlsx / catalog.sqlite from the index (local; its configured roots)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 05).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Channel overviews, debate pages, catalog.xlsx / catalog.sqlite from the index (local; its configured roots)"
API = False
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("05")                     # reads its own configured roots; the folder is not used
