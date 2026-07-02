#!/usr/bin/env python3
"""
safe_inplace.py - Generic safety wrapper for in-place rewrite scripts.

Wraps any imported script whose registry entry names this wrapper. The wrapped
script itself is run unmodified via subprocess; this wrapper provides the four
guarantees the imported scripts lack:

  1. Dry-run by default. --apply is required to invoke the underlying script.
  2. Per-file .bak BEFORE the underlying script runs, into a timestamped
     backup set under <packet>/ARCHIVE/<script_id>-<utc>/.
  3. JSON manifest emitted to OUTPUT/wrap-manifest-<script_id>-<utc>.json
     with per-file {path, status, bytes_before, bytes_after, backup_path}.
  4. --rollback <manifest> restores from a prior backup set.

Usage:
  python SCRIPTS/wrappers/safe_inplace.py --script <id> --root <path>
  python SCRIPTS/wrappers/safe_inplace.py --script <id> --root <path> --apply
  python SCRIPTS/wrappers/safe_inplace.py --rollback OUTPUT/wrap-manifest-...json

Script ids come from CONFIG/script_registry.json. Tiers handled:
  blocked  -> require --apply, full backup+manifest cycle
  wrapped  -> same as blocked (just less paranoid messaging)
  primary  -> wrapper refuses (script is GUI-safe direct, don't wrap)
  deprecated -> wrapper refuses (do not run at all)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


PACKET_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = PACKET_ROOT / "CONFIG" / "script_registry.json"
ARCHIVE_ROOT = PACKET_ROOT / "ARCHIVE"
OUTPUT_ROOT = PACKET_ROOT / "OUTPUT"
ERROR_ROOT = PACKET_ROOT / "ERROR"


def utc_stamp() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def find_entry(registry: dict, script_id: str) -> dict | None:
    for entry in registry.get("scripts", []):
        if entry.get("id") == script_id:
            return entry
    return None


def resolve_root(entry: dict, cli_root: str | None) -> Path:
    """CLI --root wins. Otherwise fall back to target_root_default if it resolves."""
    if cli_root:
        return Path(cli_root).resolve()
    default = entry.get("target_root_default")
    if default and not str(default).startswith("{"):
        return Path(default).resolve()
    raise SystemExit(
        f"[safe_inplace] script '{entry['id']}' has no concrete target_root_default "
        f"({default!r}); pass --root explicitly."
    )


def discover_targets(root: Path, glob: str) -> list[Path]:
    if not root.exists():
        raise SystemExit(f"[safe_inplace] target root does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"[safe_inplace] target root is not a directory: {root}")
    return sorted(p for p in root.glob(glob) if p.is_file())


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def stage_backups(targets: list[Path], root: Path, backup_dir: Path) -> list[dict]:
    backup_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for src in targets:
        rel = src.relative_to(root)
        dst = backup_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        records.append({
            "path": str(src),
            "rel": str(rel),
            "backup_path": str(dst),
            "sha256_before": sha256_of(src),
            "bytes_before": src.stat().st_size,
        })
    return records


def run_script(entry: dict, root: Path, dry_run: bool) -> dict:
    """Invoke the underlying script. CWD is set to root so {script_dir}-style
    scripts behave. If the script roots itself via Path(__file__).parents[1],
    that won't move based on CWD, but the wrapper still owns the backups, so
    the worst case is the script no-ops against an unexpected root."""
    script_path = (PACKET_ROOT / entry["path"]).resolve()
    if not script_path.exists():
        raise SystemExit(f"[safe_inplace] script not found at {script_path}")
    if dry_run:
        return {"invoked": False, "reason": "dry-run", "argv": [sys.executable, str(script_path)], "cwd": str(root)}
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "invoked": True,
        "argv": [sys.executable, str(script_path)],
        "cwd": str(root),
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def verify_post(records: list[dict]) -> list[dict]:
    for rec in records:
        src = Path(rec["path"])
        if not src.exists():
            rec["sha256_after"] = None
            rec["bytes_after"] = 0
            rec["status"] = "MISSING_AFTER"
            continue
        rec["sha256_after"] = sha256_of(src)
        rec["bytes_after"] = src.stat().st_size
        if rec["sha256_after"] == rec["sha256_before"]:
            rec["status"] = "UNCHANGED"
        else:
            rec["status"] = "MODIFIED"
    return records


def emit_manifest(entry: dict, root: Path, stamp: str, records: list[dict], run: dict, applied: bool) -> Path:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT_ROOT / f"wrap-manifest-{entry['id']}-{stamp}.json"
    summary = {
        "MODIFIED": sum(1 for r in records if r.get("status") == "MODIFIED"),
        "UNCHANGED": sum(1 for r in records if r.get("status") == "UNCHANGED"),
        "MISSING_AFTER": sum(1 for r in records if r.get("status") == "MISSING_AFTER"),
        "STAGED_NOT_RUN": sum(1 for r in records if "status" not in r),
    }
    manifest_path.write_text(
        json.dumps({
            "wrapper": "safe_inplace.py",
            "script_id": entry["id"],
            "script_path": entry["path"],
            "safety_tier": entry.get("safety_tier"),
            "target_root": str(root),
            "target_glob": entry.get("target_glob"),
            "utc": stamp,
            "applied": applied,
            "summary": summary,
            "underlying_run": run,
            "files": records,
        }, indent=2),
        encoding="utf-8",
    )
    return manifest_path


def cmd_run(args: argparse.Namespace) -> int:
    registry = load_registry()
    entry = find_entry(registry, args.script)
    if entry is None:
        raise SystemExit(f"[safe_inplace] unknown script id: {args.script}")
    tier = entry.get("safety_tier")
    if tier == "primary":
        raise SystemExit(
            f"[safe_inplace] '{args.script}' is tier=primary; do not wrap. Call it directly."
        )
    if tier == "deprecated":
        raise SystemExit(
            f"[safe_inplace] '{args.script}' is tier=deprecated; refusing to run."
        )
    if tier == "primary-legacy":
        sys.stderr.write(
            f"[safe_inplace] note: '{args.script}' is tier=primary-legacy. "
            f"It will run safely but emits off-spec markers until Phase 0 lands.\n"
        )

    root = resolve_root(entry, args.root)
    glob = entry.get("target_glob") or "**/*"
    targets = discover_targets(root, glob)
    if not targets:
        raise SystemExit(f"[safe_inplace] zero targets matched {glob!r} under {root}.")

    stamp = utc_stamp()
    backup_dir = ARCHIVE_ROOT / f"{entry['id']}-{stamp}"

    if not args.apply:
        # Dry-run: announce what would happen, no IO beyond manifest emit.
        records = [
            {"path": str(p), "rel": str(p.relative_to(root)), "bytes_before": p.stat().st_size}
            for p in targets
        ]
        run = run_script(entry, root, dry_run=True)
        manifest = emit_manifest(entry, root, stamp, records, run, applied=False)
        print(f"[safe_inplace] DRY-RUN script={entry['id']} root={root} targets={len(targets)}")
        print(f"[safe_inplace]   would back up to: {backup_dir}")
        print(f"[safe_inplace]   would invoke:     {run['argv']} (cwd={run['cwd']})")
        print(f"[safe_inplace]   manifest:         {manifest}")
        return 0

    print(f"[safe_inplace] APPLY script={entry['id']} root={root} targets={len(targets)}")
    print(f"[safe_inplace]   staging backups -> {backup_dir}")
    records = stage_backups(targets, root, backup_dir)
    print(f"[safe_inplace]   invoking underlying script...")
    run = run_script(entry, root, dry_run=False)
    records = verify_post(records)
    manifest = emit_manifest(entry, root, stamp, records, run, applied=True)
    modified = sum(1 for r in records if r["status"] == "MODIFIED")
    unchanged = sum(1 for r in records if r["status"] == "UNCHANGED")
    missing = sum(1 for r in records if r["status"] == "MISSING_AFTER")
    print(f"[safe_inplace]   modified={modified} unchanged={unchanged} missing_after={missing}")
    print(f"[safe_inplace]   manifest: {manifest}")
    print(f"[safe_inplace]   rollback: python {Path(__file__).name} --rollback {manifest}")
    if run["returncode"] != 0:
        print(f"[safe_inplace]   warning: underlying script exited {run['returncode']}", file=sys.stderr)
    return 0 if run["returncode"] == 0 and missing == 0 else 1


def cmd_rollback(args: argparse.Namespace) -> int:
    manifest_path = Path(args.rollback).resolve()
    if not manifest_path.exists():
        raise SystemExit(f"[safe_inplace] manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not manifest.get("applied"):
        raise SystemExit(f"[safe_inplace] manifest is from a dry-run; nothing to roll back.")
    restored = 0
    failed = []
    for rec in manifest.get("files", []):
        src_backup = Path(rec["backup_path"])
        dst = Path(rec["path"])
        if not src_backup.exists():
            failed.append((str(dst), "backup missing"))
            continue
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_backup, dst)
            restored += 1
        except OSError as e:
            failed.append((str(dst), str(e)))
    print(f"[safe_inplace] ROLLBACK manifest={manifest_path.name} restored={restored} failed={len(failed)}")
    if failed:
        ERROR_ROOT.mkdir(parents=True, exist_ok=True)
        err_log = ERROR_ROOT / f"rollback-failures-{utc_stamp()}.json"
        err_log.write_text(json.dumps(failed, indent=2), encoding="utf-8")
        print(f"[safe_inplace]   failures logged to: {err_log}")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="safe_inplace.py",
        description="Generic safety wrapper for in-place rewrite scripts.",
    )
    parser.add_argument("--script", help="Script id from CONFIG/script_registry.json")
    parser.add_argument("--root", help="Target root directory. Overrides target_root_default.")
    parser.add_argument("--apply", action="store_true",
                        help="Actually run the underlying script. Default is dry-run.")
    parser.add_argument("--rollback", metavar="MANIFEST",
                        help="Restore files from a prior apply manifest. Skips --script/--root/--apply.")
    args = parser.parse_args()

    if args.rollback:
        return cmd_rollback(args)
    if not args.script:
        parser.error("--script is required (or use --rollback)")
    return cmd_run(args)


if __name__ == "__main__":
    raise SystemExit(main())
