#!/usr/bin/env python3
"""Inject a repeatable Fruits dashboard into an article HTML copy.

The source article is never modified. Existing generated blocks are replaced
between stable markers so the operation is safe to repeat.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from collections import Counter
from pathlib import Path


START = "<!-- FRUITS-DASHBOARD:START -->"
END = "<!-- FRUITS-DASHBOARD:END -->"
STYLE_START = "/* FRUITS-DASHBOARD:STYLE-START */"
STYLE_END = "/* FRUITS-DASHBOARD:STYLE-END */"
FRUITS = ["love", "joy", "peace", "patience", "kindness", "goodness", "faithfulness", "gentleness", "self-control"]


CSS = r"""
/* FRUITS-DASHBOARD:STYLE-START */
.ftp-fruits{margin:0 0 4rem;padding:1.15rem;border:1px solid var(--gold-border2);background:linear-gradient(145deg,rgba(212,175,55,.08),rgba(255,255,255,.015) 45%,rgba(80,200,120,.035));font-family:var(--sans);position:relative;overflow:hidden}
.ftp-fruits:before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:linear-gradient(var(--gold-bright),#70bc8b,var(--red-soft))}
.ftp-fruits *{box-sizing:border-box}.ftp-fruits__eyebrow{font:600 .68rem/1.3 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-bright)}
.ftp-fruits h2{margin:.4rem 0 .3rem;font:600 clamp(1.8rem,4vw,3.2rem)/1.03 var(--display);letter-spacing:.015em;text-transform:uppercase;color:var(--text)}
.ftp-fruits__dek{max-width:780px;color:var(--text-dim);font:400 1rem/1.55 var(--sans)}
.ftp-fruits__stamp{display:inline-flex;gap:.55rem;flex-wrap:wrap;margin-top:.85rem;font:.65rem/1.4 var(--mono);color:var(--text-muted)}
.ftp-fruits__stamp span{border:1px solid var(--border);padding:.22rem .48rem;background:rgba(0,0,0,.22)}
.ftp-fruits__grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(260px,.8fr);gap:1rem;margin-top:1.15rem}
.ftp-fruits__panel{background:rgba(5,5,5,.42);border:1px solid var(--border);padding:1rem}.ftp-fruits__panel h3{margin:0 0 .7rem;font:600 .74rem/1.2 var(--mono);letter-spacing:.11em;text-transform:uppercase;color:var(--gold)}
.ftp-fruits__finding{font:400 1.06rem/1.55 var(--serif);color:var(--text)}
.ftp-fruits__bars{display:grid;gap:.48rem}.ftp-fruits__bar{display:grid;grid-template-columns:92px 1fr 42px;gap:.55rem;align-items:center;font:.68rem/1.2 var(--mono);text-transform:uppercase;color:var(--text-dim)}
.ftp-fruits__track{height:9px;background:#222;position:relative;overflow:hidden}.ftp-fruits__pos,.ftp-fruits__neg{position:absolute;top:0;height:100%}.ftp-fruits__pos{left:50%;background:#70bc8b}.ftp-fruits__neg{right:50%;background:#bd6060}.ftp-fruits__axis{position:absolute;left:50%;top:-2px;bottom:-2px;width:1px;background:#777;z-index:2}.ftp-fruits__score{text-align:right;color:var(--text)}
.ftp-fruits__legend{display:flex;justify-content:space-between;margin-top:.6rem;font:.61rem/1.2 var(--mono);color:var(--text-muted)}
.ftp-fruits__cards{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin-top:.8rem}.ftp-fruits__card{border-top:2px solid var(--gold-border2);background:rgba(255,255,255,.025);padding:.8rem}.ftp-fruits__card strong{display:block;margin-bottom:.35rem;font:600 .7rem/1.3 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--gold)}.ftp-fruits__card p{margin:0;font:400 .86rem/1.48 var(--sans);color:var(--text-dim)}
.ftp-fruits__mirror{margin-top:.9rem;padding:1rem;border-left:3px solid #bd6060;background:rgba(189,96,96,.06)}.ftp-fruits__mirror strong{color:#e49a9a;font:600 .72rem/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase}.ftp-fruits__mirror p{margin:.35rem 0 0;font:400 .95rem/1.55 var(--sans);color:var(--text)}
.ftp-fruits details{margin-top:.85rem;border-top:1px solid var(--border);padding-top:.8rem}.ftp-fruits summary{cursor:pointer;font:600 .72rem/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-bright)}
.ftp-fruits__evidence{display:grid;gap:.65rem;margin-top:.8rem}.ftp-fruits__quote{padding:.7rem;border:1px solid var(--border);background:rgba(0,0,0,.2)}.ftp-fruits__quote b{font:600 .64rem/1.3 var(--mono);color:var(--gold);text-transform:uppercase}.ftp-fruits__quote p{margin:.28rem 0 0;font:italic .88rem/1.5 var(--serif);color:var(--text-dim)}
.ftp-fruits__caution{margin-top:.9rem;font:.64rem/1.5 var(--mono);color:var(--text-muted)}
@media(max-width:760px){.ftp-fruits{margin-left:-.5rem;margin-right:-.5rem;padding:1rem}.ftp-fruits__grid,.ftp-fruits__cards{grid-template-columns:1fr}.ftp-fruits__bar{grid-template-columns:82px 1fr 36px}}
/* FRUITS-DASHBOARD:STYLE-END */
"""


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render(data: dict, run: dict) -> str:
    assessments = data.get("sentence_assessments", [])
    passages = data.get("passages", [])
    summary = data.get("summary", {})
    counts = Counter((x.get("fruit", "").lower(), x.get("result", "")) for x in assessments)
    maximum = max([abs(counts[(f, "FRUIT")] - counts[(f, "ANTI_FRUIT")]) for f in FRUITS] + [1])

    bars = []
    for fruit in FRUITS:
        pos, neg = counts[(fruit, "FRUIT")], counts[(fruit, "ANTI_FRUIT")]
        score = pos - neg
        pw, nw = (pos / maximum) * 48, (neg / maximum) * 48
        bars.append(
            f'<div class="ftp-fruits__bar"><span>{esc(fruit)}</span><div class="ftp-fruits__track">'
            f'<i class="ftp-fruits__axis"></i><i class="ftp-fruits__pos" style="width:{pw:.1f}%"></i>'
            f'<i class="ftp-fruits__neg" style="width:{nw:.1f}%"></i></div><span class="ftp-fruits__score">{score:+d}</span></div>'
        )

    evidence = sorted(passages, key=lambda x: (x.get("importance", 0), x.get("confidence", 0)), reverse=True)[:6]
    quotes = "".join(
        f'<div class="ftp-fruits__quote"><b>{esc(x.get("actor"))} → {esc(x.get("target"))} · {esc(x.get("fruit"))} · {esc(x.get("result"))}</b>'
        f'<p>“{esc(x.get("exact_quotation"))}”</p></div>' for x in evidence
    )
    counterfeits = data.get("counterfeits", [])
    counterfeit_text = "; ".join(
        f'{x.get("claimed_fruit", "fruit")} without {x.get("missing_companion", "its companion")}' for x in counterfeits
    ) or "No counterfeit pattern was flagged."
    revision = summary.get("recommended_revision", "No revision supplied.")

    return f"""{START}
<section class="ftp-fruits" id="fruits-of-the-spirit" aria-labelledby="fruits-title">
  <div class="ftp-fruits__eyebrow">Fruits of the Spirit · relational audit · pilot</div>
  <h2 id="fruits-title">What This Paper Produces Between People</h2>
  <p class="ftp-fruits__dek">This reading asks who acts, who receives the action, which fruit appears or fails, and whether the paper keeps the same moral standard it teaches.</p>
  <div class="ftp-fruits__stamp"><span>DeepSeek: {esc(run.get('evaluation', {}).get('model'))}</span><span>{len(assessments)} classified sentences</span><span>{len(passages)} evidence passages</span><span>run {esc(str(run.get('run_id', ''))[:8])}</span></div>
  <div class="ftp-fruits__grid">
    <div class="ftp-fruits__panel"><h3>Main finding</h3><p class="ftp-fruits__finding">{esc(summary.get('relational_fruit_thesis'))}</p></div>
    <div class="ftp-fruits__panel"><h3>Sentence evidence balance</h3><div class="ftp-fruits__bars">{''.join(bars)}</div><div class="ftp-fruits__legend"><span>← anti-fruit</span><span>fruit →</span></div></div>
  </div>
  <div class="ftp-fruits__cards">
    <div class="ftp-fruits__card"><strong>Greatest strength</strong><p>{esc(summary.get('greatest_strength'))}</p></div>
    <div class="ftp-fruits__card"><strong>Greatest danger</strong><p>{esc(summary.get('greatest_danger'))}</p></div>
    <div class="ftp-fruits__card"><strong>Counterfeit pattern</strong><p>{esc(counterfeit_text)}</p></div>
  </div>
  <div class="ftp-fruits__mirror"><strong>The paper turned back on itself</strong><p>{esc(summary.get('most_important_asymmetry'))}</p></div>
  <div class="ftp-fruits__cards">
    <div class="ftp-fruits__card"><strong>Recommended repair</strong><p>{esc(revision)}</p></div>
    <div class="ftp-fruits__card"><strong>What the score means</strong><p>Counts show classified relational evidence in this text. They are not a verdict on a person's salvation, character, or spiritual worth.</p></div>
    <div class="ftp-fruits__card"><strong>Human review</strong><p>Pilot output. Every label remains reviewable against its quoted sentence, especially suffering that could be mistaken for misconduct.</p></div>
  </div>
  <details><summary>Open the strongest evidence passages</summary><div class="ftp-fruits__evidence">{quotes}</div></details>
  <p class="ftp-fruits__caution">Source SHA-256: {esc(run.get('source_sha256'))} · Generated {esc(run.get('completed_at'))} · Machine-assisted interpretation; quoted evidence remains the audit trail.</p>
</section>
{END}"""


def replace_or_insert(text: str, start: str, end: str, replacement: str, anchor: str, after: bool) -> str:
    if start in text and end in text:
        left, rest = text.split(start, 1)
        _, right = rest.split(end, 1)
        return left + replacement + right
    if anchor not in text:
        raise ValueError(f"Required HTML anchor not found: {anchor}")
    return text.replace(anchor, anchor + "\n" + replacement if after else replacement + "\n" + anchor, 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_html", type=Path)
    parser.add_argument("fruits_json", type=Path)
    parser.add_argument("run_json", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()

    source_bytes = args.source_html.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    text = source_bytes.decode("utf-8")
    run = load(args.run_json)
    if run.get("source_sha256") and run["source_sha256"] != source_hash:
        raise SystemExit("Refusing injection: source HTML hash does not match the analyzed source.")

    text = replace_or_insert(text, STYLE_START, STYLE_END, CSS.strip(), "</head>", False)
    text = replace_or_insert(text, START, END, render(load(args.fruits_json), run), "<main>", True)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(text, encoding="utf-8", newline="\n")
    print(f"Created: {args.output_html}")
    print(f"Preserved source: {args.source_html}")
    print(f"Source SHA-256: {source_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
