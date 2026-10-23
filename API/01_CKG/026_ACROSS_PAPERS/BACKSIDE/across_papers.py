r"""ACROSS PAPERS: many CKG V4 reviews of one argument -> one claim ledger + one synthesis.

    python across_papers.py <reviews_folder> <out_folder> --topic "Math Is Moral" [--workers 6] [--redo]

Step 1 (one call per review): code cuts each review to the parts a ruling needs (finding, legs,
        what is new, claim discipline, audit, build next; the pasted original is dropped), then the
        model turns that into a compact JSON record. Saved in <out>/_condensed/, reused on reruns.
Step 2:  LEDGER    built in CODE from the reviews' own groupings (strongest / must defend / probably
                  wrong), every claim kept, flagged-first, with an empty Ruling column
                                                       -> <TOPIC>_CLAIM_LEDGER.md / .json
        SYNTHESIS every leg across the corpus, contradictions between papers, the spine of the
                  final paper, what is missing          -> <TOPIC>_SYNTHESIS.md
Nothing here rules on anything; it proposes. The ruling column is David's.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
KEEP = ["what this paper is", "every leg", "the argument", "claim discipline", "audit", "build next"]


def call(prompt: str, max_tokens: int = 8000, temperature: float = 0.2) -> dict:
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "response_format": {"type": "json_object"},
                       "max_tokens": max_tokens, "temperature": temperature}).encode()
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL, body, {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read())
            ch = data["choices"][0]
            if ch.get("finish_reason") == "length":
                raise RuntimeError("reply hit the token limit")
            return json.loads(ch["message"]["content"])
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"call failed after 4 tries: {last}")


def cut(review: str) -> str:
    """Keep only the sections a ruling needs; drop the pasted original and trim the synopsis."""
    review = review.split("\n# ORIGINAL ARTICLE")[0]
    head = review.split("\n## ")[0]
    parts = [head.strip()[:1500]]
    for block in review.split("\n## ")[1:]:
        name = block.split("\n", 1)[0].strip().lower()
        if any(name.startswith(k) for k in KEEP):
            text = block if not name.startswith("what this paper is") else block[:2500]
            parts.append("## " + text.strip())
    return "\n\n".join(parts)


def condense(review_path: Path, out_dir: Path, redo: bool) -> tuple[str, bool, str]:
    paper = review_path.stem.replace(" · CKG", "")
    dest = out_dir / (paper + ".json")
    if dest.exists() and not redo:
        return review_path.name, True, "cached"
    prompt = (HERE / "condense_prompt.md").read_text(encoding="utf-8").replace(
        "{{paper}}", paper).replace("{{review}}", cut(review_path.read_text(encoding="utf-8")))
    try:
        rec = call(prompt, max_tokens=6000, temperature=0.0)
        rec["paper"] = paper
        dest.write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding="utf-8")
        return review_path.name, True, f"{len(rec.get('claims', []))} claims, {len(rec.get('legs', []))} legs"
    except Exception as e:  # noqa: BLE001
        return review_path.name, False, str(e)[:160]


def cell(v) -> str:
    return str(v or "").replace("|", "/").replace("\n", " ")


def main() -> int:
    ap = argparse.ArgumentParser(prog="across_papers")
    ap.add_argument("reviews")
    ap.add_argument("out")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("DEEPSEEK_API_KEY is not set")
        return 2
    rev, out = Path(a.reviews), Path(a.out)
    cdir = out / "_condensed"
    cdir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in rev.glob("* · CKG.md") if "DRY_RUN" not in p.name)
    print(f"[{datetime.now():%H:%M:%S}] step 1: condensing {len(files)} reviews, {a.workers} at once", flush=True)
    with ThreadPoolExecutor(a.workers) as ex:
        for name, ok, info in ex.map(lambda p: condense(p, cdir, a.redo), files):
            print(f"  {'ok  ' if ok else 'FAIL'} {name[:70]}  ({info})", flush=True)
    recs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(cdir.glob("*.json"))]
    if len(recs) < len(files):
        print(f"  ! only {len(recs)} of {len(files)} condensed; merging what exists")
    legend = {}                                            # short paper codes keep the merge replies small
    for i, r in enumerate(recs, 1):
        code = f"P{i:02d}"
        legend[code] = r.get("paper", "")
        r["paper"] = code
    blob = json.dumps(recs, ensure_ascii=False)
    print(f"[{datetime.now():%H:%M:%S}] step 2: merging {len(recs)} records (~{len(blob)//4:,} tokens)", flush=True)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", a.topic).strip("_").upper()

    # The ledger is built in code from the reviews' own groupings: nothing dropped, nothing re-weighted.
    groups = [("PROBABLY_WRONG", "Probably wrong or overstated", "Defensible version"),
              ("MUST_DEFEND", "Must defend", "Attack / best answer"),
              ("STRONGEST", "Strongest (what held)", "Why it holds")]
    order = {"STRUCTURAL": 0, "LOCAL": 1, "INERT": 2}
    ledger, md = [], [f"# {a.topic}: claim ledger", "",
                      f"*Every claim the {len(recs)} CKG V4 reviews singled out, in the reviews' own groups, with their reasons. "
                      f"Built by code from the review records ({datetime.now():%Y-%m-%d}): nothing dropped or re-weighted. "
                      "The Ruling column is David's.*", ""]
    for key, title, third in groups:
        rows = [(r["paper"], c) for r in recs for c in r.get("claims", []) if c.get("group") == key]
        rows.sort(key=lambda x: (order.get(x[1].get("blast_radius"), 3), x[0]))
        md += [f"## {title} ({len(rows)})", "", f"| # | Paper | Claim | {third} | Blast | Ruling |", "|---|---|---|---|---|---|"]
        for i, (code, c) in enumerate(rows, 1):
            if key == "PROBABLY_WRONG":
                extra = c.get("defensible_version") or c.get("why")
            elif key == "MUST_DEFEND":
                extra = f"{c.get('attack', '')} / {c.get('answer', '')}".strip(" /")
            else:
                extra = c.get("why")
            md.append(f"| {i} | {code} | {cell(c.get('claim'))} | {cell(extra)} | {cell(c.get('blast_radius'))} |  |")
            ledger.append({**c, "paper": code, "paper_name": legend.get(code)})
        md.append("")
    md += ["## Paper codes", ""] + [f"- **{k}** {v}" for k, v in legend.items()]
    (out / f"{slug}_CLAIM_LEDGER.json").write_text(json.dumps({"claims": ledger, "papers": legend}, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / f"{slug}_CLAIM_LEDGER.md").write_text("\n".join(md), encoding="utf-8")
    print(f"  ledger: {len(ledger)} claims, " + ", ".join(f"{k}={sum(c.get('group') == k for c in ledger)}" for k, _, _ in groups), flush=True)

    syn = call((HERE / "synthesis_prompt.md").read_text(encoding="utf-8").replace("{{topic}}", a.topic)
               .replace("{{records}}", blob), max_tokens=8000, temperature=0.3)
    (out / f"{slug}_SYNTHESIS.md").write_text(syn.get("markdown", "") + "\n\n## Paper codes\n\n"
                                              + "\n".join(f"- **{k}** {v}" for k, v in legend.items()) + "\n", encoding="utf-8")
    print(f"[{datetime.now():%H:%M:%S}] done -> {out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
