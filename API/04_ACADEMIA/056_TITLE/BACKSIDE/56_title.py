"""56_TITLE: standard title + keywords + move for each item, before any CKG (_system/tools/standard_title.py --apply).

With no items it titles the notes waiting in its own INBOX. Folders obey their
_PICK.md like every API station."""
from pathlib import Path
import argparse, subprocess, sys
MAIN = next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir())
TOOL = MAIN / "_system" / "tools" / "standard_title.py"
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="*"); ap.add_argument("--outbox")
    ap.add_argument("--workers", type=int, default=1); ap.add_argument("--focus", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    items = a.items
    if not items:
        inbox = Path(__file__).resolve().parent.parent / "INBOX"
        items = [str(inbox)] if any(inbox.rglob("*.md")) else []
        print(f"56_TITLE: {'titling its INBOX' if items else 'no .md notes waiting in its INBOX; nothing to title'}")
    flags = [] if a.dry_run else ["--apply"]
    flags += ["--all"] if a.all else []
    raise SystemExit(subprocess.run([sys.executable, str(TOOL), *items, *flags]).returncode if items else 0)
