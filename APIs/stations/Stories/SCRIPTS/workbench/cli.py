from __future__ import annotations
import argparse, json, shutil, sys, time, uuid
from pathlib import Path
from .station import Runner

RUNTIME_DIRS=["INBOX/_PRIORITY","INBOX/SERIES","OUTBOX","PROCESSED_ORIGINALS","REVIEW","FAILED","LOGS","STATE"]

def station_root() -> Path:
    # Installed copies invoke this file from SCRIPTS/workbench; cwd is irrelevant.
    here=Path(__file__).resolve()
    candidate=here.parents[2]
    return candidate if (candidate/"CONFIG"/"station.json").exists() else Path.cwd()

def setup(root: Path):
    for item in RUNTIME_DIRS: (root/item).mkdir(parents=True,exist_ok=True)
    identity=root/"STATE"/"identity.json"
    if not identity.exists(): identity.write_text(json.dumps({"station_id":str(uuid.uuid4()),"created_by":"setup"},indent=2)+"\n")
    return identity

def create(template: Path, destination: Path):
    if destination.exists(): raise FileExistsError(destination)
    ignored=shutil.ignore_patterns("private.local.json","*.key","*.pem","__pycache__",".venv","venv","*.pyc")
    shutil.copytree(template,destination,ignore=ignored)
    for directory in RUNTIME_DIRS:
        target=destination/directory
        if target.exists():
            for child in target.iterdir():
                if child.name not in {".gitkeep"}: shutil.rmtree(child) if child.is_dir() else child.unlink()
        target.mkdir(parents=True,exist_ok=True)
    setup(destination)
    return destination

def check(root: Path):
    required=["CONFIG/station.json","SCRIPTS/workbench/cli.py",*RUNTIME_DIRS]
    missing=[p for p in required if not (root/p).exists()]
    config=json.loads((root/"CONFIG"/"station.json").read_text()) if not missing else {}
    print(json.dumps({"ok":not missing,"root":str(root),"missing":missing,"station_id":json.loads((setup(root)).read_text())["station_id"],"provider":config.get("provider",{}).get("name"),"model":config.get("provider",{}).get("model")},indent=2))
    return 0 if not missing else 1

def main(argv=None):
    parser=argparse.ArgumentParser(prog="portable-workbench")
    parser.add_argument("command",choices=["setup","check","run-once","watch","retry","reprocess"]); parser.add_argument("--root",type=Path); parser.add_argument("--interval",type=float,default=2)
    args=parser.parse_args(argv); root=(args.root or station_root()).resolve(); setup(root)
    if args.command=="setup": return 0
    if args.command=="check": return check(root)
    if args.command=="retry":
        for p in (root/"STATE"/"jobs").glob("*.json"):
            state=json.loads(p.read_text());
            if state.get("status")=="failed": state.pop("status",None); p.write_text(json.dumps(state,indent=2)+"\n")
        return 0
    if args.command=="reprocess":
        shutil.rmtree(root/"STATE"/"jobs",ignore_errors=True); return 0
    if args.command=="run-once": Runner(root).run_once(); return 0
    print("Watcher active in this terminal; Ctrl+C stops it.")
    from .station import StationLock
    with StationLock(root):
        while True:
            Runner(root).run_once(acquire_lock=False); time.sleep(args.interval)

if __name__=="__main__": raise SystemExit(main())
