"""yt_clean: station 02 as an action. Raw transcripts -> readable notes in <Channel>/Clean MD (same as `clean`)

The station is not rewritten; this runs it through ONE_MENU (engine/menu.py 02).
"""
import importlib.util
from pathlib import Path

ABOUT = "Raw transcripts -> readable notes in <Channel>/Clean MD (same as `clean`)"
API = False
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("action_clean", here / "clean.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.run_folder(folder)
