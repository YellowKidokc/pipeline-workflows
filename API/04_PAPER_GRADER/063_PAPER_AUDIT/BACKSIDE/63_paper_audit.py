"""63_PAPER_AUDIT: one paper through the whole audit, station after station, into one OUTBOX.

The steps are the "chain" list in station.json (edit it to add, drop or reorder a step). Each step is the real
station, run the way its own button runs it, wherever its front folder has been moved.

The two buttons (`1 RUN HERE`, `2 RUN ON FOLDER`) do the same through engine/button.py and ask the usual questions.
No questions:  python BACKSIDE\\63_paper_audit.py <papers or folder> --outbox <folder> --workers 8
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "_system").is_dir()) / "_system"))
from engine import button, pick  # noqa: E402


def main() -> int:
    st = json.loads((HERE / "station.json").read_text(encoding="utf-8"))
    p = argparse.ArgumentParser(prog=st["label"], description=st["description"])
    p.add_argument("items", nargs="*", help="papers, folders of papers, or @list.txt (default: this INBOX)")
    p.add_argument("--outbox", "--out", dest="out", help=f"default {FRONT / 'OUTBOX'}")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--limit", type=int)
    p.add_argument("--focus", action="append", default=[])
    p.add_argument("--dry-run", action="store_true", help="list the papers and the steps; run nothing")
    a = p.parse_args()
    notes = [n for n in pick.resolve(a.items or [str(FRONT / "INBOX")]) if n.suffix.lower() in (".md", ".txt")]
    notes = notes[:a.limit] if a.limit else notes
    if not notes:
        print(f"{st['label']}: no papers. Drop .md files into {FRONT / 'INBOX'} or pass them.")
        return 0
    print(f"{st['label']}: {len(notes)} paper(s) through {' > '.join(st['chain'])}")
    if a.dry_run:
        for n in notes:
            print("PLAN", n)
        return 0
    return button.run_station(FRONT, st, notes, Path(a.out) if a.out else FRONT / "OUTBOX", a.workers, a.focus)


if __name__ == "__main__":
    raise SystemExit(main())
