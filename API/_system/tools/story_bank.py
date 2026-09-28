"""Story Bank: every retellable story, fact and rebuttal from every CKG, in one place to search. Local, no API.

The deep CKG writes a "## Story Bank" section (### SB<n> · <title> entries with Kind / Use it for / Where /
Retell it / Their words / Why it matters / Check first). This collects them from every "<note> · CKG.md" under MAIN
(and any extra folder given) into _data/STORY_BANK/:
  STORY_BANK.md     grouped by "Use it for" tag (intro-hook, heart-family, apologetics-rebuttal, ...)
  STORY_BANK.jsonl  one entry per line, for other tools

    python story_bank.py                       rebuild the bank
    python story_bank.py --find "family"       rebuild, then show entries matching every word
    python story_bank.py --tag intro-hook      rebuild, then show one tag
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

MAIN = Path(__file__).resolve().parents[2]
OUT = MAIN / "_data" / "STORY_BANK"
FIELDS = {"kind": "Kind", "use": "Use it for", "where": "Where", "retell": "Retell it", "words": "Their words",
          "why": "Why it matters", "check": "Check first"}


def ckg_files(roots: list[Path]) -> list[Path]:
    seen = {}
    for root in roots:
        for p in root.rglob("* · CKG.md"):
            if "_older" in p.parts:
                continue
            seen.setdefault(p.name, p)                      # the same note's CKG in two places counts once
    return sorted(seen.values(), key=lambda p: p.name.lower())


def entries(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^#{2,3} Story Bank\s*$(.*?)(?=^#{1,2} (?!#)|\Z)", text, flags=re.M | re.S)
    if not m:
        return []
    note = path.name[: -len(" · CKG.md")]
    out = []
    for block in re.split(r"^#{3,4} ", m.group(1), flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        title = re.sub(r"^SB\d+\s*·\s*", "", head).strip()
        if not title or "{{" in title:
            continue
        e = {"note": note, "file": str(path), "title": title}
        for key, label in FIELDS.items():
            f = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\s*-\s*\*\*|\Z)", body, flags=re.S)
            e[key] = " ".join(f.group(1).split()) if f else ""
        e["tags"] = [t.strip().lower() for t in re.split(r"[,/;]", e["use"]) if t.strip()]
        out.append(e)
    return out


def render(bank: list[dict], files: int) -> str:
    by_tag = defaultdict(list)
    for e in bank:
        for t in e["tags"] or ["untagged"]:
            by_tag[t].append(e)
    L = ["# Story Bank", "", f"{len(bank)} entries from {files} CKG file(s). Rebuilt by `_system/tools/story_bank.py`; "
         "search with `--find \"words\"` or `--tag <tag>`.", "", "Tags: " +
         " · ".join(f"[[#{t}]] ({len(v)})" for t, v in sorted(by_tag.items(), key=lambda kv: -len(kv[1]))), ""]
    for tag, items in sorted(by_tag.items(), key=lambda kv: -len(kv[1])):
        L += [f"## {tag}", ""]
        for e in items:
            L += [f"### {e['title']}", f"*{e['kind']}* · [[{e['note']}]] · {e['where']}", "", e["retell"], ""]
            if e["words"]:
                L += [f"> {e['words']}", ""]
            L += [f"**Why it matters:** {e['why']}"]
            if e["check"] and e["check"].lower().strip(". ") != "none":
                L += [f"**Check first:** {e['check']}"]
            L += [""]
    return "\n".join(L)


def show(e: dict) -> None:
    print(f"\n■ {e['title']}  [{e['kind']}]  {', '.join(e['tags'])}\n  {e['note']}  @ {e['where']}\n  {e['retell']}")
    if e["words"]:
        print(f"  \"{e['words'].strip(chr(34))}\"")
    print(f"  why: {e['why']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--find", default="", help="show entries containing every one of these words")
    ap.add_argument("--tag", default="", help="show entries with this Use-it-for tag")
    ap.add_argument("--root", action="append", default=[], help="extra folder to collect CKG files from")
    a = ap.parse_args()
    files = ckg_files([MAIN, *map(Path, a.root)])
    bank = [e for f in files for e in entries(f)]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "STORY_BANK.md").write_text(render(bank, len(files)), encoding="utf-8")
    with (OUT / "STORY_BANK.jsonl").open("w", encoding="utf-8") as fh:
        for e in bank:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    with_bank = len({e["file"] for e in bank})
    print(f"Story Bank: {len(bank)} entries from {with_bank} of {len(files)} CKG file(s) -> {OUT / 'STORY_BANK.md'}")
    if a.find or a.tag:
        words = a.find.lower().split()
        hits = [e for e in bank if (not a.tag or a.tag.lower() in e["tags"])
                and all(w in json.dumps(e, ensure_ascii=False).lower() for w in words)]
        for e in hits:
            show(e)
        print(f"\n{len(hits)} match(es)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
