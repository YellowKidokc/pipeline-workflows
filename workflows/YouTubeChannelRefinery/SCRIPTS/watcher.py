#!/usr/bin/env python3
"""Watch INPUT for stable downloads and spawn a decision popup."""
from __future__ import annotations
import argparse, json, re, subprocess, sys, time
from pathlib import Path
PACKET=Path(__file__).resolve().parents[1]; SEEN=PACKET/'STATE/seen.json'
def metadata(path):
 text=path.read_text(encoding='utf-8-sig',errors='replace'); m=re.search(r'^#\s+(.+?)\s+-\s+Videos',text,re.M); return (m.group(1) if m else path.stem,len(re.findall(r'^##\s+\d+\.',text,re.M)) or 1)
def scan_once(folder=PACKET/'INPUT',seen_path=SEEN,sleep=time.sleep,stability_seconds=1,spawn=subprocess.Popen):
 seen=set(json.loads(seen_path.read_text()) if seen_path.exists() else []); launched=[]
 prefs=json.loads((PACKET/'PREFS/preferences.json').read_text())
 for path in Path(folder).glob('*.md'):
  key=str(path.resolve()); size=path.stat().st_size; sleep(stability_seconds)
  if key in seen or not path.exists() or path.stat().st_size!=size: continue
  channel,count=metadata(path); remembered=prefs.get('channel_triggers',{}).get(channel,{}); profile=remembered.get('profile',prefs.get('default_profile','general'))
  spawn([sys.executable,str(PACKET/'SCRIPTS/prompt.py'),str(path),'--channel',channel,'--count',str(count),'--profile',profile])
  seen.add(key); launched.append(path)
 seen_path.parent.mkdir(parents=True,exist_ok=True); seen_path.write_text(json.dumps(sorted(seen),indent=2)); return launched
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--once',action='store_true'); a=p.parse_args()
 while True:
  scan_once()
  if a.once: break
  time.sleep(10)
