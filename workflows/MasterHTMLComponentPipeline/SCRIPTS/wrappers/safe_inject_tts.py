#!/usr/bin/env python3
"""
safe_inject_tts.py - Safety wrapper for 03_tts_export_helpers/01_inject_tts.py.

The underlying script bakes a ClipSync API URL + device_id into the JavaScript
of every HTML file it touches. The load-bearing safety here is keeping the
outbound call off unless the user explicitly opts in. This wrapper requires
one of --with-clipsync or --no-clipsync; if --no-clipsync is selected, the
wrapper refuses to apply until a sanitized variant exists, because the
underlying script body has the URL baked into a string constant.

Usage:
  python SCRIPTS/wrappers/safe_inject_tts.py --root <path> --no-clipsync
  python SCRIPTS/wrappers/safe_inject_tts.py --root <path> --with-clipsync --apply

Backups: the underlying script already writes originals to _ORIGINALS/ under
the target root before overwrite. This wrapper layers on top: dry-run default,
JSON manifest, and the explicit ClipSync gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from safe_inplace import (  # type: ignore
    PACKET_ROOT,
    ARCHIVE_ROOT,
    OUTPUT_ROOT,
    discover_targets,
    emit_manifest,
    find_entry,
    load_registry,
    run_script,
    stage_backups,
    utc_stamp,
    verify_post,
)

SCRIPT_ID = "inject_tts"
PRODUCTION_HINTS = ("_LIVE", "_DEPLOY", "K-Production", "production")


def refuse_production_root(root: Path) -> None:
    s = str(root).lower()
    for hint in PRODUCTION_HINTS:
        if hint.lower() in s:
            raise SystemExit(
                f"[safe_inject_tts] target root contains '{hint}'; refusing to inject TTS "
                f"into a production tree. Use a staging copy."
            )


def warn_if_clipsync_baked() -> bool:
    """Return True if the underlying script still has the ClipSync URL baked in."""
    script = (PACKET_ROOT / "SCRIPTS/imported/html_master_workflow/03_tts_export_helpers/01_inject_tts.py").read_text(encoding="utf-8")
    return bool(re.search(r"clipsync-api\.[a-z0-9.-]+\.workers\.dev", script))


def main() -> int:
    parser = argparse.ArgumentParser(prog="safe_inject_tts.py")
    parser.add_argument("--root", required=True, help="Target folder of HTML files.")
    parser.add_argument("--apply", action="store_true", help="Actually run. Default is dry-run.")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--with-clipsync", action="store_true",
                     help="Explicitly accept that injected widgets POST to the ClipSync worker.")
    grp.add_argument("--no-clipsync", action="store_true",
                     help="Inject TTS only, no ClipSync outbound. NOTE: blocked until a sanitized variant exists.")
    args = parser.parse_args()

    registry = load_registry()
    entry = find_entry(registry, SCRIPT_ID)
    if entry is None:
        raise SystemExit(f"[safe_inject_tts] '{SCRIPT_ID}' missing from script_registry.json")

    root = Path(args.root).resolve()
    refuse_production_root(root)

    if args.no_clipsync and warn_if_clipsync_baked():
        raise SystemExit(
            "[safe_inject_tts] --no-clipsync requested, but the underlying script still bakes "
            "the ClipSync API URL into its TTS_BLOCK constant. Refusing to apply. "
            "Fix path: ship a sanitized TTS_BLOCK variant in the wrapper before re-running."
        )

    glob = entry.get("target_glob") or "*.html"
    targets = discover_targets(root, glob)
    if not targets:
        raise SystemExit(f"[safe_inject_tts] zero targets matched {glob!r} under {root}.")

    stamp = utc_stamp()
    backup_dir = ARCHIVE_ROOT / f"{SCRIPT_ID}-{stamp}"

    if not args.apply:
        records = [
            {"path": str(p), "rel": str(p.relative_to(root)), "bytes_before": p.stat().st_size}
            for p in targets
        ]
        run = run_script(entry, root, dry_run=True)
        manifest = emit_manifest(entry, root, stamp, records, run, applied=False)
        print(f"[safe_inject_tts] DRY-RUN root={root} targets={len(targets)} clipsync={args.with_clipsync}")
        print(f"[safe_inject_tts]   manifest: {manifest}")
        return 0

    print(f"[safe_inject_tts] APPLY root={root} targets={len(targets)} clipsync={args.with_clipsync}")
    records = stage_backups(targets, root, backup_dir)
    run = run_script(entry, root, dry_run=False)
    records = verify_post(records)
    manifest = emit_manifest(entry, root, stamp, records, run, applied=True)
    print(f"[safe_inject_tts]   manifest: {manifest}")
    print(f"[safe_inject_tts]   rollback: python SCRIPTS/wrappers/safe_inplace.py --rollback {manifest}")
    return 0 if run["returncode"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
