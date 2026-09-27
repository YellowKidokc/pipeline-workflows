"""clean: raw downloaded YouTube transcripts -> readable notes in the channel's Clean MD/ folder.

Calls the existing script (yt-transcript-downloader/Python Clean Library/clean_library.py) with --in-place; it is not
rewritten here. All local Python: paragraphs, [mm:ss] links, filler and stutter removed, and the local punctuation
model when it is installed in the downloader's venv. Already-cleaned files are skipped, so rerunning is cheap.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_system"))
from engine.paths import configured, external  # noqa: E402

ABOUT = "raw YouTube transcripts -> clean notes in <Channel>/Clean MD (local, runs clean_library.py)"
API = False
SCOPE = "folder"          # give it a channel folder (subtitles/<Channel>), or the Clean MD folder inside one


def run_folder(folder: Path) -> dict:
    if not configured("yt_downloader"):
        return {"say": "yt_downloader is not set in _system/config/paths.json"}
    root = external("yt_downloader")
    script = root / "Python Clean Library" / "clean_library.py"
    py = root / "venv" / "Scripts" / "python.exe"
    py = str(py) if py.exists() else sys.executable
    channel = folder.parent if folder.name == "Clean MD" else folder
    cmd = [py, str(script), "--src", str(channel.parent), "--channel", channel.name, "--in-place"]
    if subprocess.run([py, "-c", "import punctuators"], capture_output=True).returncode == 0:
        cmd.append("--punctuate")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    last = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return {"say": ("ok: " if r.returncode == 0 else f"FAILED ({r.returncode}): ") + (last[-1][:150] if last else "")}
