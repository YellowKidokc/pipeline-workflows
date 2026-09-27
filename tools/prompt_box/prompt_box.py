#!/usr/bin/env python3
"""Small, dependency-free Tk prompt window for workflow notes."""
import datetime as dt, json, os, re, subprocess, sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
HERE=Path(__file__).resolve().parent
REPO=Path(os.getenv("PIPELINE_WORKFLOWS_ROOT",HERE.parents[1]))
PACKET=REPO/"workflows"/"YouTubeChannelRefinery"; PROFILES=PACKET/"PROMPTS"/"profiles"; LOG=PACKET/"LOGS"/"prompt_box.jsonl"
def append(row):
 LOG.parent.mkdir(parents=True,exist_ok=True)
 with LOG.open("a",encoding="utf-8") as f:f.write(json.dumps(row,ensure_ascii=False)+"\n")
def main():
 root=tk.Tk(); root.title("Pipeline Prompt Box"); root.geometry("720x520")
 target=tk.StringVar(); profile=tk.StringVar(value="general"); engine=tk.StringVar(value="auto"); mode=tk.StringVar(value="preview")
 def pick(): target.set(filedialog.askopenfilename() or filedialog.askdirectory() or target.get())
 for i,(label,var) in enumerate((("Target",target),("Profile",profile),("Engine",engine),("Mode",mode))):
  ttk.Label(root,text=label).grid(row=i,column=0,sticky="nw",padx=8,pady=6)
  if label=="Target": ttk.Entry(root,textvariable=var,width=70).grid(row=i,column=1,sticky="ew"); ttk.Button(root,text="Browse",command=pick).grid(row=i,column=2)
  else:
   vals=([x.stem for x in PROFILES.glob("*.md")] if label=="Profile" else (["auto","nas-nlp","ollama","api"] if label=="Engine" else ["preview","write yaml","save as new prompt"]))
   ttk.Combobox(root,textvariable=var,values=vals,state="readonly").grid(row=i,column=1,sticky="ew")
 ttk.Label(root,text="Prompt").grid(row=4,column=0,sticky="nw",padx=8); prompt=tk.Text(root,height=9); prompt.grid(row=4,column=1,columnspan=2,sticky="nsew")
 ttk.Label(root,text="Result").grid(row=5,column=0,sticky="nw",padx=8); result=tk.Text(root,height=10); result.grid(row=5,column=1,columnspan=2,sticky="nsew")
 def submit():
  text=prompt.get("1.0","end").strip(); path=Path(target.get()); output=""
  try:
   if mode.get()=="save as new prompt":
    name=simpledialog.askstring("Profile name","Name (letters, digits, - or _):")
    if not name or not re.fullmatch(r"[\w-]+",name): raise ValueError("A safe profile name is required")
    dst=PROFILES/f"{name}.md"; dst.write_text("---\nthemes:\nextra_fields:\n---\n\n"+text+"\n",encoding="utf-8"); output=f"Saved {dst}"
   elif not path.exists(): raise ValueError("Choose an existing target")
   elif mode.get()=="write yaml":
    dst=path.with_suffix(path.suffix+".prompt.yaml"); dst.write_text("profile: "+json.dumps(profile.get())+"\nengine: "+json.dumps(engine.get())+"\nprompt: "+json.dumps(text)+"\n",encoding="utf-8"); output=f"Wrote {dst}"
   else:
    sample=path.read_text(encoding="utf-8",errors="replace")[:4000] if path.is_file() else "\n".join(str(x) for x in list(path.iterdir())[:50])
    output=f"PREVIEW ({engine.get()} / {profile.get()})\n\nPrompt: {text}\n\nTarget sample:\n{sample}"
   result.delete("1.0","end"); result.insert("1.0",output); append({"time":dt.datetime.now(dt.timezone.utc).isoformat(),"target":str(path),"profile":profile.get(),"engine":engine.get(),"mode":mode.get(),"prompt":text,"result":output,"ok":True})
  except Exception as e:
   append({"time":dt.datetime.now(dt.timezone.utc).isoformat(),"target":target.get(),"prompt":text,"error":str(e),"ok":False}); messagebox.showerror("Prompt Box",str(e))
 ttk.Button(root,text="Go",command=submit).grid(row=6,column=1,pady=8); root.columnconfigure(1,weight=1); root.rowconfigure(4,weight=1); root.rowconfigure(5,weight=1); root.mainloop()
if __name__=="__main__": main()
