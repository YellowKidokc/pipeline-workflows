"""manifest_tracker.py — Rebuild MANIFEST.json from packet STATUS.json files.

Scans one or more packet roots (folders whose children are workflow packets,
each holding a STATUS.json), and writes a MANIFEST.json conforming to
schemas/manifest.schema.json. The orchestrator updates the manifest
incrementally; this tool rebuilds it from the ground truth on disk.

Usage:
    python scripts/manifest_tracker.py workflows/                 # scan + write MANIFEST.json
    python scripts/manifest_tracker.py X:\\WORKFLOWS --dry-run    # print, don't write
    python scripts/manifest_tracker.py rootA rootB -o MANIFEST.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "MANIFEST.json"
STATES = ["active", "completed", "failed", "review", "hold"]


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def find_status_files(roots: list[Path]) -> list[Path]:
    found = []
    for root in roots:
        if not root.exists():
            print(f"warning: packet root does not exist: {root}", file=sys.stderr)
            continue
        if (root / "STATUS.json").is_file():
            found.append(root / "STATUS.json")
            continue
        for child in sorted(root.iterdir()):
            status = child / "STATUS.json"
            if child.is_dir() and status.is_file():
                found.append(status)
    return found


def packet_entry(status_path: Path) -> dict | None:
    try:
        status = json.loads(status_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"warning: unreadable STATUS.json at {status_path}: {exc}", file=sys.stderr)
        return None
    input_dir = status_path.parent / "INPUT"
    file_count = sum(1 for p in input_dir.rglob("*") if p.is_file()) if input_dir.exists() else 0
    return {
        "id": status.get("packet_id", status_path.parent.name),
        "workflow": status.get("workflow", "unknown"),
        "current_stage": status.get("current_stage", "pending"),
        "status": status.get("status", "active"),
        "created_at": status.get("started_at", utcnow()),
        "updated_at": status.get("updated_at", status.get("completed_at") or utcnow()),
        "file_count": file_count,
        "input_hash": status.get("input_hash", ""),
    }


def build_manifest(roots: list[Path]) -> dict:
    packets = [e for e in (packet_entry(p) for p in find_status_files(roots)) if e]
    return {
        "updated_at": utcnow(),
        "packets": packets,
        "summary": {state: sum(1 for p in packets if p["status"] == state) for state in STATES},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild MANIFEST.json from packet STATUS.json files.")
    parser.add_argument("roots", nargs="+", help="Packet root folder(s) to scan")
    parser.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--dry-run", action="store_true", help="Print the manifest, do not write")
    args = parser.parse_args(argv)

    manifest = build_manifest([Path(r) for r in args.roots])
    payload = json.dumps(manifest, indent=2)
    if args.dry_run:
        print(payload)
    else:
        out = Path(args.output)
        tmp = out.with_suffix(out.suffix + ".tmp")
        tmp.write_text(payload + "\n", encoding="utf-8")
        tmp.replace(out)
        print(f"{len(manifest['packets'])} packet(s) -> {out}")
        print(json.dumps(manifest["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
