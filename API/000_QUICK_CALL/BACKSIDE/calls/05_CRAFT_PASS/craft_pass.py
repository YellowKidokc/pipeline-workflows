r"""CRAFT PASS: one paper -> per-section craft options (the loop) -> DeepSeek's best full version.

    python craft_pass.py "path\to\paper.md"            run it
    python craft_pass.py "path\to\paper.md" --dry-run  build the prompts, send nothing

How it works:
  1. The paper is split into sections (each ## heading starts one; the title and opening are S00).
     Each section is split into units (a line or paragraph), IDs like S03.U02.
     Callout blocks (lines starting with >) and any "has and has not done" section are PROTECTED:
     copied exactly, never given options. That keeps the claim boxes and boundary sections intact.
  2. One call per section, in order. Each call gets the menu (David's cards first, then the craft
     library) plus whatever earlier sections left unused. It picks 2 fundamentals + up to 3 extras.
     Unused cards carry forward. The counts are kept here in code, not trusted to the model.
  3. One final call writes the best full version, every unit tagged with the source unit IDs it
     came from, so the writer can line it up against the original.

Output in OUTBOX\05_CRAFT_PASS\<paper>\ :
  <paper>.craftpass.json     every section's options, memorable line, analogy, loop ledger
  <paper>.craftpass.md       the same, readable
  <paper>.bestversion.json   the full rewrite, unit by unit, with source IDs and techniques
  <paper>.bestversion.md     the full rewrite as a plain page
  <paper>.receipt.json       hashes, model, tokens, per-call time
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUICK = HERE.parents[2]                                  # ...\000_QUICK_CALL
OUT_ROOT = QUICK / "OUTBOX" / "05_CRAFT_PASS"
LIBRARY = QUICK / "OUTBOX" / "04_CRAFT_EXTRACT" / "craft_library.json"
URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
PROTECTED_SECTION = re.compile(r"has and has not done", re.I)


def parse(text: str) -> tuple[str, list[dict]]:
    """Paper -> title + sections of units. Front matter is dropped (it is metadata, not prose)."""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    title, sections, cur = "", [], {"heading": None, "lines": []}
    for line in text.split("\n"):
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            sections.append(cur)
            cur = {"heading": line[3:].strip(), "lines": []}
        else:
            cur["lines"].append(line)
    sections.append(cur)
    out = []
    for s in sections:
        blocks, buf = [], []
        for line in s["lines"] + [""]:
            if line.strip():
                buf.append(line)
            elif buf:
                blocks.append("\n".join(buf))
                buf = []
        if not blocks and s["heading"] is None:
            continue
        sid = f"S{len(out):02d}"
        prot_sec = bool(s["heading"] and PROTECTED_SECTION.search(s["heading"]))
        units = [{"id": f"{sid}.U{i:02d}", "text": b,
                  "protected": prot_sec or b.lstrip().startswith(">")} for i, b in enumerate(blocks, 1)]
        out.append({"id": sid, "heading": s["heading"], "units": units, "protected": prot_sec})
    return title, out


def show_section(s: dict) -> str:
    head = f"## {s['heading']}\n" if s["heading"] else "(opening section, before the first heading)\n"
    return head + "\n".join(f"[{u['id']}]{' PROTECTED' if u['protected'] else ''} {u['text']}" for u in s["units"])


def menu() -> tuple[list[dict], list[dict]]:
    david = json.loads((HERE / "david_cards.json").read_text(encoding="utf-8"))
    lib = json.loads(LIBRARY.read_text(encoding="utf-8")) if LIBRARY.exists() else []
    lib = [c for c in lib if not str(c.get("for_written_prose", "")).lower().startswith("no")]
    return david, lib


def card_lines(cards: list[dict]) -> str:
    return "\n".join(f"- {c['card_id']} [{c.get('serves')}] {c.get('name')}: {c.get('what_it_does')}" for c in cards)


def api_key() -> str:
    return (os.environ.get("DEEPSEEK_API_KEY") or "").strip()


def call(prompt: str, max_tokens: int = 8000) -> tuple[dict, int]:
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "response_format": {"type": "json_object"},
                       "max_tokens": max_tokens, "temperature": 0.7}).encode()
    last = None
    for attempt in range(4):
        req = urllib.request.Request(URL, body, {"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            ch = data["choices"][0]
            if ch.get("finish_reason") == "length":
                raise RuntimeError("reply hit the token limit; nothing saved for this call")
            return json.loads(ch["message"]["content"]), int(data.get("usage", {}).get("total_tokens", 0))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"call failed after 4 tries: {last!r}")


def ids_in(xs) -> list[str]:
    """Pull card IDs out of whatever the model returned ('CRAFT-058 power word' -> 'CRAFT-058')."""
    out = []
    for x in xs or []:
        m = re.match(r"\s*((?:CRAFT|DAVID)-\d{3})", str(x))
        if m:
            out.append(m.group(1))
    return out


def run(paper: Path, dry: bool) -> int:
    src = paper.read_text(encoding="utf-8")
    title, sections = parse(src)
    david, lib = menu()
    names = {c["card_id"]: c.get("name") for c in david + lib}
    sec_tmpl = (HERE / "section_prompt.txt").read_text(encoding="utf-8")
    best_tmpl = (HERE / "best_version_prompt.txt").read_text(encoding="utf-8")
    out = OUT_ROOT / paper.stem
    out.mkdir(parents=True, exist_ok=True)
    receipt = {"paper": str(paper), "source_sha256": hashlib.sha256(src.encode()).hexdigest(), "model": MODEL,
               "started": datetime.now().isoformat(timespec="seconds"), "library_cards": len(lib), "calls": []}
    print(f"[{datetime.now():%H:%M:%S}] {paper.name}: {len(sections)} sections, "
          f"{sum(len(s['units']) for s in sections)} units, menu {len(david)} DAVID + {len(lib)} library cards")
    if not dry and not api_key():
        print("  DEEPSEEK_API_KEY is not set")
        return 2

    passes, counts, carried, domains = [], Counter(), [], []
    live = [s for s in sections if not s["protected"]]
    for n, s in enumerate(live, 1):
        pos = "This is the OPENING: invite the reader in (DAVID-002)." if n == 1 else (
              "This is the CLOSING section: land it." if n == len(live) else "A middle section.")
        prompt = (sec_tmpl.replace("{{section}}", show_section(s)).replace("{{index}}", str(n))
                  .replace("{{total}}", str(len(live))).replace("{{position_note}}", pos)
                  .replace("{{david_cards}}", card_lines(david)).replace("{{library}}", card_lines(lib))
                  .replace("{{carried}}", "\n".join(f"- {c} {names.get(c, '')}" for c in carried) or "(none yet)")
                  .replace("{{analogy_domains}}", ", ".join(domains) or "(none yet)")
                  .replace("{{section_id}}", s["id"]))
        if dry:
            (out / f"_dry_{s['id']}.txt").write_text(prompt, encoding="utf-8")
            continue
        t = time.time()
        try:
            res, tok = call(prompt)
        except Exception as e:
            print(f"[{datetime.now():%H:%M:%S}] {s['id']} FAILED: {e}")
            receipt["calls"].append({"section": s["id"], "ok": False, "error": str(e)})
            continue
        used = ids_in(res.get("fundamentals")) + ids_in(res.get("extras"))
        counts.update(used)
        carried = [c for c in dict.fromkeys(carried + ids_in(res.get("candidates"))) if c not in used]
        res["loop"] = {"used_here": used, "carried_forward": carried, "running_counts": dict(counts)}
        dom = ((res.get("analogy") or {}).get("domain") or "").strip()
        if dom:
            domains.append(dom)
            res["loop"]["analogy_domains_so_far"] = list(domains)
        passes.append(res)
        receipt["calls"].append({"section": s["id"], "ok": True, "tokens": tok, "seconds": round(time.time() - t, 1)})
        print(f"[{datetime.now():%H:%M:%S}] {s['id']} {s['heading'] or '(opening)'}: used {', '.join(used)}  "
              f"| {len(carried)} carried | {tok:,} tokens")
    if dry:
        print(f"  dry run: prompts written to {out}")
        return 0

    original = "\n\n".join(show_section(s) for s in sections)
    prompt = best_tmpl.replace("{{original}}", original).replace("{{passes}}", json.dumps(passes, ensure_ascii=False))
    t = time.time()
    try:
        best, tok = call(prompt)
        receipt["calls"].append({"section": "BEST_VERSION", "ok": True, "tokens": tok, "seconds": round(time.time() - t, 1)})
        print(f"[{datetime.now():%H:%M:%S}] best version: {tok:,} tokens")
    except Exception as e:
        best = None
        receipt["calls"].append({"section": "BEST_VERSION", "ok": False, "error": str(e)})
        print(f"[{datetime.now():%H:%M:%S}] best version FAILED: {e}")

    write_outputs(out, paper.stem, title, sections, passes, best, counts, names)
    receipt["finished"] = datetime.now().isoformat(timespec="seconds")
    receipt["total_tokens"] = sum(c.get("tokens", 0) for c in receipt["calls"])
    (out / f"{paper.stem}.receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"[{datetime.now():%H:%M:%S}] done: {receipt['total_tokens']:,} tokens -> {out}")
    return 0 if all(c.get("ok") for c in receipt["calls"]) else 1


def write_outputs(out: Path, stem: str, title: str, sections: list, passes: list, best, counts: Counter, names: dict) -> None:
    all_units = {u["id"]: u for s in sections for u in s["units"]}
    doc = {"title": title, "sections": sections, "passes": passes,
           "card_counts": {k: {"name": names.get(k), "uses": v} for k, v in counts.most_common()}}
    (out / f"{stem}.craftpass.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")

    md = [f"# {title} · Craft Pass", "", f"*{datetime.now():%Y-%m-%d %H:%M} · {MODEL} · AI-proposed options; nothing replaced*", ""]
    md += ["## Techniques used across the piece", "", "| Card | Name | Uses |", "|---|---|---|"]
    md += [f"| {k} | {names.get(k, '')} | {v} |" for k, v in counts.most_common()] + [""]
    for p in passes:
        md += [f"## {p.get('section_id')} · {p.get('job', '')}", "",
               f"**Fundamentals:** {', '.join(p.get('fundamentals') or [])}  ·  **Extras:** {', '.join(p.get('extras') or []) or 'none'}",
               f"**Carried forward:** {', '.join(p['loop']['carried_forward']) or 'none'}", ""]
        ml = p.get("memorable_line") or {}
        if ml.get("text"):
            flag = "  ⚠ claims more than the original" if ml.get("claims_more_than_original") else ""
            md += [f"> **Memorable line:** {ml['text']}{flag}", ""]
        an = p.get("analogy")
        if an:
            md += [f"**Analogy ({an.get('pair')}):** {an.get('line')}  ", f"*Mapping:* {an.get('mapping')}  ", f"*Breaks at:* {an.get('breaks_at')}", ""]
        for o in p.get("options") or []:
            md += [f"**{o.get('unit_id')}** · original: {o.get('original')}"]
            for c in o.get("choices") or []:
                mark = "★ " if c.get("best") else "- "
                flag = " ⚠ claims more" if c.get("claims_more_than_original") else ""
                md += [f"  {mark}{c.get('text')}  _[{', '.join(c.get('techniques') or [])}]{flag}_"]
            md += [""]
    (out / f"{stem}.craftpass.md").write_text("\n".join(md), encoding="utf-8")

    if not best:
        return
    if best.get("title") != title:                      # the title is David's; the model never changes it
        best["title_proposed"] = best.get("title")
        best["title"] = title
    checks = {"protected_changed": [], "originals_not_used": []}
    used_src = set()
    for s in best.get("sections", []):
        for u in s.get("units", []):
            for sid in u.get("source_ids") or []:
                used_src.add(sid)
                orig = all_units.get(sid)
                if orig and orig["protected"] and u.get("text", "").strip() != orig["text"].strip():
                    checks["protected_changed"].append(sid)
    checks["originals_not_used"] = [k for k in all_units if k not in used_src]
    best["checks"] = checks
    (out / f"{stem}.bestversion.json").write_text(json.dumps(best, indent=1, ensure_ascii=False), encoding="utf-8")
    page = [f"# {best.get('title') or title}", ""]
    for s in best.get("sections", []):
        if s.get("heading"):
            page += [f"## {s['heading']}", ""]
        for u in s.get("units", []):
            page += [u.get("text", ""), ""]
    (out / f"{stem}.bestversion.md").write_text("\n".join(page), encoding="utf-8")
    if checks["protected_changed"]:
        print(f"  ! protected units changed by the model: {checks['protected_changed']}")
    if checks["originals_not_used"]:
        print(f"  note: {len(checks['originals_not_used'])} original unit(s) not carried into the best version")


def main() -> int:
    ap = argparse.ArgumentParser(prog="craft_pass")
    ap.add_argument("paper")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    p = Path(a.paper)
    if not p.is_file():
        print(f"not found: {p}")
        return 1
    return run(p, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
