"""Corpus puller: search everything the API has produced, COPY hits to a destination.
Never moves or deletes. History of past search terms (with hit counts) is shown at
launch so you can see what has worked before. History: SCRIPTS\\pull_history.json
"""
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent  # LEAN4

# Console-proof printing: Greek letters etc. in filenames must never crash a run.
try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass

# Every place API output lands. Add lines freely; missing paths are skipped.
SCAN_ROOTS = [
    Path(str(Path(__file__).resolve().parents[2] / 'LEAN4/OUTBOX/READING_LIBRARY')),
    ROOT / "OUTBOX",
    Path(str(Path(__file__).resolve().parents[2] / 'EVIDENCE/OUTBOX')),
    Path(str(Path(__file__).resolve().parents[2] / 'LEAN4/OUTBOX')),
]
DEST_BASE = Path(str(Path(__file__).resolve().parents[2] / 'LEAN4/OUTBOX/SELECTED_PAPERS'))
HISTORY = SCRIPTS / "pull_history.json"
EXTS = {".md", ".txt"}
MAX_BYTES = 2_000_000  # skip huge files (MASTER_LIST.csv etc. are indexes, not papers)
SKIP_DIRS = {".lake", ".git", ".venv", "__pycache__", "node_modules", "_support"}


def load_history():
    try:
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"terms": []}


def save_history(hist):
    HISTORY.write_text(json.dumps(hist, indent=2, ensure_ascii=False), encoding="utf-8")


def slugify(term):
    return re.sub(r"[^A-Za-z0-9]+", "_", term).strip("_").upper() or "PULL"


def iter_files():
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                p = Path(dirpath) / name
                if p.suffix.lower() in EXTS:
                    yield p


def matches(path, needle):
    """Hit on filename or (for small files) content, case-insensitive."""
    if needle in path.name.lower():
        return True
    try:
        if path.stat().st_size > MAX_BYTES:
            return False
        text = path.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return False
    return needle in text


def copy_hit(src, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if dest.exists():
        try:
            if dest.stat().st_size == src.stat().st_size:
                return dest, False  # same-size copy already there
        except OSError:
            pass
        dest = dest_dir / f"{src.stem}__{abs(hash(str(src))) % 99999}{src.suffix}"
    shutil.copy2(src, dest)  # COPY, never move
    return dest, True


def main():
    hist = load_history()
    print("=" * 70)
    print(" CORPUS PULLER — searches all API output, COPIES hits (never cuts)")
    print("=" * 70)
    if hist["terms"]:
        print("\nPrevious pulls that had hits:")
        for t in sorted(hist["terms"], key=lambda x: x.get("last_run", ""), reverse=True):
            print(f"  {t['hits']:>4} hits  {t['term']}   (last: {t.get('last_run','?')[:10]})")
    else:
        print("\nNo previous pulls yet.")
    term = input("\nWhat do you want to pull now? (words to search, blank = quit): ").strip()
    if not term:
        return 0
    needle = term.lower()
    dest_dir = DEST_BASE / slugify(term)
    print(f"\nSearching for '{term}' ... copies go to:\n  {dest_dir}\n")
    hits = copied = 0
    for path in iter_files():
        if matches(path, needle):
            hits += 1
            dest, was_new = copy_hit(path, dest_dir)
            tag = "COPIED " if was_new else "already"
            print(f"  [{tag}] {path}")
    print(f"\nDone: {hits} hit(s), destination: {dest_dir}")

    # Record the term in history (kept even at 0 hits, so misspellings are visible)
    for t in hist["terms"]:
        if t["term"].lower() == needle:
            t["hits"] = hits
            t["last_run"] = datetime.now().isoformat(timespec="seconds")
            break
    else:
        hist["terms"].append({
            "term": term,
            "hits": hits,
            "last_run": datetime.now().isoformat(timespec="seconds"),
            "destination": str(dest_dir),
        })
    save_history(hist)
    return 0


if __name__ == "__main__":
    sys.exit(main())
