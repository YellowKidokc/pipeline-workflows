"""65_PAPER_INTELLIGENCE: the Theophysics Paper Intelligence Suite v2.0 on each paper, local, no API.

The suite (X:\\THEOPHYSICS_PAPER_INTELLIGENCE, vendored as vendor/paper_intelligence, code unchanged except drive
letters) runs every paper through its layers:
  L1 text analytics (readability x8, vocabulary, keywords, n-grams)   L2 academic standard (citations, structure, grade)
  L3 Theophysics metrics (chi, wisdom/knowledge, fruits, the ten Master Equation variables, CKG tier)
  L5 NLP deep (entities, topics, key sentences)   L6 Truth Engine (fruits + chi anchors in embedding space, tier)
  L8 emotion profile   L9 linguistic depth   L10 idea density   L7 knowledge graph across every paper of the run
L4 (OpenAI 7Q) stays off here: it is an API call, and Academia is the local side (API work lives in 08_API_DEEP).

All papers of one run go through the suite together, so the knowledge graph links them. Output:
  <note> · 65_PAPER_INTEL.md          every measure of that paper, a table per layer
  PAPER_INTELLIGENCE\\<stamp>\\        the suite's own workbook (one row per paper), JSON, knowledge graph (.html/.graphml)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "_system").is_dir()) / "_system"))
from engine import pick  # noqa: E402
from engine.paths import inside  # noqa: E402
from engine.text import strip_front_matter  # noqa: E402

LABEL = "65_PAPER_INTEL"
SUITE = inside("vendor", "paper_intelligence")
LAYERS = {"L1": "Text analytics", "L2": "Academic standard", "L3": "Theophysics metrics", "L5": "NLP deep",
          "L6": "Truth Engine", "L7": "Knowledge graph", "L8": "Emotion profile", "L9": "Linguistic depth", "L10": "Idea density"}


def source_of(note: Path) -> tuple[str, str]:
    """(title, text the suite reads): the note without our analysis blocks and YAML, its title as the top heading."""
    raw = note.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', raw[:2000], re.M)
    title = m.group(1).strip() if m else note.stem
    raw = re.sub(r"<!-- (analysis|analysis-detail|scorecard):start -->.*?<!-- \1:end -->\n?", "", raw, flags=re.S)
    body = strip_front_matter(raw).strip()
    return title, body if body.startswith("# ") else f"# {title}\n\n{body}"


def report(row: dict, title: str) -> str:
    md = [f"# Paper intelligence: {title}\n", "Theophysics Paper Intelligence Suite v2.0, local. Every number is computed in Python; "
          "none is a truth ruling.\n", "| Layer | Status |", "|---|---|"]
    md += [f"| {k} {LAYERS.get(k, '')} | {v} |" for k, v in (row.get("_layer_status") or {}).items()]
    for layer, name in LAYERS.items():
        rows = [(k[len(layer) + 1:], v) for k, v in row.items() if k.startswith(layer + "_") and not isinstance(v, (dict, list))]
        if rows:
            md += [f"\n## {layer} {name}\n", "| Measure | Value |", "|---|---|"]
            md += [f"| {k} | {str(v).replace('|', '/')[:300]} |" for k, v in rows]
    return "\n".join(md) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="65_PAPER_INTELLIGENCE", description=__doc__.splitlines()[0])
    p.add_argument("items", nargs="*", help="papers, folders of papers, or @list.txt (default: this INBOX)")
    p.add_argument("--outbox", "--out", dest="out", help=f"default {FRONT / 'OUTBOX'}")
    p.add_argument("--limit", type=int)
    p.add_argument("--workers", type=int, default=1, help="accepted for the button; the suite runs the papers in one pass")
    p.add_argument("--focus", action="append", default=[], help="accepted for the button; nothing is sent anywhere")
    p.add_argument("--redo", action="store_true", help="accepted for the button; the suite always runs fresh")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    notes = [n for n in pick.resolve(a.items or [str(FRONT / "INBOX")]) if n.is_file() and n.suffix.lower() in (".md", ".txt")]
    notes = notes[:a.limit] if a.limit else notes
    if not notes:
        print(f"{LABEL}: no papers. Drop .md files into {FRONT / 'INBOX'} or pass them.")
        return 0
    out = Path(a.out) if a.out else FRONT / "OUTBOX"
    if a.dry_run:
        for n in notes:
            print("PLAN", n)
        return 0
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suite_out = out / "PAPER_INTELLIGENCE" / stamp
    suite_out.mkdir(parents=True, exist_ok=True)
    print(f"{LABEL}: {len(notes)} paper(s) through the Paper Intelligence Suite (local), results -> {out}")
    with tempfile.TemporaryDirectory(prefix="pi_") as tmp:
        series = Path(tmp) / "papers"
        series.mkdir()
        names, titles = {}, {}
        for i, n in enumerate(notes, 1):                 # the suite reads files named NN_*.md from one folder
            title, text = source_of(n)
            name = f"{i:02d}_{re.sub(r'[^A-Za-z0-9]+', '_', n.stem)[:80]}.md"
            (series / name).write_text(text, encoding="utf-8")
            names[name], titles[name] = n, title
        r = subprocess.run([sys.executable, "-u", str(SUITE / "00_ORCHESTRATOR" / "run_pipeline.py"), "--series", str(series),
                            "--output", str(suite_out)], cwd=SUITE, text=True, encoding="utf-8", errors="replace")
    results = sorted(suite_out.glob("*_pipeline_results_*.json"))
    if r.returncode != 0 or not results:
        print(f"{LABEL}: the suite failed (exit {r.returncode}); see {suite_out}", file=sys.stderr)
        return 1
    done = 0
    for row in json.loads(results[-1].read_text(encoding="utf-8")):
        note = names.get(row.get("file"))
        if not note:
            continue
        (out / f"{note.stem} · {LABEL}.md").write_text(report(row, titles[row["file"]]), encoding="utf-8")
        (out / "_json").mkdir(exist_ok=True)
        (out / "_json" / f"{note.stem} · {LABEL}.json").write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")
        done += 1
        print(f"  OK   {note.name}  ({', '.join(f'{k}:{v}' for k, v in (row.get('_layer_status') or {}).items())})")
    for f in suite_out.glob("knowledge_graph_*.html"):     # the graph page needs its scripts next to it
        shutil.copytree(SUITE / "lib", suite_out / "lib", dirs_exist_ok=True)
        break
    print(f"{LABEL}: {done} of {len(notes)} written; workbook and graph in {suite_out}")
    return 0 if done == len(notes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
