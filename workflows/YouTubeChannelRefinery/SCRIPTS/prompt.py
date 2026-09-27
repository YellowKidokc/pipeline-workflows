#!/usr/bin/env python3
"""Always-on-top, non-blocking (separate process) download decision prompt."""
from __future__ import annotations
import argparse, json, sys, tkinter as tk
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent)); from job_queue import enqueue

def show(file,channel,count,profile,timeout=300,prefs=None):
 prefs=prefs or {}; root=tk.Tk(); root.title('New download detected'); root.attributes('-topmost',True); choice={'value':None}; selected=tk.StringVar(value=profile); remember=tk.BooleanVar(value=False)
 tk.Label(root,text=f"New download detected\n{channel} — {count} videos (channel)\nEstimated: calculating · profile:").pack(padx=20,pady=8); tk.OptionMenu(root,selected,'christian','conspiracy','general','science').pack()
 buttons=tk.Frame(root); buttons.pack(pady=8)
 def finish(trigger,split=False):
  if choice['value'] is not None:return
  choice['value']=enqueue(file,selected.get(),trigger,channel,split,video_count=count)
  if remember.get():
   prefs.setdefault('channel_triggers',{})[channel]={'profile':selected.get(),'trigger':trigger}; Path(__file__).parents[1].joinpath('PREFS/preferences.json').write_text(json.dumps(prefs,indent=2),encoding='utf-8')
  root.destroy()
 for label,trigger,split in [('Run now','now',False),('When PC idle 30 min','idle',False),('Tonight at 1:00','tonight',False),('Only split, no NLP','now',True),('Skip','skip',False)]: tk.Button(buttons,text=label,command=lambda t=trigger,s=split:finish(t,s)).pack(side='left')
 tk.Checkbutton(root,text='Remember this choice for this channel',variable=remember).pack(); root.after(timeout*1000,lambda:finish(prefs.get('default_trigger','idle'))); root.mainloop(); return choice['value']
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('file'); p.add_argument('--channel',default='Unknown'); p.add_argument('--count',type=int,default=1); p.add_argument('--profile',default='general'); p.add_argument('--timeout',type=int,default=300); a=p.parse_args(); prefs=json.loads(Path(__file__).parents[1].joinpath('PREFS/preferences.json').read_text()); show(a.file,a.channel,a.count,a.profile,a.timeout,prefs)
