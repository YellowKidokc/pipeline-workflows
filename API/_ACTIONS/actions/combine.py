"""combine: every .md in a folder (and its sub-folders) -> one <folder>__combined.md beside the folder.

Calls file_actions.py combine-markdown (Codex-Powershell_GUI); it never overwrites and writes a JSON receipt.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.paths import configured, external  # noqa: E402

ABOUT = "all .md files in a folder -> one combined .md beside it, with a receipt (file_actions.py)"
API = False
SCOPE = "folder"


def run_folder(folder: Path) -> dict:
    if not configured("file_tools"):
        return {"say": "file_tools is not set in _system/config/paths.json"}
    tool = external("file_tools") / "file_actions.py"
    r = subprocess.run([sys.executable, str(tool), "combine-markdown", str(folder), str(folder.parent)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        made = sorted(folder.parent.glob(f"{folder.name}__combined*.md"), key=lambda p: p.stat().st_mtime)
        return {"say": f"-> {made[-1] if made else folder.parent}"}
    last = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return {"say": f"FAILED ({r.returncode}): " + (last[-1][:160] if last else "")}
