"""Apply an approved repo move plan.

Input format:
[
  {"from": "old/path", "to": "new/path", "approved": true}
]

This script refuses paths outside the repo and skips unapproved moves.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def resolve_inside_repo(path: str) -> Path:
    resolved = (REPO_ROOT / path).resolve()
    if not str(resolved).lower().startswith(str(REPO_ROOT.resolve()).lower()):
        raise ValueError(f"refusing path outside repo: {path}")
    return resolved


def move_one(src_rel: str, dst_rel: str, dry_run: bool) -> str:
    src = resolve_inside_repo(src_rel)
    dst = resolve_inside_repo(dst_rel)
    if not src.exists():
        return f"missing: {src_rel}"
    if dst.exists():
        return f"exists: {dst_rel}"
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
    return f"moved: {src_rel} -> {dst_rel}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", help="JSON file containing approved moves")
    parser.add_argument("--execute", action="store_true", help="Actually move files")
    args = parser.parse_args()

    plan_path = resolve_inside_repo(args.plan)
    moves = json.loads(plan_path.read_text(encoding="utf-8"))
    dry_run = not args.execute
    for move in moves:
        if move.get("approved") is not True:
            print(f"skip unapproved: {move.get('from')} -> {move.get('to')}")
            continue
        print(move_one(move["from"], move["to"], dry_run=dry_run))
    if dry_run:
        print("dry run only; pass --execute to apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
