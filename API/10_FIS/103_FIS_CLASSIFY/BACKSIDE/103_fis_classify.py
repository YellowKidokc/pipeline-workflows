"""103_FIS_CLASSIFY: classify by rules first, the LLM only for what rules leave unresolved; a thin wrapper around
David-OSv3's engine/understand.py.

  python 103_fis_classify.py              rules results + the packets that WOULD go to Forge (nothing sent)
  python 103_fis_classify.py --apply      send the unresolved folders to Forge, store the answers

Rules: understand.scan already ran them when 101 inventoried (folder kind + domain, with evidence and denominators;
registry answers win). Unresolved = the open questions it raised (low confidence, enough files, near the top).
Those go to Forge, POST {FORGE_URL}/v1/chat/completions (default http://127.0.0.1:8790) through
understand.escalate_forge: folder name, file names, extension mix. Never file contents. No provider URL or key here.
Answers are stored as shadow inferences (source llm:forge); nothing on disk changes. Collection roots
(D:\\CHI PARTS) are left out.

The engine classifies FOLDERS. Per-document classification (spec stage 4: doc type, subjects, version) is not in the
engine yet; this station does not invent it.
"""
import argparse
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


def under(path: str, roots: list[str]) -> bool:
    p = os.path.normcase(os.path.normpath(path))
    return any(p == os.path.normcase(os.path.normpath(r)) or p.startswith(os.path.normcase(os.path.normpath(r)) + os.sep)
               for r in roots)


def main() -> int:
    ap = argparse.ArgumentParser(description="FIS classify: rules first, Forge only for the unresolved (dry run by default)")
    ap.add_argument("items", nargs="*", help="(ignored: this station works on a scan, not on notes)")
    ap.add_argument("--scan", type=int, help="scan id (default: 101's last scan, else the newest)")
    ap.add_argument("--apply", action="store_true", help="send the unresolved folders to Forge (default: show the packets only)")
    ap.add_argument("--limit", type=int, default=25, help="at most this many folders to Forge per run (default 25)")
    ap.add_argument("--model", default=os.environ.get("FORGE_CHAT_MODEL", "default"), help="model name Forge routes")
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
    collections = fis.collection_roots(con, scan_id)
    fis.protect([fis.Root(r, "register") for r in roots], db, out)
    if collections and a.apply:                       # collections are inventory-only: their questions are closed, not sent
        n = 0
        for qid, folder in con.execute("SELECT qid, folder FROM questions WHERE scan_id=? AND status='open'", (scan_id,)).fetchall():
            if under(folder, collections):
                con.execute("UPDATE questions SET status='collection' WHERE qid=?", (qid,))
                n += 1
        con.commit()
        if n:
            print(f"  {n} question(s) inside collection roots closed as 'collection' (not sent to Forge)")
    kinds = con.execute("SELECT f.path, f.total_files, i.value, i.confidence, i.source, i.evidence FROM folders f "
                        "JOIN inferences i ON i.scan_id=f.scan_id AND i.folder=f.path AND i.facet='kind' "
                        "WHERE f.scan_id=? AND f.depth<=2 AND f.total_files>0 ORDER BY f.path", (scan_id,)).fetchall()
    rules = [k for k in kinds if not str(k[4]).startswith("llm:")]
    by_source = Counter(k[4] for k in rules)
    open_q = con.execute("SELECT COUNT(*) FROM questions WHERE scan_id=? AND status='open'", (scan_id,)).fetchone()[0]
    packets = understand.escalate_forge(con, scan_id, print, model=a.model, limit=a.limit, dry_run=not a.apply)
    packets = [p for p in packets if not under(p["folder"], collections)]   # dry run: the database was not touched
    llm = con.execute("SELECT folder, value, confidence, source FROM inferences WHERE scan_id=? AND facet='kind' "
                      "AND source LIKE 'llm:forge:%' ORDER BY folder", (scan_id,)).fetchall()
    errors = con.execute("SELECT folder, response FROM llm_requests WHERE scan_id=? AND provider LIKE 'forge:%' AND status='error'",
                         (scan_id,)).fetchall()
    stamp = datetime.now().strftime("%Y-%m-%d %H%M")
    lines = [f"# FIS classify · scan {scan_id} · {'RUN' if a.apply else 'PLAN (dry run, nothing sent)'} · {stamp}", "",
             f"Rules: {len(rules)} folders (depth ≤ 2) · " + ", ".join(f"{s} {c}" for s, c in by_source.most_common()),
             f"Unresolved (open questions): {open_q} · {'sent' if a.apply else 'would send'} to Forge: {len(packets)} "
             f"(folder name, file names, extension mix; no contents)", "",
             "All answers are shadow inferences: nothing on disk changes, and nothing here is a decision.", "",
             "## Rules results (depth ≤ 2)", "", "| folder | files | kind | confidence | source | evidence |", "|---|---|---|---|---|---|"]
    lines += [f"| `{p}` | {n:,} | {v} | {c:.2f} | {s} | {'; '.join(json.loads(e))} |" for p, n, v, c, s, e in rules]
    if a.apply:
        lines += ["", f"## Forge answers ({len(llm)})", "", "| folder | kind | confidence | source |", "|---|---|---|---|"]
        lines += [f"| `{f}` | {v} | {c:.2f} | {s} |" for f, v, c, s in llm]
        if errors:
            lines += ["", f"## Forge errors ({len(errors)})", ""] + [f"- `{f}`: {r[:300]}" for f, r in errors]
    else:
        lines += ["", "## Packets that would go to Forge", ""] + [f"- `{p['folder']}`: {len(p['sample_file_names'])} names, "
                                                                   f"{len(p['ext_counts'])} extensions" for p in packets]
    lines += ["", "Per-document classification (doc type, subjects, version) is not in the engine yet."]
    out.mkdir(parents=True, exist_ok=True)
    report = out / f"FIS CLASSIFY · scan {scan_id} · {stamp}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Rules: {len(rules)} folders; unresolved {open_q}; Forge {'answered ' + str(len(llm)) if a.apply else 'not called (plan)'}. "
          f"Report: {report}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
