from __future__ import annotations
import csv, json
from pathlib import Path

def discover(roots: list[Path]):
    stations=[]; identities={}
    for selected in roots:
        root=selected.resolve()
        if not root.exists(): stations.append({"path":str(root),"status":"stale_path"}); continue
        for manifest in root.rglob("station.json"):
            if manifest.parent.name != "CONFIG": continue
            station=manifest.parent.parent
            try:
                config=json.loads(manifest.read_text()); identity=json.loads((station/"STATE"/"identity.json").read_text())
                sid=identity["station_id"]; events=_events(station/"LOGS"/"events.jsonl")
                item={"station_id":sid,"name":config.get("name",station.name),"description":config.get("description",""),"path":str(station),"inputs":["INBOX","INBOX/_PRIORITY","INBOX/SERIES"],"output":"OUTBOX","prompts":[s.get("prompt") for s in config.get("steps",[]) if s.get("prompt")],"steps":config.get("steps",[]),"provider":{"name":config.get("provider",{}).get("name"),"model":config.get("provider",{}).get("model")},"nlp_capabilities":[s.get("handler") for s in config.get("steps",[]) if s.get("type")=="nlp"],"dependencies":config.get("dependencies",[]),"handoff":config.get("handoff"),"activity":_summary(events),"status":"ok"}
                if sid in identities: item["status"]="duplicate_identity"; identities[sid]["status"]="duplicate_identity"
                else: identities[sid]=item
                stations.append(item)
            except (OSError,ValueError,KeyError) as exc: stations.append({"path":str(station),"status":"invalid","error":str(exc)})
    return {"selected_roots":[str(Path(r).resolve()) for r in roots],"stations":stations}

def _events(path):
    if not path.exists(): return []
    rows=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        try: rows.append(json.loads(line))
        except json.JSONDecodeError: pass
    return rows
def _summary(events):
    jobs=[e for e in events if e.get("event")=="job_end"]
    success=[e for e in jobs if e.get("status")=="completed"]
    return {"jobs":len(jobs),"failures":sum(e.get("status")=="failed" for e in jobs),"last_success":success[-1].get("time") if success else None,"current":events[-1] if events else None}

def aggregate(inventory: dict, destination: Path):
    rows=[]
    for station in inventory["stations"]:
        path=Path(station.get("path",""))/"LOGS"/"events.jsonl"
        for event in _events(path):
            marker=(event.get("station_id"),event.get("run_id"),event.get("job_id"),event.get("call_id"),event.get("event"),event.get("time"))
            rows.append((marker,event))
    unique={marker:row for marker,row in rows}; destination.parent.mkdir(parents=True,exist_ok=True)
    fields=sorted({k for row in unique.values() for k in row}) or ["station_id"]
    with destination.open("w",newline="",encoding="utf-8") as fh:
        writer=csv.DictWriter(fh,fieldnames=fields,extrasaction="ignore"); writer.writeheader(); writer.writerows(unique.values())
    return len(unique)
