"""61_SERIES_SHEET: one run over a whole series. Reads every file (evidence companions, the series notebook, the grand-synthesis
master paper), writes `<file> \u00b7 61_SHEET.md` and `<file> \u00b7 61_SHEET.json` for each, and `<series> \u00b7 SERIES_SHEET.html` for the
series (plus `ALL \u00b7 SERIES_SHEET.html` when the run spans several series). Local: no API call, the sources are never changed.

    python 61_series_sheet.py <series folder> [<series folder> ...] [--outbox <folder>] [--workers 8]
    python 61_series_sheet.py @listfile --outbox <folder>              (what the button passes)

Without a folder it reads this station's INBOX. The series name is the name of the folder a file sits in.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "_system").is_dir()) / "_system"))
from engine import pick, series_sheet as S      # noqa: E402

LABEL = "61_SHEET"


def discover(items: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in items or [str(FRONT / "INBOX")]:
        if raw.startswith("@"):
            found += [p for p in pick.read_list(Path(raw[1:])) if p.is_file()]
            continue
        p = Path(raw).expanduser()
        if p.is_file():
            found.append(p)
        elif p.is_dir():
            found += sorted(f for f in p.rglob("*.md") if not any(part.startswith(("_", ".")) for part in f.relative_to(p).parts)
                            and f.name != ".gitkeep" and f" \u00b7 {LABEL}" not in f.name)
        else:
            print(f"not found: {p}", file=sys.stderr)
    return list(dict.fromkeys(found))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("items", nargs="*")
    ap.add_argument("--outbox", help="output folder (default: this station's OUTBOX)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run", action="store_true")
    for ignored in ("--provider", "--model", "--focus", "--channel"):      # the menu may pass these; this station calls no model
        ap.add_argument(ignored, action="append")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()
    files = discover(args.items)[: args.limit]
    out = Path(args.outbox) if args.outbox else FRONT / "OUTBOX"
    if not files:
        print("61_SERIES_SHEET: no files found")
        return 0
    series_of = {f: f.parent.name for f in files}
    print(f"61_SERIES_SHEET: {len(files)} file(s) in {len(set(series_of.values()))} series -> {out}")
    if args.dry_run:
        for f in files:
            print(f"  would read {f}")
        return 0
    out.mkdir(parents=True, exist_ok=True)

    def one(f: Path):
        try:
            rec = S.parse(f, series_of[f])
            (out / f"{f.stem} \u00b7 {LABEL}.md").write_text(S.sheet_md(rec), encoding="utf-8")
            (out / f"{f.stem} \u00b7 {LABEL}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  ok  {f.name}", flush=True)
            return rec
        except Exception as exc:                              # one bad file never stops the series
            print(f"  FAILED {f.name}: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
            return None

    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, len(files)))) as pool:
        records = [r for r in pool.map(one, files) if r]
    link = lambda rec, kind: quote(f"{rec['stem']} \u00b7 {LABEL}.{kind}")
    by_series: dict[str, list[dict]] = {}
    for r in records:
        by_series.setdefault(r["series"], []).append(r)
    for name, recs in by_series.items():
        (out / f"{name} \u00b7 SERIES_SHEET.html").write_text(S.series_html(name, recs, link), encoding="utf-8")
        (out / f"{name} \u00b7 SERIES_SHEET.json").write_text(json.dumps(
            [{k: v for k, v in r.items() if k not in ("sections", "tables")} for r in recs], indent=2, ensure_ascii=False), encoding="utf-8")
    if len(by_series) > 1:
        (out / "ALL \u00b7 SERIES_SHEET.html").write_text(S.series_html("All series", records, link), encoding="utf-8")
    failed = len(files) - len(records)
    print(f"61_SERIES_SHEET: {len(records)} of {len(files)} done, {len(by_series)} series page(s) in {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
