"""101_FIS_INVENTORY: FIS stage 1 (inventory), a thin wrapper around David-OSv3's engine/understand.py.

  python 101_fis_inventory.py                      roots from INBOX lists, else the registered FIS roots: PLAN only
  python 101_fis_inventory.py D:\\some\\root --apply  inventory that root into the FIS database

Default is a dry run: the plan (each root, its treatment, whether it can be read) goes to OUTBOX and nothing else
happens. --apply runs understand.scan(..., dedupe=False) over every root to register, in ONE scan, so 102 can match
copies across roots. Roots registered as a collection (D:\\CHI PARTS) are inventoried and recorded as one collection;
102 and 103 leave them out. Roots marked skip are not walked. Every root is read-only (path_write_policy); output
goes to the FIS database and this OUTBOX only. Unreadable files and folders are listed with the reason.

Stage 2 (identify + extract: real format, text, headings) is not in the engine yet; this station does not invent it.
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine import fis  # noqa: E402

FRONT = Path(__file__).resolve().parents[1]


def readable(path: str) -> str:
    if not os.path.exists(path):
        return "missing"
    if not os.path.isdir(path):
        return "not a folder"
    try:
        next(os.scandir(path), None)
        return "ok"
    except OSError as e:
        return f"unreadable: {e.__class__.__name__}"


def main() -> int:
    ap = argparse.ArgumentParser(description="FIS stage 1: inventory roots into the FIS database (dry run by default)")
    ap.add_argument("roots", nargs="*", help="folders to inventory (default: INBOX lists, else the registered FIS roots)")
    ap.add_argument("--apply", action="store_true", help="really scan (default: plan only)")
    ap.add_argument("--db", help="FIS database (default: David-OSv3/.data/fis_understand.sqlite)")
    ap.add_argument("--outbox", help="where the report goes (default: this station's OUTBOX)")
    ap.add_argument("--max-files", type=int, help="stop after this many files (for a test run)")
    ap.add_argument("--dry-run", action="store_true", help="plan only (the default; overrides --apply)")
    a = ap.parse_args()
    a.apply = a.apply and not a.dry_run
    out = Path(a.outbox) if a.outbox else FRONT / "OUTBOX"
    roots = fis.chosen_roots([r for r in a.roots if not r.startswith("@")], FRONT)
    db = Path(a.db) if a.db else fis.default_db()
    if not roots:
        print("No roots: drop a .txt list of folders in INBOX, register them in folder_registry.yaml (fis: register), "
              "or name one on the command line.")
        return 0
    plan = [(r, readable(r.path)) for r in roots]
    walk = [r for r, state in plan if r.treatment in ("register", "collection") and state == "ok"]
    stamp = datetime.now().strftime("%Y-%m-%d %H%M")
    lines = [f"# FIS inventory · {'RUN' if a.apply else 'PLAN (dry run, nothing scanned)'} · {stamp}", "",
             f"Database: `{db}`", "", "| root | treatment | readable | source | note |", "|---|---|---|---|---|"]
    lines += [f"| `{r.path}` | {r.treatment}{' (' + r.collection + ')' if r.collection else ''} | {state} | {r.source} | {r.note} |"
              for r, state in plan]
    lines += ["", f"{len(walk)} root(s) to walk in one scan; skipped or unreadable roots are not walked.",
              "Stage 2 (identify + extract) is not in the engine yet."]
    for r, state in plan:
        print(f"  {r.treatment:<10} {state:<22} {r.path}")
    if not a.apply:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"FIS INVENTORY · PLAN · {stamp}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Plan only. Add --apply to scan. Plan: {out}")
        return 0
    if not walk:
        print("Nothing readable to walk.")
        return 1
    fis.protect(walk, db, out)                      # read-only on every root; refuse output inside one
    understand, _ = fis.engine()
    con = understand.connect(db)
    scan_id = understand.scan([r.path for r in walk], con, max_files=a.max_files, dedupe=False)
    for r in walk:
        if r.treatment == "collection":
            con.execute("INSERT INTO observations VALUES (?,?,?,?,?)",
                        (scan_id, os.path.normpath(r.path), "collection", r.collection or "collection", "folder_registry"))
    con.commit()
    stats = json.loads(con.execute("SELECT stats FROM scans WHERE scan_id=?", (scan_id,)).fetchone()[0] or "{}")
    skipped = con.execute("SELECT path, reason FROM skipped WHERE scan_id=? AND reason!='excluded dir' ORDER BY path",
                          (scan_id,)).fetchall()
    per_root = []
    for r in walk:
        n = con.execute("SELECT total_files, total_bytes FROM folders WHERE scan_id=? AND path=?",
                        (scan_id, os.path.normpath(r.path))).fetchone()
        per_root.append((r.path, n[0] if n else 0, (n[1] if n else 0) / 1e6))
    lines += ["", f"## Scan {scan_id}", "", f"{stats.get('files', 0):,} files · {stats.get('folders', 0):,} folders · "
              f"{stats.get('seconds', 0)} s", "", "| root | files | MB |", "|---|---|---|"]
    lines += [f"| `{p}` | {n:,} | {mb:,.1f} |" for p, n, mb in per_root]
    lines += ["", f"## Unreadable ({len(skipped)})", ""] + ([f"- `{p}`: {why}" for p, why in skipped[:2000]] or ["none"])
    if len(skipped) > 2000:
        lines.append(f"- … {len(skipped) - 2000:,} more in the database (table `skipped`, scan {scan_id})")
    fis.save_scan(out, scan_id)
    report = out / f"FIS INVENTORY · scan {scan_id} · {stamp}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Scan {scan_id}: {stats.get('files', 0):,} files, {len(skipped)} unreadable. Report: {report}")
    print("Next: 102_FIS_EXACT_COPIES on this scan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
