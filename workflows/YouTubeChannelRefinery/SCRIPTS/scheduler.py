#!/usr/bin/env python3
"""Resumable one-video scheduler with Windows idle/fullscreen checks and test hooks."""
from __future__ import annotations
import argparse, ctypes, datetime as dt, json, os, shutil, subprocess, sys, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent)); from job_queue import PATH,load,save
PACKET=Path(__file__).resolve().parents[1]
def idle_seconds():
 if os.name!='nt': return 10**9
 class LASTINPUTINFO(ctypes.Structure): _fields_=[('cbSize',ctypes.c_uint),('dwTime',ctypes.c_uint)]
 info=LASTINPUTINFO(); info.cbSize=ctypes.sizeof(info); ctypes.windll.user32.GetLastInputInfo(ctypes.byref(info)); return (ctypes.windll.kernel32.GetTickCount()-info.dwTime)/1000
def cpu_percent():
 try:
  import psutil; return psutil.cpu_percent(interval=.1)
 except ImportError: return 0.0
def fullscreen_active():
 if os.name!='nt': return False
 hwnd=ctypes.windll.user32.GetForegroundWindow(); rect=(ctypes.c_long*4)(); ctypes.windll.user32.GetWindowRect(hwnd,ctypes.byref(rect)); return rect[0]<=0 and rect[1]<=0 and rect[2]>=ctypes.windll.user32.GetSystemMetrics(0) and rect[3]>=ctypes.windll.user32.GetSystemMetrics(1)
def eligible(job,prefs,idle_fn=idle_seconds,cpu_fn=cpu_percent,fullscreen_fn=fullscreen_active,now_fn=dt.datetime.now):
 if job['trigger']=='skip': return False
 if job['trigger']=='now': return True
 if job['trigger']=='idle': return idle_fn()>=60*int(prefs.get('idle_minutes',30)) and cpu_fn()<float(prefs.get('max_desktop_cpu',30)) and not fullscreen_fn()
 if job['trigger']=='tonight':
  now=now_fn(); start=int(prefs.get('night_start_hour',1)); stop=int(prefs.get('stop_hour',7)); return (start<=now.hour<stop) if start<stop else (now.hour>=start or now.hour<stop)
 return False
def process_once(queue_path=PATH,prefs=None,idle_fn=idle_seconds,cpu_fn=cpu_percent,fullscreen_fn=fullscreen_active,runner=None):
 prefs=prefs or json.loads((PACKET/'PREFS/preferences.json').read_text()); data=load(queue_path)
 def default_runner(job,video=None):
  command=[sys.executable,str(PACKET/'SCRIPTS/run_pipeline.py'),'--input',job['file'],'--profile',job['profile'],'--ledger',prefs.get('ledger','openintel.sqlite'),'--collection',prefs.get('collection','GEN'),'--keep-input']
  if video is not None: command += ['--chapter',str(video)]
  if not job.get('split_only'): command.append('--station-chain')
  else: command.append('--split-only')
  return command
 runner=runner or default_runner
 for job in data['jobs']:
  if job['status'] not in ('QUEUED','PAUSED') or not eligible(job,prefs,idle_fn,cpu_fn,fullscreen_fn): continue
  job['status']='RUNNING'; save(data,queue_path)
  videos=job.get('videos') or [None]
  for video in videos:
   if video in job['completed_videos']: continue
   job['current_video']=video; save(data,queue_path); command=runner(job,video)
   if callable(command): command()
   else: subprocess.run(command,check=True)
   job['completed_videos'].append(video); job['current_video']=None; save(data,queue_path)
   # The current video is atomic. Returning input pauses before the next one.
   if video != videos[-1] and job['trigger'] in ('idle','tonight') and not eligible(job,prefs,idle_fn,cpu_fn,fullscreen_fn):
    job['status']='PAUSED'; save(data,queue_path); return job
  job['status']='DONE'; job['finished_at']=dt.datetime.now(dt.timezone.utc).isoformat(); save(data,queue_path)
  source=Path(job['file']); archive=PACKET/'ARCHIVE'/source.name
  if source.exists() and source.resolve()!=archive.resolve(): archive.parent.mkdir(exist_ok=True); shutil.move(source,archive)
  state_dir=(PACKET/'STATE') if Path(queue_path)==PATH else Path(queue_path).parent
  complete=state_dir/f"{job['id']}_RUN_COMPLETE.json"; complete.write_text(json.dumps(job,indent=2),encoding='utf-8')
  (state_dir/f"{job['id']}.READY").write_text(job['finished_at']+'\n',encoding='utf-8')
  if os.name=='nt':
   message=f"{job.get('channel') or 'Channel'} done — {len(job['completed_videos'])} videos processed"
   safe=message.replace("'","''"); script=f"$t=[Windows.UI.Notifications.ToastTemplateType]::ToastText02;$x=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($t);$n=$x.GetElementsByTagName('text');$n.Item(0).AppendChild($x.CreateTextNode('OpenIntel'))>$null;$n.Item(1).AppendChild($x.CreateTextNode('{safe}'))>$null;$toast=[Windows.UI.Notifications.ToastNotification]::new($x);[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('OpenIntel').Show($toast)"
   subprocess.Popen(['powershell','-NoProfile','-Command',script],creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
  return job
 return None
def main():
 p=argparse.ArgumentParser(); p.add_argument('--once',action='store_true'); a=p.parse_args()
 while True:
  process_once()
  if a.once: break
  time.sleep(15)
if __name__=='__main__': main()
