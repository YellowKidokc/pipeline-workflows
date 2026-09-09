#!/usr/bin/env python3
"""
safe_canonical_sort.py - Safety wrapper for 04_sorting_triage/01_canonical_sort.py.

The underlying script bakes NAS IP 192.168.1.177 and a path with an apostrophe
into its source/dest constants. It only copies (not moves), so blast radius is
limited, but pointing it off-machine produces a silent no-op. This wrapper
probes NAS reachability before invocation and externalizes source/dest into
CLI flags.

Usage:
  python SCRIPTS/wrappers/safe_canonical_sort.py --source <unc> --dest <unc>
  python SCRIPTS/wrappers/safe_canonical_sort.py --source <unc> --dest <unc> --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from safe_inplace import (  # type: ignore
    PACKET_ROOT,
    OUTPUT_ROOT,
    find_entry,
    load_registry,
    run_script,
    utc_stamp,
)

SCRIPT_ID = "canonical_sort"


def probe(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"[safe_canonical_sort] {label} not reachable: {path}")
    if not path.is_dir():
        raise SystemExit(f"[safe_canonical_sort] {label} is not a directory: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(prog="safe_canonical_sort.py")
    parser.add_argument("--source", required=True, help="Source HTML root (e.g. NAS share).")
    parser.add_argument("--dest", required=True, help="Destination 4-pillar root.")
    parser.add_argument("--apply", action="store_true", help="Actually run. Default is dry-run.")
    args = parser.parse_args()

    registry = load_registry()
    entry = find_entry(registry, SCRIPT_ID)
    if entry is None:
        raise SystemExit(f"[safe_canonical_sort] '{SCRIPT_ID}' missing from script_registry.json")

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()
    probe(source, "source")
    probe(dest, "dest")

    stamp = utc_stamp()

    if not args.apply:
        run = run_script(entry, source, dry_run=True)
        print(f"[safe_canonical_sort] DRY-RUN source={source} dest={dest}")
        print(f"[safe_canonical_sort]   would invoke: {run['argv']}")
        print(f"[safe_canonical_sort]   note: underlying script has source/dest hard-coded. "
              f"For real apply, your --source and --dest must match the script body, OR a sanitized "
              f"variant must be shipped that takes them via env vars.")
        return 0

    # The underlying script does NOT read source/dest from CLI or env. Re-invoking it
    # would just use its baked-in NAS path. Refuse to fake safety we can't deliver.
    raise SystemExit(
        "[safe_canonical_sort] --apply is not yet supported because the underlying script "
        "has source/dest hard-coded. Ship a sanitized variant that reads env CANONICAL_SORT_SRC "
        "and CANONICAL_SORT_DST, then this wrapper can pass them through."
    )


if __name__ == "__main__":
    raise SystemExit(main())
