"""43_PAPER_GRADER: three local passes on each paper, no API calls.

  1. paper_grader 0.2.0 (vendor/grader_v2/paper_grader.py, "L15 atom analytics", from NAS
     Desktop/Folders/APIs/MAIN/PYTHON/SCRIPTS): structure, terms, math, evidence, argument, bridges,
     falsifiability, voice, readiness checks.
  2. July paper-proof-grader (vendor/grader/pipeline.py): metrics, sections, equations, claim candidates
     with maturity labels.
  3. Advanced metrics (vendor/grader_metrics, OPERATOR_2 modules + the Theophysics Paper Metrics Engine, NAS
     Academic Paper Grading): causal claims and their warrants, hedges vs boosters, propositional idea density,
     concept drift across sections, paragraph topic coherence, self-contradiction (NLI), and the 76-field
     metrics engine (readability composite, MTLD / HD-D, wisdom / knowledge terms, fruits, coherence).
     Concept drift and topic coherence use all-MiniLM-L6-v2; self-contradiction uses DeBERTa-v3 NLI
     (downloaded once, on first use). A metric that cannot run is reported, never fatal.

All read the note's source only (our analysis blocks stripped). The vendored code is used unchanged: this
script imports its functions instead of letting it walk its own drop folders and archive the papers.
Output: one `<note> · 43_PAPER_GRADER.md` per paper (every pass), JSON and HTML in the item's run folder.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from dataclasses import asdict
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
METRICS = inside("vendor", "grader_metrics")
# (title, module, function, keyword arguments): each returns a dict whose "document" part is the paper-level result
ADVANCED = [("Causal claims and warrants", "causal_claims", "score_causal_claims", {}),
            ("Hedges and boosters", "hedge_detector", "score_hedges", {}),
            ("Propositional idea density", "idea_density", "score_idea_density", {}),
            ("Concept drift across sections", "concept_drift", "score_concept_drift", {}),
            ("Paragraph topic coherence", "topic_coherence", "score_topic_coherence", {}),
            ("Self-contradiction (NLI)", "self_contradiction", "score_contradictions", {"max_pairs": 300})]


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


def scalars(d: dict, prefix: str = "") -> list[tuple[str, object]]:
    """The numbers and labels of a result, flattened one level deep (lists are counted, not printed)."""
    rows = []
    for k, v in d.items():
        if isinstance(v, dict) and not prefix:
            rows += scalars(v, f"{k}.")
        elif isinstance(v, (list, tuple)) and v and len(v) <= 12 and all(isinstance(x, (str, int, float)) for x in v):
            rows.append((f"{prefix}{k}", ", ".join(map(str, v))))
        elif isinstance(v, (list, tuple)):
            rows.append((f"{prefix}{k}", f"{len(v)} item(s)"))
        elif not isinstance(v, dict):
            rows.append((f"{prefix}{k}", round(v, 4) if isinstance(v, float) else v))
    return rows


def advanced(text: str, source: Path) -> tuple[dict, str]:
    data, md = {}, []
    for title, module, func, kwargs in ADVANCED:
        try:
            result = getattr(_load(f"gm_{module}", METRICS / f"{module}.py"), func)(text, **kwargs)
            data[module] = result
            doc = result.get("document", result) if isinstance(result, dict) else {"result": result}
            md += [f"### {title}\n", "| Measure | Value |", "|---|---|"]
            md += [f"| {k} | {v} |" for k, v in scalars(doc) if k not in ("metric", "version")]
            md.append("")
        except Exception as exc:                          # a missing model or library never stops the paper
            data[module] = {"error": f"{type(exc).__name__}: {exc}"}
            md += [f"### {title}\n", f"Not run: {type(exc).__name__}: {str(exc)[:200]}\n"]
    try:
        engine = _load("gm_paper_metrics_engine", METRICS / "paper_metrics_engine.py").PaperMetricsEngine()
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / source.name
            f.write_text(text, encoding="utf-8")
            pm = asdict(engine.analyze_paper(f))
        data["paper_metrics_engine"] = pm
        md += ["### Theophysics Paper Metrics Engine\n", "| Measure | Value |", "|---|---|"]
        md += [f"| {k} | {v} |" for k, v in scalars(pm) if k not in ("paper_id", "paper_name")]
    except Exception as exc:
        data["paper_metrics_engine"] = {"error": f"{type(exc).__name__}: {exc}"}
        md.append(f"### Theophysics Paper Metrics Engine\n\nNot run: {type(exc).__name__}: {str(exc)[:200]}\n")
    return data, "\n".join(md)


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
        adata, amd = advanced(text, item.source)
        failed = [k for k, v in adata.items() if isinstance(v, dict) and "error" in v]
        ctx.step(f"advanced metrics: {len(adata) - len(failed)} of {len(adata)} ran" + (f" (not run: {', '.join(failed)})" if failed else ""))
        md = (f"# Paper grade: {item.title}\n\nLocal checks only, no API. Every number measures structure, coverage "
              f"and connection; none is a truth ruling.\n\n## 1. paper_grader 0.2.0 (L15 atom analytics)\n\n{body(vmd)}\n\n"
              f"## 2. July paper-proof-grader\n\n{body(jmd)}\n\n## 3. Advanced metrics\n\n{amd}\n")
        html = page(f"Paper grade: {item.title}", f"<h1>Paper grade</h1><pre style='white-space:pre-wrap'>{esc(md)}</pre>")
        return ItemResult({"v2": vrec, "july": jdata, "advanced": adata}, html, {"claims": jdata["claims"]}, md,
                          {"readiness": vrec.get("readiness")})

    return station.run(process)


if __name__ == "__main__":
    raise SystemExit(main())
