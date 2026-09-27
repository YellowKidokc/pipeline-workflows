#!/usr/bin/env python3
"""CLI for extracting claims, proofs, and evidence from CKG companions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from workbench.extract_cpe import extract_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract claims, proofs, and evidence atoms from CKG companions."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="CKG station root directory (default: inferred from script location)",
    )
    parser.add_argument(
        "--input",
        type=Path,
        action="append",
        default=None,
        help="Companion folder to scan (can be given multiple times; default: OUTBOX/01_ALL_PAPERS)",
    )
    args = parser.parse_args(argv)

    if args.root is None:
        system = next(p for p in Path(__file__).resolve().parents if p.name == "_system")
        sys.path.insert(0, str(system))
        from engine.paths import station_dir
    root = args.root or station_dir("20_CKG_RUN").parent
    counts = extract_all(root, args.input)
    total = sum(counts.values())
    print(f"Extracted {total} atom(s):")
    for bucket, n in counts.items():
        print(f"  {bucket}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
