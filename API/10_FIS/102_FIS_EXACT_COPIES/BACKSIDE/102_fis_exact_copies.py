"""102_FIS_EXACT_COPIES: FIS stage 3 (exact copies: size, then SHA-256), a thin wrapper around
David-OSv3's understand.find_duplicates.

  python 102_fis_exact_copies.py              PLAN: which scan, how many same-size candidates (nothing hashed)
  python 102_fis_exact_copies.py --apply      hash the candidates of that scan and report the copy groups

Works on the scan 101 made (101's OUTBOX/_last_scan.txt), else the newest scan, or --scan N. Collection roots
(D:\\CHI PARTS) are left out. Every location of every copy is kept and listed: nothing is chosen, moved or deleted
here. Which copy is best is decided later, from this inventory. Files that cannot be read while hashing are listed
with the reason. Output: the FIS database (dup_groups, files.sha256) and this OUTBOX.
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine import fis  # noqa: E402

FRONT = Path(__file__).resolve().parents[1]
INVENTORY_OUTBOX = FRONT.parent / "101_FIS_INVENTORY" / "OUTBOX"


def root_of(path: str, roots: list[str]) -> str:
    best = ""
    for r in roots:
        rn = os.path.normcase(os.path.normpath(r))
        pn = os.path.normcase(os.path.normpath(path))
        if (pn == rn or pn.startswith(rn + os.sep)) and len(r) > len(best):
            best = r
    return best or "(outside the scanned roots)"


def main() -> int:
    ap = argparse.ArgumentParser(description="FIS stage 3: exact copies by size + SHA-256 (dry run by default)")
    ap.add_argument("items", nargs="*", help="(ignored: this station works on a scan, not on notes)")
    ap.add_argument("--scan", type=int, help="scan id (default: 101's last scan, else the newest)")
    ap.add_argument("--apply", action="store_true", help="really hash (default: plan only)")
    ap.add_argument("--db", help="FIS database (default: David-OSv3/.data/fis_understand.sqlite)")
    ap.add_argument("--outbox", help="where the report goes (default: this station's OUTBOX)")
    ap.add_argument("--dry-run", action="store_true", help="plan only (the default; overrides --apply)")
    a = ap.parse_args()
    a.apply = a.apply and not a.dry_run
    out = Path(a.outbox) if a.outbox else FRONT / "OUTBOX"
    understand, _ = fis.engine()
    db = Path(a.db) if a.db else fis.default_db()
    if not db.is_file():
        print(f"No FIS database at {db}: run 101_FIS_INVENTORY first.")
        return 2
    con = understand.connect(db)
    scan_id = a.scan or fis.last_scan(con, INVENTORY_OUTBOX)
    if not scan_id:
        print("No scan yet: run 101_FIS_INVENTORY first.")
        return 2
    roots = fis.scan_roots(con, scan_id)
    skip = fis.collection_roots(con, scan_id)
    cand = con.execute("SELECT COUNT(*), COALESCE(SUM(c),0) FROM (SELECT COUNT(*) c FROM files WHERE scan_id=? AND size>0 "
                       "GROUP BY size HAVING COUNT(*)>1)", (scan_id,)).fetchone()
    stamp = datetime.now().strftime("%Y-%m-%d %H%M")
    head = [f"# FIS exact copies · scan {scan_id} · {'RUN' if a.apply else 'PLAN (dry run, nothing hashed)'} · {stamp}", "",
            f"Roots: {', '.join(f'`{r}`' for r in roots)}", f"Left out (collections): {', '.join(f'`{r}`' for r in skip) or 'none'}",
            f"Same-size candidates: {cand[0]:,} sizes, {cand[1]:,} files (only these are hashed).", ""]
    print("\n".join(head))
    if not a.apply:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"FIS EXACT COPIES · PLAN · scan {scan_id} · {stamp}.md").write_text("\n".join(head) + "\nAdd --apply to hash.\n", encoding="utf-8")
        return 0
    fis.protect([fis.Root(r, "register") for r in roots], db, out)
    understand.find_duplicates(con, scan_id, print, skip)
    groups = con.execute("SELECT sha256, size, n, paths FROM dup_groups WHERE scan_id=? ORDER BY n*size DESC", (scan_id,)).fetchall()
    unreadable = con.execute("SELECT path, reason FROM skipped WHERE scan_id=? AND reason='unreadable while hashing'", (scan_id,)).fetchall()
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / f"FIS EXACT COPIES · scan {scan_id} · {stamp}.csv"
    pairs: Counter = Counter()
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["group", "sha256", "size", "copies", "root", "path"])
        for i, (h, size, n, paths) in enumerate(groups, 1):
            ps = json.loads(paths)
            where = sorted({root_of(p, roots) for p in ps})
            for x in range(len(where)):
                for y in range(x + 1, len(where)):
                    pairs[(where[x], where[y])] += 1
            if len(where) == 1:
                pairs[(where[0], where[0])] += 1
            for p in ps:
                w.writerow([i, h, size, n, root_of(p, roots), p])
    redundant = sum(n - 1 for _, _, n, _ in groups)
    mb = sum((n - 1) * size for _, size, n, _ in groups) / 1e6
    lines = head + [f"**{len(groups):,} copy groups · {redundant:,} redundant copies · {mb:,.1f} MB held more than once.**", "",
                    "Every location is kept and listed in the CSV next to this file. Nothing was chosen, moved or deleted.", "",
                    "## Where the copies are (groups by root pair)", "", "| root | root | groups |", "|---|---|---|"]
    lines += [f"| `{a_}` | `{b_}`{' (inside one root)' if a_ == b_ else ''} | {c:,} |" for (a_, b_), c in pairs.most_common()]
    lines += ["", f"## Biggest groups (of {len(groups):,})", ""]
    for i, (h, size, n, paths) in enumerate(groups[:50], 1):
        lines.append(f"{i}. {n} copies × {size / 1e6:,.2f} MB · `{h[:12]}`")
        lines += [f"   - `{p}`" for p in json.loads(paths)]
    lines += ["", f"## Unreadable while hashing ({len(unreadable)})", ""] + ([f"- `{p}`" for p, _ in unreadable] or ["none"])
    report = out / f"FIS EXACT COPIES · scan {scan_id} · {stamp}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(groups):,} copy groups, {redundant:,} redundant copies, {mb:,.1f} MB. Report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
