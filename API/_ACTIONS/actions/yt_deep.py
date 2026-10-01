"""yt_deep: station 09 as an action. Detailed, rigorous layer on top of the summary (DeepSeek)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 09).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Detailed, rigorous layer on top of the summary (DeepSeek)"
API = True
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("09", [str(folder)])
