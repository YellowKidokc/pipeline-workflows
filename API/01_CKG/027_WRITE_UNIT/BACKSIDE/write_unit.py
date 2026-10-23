r"""WRITE UNIT: closed-argument materials -> one thesis unit in David's Lowe FACTS format.

    python write_unit.py <claims_folder> <out_folder> --topic "Math Is Moral" --slug MIM

Reads from <claims_folder>: <SLUG-ish>_SYNTHESIS.md and *_CLAIM_LEDGER.json (from across_papers.py).
Writes four pieces, in order, each its own call that sees the pieces before it:
    00_PAGE_ZERO_BIAXIOSUM.md  01_PAPER_I_FOUNDATIONAL.md  02_PAPER_II_ADVERSARIAL.md  03_PAPER_III_APPLICATION.md
Templates are David's own (FORMAL_PAPERS\0*_TEMPLATE.md); voice and rules live in unit_rules.md.
Only claims the reviews held, must-defend claims with their answers, and the defensible versions of
overstated claims are given to the writer. Nothing the reviews marked wrong is offered as true.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = Path(r"C:\Users\David\Documents\faiththruphysics.com\10_VAULTS\_Theophysics_v5\04_THEOPYHISCS\FORMAL_PAPERS")
PIECES = [
    ("00_PAGE_ZERO_BIAXIOSUM", "00_BIAXIOSUM_TEMPLATE.md", "Page Zero: the Biaxiosum"),
    ("01_PAPER_I_FOUNDATIONAL", "01_PAPER_I_FOUNDATIONAL_TEMPLATE.md", "Paper I: the Foundational Claim"),
    ("02_PAPER_II_ADVERSARIAL", "02_PAPER_II_ADVERSARIAL_TEMPLATE.md", "Paper II: the Adversarial Response"),
    ("03_PAPER_III_APPLICATION", "03_PAPER_III_APPLICATION_TEMPLATE.md", "Paper III: the Application"),
]


def call(prompt: str) -> str:
    body = json.dumps({"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
                       "response_format": {"type": "json_object"}, "max_tokens": 8000, "temperature": 0.5}).encode()
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.deepseek.com/chat/completions", body,
                                         {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
                                          "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as r:
                d = json.loads(r.read())
            ch = d["choices"][0]
            if ch.get("finish_reason") == "length":
                raise RuntimeError("reply hit the token limit")
            return json.loads(ch["message"]["content"])["markdown"]
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(4 * (attempt + 1))
    raise RuntimeError(f"failed after 4 tries: {last}")


def material(cdir: Path) -> tuple[str, str]:
    syn = next(cdir.glob("*_SYNTHESIS.md")).read_text(encoding="utf-8")
    led = json.loads(next(cdir.glob("*_CLAIM_LEDGER.json")).read_text(encoding="utf-8"))
    papers = led.get("papers", {})
    lines = {"HELD": [], "MUST DEFEND": [], "OVERSTATED -> USE ONLY THE DEFENSIBLE VERSION": []}
    for c in led["claims"]:
        g, src = c.get("group"), c.get("paper", "")
        if g == "STRONGEST":
            lines["HELD"].append(f"- {c.get('claim')}  [{src}]  (why: {c.get('why', '')})")
        elif g == "MUST_DEFEND":
            lines["MUST DEFEND"].append(f"- {c.get('claim')}  [{src}]  attack: {c.get('attack', '')}  best answer: {c.get('answer', '')}")
        elif g == "PROBABLY_WRONG" and c.get("defensible_version"):
            lines["OVERSTATED -> USE ONLY THE DEFENSIBLE VERSION"].append(f"- {c.get('defensible_version')}  [{src}]")
    claims = "\n\n".join(f"### {k}\n" + "\n".join(v) for k, v in lines.items())
    claims += "\n\n### Paper codes\n" + "\n".join(f"- {k}: {v}" for k, v in papers.items())
    return syn, claims


def main() -> int:
    ap = argparse.ArgumentParser(prog="write_unit")
    ap.add_argument("claims")
    ap.add_argument("out")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("DEEPSEEK_API_KEY is not set"); return 2
    syn, claims = material(Path(a.claims))
    rules = (HERE / "unit_rules.md").read_text(encoding="utf-8")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    done: list[tuple[str, str]] = []
    for stem, tpl, title in PIECES:
        template = (TPL / tpl).read_text(encoding="utf-8")
        before = "\n\n".join(f"===== {t} (already written) =====\n{txt}" for t, txt in done) or "(this is the first piece)"
        prompt = (f"You are writing **{title}** of David Lowe's thesis unit on \"{a.topic}\" (unit {a.slug}).\n\n"
                  f"{rules}\n\n===== HIS TEMPLATE FOR THIS PIECE (follow its section order) =====\n{template}\n\n"
                  f"===== THE SYNTHESIS OF EVERY PAPER ON THIS TOPIC =====\n{syn}\n\n"
                  f"===== THE CLAIMS YOU MAY USE =====\n{claims}\n\n"
                  f"===== PIECES ALREADY WRITTEN =====\n{before}\n\n"
                  "Return ONLY a JSON object: {\"markdown\": \"the complete piece\"}")
        t0 = time.time()
        md = call(prompt)
        (out / f"{a.slug}_{stem}.md").write_text(md, encoding="utf-8")
        done.append((title, md))
        print(f"[{datetime.now():%H:%M:%S}] {title}: {len(md.split()):,} words ({time.time() - t0:.0f}s)", flush=True)
    print(f"done -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
