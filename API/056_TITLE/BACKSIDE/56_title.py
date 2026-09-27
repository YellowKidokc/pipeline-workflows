"""56_TITLE: standard title + keywords + move for each item, before any CKG (_system/tools/standard_title.py --apply).

With no items (as in a routine) it titles the notes waiting in its own INBOX and the inboxes of the stations
that run after it, so the standard name is in place before any run folder is named after the source.
Folders obey their _PICK.md like every API station."""
from pathlib import Path
import subprocess, sys
MAIN = Path(__file__).resolve().parents[2]
TOOL = MAIN / "_system" / "tools" / "standard_title.py"
INBOXES = ["056_TITLE", "057_API_DEEP", "058_ARGUMENT_GRADE"]
if __name__ == "__main__":
    items = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not items:
        items = [str(d) for d in (MAIN / n / "INBOX" for n in INBOXES) if d.is_dir() and any(d.rglob("*.md"))]
        print(f"56_TITLE: {'titling ' + ', '.join(items) if items else 'no .md notes waiting in the inboxes; nothing to title'}")
    raise SystemExit(subprocess.run([sys.executable, str(TOOL), *items, "--apply"]).returncode if items else 0)
