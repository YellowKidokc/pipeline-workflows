"""47_NEW_PAPER: create the per-paper working folder from templates/PAPER_FOLDER, then tag it (44)."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.items import create_paper  # noqa: E402

TEXT = {".md", ".txt", ".html", ".htm", ".tex"}


def main() -> int:
    p = argparse.ArgumentParser(prog="47_NEW_PAPER", description="Create per-paper working folders")
    p.add_argument("sources", nargs="*", help="paper files, or folders of papers")
    p.add_argument("--title")
    p.add_argument("--id")
    p.add_argument("--series", default="")
    p.add_argument("--own", action="store_true", help="mark as David's own work (used by 49 GAP_MAP)")
    p.add_argument("--no-tag", action="store_true", help="skip the automatic tagging")
    p.add_argument("--workers", type=int, default=1, help="accepted for the shared front door; creation is serial")
    p.add_argument("--provider", help="accepted for the shared front door; this station is local")
    p.add_argument("--model", help="accepted for the shared front door; this station is local")
    p.add_argument("--focus", action="append", default=[], help="accepted for the shared front door")
    p.add_argument("--outbox", help="accepted for the shared front door; paper folders use papers_root")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    files = []
    for raw in a.sources:
        if raw.startswith("@"):
            listing = Path(raw[1:])
            if listing.is_file():
                files += [Path(line.strip()) for line in listing.read_text(encoding="utf-8").splitlines()
                          if line.strip() and Path(line.strip()).is_file()]
            continue
        path = Path(raw).expanduser()
        files += sorted(f for f in path.rglob("*") if f.suffix.lower() in TEXT) if path.is_dir() else [path]
    if not files:
        print("47_NEW_PAPER: give one or more paper files or folders (ONE_MENU.bat 47 --item paper.md)")
        return 2
    created, failed = [], 0
    for f in files:
        if a.dry_run:
            print(f"  would create a folder for {f}")
            continue
        try:
            item = create_paper(f, title=a.title if len(files) == 1 else None, paper_id=a.id if len(files) == 1 else None,
                                series=a.series, own=a.own)
            created.append(item)
            print(f"  OK  {item.folder}")
        except (OSError, ValueError) as exc:
            failed += 1
            print(f"  ERR {f}: {exc}")
    if created and not a.no_tag:
        from engine.tagger import tag_local
        for item in created:
            tag_local(item)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
