"""
Deploy relay_watch.py + FolderWatcher.py + relay.yaml to YouTube research folders.
"""
from __future__ import annotations

import pathlib
import shutil
import sys

SOURCE = pathlib.Path(__file__).resolve().parent
RELAY_FILES = ["relay_watch.py", "FolderWatcher.py", "relay.yaml"]

TARGETS = [
    "D:/GitHub/Research-Acquisition/yt-transcript-downloader/transcripts_inbox",
    "D:/GitHub/Research-Acquisition/yt-transcript-downloader/transcripts_outbox",
    "D:/GitHub/Research-Acquisition/youtube-scraper/transcripts",
    "D:/GitHub/Research-Acquisition/youtube-scraper/transcripts_bible_contradictions",
    "D:/GitHub/Research-Acquisition/youtube-transcript-ytdlp/transcripts",
]


def main() -> int:
    missing = [name for name in RELAY_FILES if not (SOURCE / name).exists()]
    if missing:
        print(f"source files missing: {missing}", file=sys.stderr)
        return 1

    deployed = 0
    for target_str in TARGETS:
        target = pathlib.Path(target_str)
        target.mkdir(parents=True, exist_ok=True)
        for name in RELAY_FILES:
            shutil.copy2(SOURCE / name, target / name)
        print(f"deployed -> {target}")
        deployed += 1

    print(f"\ndeployed: {deployed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
