import json, re, pathlib
out = pathlib.Path(r"D:\GitHub\pipeline-workflows\API\000_QUICK_CALL\OUTBOX\04_CRAFT_EXTRACT")
lib, bad = [], []
for f in sorted(out.glob("* - answer *.md")):
    t = f.read_text(encoding="utf-8").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        d = json.loads(t)
    except Exception as e:
        bad.append((f.name, str(e)[:80]))
        continue
    for i, tech in enumerate(d.get("techniques", []), 1):
        tech["source_title"] = d.get("source_title") or f.stem
        tech["channel"] = d.get("channel")
        tech["card_id"] = f"CRAFT-{len(lib) + 1:03d}"
        lib.append(tech)
(out / "craft_library.json").write_text(json.dumps(lib, indent=1, ensure_ascii=False), encoding="utf-8")
md = ["# Craft library", "", f"{len(lib)} technique cards from {len(set(c['source_title'] for c in lib))} videos.", ""]
for c in lib:
    md += [f"## {c['card_id']} · {c.get('name')}  _(serves: {c.get('serves')}; page: {c.get('for_written_prose')})_",
           f"*{c.get('source_title')}*", "",
           f"- **Does:** {c.get('what_it_does')}",
           f"- **Weak:** {c.get('bad_example')}",
           f"- **Strong:** {c.get('good_example')}",
           f"- **Why:** {c.get('why_it_works')}",
           f"- **Use when:** {c.get('when_to_use')}  **Backfires:** {c.get('when_it_backfires')}", ""]
(out / "craft_library.md").write_text("\n".join(md), encoding="utf-8")
print("cards:", len(lib), "| unparsed files:", bad)
from collections import Counter
print("serves:", dict(Counter(c.get("serves") for c in lib)))
print("for page:", dict(Counter((c.get("for_written_prose") or "").split()[0].strip(",.") for c in lib)))
for c in lib:
    print(f"{c['card_id']} [{c.get('serves')}] {c.get('name')} :: {(c.get('what_it_does') or '')[:110]}  <{c['source_title'][:28]}>")
