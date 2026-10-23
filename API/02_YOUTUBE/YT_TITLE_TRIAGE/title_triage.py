r"""YT TITLE TRIAGE - match YouTube transcript TITLES to the debate questions, then copy only what you approve.

  python title_triage.py plan            # DeepSeek reads titles only (cheap) -> PICKLISTS\<Channel>.md/.json
  python title_triage.py copy            # copies every row with "approved": true
  python title_triage.py plan --channel "Mike Winger"   # one channel

Nothing is copied by 'plan'. Review the .md, set "approved": false in the .json for any pick you reject, then 'copy'.
Copies (never moves) go to:
  obsidian_transcripts\<Channel>\                       (the one YouTube markdown folder; station 03 reads it)
  _ARGUMENTS\..\<Q-ID>\04_SOURCES\YOUTUBE_FOR\          (side = answer)
  _ARGUMENTS\..\<Q-ID>\04_SOURCES\YOUTUBE_AGAINST\      (side = attack: skeptic channels, the best case against)
"""
import argparse, json, os, re, shutil, sys, urllib.request
from datetime import datetime, timezone

SRC  = os.environ.get("TT_SRC",  r"D:\GitHub\Research-Acquisition\yt-transcript-downloader\subtitles")
HUB  = os.environ.get("TT_HUB",  r"\\192.168.2.50\h_hp\Desktop\Youtube API CKG")
ARGS = os.path.join(HUB, "_ARGUMENTS")
DEST = os.path.join(HUB, "obsidian_transcripts")
HERE = os.path.dirname(os.path.abspath(__file__))
PICK = os.path.join(HERE, "PICKLISTS")

FOR_CHANNELS = ["Mike Winger", "Mike Licona", "Gary Habermas", "ReasonableFaithOrg", "Biola University", "GodLogic Apologetics",
                "Living Waters", "Answers in Genesis", "Associates for Biblical Research", "Truth is Christ", "A Seat For Jesus",
                "The Power of the Word", "The Quiet Shepherd", "Lungs of Faith", "Lakepointe Church", "University of Notre Dame"]
AGAINST_CHANNELS = ["Alex O'Connor", "Bart D. Ehrman", "Rationality Rules", "Stephen Woodford", "Majesty of Reason"]
CHUNK = 120

def questions():
    text = open(os.path.join(ARGS, "DEBATE_MAP.md"), encoding="utf-8").read()
    return re.findall(r"^- `(Q-[A-Z0-9-]+)`\s+(.+)$", text, re.M)

def q_dirs():
    out = {}
    for sec in os.listdir(ARGS):
        p = os.path.join(ARGS, sec)
        if re.match(r"^\d\d_S-", sec) and os.path.isdir(p):
            for q in os.listdir(p):
                if q.startswith("Q-"): out[q] = os.path.join(p, q)
    return out

def key():
    k = os.environ.get("DEEPSEEK_API_KEY")
    if not k:
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as h: k = winreg.QueryValueEx(h, "DEEPSEEK_API_KEY")[0]
        except Exception: pass
    if not k: sys.exit("DEEPSEEK_API_KEY not found")
    return k

def ask(titles, qs, side, mock=False):
    if mock:
        return [{"i": i, "keep": "evil" in t.lower(), "q": ["Q-EVIL-LOGICAL"] if "evil" in t.lower() else [], "why": "mock"} for i, t in enumerate(titles)]
    qlist = "\n".join(f"{q} | {t}" for q, t in qs)
    role = ("These are from a CHRISTIAN channel. Keep a video only if it substantially ANSWERS one of the questions."
            if side == "for" else
            "These are from a SKEPTIC channel. Keep a video only if it makes a substantial CASE AGAINST Christianity on one of the questions (the best objection, not mockery).")
    sys_p = ("You triage YouTube video titles against a fixed list of debate questions. " + role +
             " Skip worship songs, announcements, channel news, personal vlogs, drama and anything only loosely related. "
             "Be strict: when unsure, keep=false. Use only Q-IDs from the list. At most 3 Q-IDs per video. "
             "Return ONLY JSON: {\"rows\":[{\"i\":<index>,\"keep\":true|false,\"q\":[\"Q-...\"],\"why\":\"<=12 words\"}]} with one row per title.")
    user = "QUESTIONS:\n" + qlist + "\n\nTITLES:\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(titles))
    body = {"model": "deepseek-chat", "temperature": 0, "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": sys_p}, {"role": "user", "content": user}]}
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", json.dumps(body).encode(),
                                 {"Content-Type": "application/json", "Authorization": "Bearer " + key()})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(json.loads(r.read())["choices"][0]["message"]["content"])["rows"]
        except Exception as e:
            err = e
    raise RuntimeError(f"DeepSeek failed 3 times: {err}")

def plan(only=None, mock=False):
    qs = questions(); valid = {q for q, _ in qs}; os.makedirs(PICK, exist_ok=True)
    for side, chans in (("for", FOR_CHANNELS), ("against", AGAINST_CHANNELS)):
        for ch in chans:
            if only and ch != only: continue
            folder = os.path.join(SRC, ch)
            if not os.path.isdir(folder): print(f"  missing: {ch}"); continue
            files = sorted(f for f in os.listdir(folder) if f.lower().endswith(".md"))
            titles = [f[:-3] for f in files]; rows = []
            for s in range(0, len(titles), CHUNK):
                part = titles[s:s + CHUNK]
                for r in ask(part, qs, side, mock):
                    i = int(r.get("i", -1))
                    if not (0 <= i < len(part)): continue
                    q = [x for x in r.get("q", []) if x in valid][:3]   # code checks: unknown Q-IDs dropped
                    keep = bool(r.get("keep")) and bool(q)
                    rows.append({"file": files[s + i], "keep": keep, "approved": keep, "q": q, "why": r.get("why", "")})
            keepers = [r for r in rows if r["keep"]]
            out = {"channel": ch, "side": side, "planned_at": datetime.now(timezone.utc).isoformat(),
                   "total": len(files), "kept": len(keepers), "rows": rows}
            json.dump(out, open(os.path.join(PICK, f"{ch}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            md = [f"# {ch}  ({'answers' if side == 'for' else 'attack side'})  - kept {len(keepers)} of {len(files)}", "",
                  "To reject a pick: open the .json, set \"approved\": false on that row. Then run: python title_triage.py copy", ""]
            by_q = {}
            for r in keepers:
                for q in r["q"]: by_q.setdefault(q, []).append(r)
            for q in sorted(by_q):
                md.append(f"## {q}"); md += [f"- {r['file'][:-3]}  _({r['why']})_" for r in by_q[q]]; md.append("")
            open(os.path.join(PICK, f"{ch}.md"), "w", encoding="utf-8").write("\n".join(md))
            print(f"  {ch:<34} kept {len(keepers):>4} of {len(files)}")

def copy():
    qd = q_dirs(); n = 0
    for f in sorted(os.listdir(PICK)):
        if not f.endswith(".json"): continue
        pl = json.load(open(os.path.join(PICK, f), encoding="utf-8")); ch = pl["channel"]
        sub = "YOUTUBE_FOR" if pl["side"] == "for" else "YOUTUBE_AGAINST"
        for r in pl["rows"]:
            if not r.get("approved"): continue
            src = os.path.join(SRC, ch, r["file"])
            if not os.path.isfile(src): continue
            targets = [os.path.join(DEST, ch)] + [os.path.join(qd[q], "04_SOURCES", sub, ch) for q in r["q"] if q in qd]
            for t in targets:
                os.makedirs(t, exist_ok=True); dst = os.path.join(t, r["file"])
                if not os.path.exists(dst): shutil.copy2(src, dst); n += 1
    print(f"copied {n} files (existing copies skipped)")

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("mode", choices=["plan", "copy"]); a.add_argument("--channel"); a.add_argument("--mock", action="store_true")
    x = a.parse_args(); plan(x.channel, x.mock) if x.mode == "plan" else copy()
