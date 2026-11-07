"""Gather every paper's statistics (from 42_STATISTICS_WALL) into ONE Excel workbook.

Station 42 writes <paper folder>/03_REPORT/statistics.json for each paper it runs on.
This script finds all of them and builds ALL_STATISTICS.xlsx with:
  * Matrix   - one row per paper, one column per metric (the raw values)
  * Long     - one row per paper x metric, with percentiles, method, change since last run
  * Guide    - every metric: family, unit, which direction is "better", how many papers have it
  * Sources  - exactly which statistics.json files were read (so you know where the numbers come from)

Usage:  python stats_to_excel.py [folder ...] [-o out.xlsx] [--open]
Default folder: the pipeline's API\\_data (every paper and video the pipeline has processed).
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent / "API" / "_data"
CATALOG = HERE.parent / "API" / "_system" / "config" / "metric_catalog.json"
DIR_WORDS = {"up": "higher is better", "down": "lower is better", "band": "no better/worse (descriptive)"}


def find(roots: list[Path]) -> list[Path]:
    out = []
    for r in roots:
        for dirpath, dirnames, filenames in os.walk(r):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "worktrees", ".obsidian")]
            if "statistics.json" in filenames and Path(dirpath).name == "03_REPORT":
                out.append(Path(dirpath) / "statistics.json")
    return sorted(out)


def autosize(ws, max_w=60):
    for i, col in enumerate(ws.iter_cols(min_row=1, max_row=min(ws.max_row, 200)), 1):
        w = max((len(str(c.value)) for c in col if c.value is not None), default=8)
        ws.column_dimensions[get_column_letter(i)].width = min(max(w + 2, 8), max_w)


def header(ws, row):
    ws.append(row)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="305496")
    ws.freeze_panes = "B2"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="*")
    ap.add_argument("-o", "--out")
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()
    roots = [Path(f) for f in a.folders if f] or [DEFAULT_ROOT]
    files = find(roots)
    out = Path(a.out) if a.out else roots[0] / "ALL_STATISTICS.xlsx"
    print(f"Found {len(files)} statistics.json file(s) under: {', '.join(map(str, roots))}")
    if not files:
        print("Nothing to aggregate yet. Run station 42_STATISTICS_WALL on some papers first.")
        return 1

    catalog = {}
    if CATALOG.exists():
        for f in json.loads(CATALOG.read_text(encoding="utf-8"))["families"]:
            for m in f["metrics"]:
                catalog[(f["n"], m["name"])] = m

    papers, metric_order, seen = [], [], set()
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"  skip {f}: {e}")
            continue
        item = d.get("item", {})
        papers.append((f, item, d.get("metrics", []), d.get("corpus", {})))
        for m in d.get("metrics", []):
            k = (m.get("family_name", m["family"]), m["name"])
            if k not in seen:
                seen.add(k)
                metric_order.append(k)

    wb = Workbook()
    mx = wb.active
    mx.title = "Matrix"
    header(mx, ["Paper", "Series", "Kind"] + [f"{fam}: {name}" for fam, name in metric_order])
    for f, item, metrics, _ in papers:
        vals = {(m.get("family_name", m["family"]), m["name"]): m["value"] for m in metrics}
        mx.append([item.get("title") or item.get("id") or f.parent.parent.name, item.get("series"), item.get("kind")]
                  + [vals.get(k) for k in metric_order])
    autosize(mx, 40)

    lg = wb.create_sheet("Long")
    header(lg, ["Paper", "Family", "Metric", "Value", "Unit", "Corpus percentile", "Papers compared (corpus n)",
                "Series percentile", "Series n", "Previous value", "Change", "Better is", "Method"])
    for f, item, metrics, _ in papers:
        t = item.get("title") or item.get("id") or f.parent.parent.name
        for m in metrics:
            lg.append([t, m.get("family_name", m["family"]), m["name"], m["value"], m.get("unit"), m.get("corpus_percentile"),
                       m.get("corpus_n"), m.get("series_percentile"), m.get("series_n"), m.get("previous"),
                       m.get("change_since_previous"), DIR_WORDS.get(m.get("dir"), m.get("dir")), m.get("method")])
    lg.auto_filter.ref = lg.dimensions
    autosize(lg)

    gd = wb.create_sheet("Guide")
    header(gd, ["Family", "Metric", "Unit", "Better is", "Papers that have it", "Min", "Max", "Average"])
    for k in metric_order:
        vs = [m["value"] for _, _, ms, _ in papers for m in ms
              if (m.get("family_name", m["family"]), m["name"]) == k and isinstance(m.get("value"), (int, float))]
        info = catalog.get(k, {})
        gd.append([k[0], k[1], info.get("unit", ""), DIR_WORDS.get(info.get("dir", "band")), len(vs),
                   min(vs) if vs else None, max(vs) if vs else None, round(sum(vs) / len(vs), 4) if vs else None])
    gd.auto_filter.ref = gd.dimensions
    autosize(gd)

    sr = wb.create_sheet("Sources")
    header(sr, ["Paper", "Metrics in file", "Corpus size when computed", "File"])
    for f, item, metrics, corpus in papers:
        sr.append([item.get("title") or item.get("id"), len(metrics), corpus.get("n"), str(f)])
    autosize(sr, 120)

    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"{len(papers)} paper(s) x {len(metric_order)} metric(s) -> {out}")
    if a.open:
        os.startfile(out)  # noqa: S606 (Windows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
