#!/usr/bin/env python3
"""Portable rule-driven drop watcher (stdlib; watchdog is optional)."""
from __future__ import annotations
import argparse, datetime as dt, fnmatch, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load_rules(path: Path) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except ImportError:
        # Parser for the deliberately small watch_rules.yaml vocabulary.
        out, rules, current, actions = {}, [], None, None
        for raw in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw.split("#",1)[0].rstrip()
            if not line.strip(): continue
            indent=len(line)-len(line.lstrip()); s=line.strip()
            if s == "rules:": out["rules"]=rules; continue
            if s.startswith("- name:"):
                current={"name":scalar(s.split(":",1)[1])}; rules.append(current); actions=None; continue
            if current is None:
                k,v=s.split(":",1); out[k]=scalar(v); continue
            if s == "actions:": current["actions"]=[]; actions=current["actions"]; continue
            if s.startswith("-") and actions is not None:
                k,v=s[1:].strip().split(":",1); actions.append({k:scalar(v)}); continue
            k,v=s.split(":",1)
            if actions is not None and indent >= 6: actions[-1][k]=scalar(v)
            else: current[k]=scalar(v)
        return out

def scalar(v):
    v=v.strip().strip('"\'')
    if v.lower() in ("true","false"): return v.lower()=="true"
    try: return int(v)
    except ValueError: return v

def file_hash(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""): h.update(block)
    return h.hexdigest()

def render(s: str, p: Path) -> str:
    now=dt.datetime.now()
    vals={"file":str(p),"stem":p.stem,"name":p.name,"dir":str(p.parent),"yyyy":f"{now.year:04}","mm":f"{now.month:02}","dd":f"{now.day:02}"}
    return str(s).format(**vals)

class Watcher:
    def __init__(self, root, config, dry=False):
        self.root=Path(root).resolve(); self.cfg=config; self.dry=dry
        self.logs=self.root/"LOGS"; self.state_dir=self.root/"_state"
        self.log=self.logs/"watch_actions.jsonl"; self.state=self.state_dir/"seen.json"
        try: self.seen=json.loads(self.state.read_text())
        except (OSError,json.JSONDecodeError): self.seen={}
    def record(self, rule, action, src, dst="", ok=True, error=""):
        row={"time":dt.datetime.now(dt.timezone.utc).isoformat(),"rule":rule,"action":action,"src":str(src),"dst":str(dst),"ok":ok,"error":str(error)}
        print(json.dumps(row));
        if not self.dry:
            self.logs.mkdir(parents=True,exist_ok=True)
            with self.log.open("a",encoding="utf-8") as f: f.write(json.dumps(row)+"\n")
    def act(self, p, rule):
        original=p
        try:
            for spec in rule.get("actions",[]):
                dry=self.dry or bool(spec.get("dry_run",False)); key=next(k for k in spec if k not in ("dry_run",))
                value=spec[key]
                if key in ("move","copy"):
                    dst=Path(render(value,p)); dst=dst/p.name if str(value).endswith(("/","\\")) or not dst.suffix else dst
                    self.record(rule["name"],key,p,dst)
                    if not dry: dst.parent.mkdir(parents=True,exist_ok=True); (shutil.move if key=="move" else shutil.copy2)(p,dst); p=dst
                elif key=="rename":
                    dst=p.with_name(render(value,p)); self.record(rule["name"],key,p,dst)
                    if not dry: p.rename(dst); p=dst
                elif key=="mkdir":
                    dst=Path(render(value,p)); self.record(rule["name"],key,p,dst)
                    if not dry: dst.mkdir(parents=True,exist_ok=True)
                elif key=="run":
                    cmd=render(value,p); self.record(rule["name"],key,p,cmd)
                    if not dry: subprocess.run(cmd,shell=True,check=True)
                elif key=="pipeline":
                    repo=Path(os.getenv("PIPELINE_WORKFLOWS_ROOT", self.root))
                    packet=repo/"workflows"/str(value); inbox=packet/"INPUT"; dst=inbox/p.name
                    self.record(rule["name"],key,p,dst)
                    if not dry:
                        inbox.mkdir(parents=True,exist_ok=True); shutil.move(p,dst)
                        runner=packet/"SCRIPTS"/"run_pipeline.py"
                        if runner.exists(): subprocess.run([sys.executable,str(runner),"--input",str(dst)],check=True)
                        p=dst
                else: raise ValueError(f"unknown action: {key}")
            return True
        except Exception as e:
            self.record(rule.get("name","?"),"error",p,"",False,e)
            if not self.dry:
                err=self.root/"ERROR"/original.name; err.parent.mkdir(parents=True,exist_ok=True)
                if original.exists(): shutil.move(original,err)
                err.with_suffix(err.suffix+".error.txt").write_text(str(e),encoding="utf-8")
            return False
    def scan(self):
        globber=self.root.rglob if self.cfg.get("recursive") else self.root.glob
        ignored={"LOGS","_state","ERROR","ARCHIVE","_processed"}
        for p in globber("*"):
            if not p.is_file() or any(part in ignored for part in p.relative_to(self.root).parts): continue
            for rule in self.cfg.get("rules",[]):
                if fnmatch.fnmatch(p.name,rule.get("match","")):
                    digest=file_hash(p)
                    if digest not in self.seen and self.act(p,rule) and not self.dry:
                        self.seen[digest]={"file":p.name,"time":dt.datetime.now().isoformat()}; self.state_dir.mkdir(exist_ok=True); self.state.write_text(json.dumps(self.seen,indent=2))
                    if not rule.get("continue",False): break
    def run(self, once=False):
        settle=float(self.cfg.get("settle_seconds",20)); sizes={}
        while True:
            now=time.monotonic()
            for p in self.root.rglob("*") if self.cfg.get("recursive") else self.root.glob("*"):
                if p.is_file():
                    sig=(p.stat().st_size,p.stat().st_mtime_ns); old=sizes.get(p)
                    sizes[p]=(sig, old[1] if old and old[0]==sig else now)
            if once:
                if settle: time.sleep(settle); self.scan(); return
            if any(now-since>=settle for sig,since in sizes.values()): self.scan()
            time.sleep(min(2,max(.2,settle/4)))

def undo(root: Path,n:int):
    log=root/"LOGS"/"watch_actions.jsonl"
    rows=[json.loads(x) for x in log.read_text().splitlines() if x.strip()]
    done=0
    for row in reversed(rows):
        if done>=n: break
        if row.get("ok") and row.get("action") in ("move","rename","pipeline"):
            src,dst=Path(row["src"]),Path(row["dst"])
            if dst.exists() and not src.exists(): src.parent.mkdir(parents=True,exist_ok=True); shutil.move(dst,src); done+=1; print(f"restored {dst} -> {src}")
    return 0 if done==n else 1

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--path",default=str(HERE)); ap.add_argument("--rules"); ap.add_argument("--recursive",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--once",action="store_true"); ap.add_argument("--undo",type=int)
    a=ap.parse_args(); root=Path(a.path).resolve()
    if a.undo is not None: return undo(root,a.undo)
    cfg=load_rules(Path(a.rules) if a.rules else root/"watch_rules.yaml"); cfg["recursive"]=a.recursive or cfg.get("recursive",False)
    Watcher(root,cfg,a.dry_run).run(a.once)
if __name__=="__main__": raise SystemExit(main())
