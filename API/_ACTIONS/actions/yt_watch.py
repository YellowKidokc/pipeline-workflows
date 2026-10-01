"""yt_watch: station 06 as an action. Automatic chain for the channels in WATCH_CHANNELS: convert, clean, index, summary (DeepSeek; its configured roots)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 06).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Automatic chain for the channels in WATCH_CHANNELS: convert, clean, index, summary (DeepSeek; its configured roots)"
API = True
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("06")                     # reads its own configured roots; the folder is not used
