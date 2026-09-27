"""
Deploy portable channel watchers to every subtitles/<Channel>/ folder
that contains at least one .md transcript.

Copies watch.py + FolderWatcher.py from the Gary Habermas seed folder.
Idempotent: skips folders that already have both files.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
SEED = HERE / "Gary Habermas"
WATCHER_FILES = ["watch.py", "FolderWatcher.py"]


def needs_watcher(folder: pathlib.Path) -> bool:
    return any(not (folder / name).exists() for name in WATCHER_FILES)


def main() -> int:
    if not SEED.exists():
        print(f"seed folder not found: {SEED}", file=sys.stderr)
        return 1

    missing_seed = [name for name in WATCHER_FILES if not (SEED / name).exists()]
    if missing_seed:
        print(f"seed files missing: {missing_seed}", file=sys.stderr)
        return 1

    folders = sorted(HERE.iterdir())
    with_md = [p for p in folders if p.is_dir() and any(p.glob("*.md"))]
    no_md = [p for p in folders if p.is_dir() and p not in with_md]

    targets = [p for p in with_md if p.name != "Gary Habermas" and needs_watcher(p)]
    already = [p for p in with_md if not needs_watcher(p)]

    for folder in targets:
        for name in WATCHER_FILES:
            shutil.copy2(SEED / name, folder / name)
        print(f"deployed -> {folder.name}")

    for folder in already:
        print(f"skipped  -> {folder.name} (already has watcher)")

    for folder in no_md:
        print(f"skipped  -> {folder.name} (no .md transcripts)")

    print(f"\ndeployed: {len(targets)}  already present: {len(already)}  no .md: {len(no_md)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
