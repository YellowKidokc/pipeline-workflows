#!/usr/bin/env python3
"""
safe_sort_unsorted.py - Safe replacement for 04_sorting_triage/03_sort_unsorted.py.

The underlying script is destructive (shutil.move) with `except Exception: pass`
silently swallowing failures. This wrapper does NOT invoke the underlying script.
Instead it re-implements the same regex-on-filename mapping (sourced from the
script itself) using copy-verify-delete semantics with an explicit failure log.

Usage:
  python SCRIPTS/wrappers/safe_sort_unsorted.py --source <dir>
  python SCRIPTS/wrappers/safe_sort_unsorted.py --source <dir> --apply

Defaults: dry-run, lists planned moves; never touches files without --apply.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from safe_inplace import (  # type: ignore
    PACKET_ROOT,
    ERROR_ROOT,
    OUTPUT_ROOT,
    find_entry,
    load_registry,
    sha256_of,
    utc_stamp,
)

SCRIPT_ID = "sort_unsorted"
UNDERLYING = PACKET_ROOT / "SCRIPTS/imported/html_master_workflow/04_sorting_triage/03_sort_unsorted.py"


def load_mapping_from_underlying() -> tuple[dict, dict]:
    """Import the underlying script as a module to read its `mapping` and
    `folder_map` constants without executing its top-level for-loop. Since the
    script's loop runs at import time, we read it as text and exec a stub."""
    text = UNDERLYING.read_text(encoding="utf-8")
    namespace: dict = {}
    # Cut at the top-level loop. The script defines mapping + folder_map at the top
    # and then runs `moved_count = 0` etc. Grab everything before the loop.
    cut = text.find("moved_count = 0")
    if cut < 0:
        raise SystemExit("[safe_sort_unsorted] could not locate underlying script's loop boundary.")
    exec(text[:cut], namespace)
    mapping = namespace.get("mapping")
    folder_map = namespace.get("folder_map")
    if not mapping or not folder_map:
        raise SystemExit("[safe_sort_unsorted] underlying script did not expose `mapping` / `folder_map`.")
    return mapping, folder_map


def classify(filename: str, mapping: dict) -> str | None:
    for code, patterns in mapping.items():
        for pattern in patterns:
            p = pattern.replace(".", "[_ \\-]")
            if re.search(p, filename, re.IGNORECASE):
                return code
    return None


def main() -> int:
    parser = argparse.ArgumentParser(prog="safe_sort_unsorted.py")
    parser.add_argument("--source", required=True, help="DMP_Unsorted-style source directory.")
    parser.add_argument("--target-base", default=".", help="Base directory containing category folders. Default CWD.")
    parser.add_argument("--apply", action="store_true", help="Actually move files. Default is dry-run.")
    args = parser.parse_args()

    registry = load_registry()
    entry = find_entry(registry, SCRIPT_ID)
    if entry is None:
        raise SystemExit(f"[safe_sort_unsorted] '{SCRIPT_ID}' missing from script_registry.json")

    source = Path(args.source).resolve()
    base = Path(args.target_base).resolve()
    if not source.is_dir():
        raise SystemExit(f"[safe_sort_unsorted] source not a directory: {source}")
    if not base.is_dir():
        raise SystemExit(f"[safe_sort_unsorted] target_base not a directory: {base}")

    mapping, folder_map = load_mapping_from_underlying()
    plan = []
    unmatched = []
    for child in sorted(source.iterdir()):
        if child.is_dir():
            continue
        code = classify(child.name, mapping)
        if code is None:
            unmatched.append(str(child))
            continue
        target_dir = base / folder_map[code] / "_drafts"
        plan.append({
            "src": str(child),
            "dst": str(target_dir / child.name),
            "code": code,
            "bytes": child.stat().st_size,
        })

    stamp = utc_stamp()
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT_ROOT / f"wrap-manifest-{SCRIPT_ID}-{stamp}.json"

    if not args.apply:
        manifest_path.write_text(json.dumps({
            "wrapper": "safe_sort_unsorted.py",
            "script_id": SCRIPT_ID,
            "utc": stamp,
            "applied": False,
            "source": str(source),
            "target_base": str(base),
            "planned": plan,
            "unmatched": unmatched,
            "summary": {"planned": len(plan), "unmatched": len(unmatched)},
        }, indent=2), encoding="utf-8")
        print(f"[safe_sort_unsorted] DRY-RUN source={source} planned={len(plan)} unmatched={len(unmatched)}")
        print(f"[safe_sort_unsorted]   manifest: {manifest_path}")
        return 0

    moved = []
    failures = []
    for item in plan:
        src = Path(item["src"])
        dst = Path(item["dst"])
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            # Copy-verify-delete instead of move.
            shutil.copy2(src, dst)
            if not dst.exists() or dst.stat().st_size != item["bytes"]:
                failures.append({"src": str(src), "dst": str(dst), "reason": "size mismatch after copy"})
                continue
            if sha256_of(src) != sha256_of(dst):
                failures.append({"src": str(src), "dst": str(dst), "reason": "hash mismatch after copy"})
                continue
            os.remove(src)
            moved.append({"src": str(src), "dst": str(dst), "bytes": item["bytes"]})
        except OSError as e:
            failures.append({"src": str(src), "dst": str(dst), "reason": str(e)})

    manifest_path.write_text(json.dumps({
        "wrapper": "safe_sort_unsorted.py",
        "script_id": SCRIPT_ID,
        "utc": stamp,
        "applied": True,
        "source": str(source),
        "target_base": str(base),
        "moved": moved,
        "failures": failures,
        "unmatched": unmatched,
        "summary": {"moved": len(moved), "failures": len(failures), "unmatched": len(unmatched)},
    }, indent=2), encoding="utf-8")

    if failures:
        ERROR_ROOT.mkdir(parents=True, exist_ok=True)
        err_path = ERROR_ROOT / f"safe_sort_unsorted-failures-{stamp}.json"
        err_path.write_text(json.dumps(failures, indent=2), encoding="utf-8")
        print(f"[safe_sort_unsorted] APPLY moved={len(moved)} failures={len(failures)} log={err_path}")
        return 1

    print(f"[safe_sort_unsorted] APPLY moved={len(moved)} unmatched={len(unmatched)} manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
