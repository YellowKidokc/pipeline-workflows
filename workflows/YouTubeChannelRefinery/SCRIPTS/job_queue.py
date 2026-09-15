"""Atomic JSON queue shared by watcher, popup, scheduler, and launcher."""
from __future__ import annotations
import datetime as dt, json, os, tempfile, uuid
from pathlib import Path
PACKET=Path(__file__).resolve().parents[1]; PATH=PACKET/'STATE/queue.json'
def load(path=PATH):
 try: return json.loads(Path(path).read_text(encoding='utf-8'))
 except (FileNotFoundError,json.JSONDecodeError): return {'jobs':[]}
def save(data,path=PATH):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,indent=2),encoding='utf-8'); os.replace(tmp,path)
def enqueue(file,profile='general',trigger='idle',channel='',split_only=False,path=PATH,video_count=0):
 data=load(path); job={'id':uuid.uuid4().hex[:12],'file':str(Path(file).resolve()),'channel':channel,'profile':profile,'trigger':trigger,'split_only':split_only,'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'QUEUED','current_video':None,'videos':list(range(1,video_count+1)) if video_count else [],'completed_videos':[]}; data['jobs'].append(job); save(data,path); return job
