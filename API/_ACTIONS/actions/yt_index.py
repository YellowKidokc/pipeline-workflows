"""yt_index: station 03 as an action. Standard CKG argument-first index of each video in the folder (DeepSeek)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 03).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Standard CKG argument-first index of each video in the folder (DeepSeek)"
API = True
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("03", [str(folder)])
