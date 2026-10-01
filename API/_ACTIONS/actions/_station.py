"""Shared by the yt_* actions: run one existing station through ONE_MENU (relay, limiter, receipts), on a folder.

The station keeps its own code; an action is the small, named front for it (AGENTS.md section 5: wrap, don't rewrite).
"""
import subprocess
import sys
from pathlib import Path

SYSTEM = next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"


def run_station(number: str, items: list[str] | None = None, workers: int = 8) -> dict:
    cmd = [sys.executable, str(SYSTEM / "engine" / "menu.py"), number, "--yes", "--workers", str(workers)]
    for item in items or []:
        cmd += ["--item", str(item)]
    code = subprocess.run(cmd, cwd=SYSTEM).returncode
    return {"say": f"station {number}: " + ("done" if code == 0 else f"FAILED (exit {code})")}
