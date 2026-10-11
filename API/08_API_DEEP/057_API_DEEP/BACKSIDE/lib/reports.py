"""The API Deep reports: one page per station, with visuals, and one combined HTML that holds them all.

  ledger   claims, proofs, evidence, Lean and audit in the Atom Ledger template (templates/atom_ledger.html),
           its data block (window.LEDGER) generated from atoms, axiom nodes, Lean 4 and coherence
  fruits   the nine fruits: verdict scores, sentence means, gates, Love x Truth, paragraph heat strip
  me       the Master Equation: ten slots coloured by fit, product test, analog strength, breaks
  lean     Lean 4 formalization candidates, one card each
  axioms   axiom nodes by mode x alignment, with the quote each one rests on
  REPORT.html  all of them in one file, one tab per report (each report keeps its own styles)

Everything is read from a finished run folder; nothing is called. `build_all(run_dir)` writes the files into it.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

LIB = Path(__file__).resolve().parent
TEMPLATE = LIB.parent / "templates" / "atom_ledger.html"
FRUITS = ["love", "joy", "peace", "patience", "kindness", "goodness", "faithfulness", "gentleness", "self_control"]
FIT = {"direct": 3, "analogous": 2, "stretched": 1, "absent": 0}

CSS = """:root{--bg:#0b0d12;--panel:#141923;--panel2:#1a2130;--line:#2b3546;--ink:#e9eef7;--mut:#8f9db2;--dim:#5f6c80;
--gold:#d9a94a;--cyan:#49b4e0;--green:#63c991;--amber:#d7a94b;--red:#d86b70;--blue:#76a7ff;--purple:#9c86ef;
--mono:ui-monospace,"Cascadia Code",Consolas,monospace;--sans:Inter,"Segoe UI",Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 var(--sans)}
.wrap{max-width:1180px;margin:0 auto;padding:22px 18px 60px}h1{font-size:22px;margin:0 0 4px}h2{font-size:15px;margin:26px 0 10px;color:var(--gold);
font-family:var(--mono);letter-spacing:.08em;text-transform:uppercase}.mut{color:var(--mut)}.dim{color:var(--dim)}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px}
.card h3{margin:0 0 6px;font-size:14px}.k{font:700 10px var(--mono);letter-spacing:.1em;color:var(--dim);text-transform:uppercase}
.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font:600 11px var(--mono);margin:2px 4px 2px 0}
.big{font:700 28px var(--mono)}table{width:100%;border-collapse:collapse;font-size:13px}td,th{border-bottom:1px solid var(--line);
padding:6px;text-align:left;vertical-align:top}th{color:var(--mut);font-weight:600}q{color:var(--mut);font-style:italic}
.ok{color:var(--green)}.warn{color:var(--amber)}.bad{color:var(--red)}svg text{font-family:var(--mono)}"""


def esc(v) -> str:
    return html.escape("" if v is None else str(v))


def load(run: Path, name: str):
    p = run / name
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def page(title: str, body: str) -> str:
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body><div class='wrap'>{body}</div></body></html>")


# ------------------------------------------------------------------ ledger (claims, proofs, evidence, Lean, audit)

def _status(v: str | None) -> str:
    v = (v or "").lower()
    return "VERIFIED" if v in ("verified", "kernel_checked", "machine_checked", "formal") else \
           "DRAFT" if v in ("candidate", "draft", "formalizing", "sorry") else "PROSE"


def ledger_data(run: Path, paper: str) -> dict:
    atoms = (load(run, "atoms.json") or {}).get("atoms", [])
    domain = (load(run, "atoms.json") or {}).get("domainType") or "Theophysics"
    ax = load(run, "axiom_nodes.json") or {}
    lean = (load(run, "lean4.json") or {}).get("formal_candidates", [])
    coh = load(run, "coherence.json") or {}
    by_id = {a.get("atom_id"): a for a in atoms}
    lean_of = {}
    for c in lean:
        lean_of.setdefault((c.get("identity") or {}).get("claim_id"), []).append(c)
    audits_of = {}
    for kind in ("contradictions", "tensions"):
        for i, t in enumerate(coh.get(kind, []), 1):
            for aid in t.get("atoms", []):
                audits_of.setdefault(aid, []).append((f"{kind[:-1].upper()}-{i:02d}", t))
    rows = []
    for a in atoms:                                       # source order, never sorted
        aid, nt = a.get("atom_id", ""), (a.get("nodeType") or "").lower()
        typ = "EVIDENCE" if nt == "evidence" else "AUDIT" if nt in ("kill", "check") else "CLAIM"
        if nt in ("paper", "series", "raw"):
            continue
        neighbors = []
        for e in a.get("edges", [])[:3]:
            tgt = by_id.get(e.get("target"))
            if tgt:
                neighbors.append({"id": tgt.get("atom_id"), "role": "claim", "title": tgt.get("name", ""), "edge": e.get("type", "")})
        for c in lean_of.get(aid, [])[:2]:
            neighbors.append({"id": (c.get("identity") or {}).get("candidate_uuid", "lean"), "role": "lean",
                              "title": (c.get("formal_object") or {}).get("object_type", "Lean candidate"), "edge": "formalizes"})
        for tid, t in audits_of.get(aid, [])[:2]:
            neighbors.append({"id": tid, "role": "audit", "title": t.get("description", "")[:70], "edge": "challenges"})
        src = a.get("source_sentences") or []
        if src:
            neighbors.append({"id": f"{src[0]}..{src[-1]}" if len(src) > 1 else src[0], "role": "evidence",
                              "title": f"{len(src)} source sentence(s)", "edge": "sources"})
        rows.append({"type": typ, "text": f"{a.get('name', '')}: {a.get('statementPlain') or a.get('statementTechnical') or ''}"[:220],
                     "domain": domain, "family": a.get("claimClass") or nt, "status": _status(a.get("verificationStatus")),
                     "receipt": (src[0] if src else "—"),
                     "atom": {"id": aid, "role": nt.title(), "title": a.get("name", ""),
                              "claim": a.get("statementTechnical") or a.get("statementPlain") or "",
                              "markers": {"home": domain, "objectType": nt, "commitment": a.get("stage", ""),
                                          "standing": a.get("challengeStatus", ""), "evidenceGrade": a.get("verificationStatus", "")},
                              "neighbors": neighbors[:6]}})
    for c in lean:
        fo, rb, cid = c.get("formal_object") or {}, c.get("result_and_boundary") or {}, (c.get("identity") or {}).get("claim_id")
        claim = by_id.get(cid, {})
        rows.append({"type": "LEAN", "text": f"{fo.get('object_type', 'Candidate')} for {cid}: {fo.get('exact_proposed_statement', '')}"[:220],
                     "domain": domain, "family": "Lean 4", "status": _status(rb.get("verification_status")), "receipt": "—",
                     "atom": {"id": (c.get("identity") or {}).get("candidate_uuid", ""), "role": "Lean candidate",
                              "title": claim.get("name", cid or ""), "claim": fo.get("exact_proposed_statement", ""),
                              "markers": {"home": domain, "objectType": fo.get("object_type", ""), "commitment": (c.get("source_selection") or {}).get("selection_disposition", ""),
                                          "standing": rb.get("verification_status", ""), "evidenceGrade": "not compiled"},
                              "neighbors": [{"id": cid, "role": "claim", "title": claim.get("name", ""), "edge": "formalizes"}]}})
    for kind, label in (("contradictions", "Contradiction"), ("tensions", "Tension")):
        for i, t in enumerate(coh.get(kind, []), 1):
            rows.append({"type": "AUDIT", "text": f"{label}: {t.get('description', '')}"[:220], "domain": domain,
                         "family": "Coherence", "status": "PROSE", "receipt": t.get("severity", "—"),
                         "atom": {"id": f"{kind[:-1].upper()}-{i:02d}", "role": label, "title": label,
                                  "claim": t.get("description", ""),
                                  "markers": {"home": domain, "objectType": "audit", "commitment": "", "standing": t.get("severity", ""),
                                              "evidenceGrade": ""},
                                  "neighbors": [{"id": x, "role": "claim", "title": by_id.get(x, {}).get("name", x), "edge": "involves"}
                                                for x in t.get("atoms", [])][:6]}})
    for n in ax.get("axiom_nodes", []):
        if n.get("alignment") == "directly_asserted":
            rows.append({"type": "EVIDENCE", "text": f"Axiom {n.get('node_id')} {n.get('name')}: \"{n.get('evidence_quote', '')}\""[:220],
                         "domain": domain, "family": n.get("mode", "axiom"), "status": "PROSE", "receipt": n.get("confidence", "—"),
                         "atom": {"id": n.get("node_id", ""), "role": "Axiom node", "title": n.get("name", ""), "claim": n.get("evidence_quote", ""),
                                  "markers": {"home": domain, "objectType": n.get("mode", ""), "commitment": n.get("alignment", ""),
                                              "standing": n.get("confidence", ""), "evidenceGrade": "quoted"}, "neighbors": []}})
    return {"paper": {"label": paper, "rows": rows}, "corpus": {"label": paper + " (this run)", "rows": rows}}


def ledger_page(run: Path, paper: str) -> str:
    t = TEMPLATE.read_text(encoding="utf-8")
    start, end = t.index("var CI ="), t.index("var LANE_ROLES")
    data = json.dumps(ledger_data(run, paper), ensure_ascii=False).replace("</", "<\\/")
    t = t[:start] + f"window.LEDGER = {data};\n\n" + t[end:]
    return re.sub(r"<title>.*?</title>", f"<title>Atom Ledger · {esc(paper)}</title>", t, count=1, flags=re.S)


# ------------------------------------------------------------------ fruits

def _bars(values: dict, lo: float, hi: float, width=560, label_w=110) -> str:
    rows, h = list(values.items()), 26
    zero = label_w + (0 - lo) / (hi - lo) * (width - label_w - 40)
    out = [f"<svg viewBox='0 0 {width} {len(rows) * h + 10}' width='100%'>",
           f"<line x1='{zero:.0f}' y1='0' x2='{zero:.0f}' y2='{len(rows) * h}' stroke='#2b3546'/>"]
    for i, (k, v) in enumerate(rows):
        y, v = i * h + 6, float(v or 0)
        x = label_w + (min(max(v, lo), hi) - lo) / (hi - lo) * (width - label_w - 40)
        col = "#63c991" if v > 0 else "#d86b70" if v < 0 else "#5f6c80"
        out.append(f"<text x='0' y='{y + 13}' fill='#8f9db2' font-size='11'>{esc(k.replace('_', ' '))}</text>"
                   f"<rect x='{min(x, zero):.0f}' y='{y}' width='{abs(x - zero):.0f}' height='16' rx='3' fill='{col}'/>"
                   f"<text x='{max(x, zero) + 6:.0f}' y='{y + 13}' fill='#e9eef7' font-size='11'>{v:g}</text>")
    return "".join(out) + "</svg>"


def _strip(values: dict, width=1100) -> str:
    items = list(values.items())
    if not items:
        return ""
    w = width / len(items)
    cells = []
    for i, (k, v) in enumerate(items):
        v = float(v or 0)
        col = f"rgba(99,201,145,{min(1, abs(v)):.2f})" if v > 0 else f"rgba(216,107,112,{min(1, abs(v)):.2f})" if v < 0 else "#1a2130"
        cells.append(f"<rect x='{i * w:.1f}' y='0' width='{w + .5:.1f}' height='34' fill='{col}'><title>{esc(k)}: {v:g}</title></rect>")
    return f"<svg viewBox='0 0 {width} 34' width='100%' preserveAspectRatio='none'>{''.join(cells)}</svg>"


def fruits_page(run: Path, paper: str) -> str:
    fr, fs, lt = load(run, "fruits.json") or {}, (load(run, "fruits_sentences.json") or {}).get("summary", {}), load(run, "love_truth.json") or {}
    verdict = {p["fruit_id"].split(".")[-1]: p.get("score") for p in fr.get("fruit_profile", [])}
    gates = fr.get("gate_results", [])
    prof = lt.get("profile") or {}
    agg = fr.get("aggregation") or {}
    body = [f"<h1>Fruits of the Spirit</h1><div class='mut'>{esc(paper)}</div>",
            "<div class='grid' style='margin-top:14px'>",
            f"<div class='card'><div class='k'>System status</div><div class='big'>{esc(fr.get('system_status', '—'))}</div><div class='mut'>{esc(fr.get('epistemic_status', ''))}</div></div>",
            f"<div class='card'><div class='k'>Weakest fruit</div><div class='big'>{esc((agg.get('minimum_fruit') or {}).get('fruit_id', '—').split('.')[-1])}</div><div class='mut'>score {esc((agg.get('minimum_fruit') or {}).get('score', ''))}</div></div>",
            f"<div class='card'><div class='k'>Love x Truth</div><div class='big'>{esc(prof.get('quadrant', '—'))}</div><div class='mut'>love {esc(prof.get('love_axis', ''))} · truth {esc(prof.get('truth_axis', ''))}</div></div>",
            f"<div class='card'><div class='k'>Balance</div><div class='big'>{esc(agg.get('geometric_balance', '—'))}</div><div class='mut'>geometric · arithmetic {esc(agg.get('arithmetic_summary', ''))}</div></div>",
            "</div>",
            "<h2>Verdict score per fruit (0-4)</h2>", _bars({f: verdict.get(f, 0) for f in FRUITS}, 0, 4) if verdict else "<p class='dim'>No verdict.</p>",
            "<h2>Every sentence, mean per fruit (-2..+2)</h2>", _bars({f: (fs.get("fruit_means") or {}).get(f, 0) for f in FRUITS}, -0.5, 0.5),
            "<h2>Love through the paper (one cell per paragraph)</h2>", _strip(fs.get("paragraph_love") or {}),
            "<h2>Gates</h2><table><tr><th>Gate</th><th>Status</th><th>Why</th></tr>"]
    for g in gates:
        cls = "ok" if g.get("status") == "PASS" else "bad" if g.get("status") == "FAIL" else "warn"
        body.append(f"<tr><td class='mono'>{esc(g.get('gate_id'))}</td><td class='{cls}'>{esc(g.get('status'))}</td><td>{esc(g.get('rationale', ''))[:400]}</td></tr>")
    body.append("</table><h2>Each fruit</h2><div class='grid'>")
    for p in fr.get("fruit_profile", []):
        body.append(f"<div class='card'><h3>{esc(p['fruit_id'].split('.')[-1].replace('_', ' ').title())} · {esc(p.get('score'))}</h3>"
                    f"<div class='mut'>{esc(p.get('rationale', ''))[:420]}</div></div>")
    body.append("</div>")
    if fr.get("repair_path"):
        body.append("<h2>Repair path</h2><ol>" + "".join(f"<li>{esc(x if isinstance(x, str) else json.dumps(x, ensure_ascii=False))[:300]}</li>" for x in fr["repair_path"]) + "</ol>")
    return page(f"Fruits · {paper}", "".join(body))


# ------------------------------------------------------------------ master equation

def me_page(run: Path, paper: str) -> str:
    me = load(run, "master_equation.json") or {}
    slots = me.get("slots", [])
    cells = []
    for i, s in enumerate(slots):
        f = FIT.get(s.get("fit_1") or "absent", 0)
        col = ["#1a2130", "#5a3b3d", "#3d5a6b", "#2f6b4a"][f]
        x, y = (i % 5) * 216, (i // 5) * 120
        cells.append(f"<g><rect x='{x}' y='{y}' width='206' height='110' rx='10' fill='{col}' stroke='#2b3546'/>"
                     f"<text x='{x + 14}' y='{y + 38}' fill='#d9a94a' font-size='28' font-weight='700'>{esc(s.get('slot'))}</text>"
                     f"<text x='{x + 14}' y='{y + 64}' fill='#e9eef7' font-size='12'>{esc(s.get('fit_1') or 'absent')}"
                     f"{'' if s.get('fit_1') == s.get('fit_2') else ' / ' + esc(s.get('fit_2'))}</text>"
                     f"<text x='{x + 14}' y='{y + 86}' fill='#8f9db2' font-size='11'>{esc(s.get('status', ''))}</text></g>")
    pt = me.get("product_test") or {}
    body = [f"<h1>Master Equation</h1><div class='mut'>{esc(paper)}</div>",
            f"<p>{esc(me.get('one_line', ''))}</p><div class='grid'>",
            f"<div class='card'><div class='k'>Product test</div><div class='big'>{esc(pt.get('run1', '—'))}</div><div class='mut'>{esc(pt.get('status', ''))}: {esc(pt.get('reason', ''))[:220]}</div></div>",
            f"<div class='card'><div class='k'>Analog strength</div><div class='big'>{esc(me.get('analog_strength', '—'))} / 5</div><div class='mut'>spread {esc(me.get('analog_strength_spread', ''))}</div></div>",
            f"<div class='card'><div class='k'>Slots filled</div><div class='big'>{sum(1 for s in slots if FIT.get(s.get('fit_1') or 'absent', 0) > 0)} / {len(slots)}</div><div class='mut'>equations present: {esc(me.get('equations_present'))}</div></div></div>",
            f"<h2>The ten slots</h2><svg viewBox='0 0 1080 {120 * ((len(slots) + 4) // 5)}' width='100%'>{''.join(cells)}</svg>",
            "<h2>What plays each role</h2><table><tr><th>Slot</th><th>Plays the role</th><th>Quote</th></tr>"]
    body += [f"<tr><td class='mono'>{esc(s.get('slot'))}</td><td>{esc(s.get('plays_role', ''))}</td><td><q>{esc(s.get('quote', ''))}</q></td></tr>" for s in slots]
    body.append("</table>")
    if me.get("breaks"):
        body.append("<h2>Where the analogy breaks</h2><ul>" + "".join(f"<li>{esc(b if isinstance(b, str) else json.dumps(b, ensure_ascii=False))[:300]}</li>" for b in me["breaks"]) + "</ul>")
    return page(f"Master Equation · {paper}", "".join(body))


# ------------------------------------------------------------------ lean

def lean_page(run: Path, paper: str) -> str:
    ln = load(run, "lean4.json") or {}
    cands = ln.get("formal_candidates", [])
    body = [f"<h1>Lean 4</h1><div class='mut'>{esc(paper)} · {len(cands)} formalization candidate(s)</div>",
            f"<p class='dim'>{esc(ln.get('notes', ''))}</p><div class='grid' style='grid-template-columns:1fr'>"]
    for c in cands:
        fo, rb, ss = c.get("formal_object") or {}, c.get("result_and_boundary") or {}, c.get("source_selection") or {}
        assum = (c.get("assumptions_and_dependencies") or {})
        body.append(f"<div class='card'><h3>{esc((c.get('identity') or {}).get('claim_id'))} · {esc(fo.get('object_type'))} "
                    f"<span class='tag'>{esc(ss.get('selection_disposition'))}</span><span class='tag'>{esc(rb.get('verification_status'))}</span></h3>"
                    f"<div class='k'>Proposed statement</div><p>{esc(fo.get('exact_proposed_statement', ''))}</p>"
                    f"<div class='k'>From the paper</div><p><q>{esc(ss.get('exact_source_expression', ''))}</q></p>"
                    f"<div class='k'>What it would establish</div><p class='mut'>{esc(rb.get('what_is_established', ''))}</p>"
                    f"<div class='k'>Assumptions</div><p class='mut'>{esc(json.dumps(assum, ensure_ascii=False))[:500]}</p></div>")
    body.append("</div>")
    return page(f"Lean 4 · {paper}", "".join(body))


# ------------------------------------------------------------------ axioms

def axioms_page(run: Path, paper: str) -> str:
    ax = load(run, "axiom_nodes.json") or {}
    nodes = ax.get("axiom_nodes", [])
    modes = ["AX_CORE", "AX_DERIVED", "AX_SCAFFOLD", "FW_EXTENDED", "HY_EVIDENCE"]
    aligns = ["directly_asserted", "supported", "relevant_but_not_asserted", "contested"]
    count = {(m, a): sum(1 for n in nodes if n.get("mode") == m and n.get("alignment") == a) for m in modes for a in aligns}
    top = max(count.values() or [1]) or 1
    grid = ["<table><tr><th></th>" + "".join(f"<th>{esc(a.replace('_', ' '))}</th>" for a in aligns) + "</tr>"]
    for m in modes:
        grid.append(f"<tr><td class='mono'>{m}</td>" + "".join(
            f"<td style='background:rgba(217,169,74,{count[(m, a)] / top * .55:.2f})'>{count[(m, a)] or ''}</td>" for a in aligns) + "</tr>")
    grid.append("</table>")
    body = [f"<h1>Axioms</h1><div class='mut'>{esc(paper)} · {len(nodes)} axiom node(s) engaged · primary mode {esc(ax.get('primary_mode', ''))}</div>",
            "<h2>Mode x alignment</h2>", "".join(grid), "<h2>Each node</h2><table><tr><th>Node</th><th>Mode</th><th>Alignment</th><th>Quote</th></tr>"]
    order = {a: i for i, a in enumerate(aligns)}
    for n in sorted(nodes, key=lambda n: (order.get(n.get("alignment"), 9), n.get("node_id", ""))):
        body.append(f"<tr><td class='mono'>{esc(n.get('node_id'))} {esc(n.get('name'))}</td><td>{esc(n.get('mode'))}</td>"
                    f"<td>{esc(n.get('alignment'))}</td><td><q>{esc(n.get('evidence_quote', ''))}</q></td></tr>")
    body.append("</table>")
    if ax.get("unmapped_claims"):
        body.append("<h2>Claims no axiom node covers</h2><ul>" + "".join(
            f"<li>{esc(c if isinstance(c, str) else json.dumps(c, ensure_ascii=False))[:300]}</li>" for c in ax["unmapped_claims"]) + "</ul>")
    return page(f"Axioms · {paper}", "".join(body))


# ------------------------------------------------------------------ combined

REPORTS = [("ledger", "Claims · Proof · Evidence", ledger_page), ("fruits", "Fruits of the Spirit", fruits_page),
           ("master_equation", "Master Equation", me_page), ("lean", "Lean 4", lean_page), ("axioms", "Axioms", axioms_page)]


def combined(pages: list[tuple[str, str, str]], paper: str, overview: str | None) -> str:
    tabs = ([("overview", "Overview", overview)] if overview else []) + pages
    buttons = "".join(f"<button data-t='{k}'{' class=on' if i == 0 else ''}>{esc(t)}</button>" for i, (k, t, _) in enumerate(tabs))
    frames = "".join(f"<iframe id='f-{k}' srcdoc=\"{html.escape(doc, quote=True)}\"{'' if i == 0 else ' hidden'}></iframe>"
                     for i, (k, _, doc) in enumerate(tabs))
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>API Deep · {esc(paper)}</title><style>{CSS}
.bar{{position:sticky;top:0;z-index:5;display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:10px 16px;background:rgba(11,13,18,.95);border-bottom:1px solid var(--line)}}
.bar b{{font:700 12px var(--mono);letter-spacing:.12em;color:var(--gold);margin-right:12px;text-transform:uppercase}}
.bar button{{border:1px solid var(--line);background:var(--panel);color:var(--mut);border-radius:999px;padding:6px 13px;cursor:pointer;font:600 11px var(--mono)}}
.bar button.on{{border-color:var(--cyan);color:var(--cyan)}}iframe{{display:block;width:100%;height:calc(100vh - 52px);border:0}}iframe[hidden]{{display:none}}
</style></head><body><div class='bar'><b>API Deep · {esc(paper)}</b>{buttons}</div>{frames}
<script>document.querySelectorAll('.bar button').forEach(function(b){{b.onclick=function(){{
document.querySelectorAll('.bar button').forEach(function(x){{x.classList.toggle('on',x===b)}});
document.querySelectorAll('iframe').forEach(function(f){{f.hidden=f.id!=='f-'+b.dataset.t}});}}}});</script></body></html>"""


def build_all(run: Path, paper: str | None = None) -> Path:
    paper = paper or run.parent.name
    pages = []
    for key, title, fn in REPORTS:
        try:
            doc = fn(run, paper)
        except Exception as exc:                           # one report failing never loses the others
            doc = page(title, f"<h1>{esc(title)}</h1><p class='bad'>Not built: {esc(type(exc).__name__)}: {esc(exc)}</p>")
        (run / f"REPORT_{key}.html").write_text(doc, encoding="utf-8")
        pages.append((key, title, doc))
    overview = (run / "API_DEEP.html").read_text(encoding="utf-8") if (run / "API_DEEP.html").is_file() else None
    out = run / "REPORT.html"
    out.write_text(combined(pages, paper, overview), encoding="utf-8")
    return out


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:] or ["."]:
        print(build_all(Path(arg).resolve()))
