"""43_PAPER_GRADER: two local graders on each paper, no API calls.

  * July paper-proof-grader (vendor/grader/pipeline.py): metrics, sections, equations, claim candidates
    with maturity labels.
  * paper_grader 0.2.0 (vendor/grader_v2/paper_grader.py, "L15 atom analytics", from NAS
    Desktop/Folders/APIs/MAIN/PYTHON/SCRIPTS): structure, terms, math, evidence, argument, bridges,
    falsifiability, voice, readiness checks.

Both read the note's source only (our analysis blocks stripped). The vendored code is used unchanged: this
script imports its functions instead of letting it walk its own drop folders and archive the papers.
Output: one `<note> · 43_PAPER_GRADER.md` per paper (both reports), JSON and HTML in the item's run folder.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.output import esc, page  # noqa: E402
from engine.paths import inside  # noqa: E402
from engine.station import ItemResult, Station  # noqa: E402

LABEL = "43_PAPER_GRADER"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


JULY = _load("grader_july", inside("vendor", "grader", "pipeline.py"))
V2 = _load("grader_v2", inside("vendor", "grader_v2", "paper_grader.py"))
NO_CKG = {"sha": {}, "name": {}}


def july(text: str, paper_id: str, source: Path) -> tuple[dict, str]:
    sections = JULY._sections(text)
    equations = JULY._equations(text)
    claims = JULY._claim_candidates(text, sections, equations)
    for claim in claims:
        claim["paper_id"] = paper_id
    data = {"paper_id": paper_id, "source_file": str(source), "generated_at": datetime.now().isoformat(timespec="seconds"),
            "metrics": JULY._metrics(text, sections, equations, claims),
            "sections": sections, "equations": equations, "claims": claims}
    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "report.md"
        JULY._write_markdown(md, data)
        return data, md.read_text(encoding="utf-8")


def v2(source: Path, text: str, series: str | None) -> tuple[dict, str]:
    raw = text.encode("utf-8")
    rec = V2.grade_paper(source, raw, text, V2.sha256_bytes(raw), "PRIORITY", series, NO_CKG, None)
    return rec, V2.render_paper_md(rec, "")


def body(md: str) -> str:
    """A report without its own front matter and top heading, so it sits under ours."""
    if md.startswith("---\n"):
        md = md.split("\n---\n", 1)[-1].lstrip()
    return md.split("\n", 1)[1] if md.startswith("# ") else md


def main() -> int:
    station = Station(LABEL)

    def process(ctx):
        item = ctx.item
        text = item.text()
        jdata, jmd = july(text, item.id, item.source)
        ctx.step(f"July grader: {len(jdata['claims'])} claim candidate(s), {len(jdata['sections'])} section(s)")
        vrec, vmd = v2(item.source, text, item.meta.get("series") or None)
        ctx.step(f"paper_grader 0.2.0: readiness {vrec.get('readiness')}, source class {vrec.get('source_class')}")
        md = (f"# Paper grade: {item.title}\n\nLocal checks only, no API. Every number measures structure, coverage "
              f"and connection; none is a truth ruling.\n\n## 1. paper_grader 0.2.0 (L15 atom analytics)\n\n{body(vmd)}\n\n"
              f"## 2. July paper-proof-grader\n\n{body(jmd)}\n")
        html = page(f"Paper grade: {item.title}", f"<h1>Paper grade</h1><pre style='white-space:pre-wrap'>{esc(md)}</pre>")
        return ItemResult({"v2": vrec, "july": jdata}, html, {"claims": jdata["claims"]}, md,
                          {"readiness": vrec.get("readiness")})

    return station.run(process)


if __name__ == "__main__":
    raise SystemExit(main())
