from __future__ import annotations
import hashlib, json, os, shutil, socket, time, uuid
from contextlib import nullcontext
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from . import nlp
from .config import load_config, make_provider
from .events import append, session_csv

def digest(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def workflow_hash(root: Path, config: dict) -> str:
    material=json.dumps(config.get("steps", []), sort_keys=True).encode()
    for step in config.get("steps", []):
        if step.get("prompt"): material += (root/"PROMPTS"/step["prompt"]).read_bytes()
    return digest(material)
def relative(path: Path, root: Path) -> str: return path.resolve().relative_to(root.resolve()).as_posix()

class StationLock:
    def __init__(self, root: Path): self.path=root/"STATE"/"station.lock"
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try: self.path.mkdir(); (self.path/"owner.json").write_text(json.dumps({"pid":os.getpid(),"host":socket.gethostname()}))
        except FileExistsError: raise RuntimeError("station is already running")
        return self
    def __exit__(self, *args): shutil.rmtree(self.path, ignore_errors=True)

class Runner:
    def __init__(self, root: Path, provider=None):
        self.root=root.resolve(); self.config=load_config(self.root); self.provider=provider or make_provider(self.config)
        self.station_id=self._identity(); self.events=self.root/"LOGS"/"events.jsonl"
    def _identity(self):
        path=self.root/"STATE"/"identity.json"
        if not path.exists(): path.write_text(json.dumps({"station_id":str(uuid.uuid4()),"created_at":time.time()}, indent=2)+"\n")
        return json.loads(path.read_text())["station_id"]
    def candidates(self):
        priority=sorted(p for p in (self.root/"INBOX"/"_PRIORITY").rglob("*") if p.is_file() and not p.name.startswith("."))
        regular=sorted(p for p in (self.root/"INBOX").rglob("*") if p.is_file() and not p.name.startswith(".") and "_PRIORITY" not in p.parts)
        # A 3:1 weighted merge prevents regular-work starvation.
        out=[]
        while priority or regular:
            out.extend(priority[:3]); del priority[:3]
            if regular: out.append(regular.pop(0))
        return out
    def settled(self, path: Path):
        delay=float(self.config.get("queue",{}).get("settle_seconds",1)); a=(path.stat().st_size,path.stat().st_mtime_ns)
        if delay: time.sleep(delay)
        return path.exists() and a==(path.stat().st_size,path.stat().st_mtime_ns)
    def run_once(self, acquire_lock=True):
        run_id=str(uuid.uuid4()); selected=self.candidates(); rows=[]
        append(self.events,{"station_id":self.station_id,"run_id":run_id,"event":"run_start","status":"started","workflow":self.config["workflow"]})
        workers=int(self.config.get("concurrency",12))
        with (StationLock(self.root) if acquire_lock else nullcontext()), ThreadPoolExecutor(max_workers=workers) as pool:
            futures={pool.submit(self.process,p,run_id):p for p in selected}
            try:
                for future in as_completed(futures):
                    try: rows.append(future.result())
                    except Exception as exc: rows.append({"station_id":self.station_id,"run_id":run_id,"event":"job_end","status":"failed","source":relative(futures[future],self.root),"error_category":type(exc).__name__})
            except KeyboardInterrupt:
                for future,path in futures.items():
                    if not future.done(): rows.append({"station_id":self.station_id,"run_id":run_id,"event":"job_end","status":"interrupted","source":relative(path,self.root)})
                raise
        for row in rows: append(self.events,row)
        append(self.events,{"station_id":self.station_id,"run_id":run_id,"event":"run_end","status":"completed","workflow":self.config["workflow"]})
        session_csv(self.root/"LOGS"/f"session-{run_id}.csv",rows)
        return rows
    def process(self, source: Path, run_id: str):
        if not self.settled(source): return self._row(run_id,None,source,"skipped",error_category="copy_not_settled")
        raw=source.read_bytes(); source_hash=digest(raw); whash=workflow_hash(self.root,self.config); job_id=str(uuid.uuid5(uuid.UUID(self.station_id),source_hash+whash))
        state_path=self.root/"STATE"/"jobs"/f"{job_id}.json"; state_path.parent.mkdir(parents=True,exist_ok=True)
        if state_path.exists():
            state=json.loads(state_path.read_text())
            ordered=[s["name"] for s in self.config["steps"]]
            hashes=state.get("output_hashes",{})
            bad=next((i for i,name in enumerate(ordered) if name in state.get("completed_steps",{}) and
                      (not (self.root/state["completed_steps"][name]).exists() or digest((self.root/state["completed_steps"][name]).read_bytes()) != hashes.get(name))),None)
            if bad is not None:
                for name in ordered[bad:]: state.get("completed_steps",{}).pop(name,None); hashes.pop(name,None)
                state["outputs"]=[p for name,p in state.get("completed_steps",{}).items()]
                state.pop("status",None)
            if state.get("status")=="completed" and all((self.root/p).exists() for p in state.get("outputs",[])):
                return self._row(run_id,job_id,source,"skipped",source_hash=source_hash,error_category="already_completed")
        else: state={"job_id":job_id,"source_hash":source_hash,"workflow_hash":whash,"completed_steps":{},"output_hashes":{},"outputs":[]}
        original=self.root/"PROCESSED_ORIGINALS"/source_hash[:12]/source.name; original.parent.mkdir(parents=True,exist_ok=True)
        if not original.exists(): shutil.copy2(source,original)
        text=raw.decode("utf-8"); context=text; stem=source.stem
        coverage=list(state.get("coverage",[]))
        try:
            for number,step in enumerate(self.config["steps"],1):
                name=step["name"]
                if name in state["completed_steps"]:
                    context=(self.root/state["completed_steps"][name]).read_text(encoding="utf-8"); continue
                step_input=text if step.get("input")=="source" else context
                if step["type"]=="preserve": output=text
                elif step["type"]=="nlp": output=nlp.HANDLERS[step["handler"]](step_input,step.get("options"))
                elif step["type"]=="api": output, cov=self._api(step,step_input,job_id,run_id,source_hash); coverage.extend(cov)
                elif step["type"]=="validate":
                    if not context.strip(): raise ValueError("validation failed: empty result")
                    output=context
                else: raise ValueError(f"unsupported safe step type: {step['type']}")
                filename=f"{stem}__{number:02d}_{name}.md"; target=self.root/"OUTBOX"/filename
                target.write_text(output,encoding="utf-8"); context=output
                rel=relative(target,self.root); state["completed_steps"][name]=rel; state.setdefault("output_hashes",{})[name]=digest(target.read_bytes()); state["outputs"].append(rel); state["coverage"]=coverage; self._save(state_path,state)
            receipt=self.root/"OUTBOX"/f"{stem}__receipt.json"
            receipt.write_text(json.dumps({"station_id":self.station_id,"run_id":run_id,"job_id":job_id,"source":relative(source,self.root),"source_hash":source_hash,"workflow_hash":whash,"coverage":coverage,"outputs":[{"path":p,"sha256":digest((self.root/p).read_bytes())} for p in state["outputs"]]},indent=2)+"\n")
            state.update(status="completed",receipt=relative(receipt,self.root)); self._save(state_path,state)
            self._handoff(receipt,state)
            return self._row(run_id,job_id,source,"completed",source_hash=source_hash,output=relative(receipt,self.root),output_hash=digest(receipt.read_bytes()))
        except Exception as exc:
            state.update(status="failed",error_category=getattr(exc,"category",type(exc).__name__)); self._save(state_path,state)
            message=str(exc)
            secret=getattr(self.provider,"_key",None)
            if secret: message=message.replace(secret,"[REDACTED]")
            failed=self.root/"FAILED"/f"{stem}__{job_id[:8]}.json"; failed.write_text(json.dumps({"job_id":job_id,"error_category":state["error_category"],"message":message[:500]},indent=2))
            return self._row(run_id,job_id,source,"failed",source_hash=source_hash,error_category=state["error_category"])
    def _api(self,step,text,job_id,run_id,source_hash):
        prompt=(self.root/"PROMPTS"/step["prompt"]).read_text(encoding="utf-8")
        prompt_version=digest(prompt.encode())
        chunks=nlp.chunk(text,int(step.get("chunk_chars",self.config.get("token_limits",{}).get("input_chars",24000))),int(step.get("overlap_chars",200)))
        outputs=[]; coverage=[]
        for i,(start,end,body) in enumerate(chunks):
            call_id=str(uuid.uuid5(uuid.UUID(job_id),f"{step['name']}:{i}:{digest(body.encode())}"))
            base={"station_id":self.station_id,"run_id":run_id,"job_id":job_id,"call_id":call_id,"workflow":self.config["workflow"],"source_hash":source_hash,"step":step["name"],"prompt_version":prompt_version,"provider":self.provider.name,"model":self.provider.model}
            append(self.events,{**base,"event":"call_start","status":"started"})
            try:
                result=self.provider.complete(f"{prompt}\n\nSOURCE CHUNK {i+1}/{len(chunks)} [{start}:{end}]\n{body}",int(self.config.get("token_limits",{}).get("output_tokens",2000)),call_id)
            except Exception as exc:
                append(self.events,{**base,"event":"call_end","status":"failed","error_category":getattr(exc,"category",type(exc).__name__)})
                raise
            usage=result.usage or {}
            append(self.events,{**base,"event":"call_end","status":"completed","retries":result.retries,"input_tokens":usage.get("input_tokens"),"output_tokens":usage.get("output_tokens"),"reported_cost":result.reported_cost,"estimated_cost":None})
            outputs.append(result.text); coverage.append({"step":step["name"],"chunk":i+1,"chunks":len(chunks),"start":start,"end":end,"source_chars":len(text),"call_id":call_id,"usage":result.usage,"reported_cost":result.reported_cost})
        return "\n\n".join(outputs),coverage
    def _handoff(self,receipt,state):
        handoff=self.config.get("handoff")
        if not handoff or not handoff.get("enabled"): return
        destination=Path(handoff["destination"])
        if not destination.is_absolute(): destination=self.root/destination
        destination.mkdir(parents=True,exist_ok=True)
        packet={"provenance_receipt":json.loads(receipt.read_text()),"files":state["outputs"]}
        (destination/f"handoff-{state['job_id']}.json").write_text(json.dumps(packet,indent=2)+"\n")
    def _save(self,path,state):
        temp=path.with_suffix(".tmp"); temp.write_text(json.dumps(state,indent=2)+"\n"); os.replace(temp,path)
    def _row(self,run_id,job_id,source,status,**kw):
        return {"station_id":self.station_id,"run_id":run_id,"job_id":job_id,"event":"job_end","workflow":self.config["workflow"],"status":status,"source":relative(source,self.root),"provider":self.provider.name,"model":self.provider.model,**kw}
