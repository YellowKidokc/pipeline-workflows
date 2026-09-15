"""Shared runtime for independently runnable refinery stations."""
from __future__ import annotations
import datetime as dt, importlib.util, json, sys
from dataclasses import dataclass
from pathlib import Path

PACKET=Path(__file__).resolve().parents[1]; REPO=PACKET.parents[1]
if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
from openintel.ledger import Ledger

STATIONS=[f"s{i}_{name}" for i,name in enumerate(("intake","chunks","entities","resolve","dates","claims","themes","citations","checkbacks","validate","project"))]
@dataclass
class Context:
 ledger: Ledger; video: object; packet: Path=PACKET
 @property
 def video_id(self): return self.video["id"]
 @property
 def profile(self): return self.video["profile"]
 @property
 def state_dir(self):
  p=self.packet/"STATE"/self.video_id; p.mkdir(parents=True,exist_ok=True); return p

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def load_station(name):
 path=PACKET/"SCRIPTS"/"stations"/f"{name}.py"
 spec=importlib.util.spec_from_file_location(f"refinery_{name}",path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def run_station(ledger_path,video_id,name,force=False):
 if name not in STATIONS: raise ValueError(f"unknown station {name}")
 ledger=Ledger(ledger_path); ledger.initialize(); video=ledger.db.execute("SELECT * FROM videos WHERE id=?",(video_id,)).fetchone()
 if not video: ledger.close(); raise ValueError(f"unknown video {video_id}")
 row=ledger.db.execute("SELECT status FROM station_runs WHERE video_id=? AND station=?",(video_id,name)).fetchone()
 if row and row[0]=="DONE" and not force: ledger.close(); return "already_done"
 started=now()
 with ledger.db: ledger.db.execute("INSERT INTO station_runs VALUES(?,?,'RUNNING',?,NULL,NULL) ON CONFLICT(video_id,station) DO UPDATE SET status='RUNNING',started_at=excluded.started_at,finished_at=NULL,detail=NULL",(video_id,name,started))
 ctx=Context(ledger,video)
 try:
  detail=load_station(name).run(ctx) or {}
  finished=now()
  with ledger.db: ledger.db.execute("UPDATE station_runs SET status='DONE',finished_at=?,detail=? WHERE video_id=? AND station=?",(finished,json.dumps(detail),video_id,name))
  (ctx.state_dir/f"{name}.done.json").write_text(json.dumps({"video_id":video_id,"station":name,"finished_at":finished,"detail":detail},indent=2),encoding="utf-8")
  return "done"
 except Exception as exc:
  with ledger.db: ledger.db.execute("UPDATE station_runs SET status='FAILED',finished_at=?,detail=? WHERE video_id=? AND station=?",(now(),str(exc),video_id,name))
  raise
 finally: ledger.close()
