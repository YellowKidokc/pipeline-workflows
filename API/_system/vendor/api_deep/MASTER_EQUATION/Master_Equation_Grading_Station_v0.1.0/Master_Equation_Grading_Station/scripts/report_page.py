"""report_page.py -- Paper Grade Dashboard (Master Equation Grading Station).

Renders grading_out/<paper>.report.html from the four run JSONs
(<paper>.lexicon.json, <paper>.stats.json, <paper>.spans.json,
<paper>.canon.json). Follows the master paper-grade-dashboard template: fixed
topbar with section nav, hero with grade badge, stats ribbon, pg-sec-head
section pattern (dot + kicker + h2 + desc), pg- class prefix, BEGIN/END
component markers, data-component/data-name attributes, design tokens
(--bg:#050505, --gold:#d4af37, --green:#4ade80, --amber:#fb923c,
--red:#f87171, --blue:#38bdf8, Oswald/Crimson Text/Inter/JetBrains Mono,
max-width 1100px).

Charts are inline SVG generated in Python (charts_svg.py) -- no external JS
libraries; works over file:// and prints. Tiny vanilla JS only for the
heartbeat hover inspector, the ledger click-through, and the canon-docket
verdict filter.

Sections: Metrics (stats ribbon) / Heartbeat (per-sentence ME score EKG with
hover inspector + top-5 peaks & valleys) / Slots (ten-slot coverage chart;
absent slots shown as gaps, never hidden) / Product Test (spans with role
PRODUCT_TEST) / Ledger (clickable span table; dropped signals in a collapsed
"dropped, never data" block) / Canon (the canon docket: one row per claim,
five condition checkmarks, verdict badge, verdict filter, retirement watch) /
Reading ("The Reading", an essayist profile of the paper -- one DeepSeek call
at temp 0.3 with prompt prompts/me_narrative_v1.0.txt, cached in
grading_out/<paper>.narrative.json -- reused when both the brief hash and the
narrative prompt hash match; skipped gracefully without DEEPSEEK_API_KEY).

Every number on the page traces to the run JSONs.

Inputs:
  --paper  Path to the graded paper.
"""

import argparse
import hashlib
import html
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

import charts_svg

sys.stdout.reconfigure(encoding="utf-8")

STATION_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
OUT_DIR = STATION_DIR / "grading_out"
RUBRIC_PATH = SCRIPTS_DIR / "rubric" / "me_rubric_v0.1.0.json"
WEIGHTS_PATH = SCRIPTS_DIR / "weights.json"
NARRATIVE_PROMPT_PATH = SCRIPTS_DIR / "prompts" / "me_narrative_v1.0.txt"
NARRATIVE_PROMPT_VERSION = "me_narrative_v1.0"
STAGE = "me_report_page_v1"

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

SLOT_AXES = ["g", "m", "e", "s_eff", "t", "k", "r", "q", "f", "c"]
SLOT_CATEGORIES = [f"slot_{a}" for a in SLOT_AXES]
CANON_CONDITIONS = ["address", "grade", "receipt", "authority", "no_conflict"]
VERDICTS = ["CANON-READY", "HOLD", "NEEDS-RULING"]

# DeepSeek standard list rates (USD per 1M tokens) used for the cost estimate.
RATE_HIT, RATE_MISS, RATE_OUT = 0.07, 0.27, 1.10


def esc(s):
    return html.escape(str(s), quote=True)


def js_data(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def clamp_text(s, n=140):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


# ---------------------------------------------------------------------------
# "The Reading" -- one DeepSeek call, cached by brief hash + prompt hash
# ---------------------------------------------------------------------------

def build_brief(spans_doc, stats_doc, canon_doc, slot_totals, absent_slots,
                product_spans, role_dist, peaks, valleys):
    cm = canon_doc["manifest"]
    hold_claims = []
    for c in canon_doc["claims"]:
        if c["verdict"] == "CANON-READY":
            continue
        fails = [k for k in CANON_CONDITIONS if not c["conditions"][k]["pass"]]
        hold_claims.append({"id": c["id"], "statement": c["statement"][:200],
                            "claim_type": c["claim_type"], "verdict": c["verdict"],
                            "failing_conditions": fails})
    return {
        "paper": spans_doc["paper"],
        "in_report_stats": [
            {"key": s["key"], "value": s["value"], "unit": s["unit"]}
            for s in stats_doc["stats"] if s["in_report"]],
        "slot_totals": slot_totals,
        "slot_coverage": f"{len(SLOT_AXES) - len(absent_slots)}/10",
        "absent_slots": absent_slots,
        "product_test_span_count": len(product_spans),
        "role_distribution": dict(role_dist),
        "spans_judged": sum(1 for s in spans_doc["spans"] if s["status"] == "ok"),
        "verdict_counts": cm["verdict_counts"],
        "claims_processed": cm["claims_processed"],
        "normalization": cm["normalization"],
        "hold_and_needs_ruling_claims": hold_claims[:20],
        "retirement_watch": canon_doc.get("retirement_watch", []),
        "peaks": peaks,
        "valleys": valleys,
    }


def load_narrative_prompt():
    if not NARRATIVE_PROMPT_PATH.exists():
        sys.exit(f"ERROR: missing narrative prompt {NARRATIVE_PROMPT_PATH}")
    text = NARRATIVE_PROMPT_PATH.read_text(encoding="utf-8")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, sha


def what_this_means(api_key, brief, prompt_text):
    body = {
        "model": MODEL,
        "temperature": 0.3,
        "max_tokens": 1400,
        "messages": [
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": json.dumps(brief, ensure_ascii=False)},
        ],
    }
    r = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=body, timeout=240,
    )
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"], data.get("usage", {})


def get_narrative(stem, brief, prompt_text, prompt_sha):
    """Return (reading, meta). Reuses grading_out/<stem>.narrative.json when
    the brief hash AND the narrative prompt hash match; otherwise makes the
    single API call."""
    cache_path = OUT_DIR / f"{stem}.narrative.json"
    brief_sha = hashlib.sha256(
        json.dumps(brief, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    if cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            if (cached.get("brief_sha256") == brief_sha
                    and cached.get("narrative_prompt_sha256") == prompt_sha):
                print("[report] narrative: cache hit (0 API calls)")
                return cached["reading"], f"cached narrative · generated {cached.get('generated_at', '?')}"
        except (ValueError, KeyError):
            pass
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return "[The Reading SKIPPED: DEEPSEEK_API_KEY not set]", "skipped"
    try:
        reading, usage = what_this_means(api_key, brief, prompt_text)
        cache_path.write_text(json.dumps({
            "stage": STAGE,
            "brief_sha256": brief_sha,
            "narrative_prompt": NARRATIVE_PROMPT_VERSION,
            "narrative_prompt_sha256": prompt_sha,
            "reading": reading, "usage": usage,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": MODEL, "temperature": 0.3,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[report] narrative: 1 API call, {usage.get('total_tokens', '?')} tokens")
        return reading, (f"generated by {MODEL} (temperature 0.3), "
                         f"prompt {NARRATIVE_PROMPT_VERSION}, "
                         f"tokens: {usage.get('total_tokens', '?')}")
    except Exception as e:
        return f"[The Reading generation FAILED: {type(e).__name__}: {e}]", "error"


def reading_to_html(reading):
    out = []
    for para in esc(reading).split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.startswith("## "):
            out.append(f'<h3 class="pg-read-h">{esc(para[3:])}</h3>')
        elif para.startswith("# "):
            out.append(f'<h3 class="pg-read-h">{esc(para[2:])}</h3>')
        else:
            out.append(f"<p>{para}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Page CSS (template tokens + heartbeat/ledger/canon additions)
# ---------------------------------------------------------------------------

CSS = """
:root{
  --bg:#050505; --surface:#0a0a0a; --surface2:#111; --surface3:#1a1a1a;
  --border:#222; --border-2:#2a2a2a; --border-hi:#3a3a3a;
  --text:#e5e3df; --text-dim:#9a9a9a; --text-muted:#5a5a5a;
  --gold:#d4af37; --gold-dim:rgba(212,175,55,.1);
  --green:#4ade80; --green-dim:rgba(74,222,128,.1);
  --amber:#fb923c; --amber-dim:rgba(251,146,60,.1);
  --red:#f87171; --red-dim:rgba(248,113,113,.1);
  --blue:#38bdf8; --blue-dim:rgba(56,189,248,.1);
  --serif:'Crimson Text',Georgia,serif; --mono:'JetBrains Mono',ui-monospace,monospace;
  --display:'Oswald','Inter',sans-serif; --sans:'Inter',system-ui,sans-serif;
  --max:1100px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}

/* ═══════ COMPONENT:topbar ═══════ */
.pg-header{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:space-between;padding:.65rem 1.5rem;backdrop-filter:blur(14px) saturate(140%);background:rgba(8,8,8,.92);border-bottom:1px solid var(--border)}
.pg-brand{display:flex;align-items:center;gap:.6rem}
.pg-mark{font-family:var(--serif);font-size:1.3rem;color:var(--gold);line-height:1}
.pg-name{font-family:var(--mono);font-size:.58rem;letter-spacing:.2em;color:var(--text-muted);text-transform:uppercase}
.pg-name span{color:var(--gold)}
.pg-nav{display:flex;gap:.1rem;flex-wrap:wrap}
.pg-nav a{font-family:var(--display);font-size:.55rem;letter-spacing:.12em;text-transform:uppercase;padding:.4rem .55rem;border-radius:4px;color:var(--text-dim);transition:all .15s}
.pg-nav a:hover,.pg-nav a.active{color:var(--gold);background:var(--gold-dim)}
@media(max-width:800px){.pg-nav{display:none}}

/* ═══════ COMPONENT:hero ═══════ */
.pg-hero{position:relative;padding:6.5rem 1.5rem 2.5rem;overflow:hidden}
.pg-hero::before{content:'';position:absolute;top:15%;left:50%;transform:translate(-50%,-50%);width:700px;height:350px;background:radial-gradient(ellipse,rgba(212,175,55,.04) 0%,transparent 65%);pointer-events:none}
.pg-hero-inner{max-width:var(--max);margin:0 auto;position:relative}
.pg-hero-row{display:flex;align-items:flex-start;justify-content:space-between;gap:2rem;flex-wrap:wrap}
.pg-hero-text{flex:1;min-width:260px}
.pg-hero-eyebrow{font-family:var(--mono);font-size:.58rem;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);margin-bottom:.7rem}
.pg-hero h1{font-family:var(--display);font-weight:500;font-size:clamp(1.8rem,4.5vw,3rem);line-height:1.08;color:#fff;margin-bottom:.7rem;letter-spacing:.02em}
.pg-hero-sub{font-family:var(--serif);font-size:1rem;color:var(--text-dim);line-height:1.55;font-style:italic;max-width:560px;margin-bottom:.8rem}
.pg-hero-address{font-family:var(--mono);font-size:.62rem;color:var(--text-muted);line-height:1.7;padding:.8rem 1rem;background:var(--surface2);border:1px solid var(--border);border-radius:6px;margin-top:.6rem;overflow-wrap:anywhere}
.pg-hero-address b{color:var(--text-dim)}
.pg-grade-badge{flex:0 0 auto;padding:1.3rem 1.8rem;background:var(--surface2);border:1px solid var(--border);border-radius:8px;text-align:center;min-width:150px}
.pg-grade-label{font-family:var(--mono);font-size:.52rem;letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted);margin-bottom:.35rem}
.pg-grade-value{font-family:var(--display);font-size:2.8rem;color:var(--gold);line-height:1}
.pg-grade-sub{font-family:var(--mono);font-size:.55rem;color:var(--text-dim);margin-top:.35rem}

/* ═══════ COMPONENT:stats-ribbon ═══════ */
.pg-stats{max-width:var(--max);margin:0 auto;padding:0 1.5rem 2.5rem}
.pg-stats-inner{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:0;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--surface2)}
.pg-stat{padding:1rem .6rem;text-align:center;border-right:1px solid var(--border)}
.pg-stat:last-child{border-right:0}
.pg-stat-num{font-family:var(--display);font-size:1.35rem;color:var(--gold);display:block;margin-bottom:.15rem}
.pg-stat-label{font-family:var(--mono);font-size:.5rem;color:var(--text-dim);text-transform:uppercase;letter-spacing:.08em}

/* ═══════ COMPONENT:section:generic ═══════ */
.pg-sec{max-width:var(--max);margin:0 auto;padding:2.5rem 1.5rem}
.pg-sec-head{display:flex;align-items:center;gap:.7rem;margin-bottom:.45rem}
.pg-sec-dot{width:7px;height:7px;border-radius:50%;background:var(--gold)}
.pg-sec-kicker{font-family:var(--mono);font-size:.6rem;color:var(--text-muted);letter-spacing:.15em;text-transform:uppercase}
.pg-sec h2{font-family:var(--serif);font-size:clamp(1.25rem,2.5vw,1.6rem);font-weight:400;color:#fff;margin-bottom:.2rem}
.pg-sec-desc{font-size:.84rem;color:var(--text-dim);max-width:640px;margin-bottom:1.3rem;line-height:1.55}
.pg-panel{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:1.1rem 1.2rem}

/* ═══════ COMPONENT:heartbeat ═══════ */
.pg-inspector{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:.9rem 1.1rem;margin-bottom:.8rem;min-height:96px}
.pg-inspector h3{font-family:var(--mono);font-size:.58rem;letter-spacing:.15rem;color:var(--gold);text-transform:uppercase;margin-bottom:.45rem}
.pg-insp-text{font-family:var(--serif);font-size:1.02rem;color:var(--text);margin-bottom:.45rem}
.pg-insp-meta{display:flex;gap:1.1rem;flex-wrap:wrap;font-size:.72rem;color:var(--text-dim)}
.pg-insp-meta span{font-family:var(--mono)}
.pg-toggle-row{display:flex;gap:.45rem;flex-wrap:wrap;margin-bottom:.7rem}
.pg-toggle{background:var(--surface2);border:1px solid var(--border);color:var(--text-dim);padding:.25rem .7rem;border-radius:4px;cursor:pointer;font-size:.72rem;font-family:var(--sans)}
.pg-toggle:hover{border-color:var(--gold);color:var(--text)}
.pg-toggle.active{background:var(--gold);color:#000;border-color:var(--gold)}
.pg-ekg-tables{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:1rem}
@media(max-width:800px){.pg-ekg-tables{grid-template-columns:1fr}}

/* ═══════ COMPONENT:ledger ═══════ */
.pg-table-wrap{overflow:auto;-webkit-overflow-scrolling:touch;max-height:560px;border:1px solid var(--border);border-radius:8px}
.pg-table{width:100%;border-collapse:collapse;font-size:.78rem;min-width:760px}
.pg-table th{text-align:left;padding:.6rem .7rem;font-family:var(--mono);font-size:.52rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.08em;border-bottom:1px solid var(--border);font-weight:500;position:sticky;top:0;background:var(--bg)}
.pg-table td{padding:.45rem .7rem;border-bottom:1px solid var(--border-2);color:var(--text);vertical-align:top}
.pg-table tbody tr{cursor:pointer}
.pg-table tbody tr:hover td{background:var(--surface2)}
.pg-table tbody tr.sel td{background:var(--surface3)}
.pg-table td:first-child{font-family:var(--mono);font-size:.7rem;color:var(--gold);white-space:nowrap}
.pg-chip{display:inline-block;font-family:var(--mono);font-size:.55rem;padding:.12rem .4rem;border-radius:3px;letter-spacing:.05em;background:var(--blue-dim);color:var(--blue)}
.pg-flag{font-family:var(--mono);font-size:.62rem;color:var(--amber)}
.pg-kill{font-family:var(--mono);font-size:.62rem;color:var(--red)}
.pg-conf{font-family:var(--mono);font-size:.68rem;color:var(--text-dim)}
.pg-detail{display:none;margin-top:.9rem}
.pg-detail pre{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:.8rem;font:11px/1.5 var(--mono);color:var(--text);white-space:pre-wrap;max-height:300px;overflow:auto}
.pg-detail h3{font-family:var(--mono);font-size:.6rem;letter-spacing:.12em;color:var(--blue);text-transform:uppercase;margin:.9rem 0 .3rem}
details.pg-dropped{margin-top:.9rem;border:1px solid var(--border);border-radius:8px;background:var(--surface2)}
details.pg-dropped summary{padding:.7rem 1rem;cursor:pointer;font-family:var(--mono);font-size:.62rem;letter-spacing:.12em;color:var(--red);text-transform:uppercase}
details.pg-dropped div{padding:.4rem 1rem;font-size:.74rem;color:var(--text-dim);border-top:1px solid var(--border-2)}

/* ═══════ COMPONENT:canon ═══════ */
.pg-check{display:inline-block;width:18px;text-align:center;font-family:var(--mono);font-size:.72rem;border-radius:3px;cursor:default}
.pg-check.pass{background:var(--green-dim);color:var(--green)}
.pg-check.fail{background:var(--red-dim);color:var(--red)}
.pg-verdict{display:inline-block;padding:.15rem .6rem;border-radius:10px;font-size:.62rem;font-weight:600;letter-spacing:.05em;font-family:var(--mono);white-space:nowrap}
.pg-verdict.CANON-READY{background:var(--green-dim);color:var(--green)}
.pg-verdict.HOLD{background:var(--amber-dim);color:var(--amber)}
.pg-verdict.NEEDS-RULING{background:var(--red-dim);color:var(--red)}
.pg-canon-note{font-size:.72rem;color:var(--text-muted);margin-top:.8rem}
.pg-canon-note a{color:var(--gold)}
.pg-canon-note a:hover{text-decoration:underline}
.pg-retire{margin-top:1rem;padding:.9rem 1.1rem;background:var(--surface2);border:1px solid var(--border);border-left:3px solid var(--amber);border-radius:6px;font-size:.78rem;color:var(--text-dim)}
.pg-retire h3{font-family:var(--mono);font-size:.58rem;letter-spacing:.15em;color:var(--amber);text-transform:uppercase;margin-bottom:.4rem}

/* ═══════ COMPONENT:product-test ═══════ */
.pg-pt-card{background:var(--surface2);border:1px solid var(--border);border-left:3px solid var(--gold);border-radius:6px;padding:.9rem 1.1rem;margin-bottom:.7rem;font-size:.82rem;color:var(--text-dim)}
.pg-pt-card .pg-quote{font-family:var(--serif);font-style:italic;color:var(--text)}
.pg-pt-terms{font-family:var(--mono);font-size:.6rem;color:var(--blue);margin-top:.35rem}

/* ═══════ COMPONENT:report ═══════ */
.pg-reading p{font-size:.92rem;color:var(--text);margin-bottom:.9rem;line-height:1.7}
.pg-read-h{font-family:var(--serif);font-size:1.1rem;color:var(--gold);margin:1.1rem 0 .5rem}
.pg-read-meta{font-family:var(--mono);font-size:.58rem;color:var(--text-muted);margin-top:.8rem}

/* ═══════ COMPONENT:footer ═══════ */
.pg-footer{max-width:var(--max);margin:2.5rem auto 0;padding:2rem 1.5rem;text-align:center;border-top:1px solid var(--border)}
.pg-footer .feq{font-family:var(--mono);font-size:.7rem;color:var(--gold);opacity:.5;margin-bottom:.5rem}
.pg-footer p{color:var(--text-muted);font-size:.72rem;margin:.2rem 0}

@media(max-width:640px){
  .pg-hero-row{flex-direction:column}
  .pg-grade-badge{align-self:flex-start}
  .pg-stats-inner{grid-template-columns:repeat(3,1fr)}
  .pg-stat{border-bottom:1px solid var(--border)}
}
@media print{.pg-header{position:static}.pg-table-wrap{max-height:none;overflow:visible}}
"""

JS = r"""
/* ═══════ COMPONENT:script:scroll-header ═══════ */
window.addEventListener('scroll',()=>{
  document.getElementById('pg-header').classList.toggle('pg-header-scrolled', window.scrollY > 60);
});
/* ═══════ COMPONENT:script:smooth-nav ═══════ */
document.querySelectorAll('.pg-nav a[href^="#"]').forEach(link=>{
  link.addEventListener('click', e=>{
    const target = document.querySelector(link.getAttribute('href'));
    if(target){ e.preventDefault(); target.scrollIntoView({behavior:'smooth', block:'start'}); }
  });
});
/* ═══════ COMPONENT:script:heartbeat-inspector ═══════ */
const HB = %HB_DATA%;
const HBM = %HB_META%;
function hbMove(evt){
  const r = evt.target.getBoundingClientRect();
  let idx = Math.round((evt.clientX - r.left) / r.width * (HBM.n - 1));
  idx = Math.max(0, Math.min(HBM.n - 1, idx));
  const s = HB[idx];
  document.getElementById('hb-text').textContent = s.t;
  document.getElementById('hb-idx').textContent = 's' + s.i;
  document.getElementById('hb-total').textContent = s.w.toFixed(2);
  document.getElementById('hb-slots').textContent = s.c[0];
  document.getElementById('hb-pt').textContent = s.c[1];
  document.getElementById('hb-ground').textContent = s.c[2];
  document.getElementById('hb-contra').textContent = s.c[3];
  document.getElementById('hb-drift').textContent = s.c[4];
  document.getElementById('hb-prop').textContent = s.c[5];
  const cur = document.getElementById('hb-cursor');
  cur.setAttribute('x1', HBM.padL + idx / Math.max(1, HBM.n - 1) * HBM.iw);
  cur.setAttribute('x2', HBM.padL + idx / Math.max(1, HBM.n - 1) * HBM.iw);
  cur.setAttribute('visibility', 'visible');
}
function hbLeave(){ document.getElementById('hb-cursor').setAttribute('visibility','hidden'); }
function hbToggle(id, btn){
  const el = document.getElementById(id);
  el.style.display = (el.style.display === 'none') ? '' : 'none';
  btn.classList.toggle('active');
}
/* ═══════ COMPONENT:script:ledger-detail ═══════ */
const DETAIL = %DETAIL%;
function showSpan(id){
  document.querySelectorAll('#pg-ledger tbody tr').forEach(r=>
    r.classList.toggle('sel', r.dataset.span === String(id)));
  const d = DETAIL[id]; if(!d) return;
  const el = document.getElementById('pg-detail');
  el.style.display = 'block';
  document.getElementById('d-title').textContent =
    'Span ' + id + '  ·  sentences ' + d.range + '  ·  ' + d.role;
  document.getElementById('d-text').textContent = d.text;
  document.getElementById('d-lex').textContent = d.lex;
  document.getElementById('d-json').textContent = JSON.stringify(d.judgment, null, 2);
  el.scrollIntoView({behavior:'smooth', block:'nearest'});
}
/* ═══════ COMPONENT:script:canon-filter ═══════ */
function canonFilter(v, btn){
  document.querySelectorAll('#pg-canon tbody tr').forEach(r=>{
    r.style.display = (v === 'ALL' || r.dataset.verdict === v) ? '' : 'none';
  });
  document.querySelectorAll('.pg-canon-filter').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
}
"""


def span_lex_summary(sp, lex):
    by_idx = {s["idx"]: s for s in lex["sentences"]}
    out = []
    for i in range(sp["sent_idx_start"], sp["sent_idx_end"] + 1):
        s = by_idx.get(i)
        if not s:
            continue
        matched = {c: s["categories"][c]["matched_terms"]
                   for c in SLOT_CATEGORIES + ["product_test", "fit_language",
                                               "canon_status", "drift_marker",
                                               "grounding", "contradiction"]
                   if s["categories"][c]["matched_terms"]}
        out.append({"idx": i, "matched": matched,
                    "claim_strength": {k: v for k, v in s["claim_strength"].items() if v},
                    "hedges": s["hedges"], "absolutes": s["absolutes"]})
    return out


def main():
    ap = argparse.ArgumentParser(description="Paper Grade Dashboard — Master Equation Grading Station.")
    ap.add_argument("--paper", required=True, help="Path to the graded paper.")
    args = ap.parse_args()

    stem = Path(args.paper).stem
    lex = json.loads((OUT_DIR / f"{stem}.lexicon.json").read_text(encoding="utf-8"))
    stats_doc = json.loads((OUT_DIR / f"{stem}.stats.json").read_text(encoding="utf-8"))
    spans_path = OUT_DIR / f"{stem}.spans.json"
    canon_path = OUT_DIR / f"{stem}.canon.json"
    for p, stage in ((spans_path, "span_judge.py"), (canon_path, "canon_ledger_pass.py")):
        if not p.exists():
            sys.exit(f"ERROR: missing {p} -- run {stage} first.")
    spans_doc = json.loads(spans_path.read_text(encoding="utf-8"))
    canon_doc = json.loads(canon_path.read_text(encoding="utf-8"))
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    slot_names = {sl["id"].replace("slot.", ""): sl["name"] for sl in rubric["slots"]}

    sbk = {s["key"]: s for s in stats_doc["stats"]}
    ok_spans = [s for s in spans_doc["spans"] if s["status"] == "ok"]
    m = spans_doc["manifest"]
    cm = canon_doc["manifest"]

    # ---- aggregates ---------------------------------------------------------
    gate_counts = Counter()
    for sp in ok_spans:
        for g in sp["judgment"]["gate_flags"]:
            gate_counts[g] += 1

    span_signals = {a: {"+": 0, "-": 0} for a in SLOT_AXES}
    for sp in ok_spans:
        for sig in sp["judgment"]["slot_signals"]:
            a = sig.get("slot_id", "").replace("slot.", "")
            pol = sig.get("polarity", 0)
            if a in span_signals and pol in (1, -1):
                span_signals[a]["+" if pol == 1 else "-"] += 1

    slot_totals = {a: sbk.get(f"slot_axis.{a}.total", {}).get("value", 0) for a in SLOT_AXES}
    absent_slots = [a for a in SLOT_AXES
                    if slot_totals[a] == 0 and span_signals[a]["+"] == 0 and span_signals[a]["-"] == 0]
    coverage = f"{len(SLOT_AXES) - len(absent_slots)}/10"
    role_dist = Counter(sp["judgment"]["role"] for sp in ok_spans)
    n_sent = sbk.get("volume.sentences", {}).get("value", len(lex["sentences"]))
    n_words = sbk.get("volume.words", {}).get("value", 0)
    n_spans = len(spans_doc["spans"])
    me_score = sbk.get("me.score", {}).get("value", "?")
    verdict_counts = cm["verdict_counts"]

    span_tok = m.get("tokens", {})
    canon_tok = cm.get("tokens", {})
    tok = {"total": span_tok.get("total", 0) + canon_tok.get("total", 0),
           "cache_hit": span_tok.get("cache_hit", 0),
           "cache_miss": span_tok.get("cache_miss", 0) + canon_tok.get("prompt", 0),
           "completion": span_tok.get("completion", 0) + canon_tok.get("completion", 0)}
    cost = (tok["cache_hit"] * RATE_HIT + tok["cache_miss"] * RATE_MISS
            + tok["completion"] * RATE_OUT) / 1e6
    cost_str = f"${cost:.3f}"

    # ---- heartbeat -----------------------------------------------------------
    series = stats_doc["series"]["weighted_total"]
    smoothed = charts_svg.sma(series, window=9)
    heartbeat = charts_svg.heartbeat_svg(series, smoothed, len(series))
    hb_data = []
    for s in lex["sentences"]:
        cats = s["categories"]
        hb_data.append({
            "i": s["idx"],
            "t": s["text"][:160],
            "w": round(series[s["idx"]], 3),
            "c": [sum(cats[c]["hits"] for c in SLOT_CATEGORIES),
                  cats["product_test"]["hits"],
                  round(cats["grounding"]["weighted_score"], 2),
                  round(cats["contradiction"]["weighted_score"], 2),
                  cats["drift_marker"]["hits"],
                  round(cats["propaganda"]["weighted_score"], 2)],
        })
    hb_meta = {"n": len(series), "padL": 48, "iw": 1040 - 48 - 12}

    sent_by_idx = {s["idx"]: s for s in lex["sentences"]}

    def dom_cat(i):
        s = sent_by_idx[i]
        vals = {"slots": sum(s["categories"][c]["hits"] for c in SLOT_CATEGORIES),
                "product_test": s["categories"]["product_test"]["hits"],
                "grounding": s["categories"]["grounding"]["hits"],
                "contradiction": s["categories"]["contradiction"]["hits"],
                "drift_marker": s["categories"]["drift_marker"]["hits"],
                "propaganda": s["categories"]["propaganda"]["hits"]}
        return max(vals, key=lambda k: vals[k])

    order = sorted(range(len(series)), key=lambda i: series[i], reverse=True)
    peaks = order[:5]
    valleys = sorted(range(len(series)), key=lambda i: series[i])[:5]

    def ekg_rows(idxs, cls):
        rows = ""
        for i in idxs:
            rows += (f'<tr><td>{i}</td><td class="pg-conf" style="color:var(--{"green" if cls=="high" else "red"})">'
                     f'{series[i]:.2f}</td><td class="pg-flag">{dom_cat(i)}</td>'
                     f'<td style="color:var(--text-dim);font-size:.72rem">{esc(sent_by_idx[i]["text"][:110])}</td></tr>')
        return rows

    # ---- slot chart ----------------------------------------------------------
    slot_svg = charts_svg.slot_profile_svg(slot_totals, span_signals)

    # ---- product test ---------------------------------------------------------
    product_spans = [sp for sp in ok_spans if sp["judgment"]["role"] == "PRODUCT_TEST"]
    pt_html = ""
    for sp in product_spans:
        j = sp["judgment"]
        terms = sorted({t for i in range(sp["sent_idx_start"], sp["sent_idx_end"] + 1)
                        if i in sent_by_idx
                        for t in sent_by_idx[i]["categories"]["product_test"]["matched_terms"]})
        sig = "; ".join(f'{s["slot_id"].replace("slot.", "")} {"+" if s["polarity"] == 1 else "−" if s["polarity"] == -1 else "0"}'
                        f'/{s["fit"]}' for s in j["slot_signals"]) or "—"
        kill = (f'<br/><span class="pg-kill">kill: {esc(j["kill_condition"])}</span>'
                if j["kill_condition"] else "")
        flags = (f'<br/><span class="pg-flag">flags: {esc(", ".join(j["gate_flags"]))}</span>'
                 if j["gate_flags"] else "")
        pt_html += (f'<div class="pg-pt-card" data-component="card" data-name="product-test-span">'
                    f'<b>span {sp["span_id"]} · s{sp["sent_idx_start"]}–s{sp["sent_idx_end"]}</b> · signals: {esc(sig)}'
                    f'<br/><span class="pg-quote">“{esc(clamp_text(sp["text"], 280))}”</span>'
                    f'{kill}{flags}'
                    f'<div class="pg-pt-terms">answer language: {esc(", ".join(terms)) or "—"}</div></div>')
    if not product_spans:
        pt_html = ('<p class="pg-sec-desc" style="margin-bottom:0">No span was judged '
                   'PRODUCT_TEST in this run.</p>')

    # ---- ledger ---------------------------------------------------------------
    detail_js = {}
    rows_html = ""
    dropped_all = []
    for sp in spans_doc["spans"]:
        rng = f's{sp["sent_idx_start"]}–{sp["sent_idx_end"]}'
        if sp["status"] == "ok":
            j = sp["judgment"]
            sig = "; ".join(f'{s["slot_id"].replace("slot.", "")} '
                            f'{"+" if s["polarity"] == 1 else "−" if s["polarity"] == -1 else "0"}'
                            f'/{s["fit"]}/{s.get("quote_status", "?")}'
                            for s in j["slot_signals"]) or "—"
            gates = ", ".join(j["gate_flags"])
            kill = j["kill_condition"][:80]
            rows_html += (f'<tr data-span="{sp["span_id"]}" onclick="showSpan({sp["span_id"]})">'
                          f'<td>{sp["span_id"]}</td><td class="pg-conf">{rng}</td>'
                          f'<td><span class="pg-chip">{j["role"]}</span></td>'
                          f'<td style="font-size:.68rem">{esc(sig)}</td>'
                          f'<td class="pg-flag">{esc(gates)}</td>'
                          f'<td class="pg-kill">{esc(kill)}</td>'
                          f'<td class="pg-conf">{j["confidence"]}</td></tr>')
            detail_js[sp["span_id"]] = {
                "range": rng, "role": j["role"], "text": sp["text"],
                "lex": json.dumps(span_lex_summary(sp, lex), ensure_ascii=False, indent=1),
                "judgment": j,
            }
            for d in sp.get("dropped_signals", []):
                dropped_all.append({"span_id": sp["span_id"], **d})
        else:
            rows_html += (f'<tr><td>{sp["span_id"]}</td><td class="pg-conf">{rng}</td>'
                          f'<td><span class="pg-chip">INVALID</span></td>'
                          f'<td colspan="4" class="pg-kill">{esc(sp.get("error", ""))}</td></tr>')

    if dropped_all:
        dropped_items = "".join(
            f'<div>span {d["span_id"]} · {esc(d["signal"].get("slot_id", "?"))} · '
            f'reason: {esc(d["reason"])} · quote: “{esc(str(d["signal"].get("quote", ""))[:120])}”</div>'
            for d in dropped_all)
        dropped_html = (f'<details class="pg-dropped" data-component="panel" data-name="dropped-signals">'
                        f'<summary>dropped, never data — {len(dropped_all)} unverifiable signal(s)</summary>'
                        f'{dropped_items}</details>')
    else:
        dropped_html = (f'<details class="pg-dropped" data-component="panel" data-name="dropped-signals">'
                        f'<summary>dropped, never data — 0 unverifiable signals</summary>'
                        f'<div>Every slot-signal quote verified against the source '
                        f'(exact {m.get("quotes_exact", 0)} · normalized {m.get("quotes_normalized", 0)} · '
                        f'corrected {m.get("quotes_corrected", 0)}).</div></details>')

    # ---- canon docket -----------------------------------------------------------
    canon_rows = ""
    for c in canon_doc["claims"]:
        checks = ""
        for cond in CANON_CONDITIONS:
            cd = c["conditions"][cond]
            cls = "pass" if cd["pass"] else "fail"
            mark = "✓" if cd["pass"] else "✗"
            checks += (f'<span class="pg-check {cls}" title="{esc(cond)}: {esc(cd.get("detail", ""))}">'
                       f'{mark}</span>')
        slots = ", ".join(s.replace("slot.", "") for s in c.get("slot_refs", [])) or "—"
        kill = (f'<div class="pg-kill" style="margin-top:.15rem">kill: {esc(clamp_text(c["kill_condition"], 100))}</div>'
                if c.get("kill_condition") else "")
        canon_rows += (f'<tr data-verdict="{esc(c["verdict"])}" style="cursor:default">'
                       f'<td>{esc(c["id"])}</td>'
                       f'<td>{esc(clamp_text(c["statement"]))}{kill}</td>'
                       f'<td class="pg-conf">{esc(c["claim_type"])}</td>'
                       f'<td class="pg-conf">{esc(slots)}</td>'
                       f'<td class="pg-conf">{esc(c.get("proposed_grade") or "—")}</td>'
                       f'<td style="white-space:nowrap">{checks}</td>'
                       f'<td><span class="pg-verdict {esc(c["verdict"])}">{esc(c["verdict"])}</span></td></tr>')

    filter_buttons = (
        f'<button class="pg-toggle pg-canon-filter active" onclick="canonFilter(\'ALL\', this)">all ({len(canon_doc["claims"])})</button>'
        + "".join(
            f'<button class="pg-toggle pg-canon-filter" onclick="canonFilter(\'{v}\', this)">'
            f'{v.lower()} ({verdict_counts.get(v, 0)})</button>'
            for v in VERDICTS))

    watch = canon_doc.get("retirement_watch", [])
    if watch:
        watch_items = "".join(
            f'<div style="margin:.3rem 0"><b>{esc(w["id"])}</b> ({esc(w["reason"])}): {esc(w["detail"])}'
            f'<br/><span style="font-size:.72rem">{esc(clamp_text(w["statement"], 120))}</span></div>'
            for w in watch)
    else:
        watch_items = ("<div>Empty — no receipt source changed since the previous canon.json, "
                       "and no canon-graded claim collides with a protected marker. "
                       "First run is empty by construction; the mechanism compares against the previous run.</div>")
    retirement_html = (f'<div class="pg-retire" data-component="panel" data-name="retirement-watch">'
                       f'<h3>Retirement Watch</h3>{watch_items}</div>')

    # ---- narrative ---------------------------------------------------------------
    brief_peaks = [{"idx": i, "score": round(series[i], 3),
                    "excerpt": sent_by_idx[i]["text"][:160]} for i in peaks]
    brief_valleys = [{"idx": i, "score": round(series[i], 3),
                      "excerpt": sent_by_idx[i]["text"][:160]} for i in valleys]
    brief = build_brief(spans_doc, stats_doc, canon_doc, slot_totals, absent_slots,
                        product_spans, role_dist, brief_peaks, brief_valleys)
    narrative_prompt_text, narrative_prompt_sha = load_narrative_prompt()
    reading, reading_meta = get_narrative(stem, brief, narrative_prompt_text,
                                          narrative_prompt_sha)
    reading_html = reading_to_html(reading)

    stats_ribbon = [
        (esc(str(me_score)), "ME_SCORE"),
        (esc(coverage), "Slot coverage"),
        (f"{m['ok']}/{n_spans}", "Spans judged"),
        (f"{cm['claims_processed']}", "Claims"),
        (f"{verdict_counts.get('CANON-READY', 0)}", "CANON-READY"),
        (f"{verdict_counts.get('HOLD', 0)}", "HOLD"),
        (f"{verdict_counts.get('NEEDS-RULING', 0)}", "NEEDS-RULING"),
        (cost_str, "Est. cost"),
    ]
    ribbon_html = "".join(
        f'<div class="pg-stat" data-component="stat" data-name="stat-{esc(l.lower().replace(" ", "-"))}">'
        f'<span class="pg-stat-num">{v}</span><span class="pg-stat-label">{esc(l)}</span></div>'
        for v, l in stats_ribbon)

    weights_sha = m.get("weights_sha256", "")
    gen_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    canon_md_name = f"{stem}.canon.md"

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<!--
  PAGE_META
  title: {esc(stem)} — Paper Grade Dashboard (Master Equation Grading Station)
  template: paper-grade-dashboard
  generator: report_page.py {STAGE} (Master Equation Grading Station)
-->
<head>
<!-- BEGIN:COMPONENT:head:head-paper-grade -->
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{esc(stem)} — Paper Grade Dashboard</title>
<meta name="author" content="David Lowe"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<!-- END:COMPONENT:head:head-paper-grade -->
<!-- BEGIN:COMPONENT:style:style-paper-grade -->
<style>{CSS}</style>
<!-- END:COMPONENT:style:style-paper-grade -->
</head>
<body>

<!-- BEGIN:COMPONENT:topbar:header-paper-grade -->
<header class="pg-header" id="pg-header" data-component="topbar" data-name="header-paper-grade">
  <span class="pg-brand">
    <span class="pg-mark">χ</span>
    <span class="pg-name"><span>Paper Grade</span> // Dashboard · Master Equation Station</span>
  </span>
  <nav class="pg-nav" aria-label="Dashboard navigation" data-component="nav" data-name="section-nav">
    <a href="#metrics">Metrics</a>
    <a href="#heartbeat">Heartbeat</a>
    <a href="#slots">Slots</a>
    <a href="#product-test">Product Test</a>
    <a href="#ledger">Ledger</a>
    <a href="#canon">Canon</a>
    <a href="#report">Reading</a>
  </nav>
</header>
<!-- END:COMPONENT:topbar:header-paper-grade -->

<!-- BEGIN:COMPONENT:hero:hero-paper-grade -->
<section class="pg-hero" data-component="hero" data-name="hero-paper-grade">
  <div class="pg-hero-inner">
    <div class="pg-hero-row">
      <div class="pg-hero-text" data-component="hero-text" data-name="hero-text">
        <div class="pg-hero-eyebrow" data-static="true">Master Equation Grading Station · Paper Grader Surface</div>
        <h1 id="main-content">{esc(stem)}</h1>
        <p class="pg-hero-sub">Five-pass grading: lexicon build, lexicon pass, statistics engine, span
        judgment, canon ledger. This page makes the audit readable — the canonical record remains the JSON/XLSX.</p>
        <div class="pg-hero-address" data-component="data-block" data-name="semantic-address">
          <b>Source:</b> {esc(spans_doc["paper"])}<br/>
          <b>Model:</b> {esc(m["model"])} · <b>Prompt:</b> {esc(m.get("prompt_version", ""))} sha {esc(m["prompt_sha256"][:12])} ·
          <b>Rubric:</b> sha {esc(m["rubric_sha256"][:12])}<br/>
          <b>Weights:</b> sha {esc(weights_sha[:12])} · <b>Spans:</b> {m["ok"]} ok / {m["invalid"]} invalid ·
          <b>Canon normalization:</b> {esc(cm["normalization"])} · <b>Tokens:</b> {tok["total"]:,} · <b>ME_SCORE:</b> {esc(str(me_score))}
        </div>
      </div>
      <div class="pg-grade-badge" data-component="data-block" data-name="grade-badge">
        <div class="pg-grade-label">Slot Coverage</div>
        <div class="pg-grade-value">{esc(coverage)}</div>
        <div class="pg-grade-sub">of ten slots appear<br/>ME_SCORE {esc(str(me_score))}<br/>absent: {esc(", ".join(absent_slots) or "none")}</div>
      </div>
    </div>
  </div>
</section>
<!-- END:COMPONENT:hero:hero-paper-grade -->

<!-- BEGIN:COMPONENT:section:stats-ribbon -->
<section class="pg-stats" id="metrics" data-component="section" data-name="stats-ribbon">
  <div class="pg-stats-inner">{ribbon_html}</div>
</section>
<!-- END:COMPONENT:section:stats-ribbon -->

<!-- BEGIN:COMPONENT:section:heartbeat -->
<section class="pg-sec" id="heartbeat" data-component="section" data-name="heartbeat">
  <div class="pg-sec-head"><span class="pg-sec-dot"></span><span class="pg-sec-kicker">Signal</span></div>
  <h2>Sentence Heartbeat — per-sentence ME score</h2>
  <p class="pg-sec-desc">Weighted score of every sentence (slots +1.0 · product test +1.5 · grounding +2.0 ·
  contradiction −0.5 · jargon −0.3 · propaganda −2.0). Hover the trace to inspect any sentence.</p>

  <div class="pg-inspector" data-component="panel" data-name="sentence-inspector">
    <h3>Sentence inspector — hover the trace</h3>
    <div class="pg-insp-text" id="hb-text">Hover over the chart to inspect a sentence…</div>
    <div class="pg-insp-meta">
      <div>idx <span id="hb-idx">—</span></div>
      <div>total <span id="hb-total">—</span></div>
      <div style="color:var(--green)">slots <span id="hb-slots">—</span></div>
      <div style="color:var(--gold)">product <span id="hb-pt">—</span></div>
      <div style="color:var(--blue)">ground <span id="hb-ground">—</span></div>
      <div style="color:var(--amber)">contra <span id="hb-contra">—</span></div>
      <div>drift <span id="hb-drift">—</span></div>
      <div style="color:var(--red)">prop <span id="hb-prop">—</span></div>
    </div>
  </div>

  <div class="pg-toggle-row" data-component="controls" data-name="heartbeat-toggles">
    <button class="pg-toggle active" onclick="hbToggle('hb-raw', this)">raw</button>
    <button class="pg-toggle active" onclick="hbToggle('hb-smooth', this)">smoothed (SMA-9)</button>
  </div>

  <div class="pg-panel" data-component="panel" data-name="heartbeat-chart">{heartbeat}</div>

  <div class="pg-ekg-tables">
    <div class="pg-panel" data-component="panel" data-name="ekg-peaks">
      <h3 style="font-family:var(--mono);font-size:.6rem;letter-spacing:.12em;color:var(--green);text-transform:uppercase;margin-bottom:.5rem">Top 5 peaks</h3>
      <table class="pg-table" style="min-width:0"><thead><tr><th>#</th><th>score</th><th>dominant</th><th>excerpt</th></tr></thead>
      <tbody>{ekg_rows(peaks, "high")}</tbody></table>
    </div>
    <div class="pg-panel" data-component="panel" data-name="ekg-valleys">
      <h3 style="font-family:var(--mono);font-size:.6rem;letter-spacing:.12em;color:var(--red);text-transform:uppercase;margin-bottom:.5rem">Top 5 valleys</h3>
      <table class="pg-table" style="min-width:0"><thead><tr><th>#</th><th>score</th><th>dominant</th><th>excerpt</th></tr></thead>
      <tbody>{ekg_rows(valleys, "low")}</tbody></table>
    </div>
  </div>
</section>
<!-- END:COMPONENT:section:heartbeat -->

<!-- BEGIN:COMPONENT:section:slot-coverage -->
<section class="pg-sec" id="slots" data-component="section" data-name="slot-coverage">
  <div class="pg-sec-head"><span class="pg-sec-dot"></span><span class="pg-sec-kicker">Slot Coverage</span></div>
  <h2>Ten Slots — {esc(coverage)} covered</h2>
  <p class="pg-sec-desc">Lexicon hits (Stage 1) vs. span-judged fill signals (Stage 3: + filled, − failed).
  An <b style="color:var(--red)">ABSENT</b> slot is a finding, not a rendering gap: the paper never engages
  that factor. Absent here: {esc(", ".join(f"{a} ({slot_names[a]})" for a in absent_slots) or "none")}.</p>
  <div class="pg-panel">{slot_svg}</div>
</section>
<!-- END:COMPONENT:section:slot-coverage -->

<!-- BEGIN:COMPONENT:section:product-test -->
<section class="pg-sec" id="product-test" data-component="section" data-name="product-test">
  <div class="pg-sec-head"><span class="pg-sec-dot"></span><span class="pg-sec-kicker">Product Test</span></div>
  <h2>Product-Test Passages</h2>
  <p class="pg-sec-desc">Spans judged PRODUCT_TEST: where the paper engages the multiplicative question —
  does one zero collapse the whole? Answer language is the Stage 1 product_test lexicon terms matched in
  those sentences.</p>
  {pt_html}
</section>
<!-- END:COMPONENT:section:product-test -->

<!-- BEGIN:COMPONENT:section:ledger -->
<section class="pg-sec" id="ledger" data-component="section" data-name="ledger">
  <div class="pg-sec-head"><span class="pg-sec-dot"></span><span class="pg-sec-kicker">Ledger</span></div>
  <h2>Span Ledger</h2>
  <p class="pg-sec-desc">Every judged span in document order: role, slot signals (slot polarity/fit/quote-status),
  canon-condition flags, kill condition, confidence. Click a row for the full span text, its Stage 1 lexicon
  evidence, and the raw judgment JSON.</p>
  <div class="pg-table-wrap">
  <table class="pg-table" id="pg-ledger" data-component="table" data-name="span-ledger">
    <thead><tr><th>span</th><th>sents</th><th>role</th><th>slot signals</th>
    <th>canon flags</th><th>kill condition</th><th>conf</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
  </div>
  {dropped_html}
  <div class="pg-detail pg-panel" id="pg-detail" data-component="panel" data-name="span-detail">
    <h3 id="d-title" style="color:var(--gold);margin-top:0"></h3>
    <h3>Span text</h3><pre id="d-text"></pre>
    <h3>Lexicon evidence (Stage 1)</h3><pre id="d-lex"></pre>
    <h3>Judgment JSON</h3><pre id="d-json"></pre>
  </div>
</section>
<!-- END:COMPONENT:section:ledger -->

<!-- BEGIN:COMPONENT:section:canon-docket -->
<section class="pg-sec" id="canon" data-component="section" data-name="canon-docket">
  <div class="pg-sec-head"><span class="pg-sec-dot"></span><span class="pg-sec-kicker">Canon Docket</span></div>
  <h2>The Canon Ledger</h2>
  <p class="pg-sec-desc">Every claim the paper carries, normalized to an atom and checked IN CODE against
  the five canon conditions — address (M### assigned), grade (ruled vocabulary only), receipt (recorded
  Lean receipts only), authority (ruling citation), no-conflict (slot polarity and protected markers).
  Hover a checkmark for the condition's detail. CANON-READY needs all five; HOLD waits on a receipt or a
  grade; NEEDS-RULING waits on David.</p>
  <div class="pg-toggle-row" data-component="controls" data-name="canon-filter">{filter_buttons}</div>
  <div class="pg-table-wrap">
  <table class="pg-table" id="pg-canon" data-component="table" data-name="canon-docket">
    <thead><tr><th>id</th><th>statement</th><th>type</th><th>slots</th><th>grade</th>
    <th>address · grade · receipt · authority · no-conflict</th><th>verdict</th></tr></thead>
    <tbody>{canon_rows}</tbody>
  </table>
  </div>
  <p class="pg-canon-note">Receipt matching: {esc(cm["receipt_matching"])}<br/>
  Full review docket: <a href="./{esc(canon_md_name)}">{esc(canon_md_name)}</a> ·
  canon.json stage {esc(canon_doc["stage"])} · normalization {esc(cm["normalization"])} ·
  {cm["api_calls"]} normalization API call(s).</p>
  {retirement_html}
</section>
<!-- END:COMPONENT:section:canon-docket -->

<!-- BEGIN:COMPONENT:section:report -->
<section class="pg-sec" id="report" data-component="section" data-name="report">
  <div class="pg-sec-head"><span class="pg-sec-dot"></span><span class="pg-sec-kicker">Reading</span></div>
  <h2>The Reading</h2>
  <p class="pg-sec-desc">What this paper is like inside the Master Equation frame — and what it costs you
  to read it. A profile generated from the measured stats above; every characteristic cites the number,
  claim id, or sentence it stands on.</p>
  <div class="pg-panel pg-reading">{reading_html}
    <div class="pg-read-meta">{esc(reading_meta)}</div>
  </div>
</section>
<!-- END:COMPONENT:section:report -->

<!-- BEGIN:COMPONENT:footer:footer-paper-grade -->
<footer class="pg-footer" data-component="footer" data-name="footer-paper-grade">
  <div class="feq">χ = CW[ G · M · E · S_eff · T · K · R · Q · F · C ]</div>
  <p>Master Equation Grading Station · Paper Grade Dashboard</p>
  <p data-component="note" data-name="generation-stamp" style="margin-top:.35rem;font-size:.65rem">
    Generated {esc(gen_ts)} · sources: {esc(stem)}.lexicon.json / .stats.json / .spans.json / .canon.json<br/>
    weights sha {esc(weights_sha[:12])} · rubric sha {esc(m["rubric_sha256"][:12])} · prompt sha {esc(m["prompt_sha256"][:12])} ·
    narrative prompt {esc(NARRATIVE_PROMPT_VERSION)} sha {esc(narrative_prompt_sha[:12])} · stage {STAGE}
  </p>
</footer>
<!-- END:COMPONENT:footer:footer-paper-grade -->

<!-- BEGIN:COMPONENT:script:script-paper-grade -->
<script>{JS.replace("%HB_DATA%", js_data(hb_data)).replace("%HB_META%", js_data(hb_meta)).replace("%DETAIL%", js_data(detail_js))}</script>
<!-- END:COMPONENT:script:script-paper-grade -->
</body>
</html>"""

    out_path = OUT_DIR / f"{stem}.report.html"
    out_path.write_text(html_doc, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    print(f"[report] wrote {out_path} ({size_kb:.0f} KB)")
    print(f"[report] the-reading: {reading_meta}")


if __name__ == "__main__":
    main()
