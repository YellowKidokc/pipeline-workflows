"""station_paths.py -- print a machine path from _system/config/paths.json.

Usage:  py -3 scripts\\station_paths.py <key>

Walks up from this script to find _system, the way every station does, and
prints the value of the requested key. Used by the station's .bat launchers so
machine-specific paths live in paths.json only, never in code.
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: station_paths.py <paths.json key>")
    key = sys.argv[1]
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "_system" / "config" / "paths.json"
        if candidate.exists():
            paths = json.loads(candidate.read_text(encoding="utf-8"))
            value = str(paths.get(key, "")).strip()
            if not value:
                sys.exit(f"ERROR: paths.json key '{key}' is empty or missing.")
            print(value)
            return
    sys.exit("ERROR: _system/config/paths.json not found above this script.")


if __name__ == "__main__":
    main()
