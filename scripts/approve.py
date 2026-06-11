"""approve.py — Human approval gate helper.

Lists packets holding at _await_approval and writes the approval/rejection
files for you, so the human-in-the-loop step is one command instead of
hand-edited JSON. Corrections recorded here are BIL training data.

Usage:
    python scripts/approve.py <root> [...roots]            # list held packets
    python scripts/approve.py <packet> --yes               # approve
    python scripts/approve.py <packet> --yes --by David
    python scripts/approve.py <packet> --no --reason "wrong domain"
    python scripts/approve.py <packet> --yes \
        --correct old_route=REVIEW/ --correct new_route=OUTPUT/vault/ \
        --file INPUT/paper.md --reason "clearly a framework paper"

After approving, re-run the same orchestrator command; the held stage
re-runs, picks up the approval, and the workflow continues.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_CORRECTION_KEYS = {
    "old_verdict", "new_verdict", "old_route", "new_route",
    "old_domain", "new_domain", "old_subject", "new_subject",
}


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def is_packet(path: Path) -> bool:
    return (path / "STATUS.json").is_file()


def find_held(roots: list[Path]) -> list[tuple[Path, dict]]:
    held = []
    for root in roots:
        candidates = [root] if is_packet(root) else sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []
        for packet in candidates:
            if not is_packet(packet):
                continue
            try:
                status = load_json(packet / "STATUS.json")
            except (OSError, json.JSONDecodeError):
                continue
            if status.get("status") == "hold":
                held.append((packet, status))
    return held


def list_held(roots: list[Path]) -> int:
    held = find_held(roots)
    if not held:
        print("No packets waiting for approval.")
        return 0
    print(f"{len(held)} packet(s) waiting for approval:\n")
    for packet, status in held:
        print(f"  {packet}")
        print(f"      workflow: {status.get('workflow')}   held at: {status.get('current_stage')}")
        last = (status.get("history") or [{}])[-1]
        if last.get("notes"):
            print(f"      note: {last['notes'][:120]}")
    print(f"\nApprove with:  python scripts/approve.py <packet> --yes")
    return 0


def decide(packet: Path, approved: bool, by: str, reason: str, corrections: dict, file_path: str, stage: str) -> int:
    if not is_packet(packet):
        print(f"error: {packet} has no STATUS.json — not a packet", file=sys.stderr)
        return 1

    if corrections:
        bad = set(corrections) - VALID_CORRECTION_KEYS
        if bad:
            print(f"error: unknown correction field(s): {', '.join(sorted(bad))}", file=sys.stderr)
            print(f"valid: {', '.join(sorted(VALID_CORRECTION_KEYS))}", file=sys.stderr)
            return 1
        review_dir = packet / "REVIEW"
        review_dir.mkdir(parents=True, exist_ok=True)
        corrections_file = review_dir / "corrections.json"
        existing = []
        if corrections_file.exists():
            existing = load_json(corrections_file)
            if isinstance(existing, dict):
                existing = [existing]
        if not file_path:
            first = next((p for p in sorted((packet / "INPUT").rglob("*")) if p.is_file()), None)
            file_path = str(first) if first else str(packet / "INPUT")
        entry = {"file_path": file_path, "stage": stage, "reason": reason, **corrections}
        existing.append(entry)
        corrections_file.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        print(f"correction recorded -> {corrections_file}")

    config_dir = packet / "CONFIG"
    config_dir.mkdir(parents=True, exist_ok=True)
    decision = {"approved": approved, "by": by, "at": utcnow()}
    if reason:
        decision["reason"] = reason
    (config_dir / "approval.json").write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
    verdict = "APPROVED" if approved else "REJECTED"
    print(f"{verdict} -> {config_dir / 'approval.json'}")

    workflow = ""
    try:
        workflow = load_json(packet / "STATUS.json").get("workflow", "")
    except (OSError, json.JSONDecodeError):
        pass
    print(f"resume with:  python scripts/orchestrator.py {workflow or '<workflow>'} {packet}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List or decide packets held at the human approval gate.")
    parser.add_argument("paths", nargs="+", help="Packet folder (to decide) or packet root(s) (to list)")
    parser.add_argument("--yes", action="store_true", help="Approve the packet")
    parser.add_argument("--no", dest="reject", action="store_true", help="Reject the packet")
    parser.add_argument("--by", default="David", help="Who decided (default: David)")
    parser.add_argument("--reason", default="", help="Why — becomes BIL training signal on corrections/rejections")
    parser.add_argument("--correct", action="append", default=[], metavar="FIELD=VALUE",
                        help=f"Correction field, repeatable. Fields: {', '.join(sorted(VALID_CORRECTION_KEYS))}")
    parser.add_argument("--file", default="", help="File the correction applies to")
    parser.add_argument("--stage", default="propose-route", help="Stage the correction applies to")
    args = parser.parse_args(argv)

    if args.yes and args.reject:
        parser.error("--yes and --no are mutually exclusive")

    if not args.yes and not args.reject:
        return list_held([Path(p) for p in args.paths])

    if len(args.paths) != 1:
        parser.error("decide mode takes exactly one packet folder")
    if args.reject and not args.reason:
        parser.error("--no requires --reason (rejections teach BIL too)")

    corrections = {}
    for item in args.correct:
        if "=" not in item:
            parser.error(f"--correct expects FIELD=VALUE, got: {item}")
        key, value = item.split("=", 1)
        corrections[key.strip()] = value.strip()

    return decide(Path(args.paths[0]), args.yes, args.by, args.reason, corrections, args.file, args.stage)


if __name__ == "__main__":
    sys.exit(main())
