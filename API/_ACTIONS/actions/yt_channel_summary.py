"""yt_channel_summary: station 13 as an action. Channel summary folder: 3-sentence summary, keywords, columns (DeepSeek)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 13).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _station import run_station  # noqa: E402

ABOUT = "Channel summary folder: 3-sentence summary, keywords, columns (DeepSeek)"
API = True
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    return run_station("13", [str(folder)])
