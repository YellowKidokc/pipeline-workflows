"""64_SITE_PACKAGE: file every paper's audit into one house per series, a page per part, Markdown + HTML.

The last step of 63_PAPER_AUDIT. Each part of a series is audited on its own; every time a part comes through,
its page is (re)built and the series' title page is rebuilt from all the parts it has so far.

  <site_root>/
    00_ALL_SERIES_INDEX.md · .html · .csv           every series and standalone paper
    <NN>_<series-slug>/                             a series (YAML series/part, or INBOX\\01_SERIES\\<series>\\)
      00_manifest.md · .html                        the series title page: every part, in order, with its headline
      00_manifest/parts.json                        what the title page is built from
      <PP>_<part-slug>.md · .html                   the page for one part: the paper, then every audit result
      01_text/canonical/<part>.md                   the source, as audited (our analysis blocks left out)
      03_nlp_api/<NN_STATION>/                      every file each audit station wrote for this part
      04_data/json/ · 04_data/excel/                the JSON and the workbooks
      99_archive/superseded/<date>/                 an earlier version of a part, moved here, never deleted
      02_media/ 05_site_build/ 06_inbox_imports/ 07_exports/ 98_file_intelligence/   (empty until used)
    00_STANDALONE/<paper-slug>/                     a paper that is not part of a series: the same shape, one part

<site_root> is `site_root` in config/paths.json; if that is not set, this station's OUTBOX\\SITE.
The audit results are read from the folder the audit wrote to (--from; in the chain, the chain's output folder).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "_system").is_dir()) / "_system"))
from engine import note as N, pick  # noqa: E402
from engine.output import markdown_to_html, page  # noqa: E402
from engine.paths import expand, raw_value, station_dir  # noqa: E402

LABEL = "64_SITE_PACKAGE"
SKELETON = ["00_manifest", "01_text/canonical", "01_text/drafts", "01_text/variants_easy", "01_text/variants_academic",
            "02_media/images", "02_media/audio", "02_media/video", "02_media/thumbnails", "03_nlp_api", "04_data/json",
            "04_data/excel", "04_data/csv", "05_site_build/html", "05_site_build/page_manifests", "06_inbox_imports/unsorted",
            "07_exports/publish_packets", "07_exports/review_packets", "98_file_intelligence/reports", "99_archive/superseded"]
STATION_OF = re.compile(r" · (\d\d_[A-Z0-9_]+)\.(md|html|json|xlsx)$")


def strip_ours(text: str) -> str:
    """The note without our own analysis and scorecard blocks (the same rule every station reads by)."""
    return re.sub(r"<!-- (analysis|analysis-detail|scorecard):start -->.*?<!-- \1:end -->\n?", "", text, flags=re.S)


def slug(text: str, limit: int = 70) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:limit].strip("-") or "untitled"


def to_html(md: str) -> str:
    try:
        import markdown                                     # tables, fenced code; the engine renderer if missing
        return markdown.markdown(md, extensions=["tables", "fenced_code"])
    except ImportError:
        return markdown_to_html(md)


def place(note: Path) -> tuple[str, int, str]:
    """(series name or "", part number, title) from the note's YAML, else its INBOX\\01_SERIES\\<series>\\ folder."""
    text = note.read_text(encoding="utf-8", errors="replace")
    fields = N.fields(text)
    title = str(fields.get("doc_title") or fields.get("title") or note.stem)
    series, part = str(fields.get("series") or ""), fields.get("part")
    if not series and "01_SERIES" in note.parts:
        i = note.parts.index("01_SERIES")
        if i + 2 < len(note.parts):
            series = note.parts[i + 1]
    if series and not part:
        m = re.search(r"(?:^|[-_ ])(\d{1,3})(?:[-_ ]|$)", note.stem)
        part = int(m.group(1)) if m else 0
    return series, int(part or 0), title


def series_folder(root: Path, series: str) -> Path:
    if not series:
        return root / "00_STANDALONE"
    for d in sorted(root.glob("[0-9][0-9]_*")):            # an existing house for this series keeps its number
        if d.is_dir() and d.name.split("_", 1)[1] == slug(series):
            return d
    taken = [int(d.name[:2]) for d in root.glob("[0-9][0-9]_*") if d.is_dir() and d.name[:2].isdigit()]
    return root / f"{max(taken + [0]) + 1:02d}_{slug(series)}"


def results_for(stem: str, src: Path) -> list[Path]:
    """Every file the audit wrote for this note: flat `<stem> · NN_LABEL.*`, `_json\\<stem> · *`, and the newest
    run folder of the stations that write `<stem>\\<stamp>\\` (57 API Deep, 58 argument grades)."""
    found = sorted(src.glob(f"{glob_safe(stem)} · *")) + sorted((src / "_json").glob(f"{glob_safe(stem)} · *"))
    runs = src / stem
    if runs.is_dir():
        for stamp in sorted((d for d in runs.iterdir() if d.is_dir()), key=lambda d: d.name):
            found += [f for f in stamp.rglob("*") if f.is_file() and "calls" not in f.parts]
    return found


def glob_safe(text: str) -> str:
    return re.sub(r"([\[\]*?])", r"[\1]", text)


def station_of(f: Path) -> str:
    m = STATION_OF.search(f.name)
    if m:
        return m.group(1)
    if (f.parent / "API_DEEP.json").is_file() or (f.parent.parent / "API_DEEP.json").is_file():
        return "57_API_DEEP"
    return "58_ARGUMENT_GRADE" if "argument" in f.name.lower() else "00_OTHER"


def build_part(house: Path, note: Path, part: int, title: str, src: Path) -> dict:
    for d in SKELETON:
        (house / d).mkdir(parents=True, exist_ok=True)
    name = f"{part:02d}_{slug(title)}" if part else slug(title)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    old = [p for p in house.glob(f"{name}.*") if p.is_file()] + [p for p in (house / "03_nlp_api").glob(f"*/{name}") if p.is_dir()]
    for p in old:                                           # a rerun: the earlier version goes to the archive, whole
        dest = house / "99_archive" / "superseded" / stamp / p.relative_to(house)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dest))
    source = strip_ours(note.read_text(encoding="utf-8", errors="replace"))
    (house / "01_text" / "canonical" / f"{name}.md").write_text(source, encoding="utf-8")
    sections, headline = [], {}
    for f in results_for(note.stem, src):
        st = station_of(f)
        bucket = house / ("04_data/json" if f.suffix == ".json" else "04_data/excel" if f.suffix == ".xlsx" else "03_nlp_api")
        dest = (bucket / st / name / f.name) if bucket.name == "03_nlp_api" else (bucket / st / f"{name} · {f.name}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        if f.suffix == ".md" and f.name != "00_source_numbered.md":
            sections.append((st, f.read_text(encoding="utf-8", errors="replace"), dest.relative_to(house).as_posix()))
        if f.name.endswith("43_PAPER_GRADER.md"):
            m = re.search(r"Readiness\s+\*\*([A-Z_]+)\*\*", sections[-1][1])
            headline["readiness"] = m.group(1) if m else None
    body_md = re.sub(r"\A---\n.*?\n---\n", "", source, flags=re.S).strip()
    md = [f"# {title}\n", f"Part {part}\n" if part else "", "## The paper\n", body_md, "\n## Audit\n"]
    html = [f"<h1>{title}</h1>", f"<p class='mute'>Part {part}</p>" if part else "", "<h2>The paper</h2>", to_html(body_md), "<h2>Audit</h2>"]
    for st, text, rel in sorted(sections):
        md += [f"\n### {st}\n", f"Full file: `{rel}`\n", re.sub(r"(?m)^(#{1,4}) ", r"#\1## ", text)]
        html += [f"<details><summary><b>{st}</b> <span class='mute'>{rel}</span></summary>{to_html(text)}</details>"]
    if not sections:
        md.append("No audit results found for this paper yet.\n")
        html.append("<p class='mute'>No audit results found for this paper yet.</p>")
    (house / f"{name}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (house / f"{name}.html").write_text(page(title, "\n".join(html)), encoding="utf-8")
    shutil.copy2(house / f"{name}.html", house / "05_site_build" / "html" / f"{name}.html")
    return {"part": part, "name": name, "title": title, "source": str(note), "stations": sorted({s for s, _, _ in sections}),
            "built_at": datetime.now().isoformat(timespec="seconds"), **headline}


def build_manifest(house: Path, series: str, entry: dict) -> None:
    reg_file = house / "00_manifest" / "parts.json"
    reg = json.loads(reg_file.read_text(encoding="utf-8")) if reg_file.is_file() else {"series": series, "parts": []}
    reg["parts"] = sorted([p for p in reg["parts"] if p["name"] != entry["name"]] + [entry], key=lambda p: (p["part"], p["name"]))
    reg_file.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    title = series or "Standalone papers"
    rows = [f"| {p['part'] or ''} | [{p['title']}]({p['name']}.html) · [md]({p['name']}.md) | {p.get('readiness') or ''} | "
            f"{', '.join(p['stations'])} | {p['built_at'][:10]} |" for p in reg["parts"]]
    md = [f"# {title}\n", f"{len(reg['parts'])} part(s). Each part is audited on its own; this page is rebuilt every time one comes through.\n",
          "| Part | Page | Readiness | Audit stations | Built |", "|---|---|---|---|---|", *rows]
    (house / "00_manifest.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (house / "00_manifest.html").write_text(page(title, to_html("\n".join(md))), encoding="utf-8")


def build_index(root: Path) -> None:
    rows = []
    for reg_file in sorted(root.glob("*/00_manifest/parts.json")):
        reg = json.loads(reg_file.read_text(encoding="utf-8"))
        rows.append({"folder": reg_file.parents[1].name, "series": reg.get("series") or "(standalone)", "parts": len(reg["parts"]),
                     "manifest_html": f"{reg_file.parents[1].name}/00_manifest.html"})
    md = ["# All series\n", "| Folder | Series | Parts | Title page |", "|---|---|---|---|"]
    md += [f"| {r['folder']} | {r['series']} | {r['parts']} | [{r['manifest_html']}]({r['manifest_html']}) |" for r in rows]
    (root / "00_ALL_SERIES_INDEX.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (root / "00_ALL_SERIES_INDEX.html").write_text(page("All series", to_html("\n".join(md))), encoding="utf-8")
    with (root / "00_ALL_SERIES_INDEX.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["folder", "series", "parts", "manifest_html"])
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser(prog=LABEL, description=__doc__.splitlines()[0])
    p.add_argument("items", nargs="*", help="the audited papers, a folder, or @list.txt (default: the papers 63 last ran)")
    p.add_argument("--outbox", "--out", dest="out", help="where the audit wrote its results (in the chain: the chain's folder)")
    p.add_argument("--from", dest="src", help="read audit results from here (default: --outbox, else 063_PAPER_AUDIT\\OUTBOX)")
    p.add_argument("--site", help="the site root (default: site_root in paths.json, else this station's OUTBOX\\SITE)")
    p.add_argument("--workers", type=int, default=1, help="accepted for the button; the build is local and quick")
    p.add_argument("--focus", action="append", default=[], help="accepted for the button; nothing is sent anywhere")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    audit_box = station_dir("63").parent / "OUTBOX"
    selectors = a.items or [f"@{audit_box / '_last_run.txt'}"]
    notes = [n for n in pick.resolve(selectors) if n.is_file() and n.suffix.lower() in (".md", ".txt")]
    src = Path(a.src or a.out or audit_box)
    root = Path(a.site) if a.site else expand(raw_value("site_root")) if raw_value("site_root") else FRONT / "OUTBOX" / "SITE"
    if not notes:
        print(f"{LABEL}: no papers (run 63_PAPER_AUDIT first, or pass the papers)")
        return 0
    print(f"{LABEL}: {len(notes)} paper(s), audit results from {src}, site -> {root}")
    for note in notes:
        series, part, title = place(note)
        house = series_folder(root, series)
        if a.dry_run:
            print(f"  PLAN {note.name} -> {house.name}/{part:02d}" if part else f"  PLAN {note.name} -> {house.name}")
            continue
        entry = build_part(house, note, part, title, src)
        build_manifest(house, series, entry)
        print(f"  OK   {note.name} -> {house.name}/{entry['name']}.html  ({len(entry['stations'])} station(s))")
    if not a.dry_run:
        root.mkdir(parents=True, exist_ok=True)
        build_index(root)
        print(f"{LABEL}: index {root / '00_ALL_SERIES_INDEX.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
