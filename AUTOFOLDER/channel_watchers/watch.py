"""
Portable channel watcher for YouTube transcript folders.

Drop this file (plus FolderWatcher.py) into any subtitles/<Channel>/ folder.
It watches for new/changed .md transcripts, runs the local Clean step, then
sends the cleaned note through the DeepSeek index pipeline.

Usage:
  python watch.py                 # watch and process new files
  python watch.py --backfill      # process all existing .md files first
  python watch.py --dry-run       # log what would be done; no commands run
  python watch.py --once          # one pass, then exit
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import subprocess
import sys
import time

from FolderWatcher import FolderWatcher

HERE = pathlib.Path(__file__).resolve().parent
CHANNEL = HERE.name
REPO = HERE.parents[1]
CLEAN_SCRIPT = REPO / "Python Clean Library" / "clean_library.py"
INDEX_SCRIPT = REPO / "pipeline-workflows" / "deepseek-home" / "index_video.py"
WATCH_DIR = HERE
CLEAN_OUT = REPO / "obsidian_transcripts"

LOG_FILE = HERE / "watch.log"
STATE_FILE = HERE / ".watch_state.json"


def log(msg: str) -> None:
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(cmd: list[str], dry_run: bool) -> int:
    log(f"run: {' '.join(cmd)}")
    if dry_run:
        return 0
    return subprocess.run(cmd, check=False).returncode


def clean_channel(dry_run: bool) -> None:
    cmd = [
        sys.executable,
        str(CLEAN_SCRIPT),
        "--src", str(REPO / "subtitles"),
        "--out", str(CLEAN_OUT),
        "--channel", CHANNEL,
    ]
    rc = run(cmd, dry_run)
    if rc != 0:
        log(f"warning: clean step exited {rc}")


def index_file(path: pathlib.Path, dry_run: bool) -> None:
    cmd = [
        sys.executable,
        str(INDEX_SCRIPT),
        str(path),
    ]
    run(cmd, dry_run)


def is_transcript(path: pathlib.Path) -> bool:
    name = path.name
    return (
        path.suffix == ".md"
        and not name.startswith("_")
        and not name.startswith("channel_")
        and "Index" not in name
    )


def on_change(changed: list[tuple[str, pathlib.Path]], dry_run: bool) -> None:
    files = {path for event, path in changed if event in ("created", "modified") and is_transcript(path)}
    if not files:
        return

    log(f"{len(files)} transcript(s) changed")
    clean_channel(dry_run)
    for f in sorted(files):
        index_file(f, dry_run)


def backfill(dry_run: bool, limit: int | None = None) -> None:
    files = [p for p in sorted(HERE.glob("*.md")) if is_transcript(p)]
    if limit:
        files = files[:limit]
    log(f"backfill: {len(files)} existing transcript(s)")
    if not files:
        return
    clean_channel(dry_run)
    for f in files:
        index_file(f, dry_run)


def main():
    ap = argparse.ArgumentParser(description=f"Watch {CHANNEL} transcripts and index them.")
    ap.add_argument("--backfill", action="store_true", help="process existing files on startup")
    ap.add_argument("--limit", type=int, help="process at most N files (backfill only)")
    ap.add_argument("--dry-run", action="store_true", help="log commands without running them")
    ap.add_argument("--once", action="store_true", help="one pass, then exit")
    ap.add_argument("--debounce", type=float, default=2.0)
    args = ap.parse_args()

    if not os.environ.get("DEEPSEEK_API_KEY"):
        log("error: DEEPSEEK_API_KEY not set")
        return 1

    log(f"watching: {WATCH_DIR}")
    log(f"channel : {CHANNEL}")
    log(f"repo    : {REPO}")

    if args.backfill:
        backfill(args.dry_run, args.limit)
        if args.once:
            return 0

    def callback(changed):
        try:
            on_change(changed, args.dry_run)
        except Exception as e:
            log(f"error in callback: {e}")

    watcher = FolderWatcher(
        path=str(WATCH_DIR),
        callback=callback,
        recursive=False,
        extensions=[".md"],
        debounce=args.debounce,
        return_mode="files",
    )

    if args.once:
        log("--once: nothing to watch; exiting")
        return 0

    try:
        watcher.run_forever()
    except KeyboardInterrupt:
        log("stopped by user")
    return 0


if __name__ == "__main__":
    sys.exit(main())
