"""yt_lenses: station 04 as an action. Numbered focus lenses and lettered layers over indexed videos (DeepSeek)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 04).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Numbered focus lenses and lettered layers over indexed videos (DeepSeek)"
API = True
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("04", [str(folder)])
