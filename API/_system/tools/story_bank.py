"""story_bank.py - aggregate every story, clip and quote the lenses/index found, across all channels. No API.
Reads  <indexed_root>\<Channel>\_API\*.lens.json  (lenses: stories, clips, scripture, sources, ...)
       <indexed_root>\<Channel>\_API\*.index.json (the station-03 'stories' section)
Writes <out>\STORY_BANK.md / .csv / .json  - one row per item: channel, video, kind, label, quote, lesson/use, score, link.
Usage: python story_bank.py "<indexed_root>" "<out_dir>" [--kinds stories,clips,scripture]
"""
import json, csv, sys, re, argparse
from pathlib import Path

def secs(ts):
    n=0
    for p in str(ts or "").split(":"):
        n = n*60+int(p) if p.isdigit() else n
    return n

def link(url, at):
    return f"{url}&t={secs(at)}s" if url and at else (url or "")

def rows_from_lens(path, kinds):
    d=json.load(open(path,encoding="utf-8"))
    meta=d.get("_meta",{}); chan=path.parents[1].name; video=path.name.replace(".lens.json","")
    url=meta.get("url","")
    for kind in kinds:
        block=d.get(kind)
        if not block: continue
        items=block.get("items",block) if isinstance(block,dict) else block
        for it in items if isinstance(items,list) else []:
            if not isinstance(it,dict): continue
            yield {"channel":chan,"video":video,"kind":kind,
                   "label":it.get("label") or it.get("title") or it.get("term") or "",
                   "quote":it.get("quote") or it.get("text") or it.get("summary") or "",
                   "lesson":it.get("use") or it.get("why") or it.get("lesson") or "",
                   "score":it.get("score",""),"at":it.get("at",""),"end":it.get("end",""),
                   "link":link(url,it.get("at")),"file":str(path)}

def rows_from_index(path):
    d=json.load(open(path,encoding="utf-8"))
    meta=d.get("_meta",{}); chan=path.parents[1].name; video=path.name.replace(".index.json","")
    url=meta.get("url","")
    for s in d.get("stories",[]) or []:
        if not isinstance(s,dict): continue
        yield {"channel":chan,"video":video,"kind":"story(index)",
               "label":s.get("title",""),"quote":s.get("summary") or s.get("retelling") or "",
               "lesson":s.get("lesson") or s.get("speaker_lesson") or "",
               "score":(s.get("told") or s.get("ratings",{}).get("overall","")) if isinstance(s.get("ratings",{}),dict) else "",
               "at":s.get("at",""),"end":s.get("end",""),"link":link(url,s.get("at")),"file":str(path)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("indexed_root"); ap.add_argument("out")
    ap.add_argument("--kinds",default="stories,clips,scripture,sources")
    a=ap.parse_args(); kinds=[k.strip() for k in a.kinds.split(",") if k.strip()]
    root=Path(a.indexed_root); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in root.rglob("_API/*.lens.json"): rows+=list(rows_from_lens(p,kinds))
    for p in root.rglob("_API/*.index.json"): rows+=list(rows_from_index(p))
    rows.sort(key=lambda r:(r["kind"],-(float(r["score"]) if str(r["score"]).replace('.','',1).isdigit() else 0)))
    json.dump(rows,open(out/"STORY_BANK.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
    with open(out/"STORY_BANK.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()) if rows else ["channel"]); w.writeheader(); w.writerows(rows)
    with open(out/"STORY_BANK.md","w",encoding="utf-8") as f:
        f.write(f"# STORY BANK - {len(rows)} items across {len({r['channel'] for r in rows})} channels\n\n")
        kind=None
        for r in rows:
            if r["kind"]!=kind:
                kind=r["kind"]; f.write(f"\n## {kind} ({sum(1 for x in rows if x['kind']==kind)})\n\n")
            f.write(f"- **{r['label']}** - {r['channel']} / {r['video'][:70]}"+(f" - score {r['score']}" if r['score']!='' else "")
                    +(f" - [{r['at']}]({r['link']})" if r['link'] else (f" - {r['at']}" if r['at'] else ""))+"\n")
            if r["quote"]: f.write(f"  > \u27e6{kind.upper()}\u27e7 {str(r['quote'])[:400]} \u27e6/{kind.upper()}\u27e7\n")
            if r["lesson"]: f.write(f"  - use: {str(r['lesson'])[:200]}\n")
    print(f"{len(rows)} items -> {out}")

if __name__=="__main__": main()
