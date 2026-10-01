"""yt_summary: station 08 as an action. Base summary of each video: the questions in QUESTIONS.md (DeepSeek)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 08).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Base summary of each video: the questions in QUESTIONS.md (DeepSeek)"
API = True
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("08", [str(folder)])
