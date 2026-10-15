#!/usr/bin/env python3
"""Combine claim/evidence/proof/Lean records and inject them into an atom HTML shell."""
from __future__ import annotations
import argparse, hashlib, html, json, os, re, shutil, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXTENSIONS={".json",".yaml",".yml"}
KINDS=("claim","evidence","proof","lean")
HERE=Path(__file__).resolve().parent
FRONT=HERE.parent

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1048576),b""): h.update(block)
    return h.hexdigest()

def slug(value: str) -> str:
    return (re.sub(r"[^A-Za-z0-9._-]+","-",value).strip("-._").lower()[:100] or "atom-package")

def expand_items(raw: list[str]) -> list[Path]:
    items=[]
    for token in raw:
        if token.startswith("@") and Path(token[1:]).is_file():
            items += [Path(x.strip()) for x in Path(token[1:]).read_text(encoding="utf-8-sig").splitlines() if x.strip()]
        else: items.append(Path(token))
    found=[]
    for item in items:
        if item.is_dir(): found += [p for p in item.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS and "_older" not in p.parts]
        elif item.is_file() and item.suffix.lower() in EXTENSIONS: found.append(item)
    return list(dict.fromkeys(p.resolve() for p in found))

def load_document(path: Path) -> Any:
    text=path.read_text(encoding="utf-8-sig")
    if path.suffix.lower()==".json": return json.loads(text)
    try: import yaml
    except ImportError as exc: raise RuntimeError(f"{path}: YAML input requires PyYAML; JSON works without it.") from exc
    return yaml.safe_load(text)

def records_from(doc: Any) -> list[dict[str,Any]]:
    if isinstance(doc,list): return [x for x in doc if isinstance(x,dict)]
    if not isinstance(doc,dict): return []
    for key in ("atoms","records","items"):
        if isinstance(doc.get(key),list): return [x for x in doc[key] if isinstance(x,dict)]
    return [doc]

def first(record: dict[str,Any],*paths: str) -> Any:
    for dotted in paths:
        value: Any=record
        for part in dotted.split("."):
            if not isinstance(value,dict) or part not in value: value=None; break
            value=value[part]
        if value not in (None,"",[]): return value
    return None

def kind_of(record: dict[str,Any]) -> str:
    value=str(first(record,"type","atom.type","object_type","kind") or "record").lower()
    if "lean" in value or "formal" in value: return "lean"
    for kind in ("claim","evidence","proof"):
        if kind in value: return kind
    return value

def record_id(record: dict[str,Any],source: Path,index: int) -> str:
    value=first(record,"id","atom.id","claim_id","evidence_id","proof_id","lean_id")
    return str(value) if value else f"{source.stem}-{index+1}"

def group_key(record: dict[str,Any],source: Path) -> str:
    value=first(record,"cluster_id","group_id","paper_id","source.paper_id","provenance.paper_id")
    return str(value) if value else source.parent.name

def explicit_edges(record: dict[str,Any]) -> list[dict[str,Any]]:
    edges=[]
    graph=record.get("evidence_graph")
    if isinstance(graph,dict) and isinstance(graph.get("edges"),list): edges += [x for x in graph["edges"] if isinstance(x,dict)]
    rel=record.get("relationships")
    if isinstance(rel,list): edges += [x for x in rel if isinstance(x,dict)]
    elif isinstance(rel,dict): edges.append(rel)
    if isinstance(record.get("relation"),dict): edges.append(record["relation"])
    return edges

def canonical(key: str,entries: list[tuple[dict[str,Any],Path,int]]) -> dict[str,Any]:
    members=[]; nodes=[]; edges=[]
    for raw,source,index in entries:
        item=dict(raw); item.setdefault("id",record_id(item,source,index)); item.setdefault("type",kind_of(item))
        item["_assembly_source"]=str(source); members.append(item)
        nodes.append({"id":item["id"],"type":item["type"],"title":first(item,"title","atom.title","label")})
        edges += explicit_edges(item)
    primary=next((x for x in members if x["type"]=="claim"),members[0])
    title=str(first(primary,"title","atom.title","label","statement") or key)
    data={"spec_version":"atom-package/1.0","generated_at":datetime.now(timezone.utc).isoformat(),
          "cluster_id":key,"title":title,"atom":primary,"members":members}
    for kind in KINDS: data[kind+"s"]=[x for x in members if x["type"]==kind]
    data["evidence_graph"]={"nodes":nodes,"edges":edges}
    return data

def yaml_text(data: dict[str,Any]) -> str:
    try:
        import yaml
        return yaml.safe_dump(data,sort_keys=False,allow_unicode=True)
    except ImportError: return json.dumps(data,indent=2,ensure_ascii=False)+"\n"

def configured_shell() -> Path|None:
    direct=os.environ.get("ATOM_SHELL_HTML")
    if direct and Path(direct).is_file(): return Path(direct)
    config=None
    for parent in [FRONT,*FRONT.parents]:
        candidate=parent/"_system"/"config"/"paths.json"
        if candidate.is_file(): config=candidate; break
    if not config: return None
    try: data=json.loads(config.read_text(encoding="utf-8-sig"))
    except (OSError,json.JSONDecodeError): return None
    candidates=[]
    def walk(value: Any,key: str="") -> None:
        if isinstance(value,dict):
            for k,v in value.items(): walk(v,str(k).lower())
        elif isinstance(value,str):
            p=Path(os.path.expandvars(os.path.expanduser(value)))
            if "atom_shell" in key: candidates.append(p)
            elif key in {"atoms_repo","atom_repo","faith_through_physics_atoms"}: candidates.append(p/"_template"/"html"/"atom-shell.html")
    walk(data)
    return next((p for p in candidates if p.is_file()),None)

def shell_and_assets(shell_arg: str|None,outbox: Path) -> str:
    shell=Path(shell_arg).resolve() if shell_arg else configured_shell()
    if not shell or not shell.is_file(): return (HERE/"templates"/"atom-shell-fallback.html").read_text(encoding="utf-8")
    text=shell.read_text(encoding="utf-8-sig"); assets=outbox/"_assets"
    for suffix in (".css",".js",".json"):
        for source in shell.parent.glob("*"+suffix):
            assets.mkdir(parents=True,exist_ok=True); shutil.copy2(source,assets/source.name)
            text=text.replace('"'+source.name+'"','"_assets/'+source.name+'"').replace("'"+source.name+"'","'_assets/"+source.name+"'")
    return text

def inject(template: str,data: dict[str,Any]) -> str:
    payload=json.dumps(data,indent=2,ensure_ascii=False).replace("</","<\\/")
    if "{{ATOM_JSON}}" in template: return template.replace("{{TITLE}}",html.escape(str(data["title"]))).replace("{{ATOM_JSON}}",payload)
    tag='<script type="application/json" id="atom-data">'+payload+"</script>"
    return re.sub(r"</body\s*>",tag+"\n</body>",template,count=1,flags=re.I) if re.search(r"</body\s*>",template,re.I) else template+"\n"+tag

def archive(paths: list[Path],outbox: Path) -> None:
    existing=[p for p in paths if p.exists()]
    if not existing: return
    folder=outbox/"_older"/datetime.now().strftime("%Y-%m-%d_%H%M%S"); folder.mkdir(parents=True,exist_ok=True)
    for source in existing:
        target=folder/source.name; n=2
        while target.exists(): target=folder/f"{source.stem}-{n}{source.suffix}"; n+=1
        shutil.move(str(source),str(target))

def markdown(data: dict[str,Any]) -> str:
    lines=["# "+str(data["title"]),"",f"- Cluster: {data['cluster_id']}",f"- Records: {len(data['members'])}",
           f"- Explicit edges: {len(data['evidence_graph']['edges'])}","","## Members",""]
    lines += [f"- **{x.get('type','record')}** — {x.get('title') or x.get('id')}" for x in data["members"]]
    lines += ["","## Evidence graph","",json.dumps(data["evidence_graph"],indent=2,ensure_ascii=False),""]
    return "\n".join(lines)

def write_group(key: str,data: dict[str,Any],entries: list[tuple[dict[str,Any],Path,int]],outbox: Path,template: str,dry: bool) -> dict[str,Any]:
    name=slug(key); paths={ext:outbox/f"{name}.{ext}" for ext in ("json","yaml","md","html")}; receipt=outbox/f"{name}.receipt.json"
    if dry: print(f"would write {name}: {len(entries)} records"); return {"slug":name,"title":data["title"],"members":len(entries)}
    archive([*paths.values(),receipt],outbox)
    paths["json"].write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    paths["yaml"].write_text(yaml_text(data),encoding="utf-8"); paths["md"].write_text(markdown(data),encoding="utf-8")
    paths["html"].write_text(inject(template,data),encoding="utf-8")
    sources=sorted({p for _,p,_ in entries})
    rec={"spec_version":"atom-assembly-receipt/1.0","generated_at":datetime.now(timezone.utc).isoformat(),
         "cluster_id":key,"sources":[{"path":str(p),"sha256":sha256(p)} for p in sources],
         "outputs":[{"path":str(p),"sha256":sha256(p)} for p in paths.values()]}
    receipt.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"slug":name,"title":data["title"],"members":len(entries)}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("items",nargs="+")
    parser.add_argument("--outbox",type=Path,default=FRONT/"OUTBOX"); parser.add_argument("--workers",type=int,default=1)
    parser.add_argument("--focus",default=""); parser.add_argument("--shell"); parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args(); sources=expand_items(args.items)
    if not sources: print("No JSON/YAML inputs found.",file=sys.stderr); return 2
    groups=defaultdict(list); failures=[]
    for source in sources:
        try:
            for index,record in enumerate(records_from(load_document(source))): groups[group_key(record,source)].append((record,source,index))
        except Exception as exc: failures.append(str(exc))
    if failures: print("\n".join("ERROR: "+x for x in failures),file=sys.stderr)
    if not groups: return 2
    out=args.outbox.resolve()
    if not args.dry_run: out.mkdir(parents=True,exist_ok=True)
    template=shell_and_assets(args.shell,out); rows=[]
    for key in sorted(groups): rows.append(write_group(key,canonical(key,groups[key]),groups[key],out,template,args.dry_run))
    if not args.dry_run:
        links="".join(f'<li><a href="{html.escape(x["slug"])}.html">{html.escape(str(x["title"]))}</a> ({x["members"]} records)</li>' for x in rows)
        index=out/"index.html"; archive([index],out); index.write_text('<!doctype html><meta charset="utf-8"><title>Atom packages</title><h1>Atom packages</h1><ul>'+links+"</ul>\n",encoding="utf-8")
        (out/"_last_run.txt").write_text("\n".join(map(str,sources))+"\n",encoding="utf-8")
    print(f"Assembled {len(rows)} package(s) from {len(sources)} source file(s) -> {out}")
    return 1 if failures else 0

if __name__=="__main__": raise SystemExit(main())
