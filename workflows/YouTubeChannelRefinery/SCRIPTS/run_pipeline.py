#!/usr/bin/env python3
"""Lossless YouTube channel markdown refinery."""
from __future__ import annotations
import argparse, datetime as dt, html, json, os, re, shutil, sys, urllib.request
from collections import Counter
from pathlib import Path

PACKET=Path(__file__).resolve().parents[1]; REPO=PACKET.parents[1]
SECTION_RE=re.compile(r"(?ms)^##\s+(\d+)\.\s+(.+?)\s*$\n(.*?)(?=^---\s*$|^##\s+\d+\.|\Z)")
META_RE=re.compile(r"^\*\*(Video ID|URL|Transcript Language):\*\*\s*(.*)$",re.M)
SCRIPTURE_RE=re.compile(r"\b(?:[1-3]\s*)?(?:Genesis|Exodus|Psalms?|Isaiah|Matthew|Mark|Luke|John|Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|Hebrews|James|Peter|Jude|Revelation)\s+\d{1,3}:\d{1,3}(?:[-–]\d{1,3})?",re.I)
DATE_RE=re.compile(r"\b(?:c\.\s*)?(?:AD\s*)?\d{3,4}(?:[-–]\d{2,4})?\b",re.I)
BAD='<>:"/\\|?*'
ACCUSATION_RE=re.compile(r"\b(?:killed|murdered|stole|fraud|criminal|lied|abused|corrupt|guilty|cover(?:ed)? up)\b",re.I)
PERSON_RE=re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b")

def config():
    base={"vault_root":str(PACKET/"OUTPUT"),"nas_nlp_url":"http://192.168.2.50:8765","ollama_url":"http://192.168.2.50:11434","default_profile":"christian","chapter_prefix":"Chapter","dry_run":False}
    p=PACKET/"CONFIG"/"config.json"
    if p.exists(): base.update(json.loads(p.read_text(encoding="utf-8")))
    return base

def safe(s):
    s=''.join('-' if c in BAD or ord(c)<32 else c for c in s); return re.sub(r"\s+"," ",s).strip(" .")[:140] or "Untitled"

def parse(source):
    text=source.read_text(encoding="utf-8-sig",errors="replace")
    m=re.search(r"^#\s+(.+?)\s+-\s+Videos\s*$",text,re.M); channel=m.group(1).strip() if m else re.sub(r"^(?:channel|playlist)_","",source.stem).split("_20")[0]
    videos=[]
    for n,title,body in SECTION_RE.findall(text):
        meta=dict(META_RE.findall(body)); tm=re.search(r"(?ms)^### Transcript\s*\n(.*?)(?:\n---\s*$|\Z)",body)
        transcript=tm.group(1).strip() if tm else ""
        videos.append({"chapter":int(n),"title":title.strip(),"video_id":meta.get("Video ID",""),"url":meta.get("URL",""),"transcript_language":meta.get("Transcript Language",""),"transcript":transcript})
    if not videos: raise ValueError("No numbered video sections found")
    return channel,videos

def clean_text(raw,prefs):
    text=raw
    if prefs.get("remove_stage_directions",True): text=re.sub(r"\[(?:music|applause)\]","",text,flags=re.I)
    if prefs.get("remove_fillers",True): text=re.sub(r"(?i)(?<!\w)(?:uh+|um+)(?:[, ]+|\b)","",text)
    sentences=re.split(r"(?<=[.!?])\s+",re.sub(r"\s+"," ",text).strip()); paragraphs=[]; cur=[]; count=0
    target=int(prefs.get("paragraph_words",200))
    for sent in sentences:
        words=len(sent.split())
        if cur and count+words>target: paragraphs.append(" ".join(cur)); cur=[]; count=0
        cur.append(sent); count+=words
    if cur: paragraphs.append(" ".join(cur))
    return "\n\n".join(paragraphs)

def profile(name):
    p=PACKET/"PROMPTS"/"profiles"/f"{name}.md"; text=p.read_text(encoding="utf-8")
    head=re.search(r"(?s)^---\s*\n(.*?)\n---",text); themes=[]; extras=[]; current=None
    if head:
        for line in head.group(1).splitlines():
            if line.startswith("themes:"): current=themes
            elif line.startswith("extra_fields:"): current=extras
            elif re.match(r"\s*-\s+",line) and current is not None: current.append(re.sub(r"^\s*-\s+",'',line).strip())
    return themes,extras,text

def nas(url,endpoint,payload):
    req=urllib.request.Request(url.rstrip('/')+endpoint,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=15) as r: return json.load(r)

def extract_entities(text,url):
    counts={"people":Counter(),"places":Counter(),"organizations":Counter()}
    labels={"PER":"people","PERSON":"people","LOC":"places","GPE":"places","ORG":"organizations"}
    for start in range(0,len(text),12000):
        data=nas(url,"/ner",{"text":text[start:start+12000]})
        items=data if isinstance(data,list) else data.get("entities",data.get("results",[]))
        for x in items:
            label=labels.get(str(x.get("entity_group",x.get("label",""))).upper()); word=x.get("word",x.get("text","" )).replace("##","").strip()
            if label and word: counts[label][word]+=1
    return {k:[x for x,n in v.most_common()] for k,v in counts.items()}

def yaml_block(data):
    lines=["---"]
    for k,v in data.items(): lines.append(f"{k}: {json.dumps(v,ensure_ascii=False)}")
    return "\n".join(lines)+"\n---"

def note(channel,v,profile_name,status="split",cleaned=None,fields=None,prefix="Chapter"):
    fields=fields or {}; raw=v["transcript"]; body=cleaned if cleaned is not None else raw
    data={"type":"youtube_chapter","channel":channel,"chapter":v["chapter"],"title":v["title"],"video_id":v["video_id"],"url":v["url"],"transcript_language":v["transcript_language"],"status":"no_transcript" if not raw else status,"profile":profile_name}
    data.update(fields)
    generated=""
    if fields.get("summary"): generated+=f'\n> [!summary]- Summary\n> {fields["summary"]}\n'
    if fields.get("timeline"): generated+='\n> [!list]- Timeline\n'+"\n".join(f"> - {x}" for x in fields["timeline"])+"\n"
    raw_callout=""
    if cleaned is not None and raw:
        raw_callout="\n> [!quote]- Raw transcript\n"+"\n".join("> "+x for x in raw.splitlines())+"\n"
    return f'{yaml_block(data)}\n\n# {prefix} {v["chapter"]:03d} — {v["title"]}\n<!-- generated:start -->{generated}\n## Transcript\n{body}{raw_callout}\n<!-- generated:end -->\n\n<!-- manual -->\n'

def ledger_extract(ledger_path,collection,channel,v):
    """Write source/statement/hunch candidates. Nothing machine-made is accepted."""
    if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
    from openintel.ledger import Ledger
    ledger=Ledger(ledger_path); ledger.initialize()
    source_id=ledger.add_source(collection,title=v["title"],url=v["url"],source_type="youtube",legacy_ids=[v["video_id"]] if v["video_id"] else [])
    statements=[]
    for number,sentence in enumerate(re.split(r"(?<=[.!?])\s+",re.sub(r"\s+"," ",v["transcript"]).strip()),1):
        if not sentence: continue
        sensitive=bool(ACCUSATION_RE.search(sentence) and PERSON_RE.search(sentence))
        statements.append(ledger.add_statement(collection,source_id,sentence,locator=f"chapter:{v['chapter']}:sentence:{number}",sensitive=sensitive))
    # Conflicting four-digit years in one sentence are a reviewable machine hunch, not a finding.
    for statement_id in statements:
        row=ledger.db.execute("SELECT statement_text,sensitive FROM statements WHERE id=?",(statement_id,)).fetchone()
        years=set(re.findall(r"\b(?:19|20)\d{2}\b",row[0]))
        if len(years)>1:
            hid=ledger.next_id("HNCH",collection); now=dt.datetime.now(dt.timezone.utc).isoformat()
            with ledger.db:
                ledger.db.execute("INSERT INTO hunches(id,collection,written_by,written_at,gut_statement,what_triggered_it,what_would_make_it_real,what_would_kill_it,sensitive) VALUES(?,?,?,?,?,?,?,?,?)",(hid,collection.upper(),"system extraction",now,"The dates may conflict or describe an unexplained timeline change",statement_id,"Check the source context and independent chronology","The dates refer to distinct, explicitly identified events",row[1]))
                ledger.db.execute("INSERT INTO links(from_id,to_id,link_type,source,created_at) VALUES(?,?,'TRIGGERED_BY','youtube-refinery',?)",(hid,statement_id,now))
    ledger.close(); return source_id,len(statements)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--input",type=Path); ap.add_argument("--profile"); ap.add_argument("--stage",choices=["split","clean","extract","validate","route","all"],default="all"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--ledger",type=Path); ap.add_argument("--collection",default="GEN")
    a=ap.parse_args(); cfg=config(); dry=a.dry_run or cfg.get("dry_run",False); prof=a.profile or cfg["default_profile"]
    prefs=json.loads((PACKET/"PREFS"/"preferences.json").read_text()); source=a.input or next((PACKET/"INPUT").glob("*.md"),None)
    if not source: raise SystemExit("No input markdown found")
    channel,videos=parse(source); out=Path(cfg["vault_root"])/"YouTube"/safe(channel); themes,extras,_=profile(prof)
    print(f"PLAN: {len(videos)} chapters -> {out}")
    if dry: return 0
    out.mkdir(parents=True,exist_ok=True); index=[]; any_nas_failed=False
    for v in videos:
        nas_failed=False
        filename=f'{safe(channel)} - {cfg["chapter_prefix"]} {v["chapter"]:03d} - {safe(v["title"])}.md'; dest=out/filename; index.append(f'- [[{dest.stem}|{v["chapter"]:03d}. {v["title"]}]]')
        cleaned=clean_text(v["transcript"],prefs) if prefs.get("clean_transcript",True) and v["transcript"] else None
        fields={}
        if v["transcript"]:
            fields={"people":[],"places":[],"organizations":[],"themes":[],"scripture_refs":sorted(set(SCRIPTURE_RE.findall(v["transcript"])),key=str.lower),"dates_mentioned":sorted(set(DATE_RE.findall(v["transcript"]))),"events":[],"timeline":[],"key_claims":[],"summary":"","extracted_by":{"ner":"nas-nlp","themes":"nas-nlp/deberta-zeroshot","llm":"not_run"},"extracted_at":dt.date.today().isoformat()}
            try:
                fields.update(extract_entities(v["transcript"],cfg["nas_nlp_url"])); z=nas(cfg["nas_nlp_url"],"/zeroshot",{"text":v["transcript"][:12000],"labels":themes})
                scores=z.get("scores",[]); labels=z.get("labels",themes); fields["themes"]=[x for x,s in zip(labels,scores) if s>=prefs.get("theme_threshold",.35)][:10]
            except Exception as e:
                nas_failed=True; any_nas_failed=True; review=PACKET/"REVIEW"/f"{dest.stem}.reason.txt"; review.write_text(f"NAS NLP unavailable or invalid response: {e}\n",encoding="utf-8")
            for x in extras: fields.setdefault(x,[])
        new=note(channel,v,prof,"extracted" if v["transcript"] and not nas_failed else "cleaned",cleaned,fields,cfg["chapter_prefix"])
        if dest.exists() and "<!-- manual -->" in dest.read_text(encoding="utf-8"):
            manual=dest.read_text(encoding="utf-8").split("<!-- manual -->",1)[1]; new=new.split("<!-- manual -->",1)[0]+"<!-- manual -->"+manual
        dest.write_text(new,encoding="utf-8")
        if a.ledger and v["transcript"]:
            source_id,statement_count=ledger_extract(a.ledger,a.collection,channel,v)
            print(f"Ledger candidates: {source_id}, {statement_count} statements")
    (out/f"{safe(channel)} - 000 Index.md").write_text(f"# {channel} - Videos\n\n"+"\n".join(index)+"\n",encoding="utf-8")
    archive=PACKET/"ARCHIVE"/source.name; archive.parent.mkdir(exist_ok=True)
    if source.resolve()!=archive.resolve(): shutil.move(source,archive)
    print(f"Wrote {len(videos)} chapters and index" + ("; NAS failures sent to REVIEW" if any_nas_failed else "")); return 0
if __name__=="__main__": raise SystemExit(main())
