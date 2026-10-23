"""Run one series through 000_QUICK_CALL in order, then write the series header with all siblings.
Usage: python series_run.py   (edit SERIES / ORDER below)"""
import os, json, sys
from datetime import datetime, timezone
import quick_call

if not os.environ.get("DEEPSEEK_API_KEY"):          # key lives at Windows user level
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            os.environ["DEEPSEEK_API_KEY"] = winreg.QueryValueEx(k, "DEEPSEEK_API_KEY")[0]
    except Exception: pass

SRC = r"\\192.168.2.50\h_hp\Desktop\Folders\THEOPHYSICS_ORGANIZED (1)\O-09_Math_Is_Moral"
SERIES, CODE = "Math Is Moral", "MIM"
ORDER = ["preview-3bddf0.md", "preview-3773af.md", "preview-67381e.md", "preview-75c90b.md", "preview-c69183.md",
         "preview-725c23.md", "preview-38c3b8.txt", "preview-d4c88a.md", "preview-903e0d.md", "preview-f82c3c.md",
         "preview-a96d88.md", "preview-4a528f.md", "O-09_Math_Is_Moral.md", "O-09A_The_Moral_Absolute_of_Mathematics.md",
         "O-09B_The_Inevitability_of_the_Logos.md", "O-09C_Where_Does_2plus2_Live.md", "O-09D_Principia_Mathematica_Moralia.md",
         "O-09E_MoralReal_Derivation.md", "O-09F_Words_Before_Numbers.md", "preview-979e21.md", "preview-1526a4.md"]

members, seen = [], {}
for i, name in enumerate(ORDER, 1):
    side = quick_call.run(os.path.join(SRC, name), SERIES, i, len(ORDER))
    pid = side["identity"]["paper_uuid"]
    if pid in seen:
        print(f"   DUPLICATE: {name} is byte-identical to {seen[pid]} - same paper, not a new member"); continue
    seen[pid] = name
    n = side["nabla"]
    members.append({"code": f"{CODE}-{len(members)+1:02d}", "file": name, "paper_uuid": pid,
                    "version_uuid": side["identity"]["version_uuid"], "nabla": n.get("address"),
                    "decode": n.get("minimal_decode"), "status": n.get("status")})

head = {"series": SERIES, "code": CODE, "count": len(members), "built_at": datetime.now(timezone.utc).isoformat(), "members": members}
out = os.path.join(quick_call.PIPE, "SERIES", f"{CODE}_{SERIES.replace(' ', '_')}", "_SERIES")
os.makedirs(out, exist_ok=True)
json.dump(head, open(os.path.join(out, "SERIES_HEADER.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
lines = [f"# {SERIES.upper()} · {len(members)} papers", ""] + [f"- **{m['code']}** {m['file']} · `{m['paper_uuid'][:8]}` · {m['nabla'] or m['status']}\n  {m['decode'] or ''}" for m in members]
open(os.path.join(out, "SERIES_HEADER.md"), "w", encoding="utf-8").write("\n".join(lines))
print(f"\nSERIES DONE: {len(members)} members -> {out}")
