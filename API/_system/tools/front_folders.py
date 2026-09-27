"""Bring stations out of _system/stations into numbered front folders in MAIN (the API folder).

    python _system/tools/front_folders.py youtube            preview one family
    python _system/tools/front_folders.py youtube --apply    move it (git mv, history kept)
    python _system/tools/front_folders.py all --apply

Per station NN_NAME:  _system/stations/NN_NAME/  ->  MAIN/0NN_FRONT_NAME/BACKSIDE/
  * the station script's engine import is repointed (parents[2] -> parents[2] / "_system")
  * stations.json `folder` becomes ../0NN_FRONT_NAME/BACKSIDE
  * one launcher "1 RUN ALL.bat" (or a plain name) is written next to BACKSIDE
Never overwrites: a front folder that already exists stops the whole run.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SYSTEM = Path(__file__).resolve().parents[1]
MAIN = SYSTEM.parent
STATIONS_JSON = SYSTEM / "config" / "stations.json"

FAMILIES = {
    "youtube": range(1, 20), "ckg": range(20, 30), "evidence": range(30, 40),
    "papers": range(40, 50), "lean": range(50, 60), "bundles": range(60, 70),
}
MENU_ONLY = {"90", "91"}
# David's CODEX-sketch names where the sketch names the same API; everything else keeps its station name
FRONT_NAMES = {"20": "CKG", "21": "CLAIMS_PROOFS_EVIDENCE", "30": "EVIDENCE", "41": "STORIES",
               "45": "ATOMS", "54": "AXIOM_NODES"}
# launchers that must ask a question (a channel, a topic) run the menu without --yes
ASKS = {"01": "1 GRAB A CHANNEL.bat", "48": "1 RUN A TOPIC.bat", "49": "1 RUN A TOPIC.bat"}
PLAIN = {"22": "1 CHECK CKG INBOX.bat", "46": "1 BUILD REPORT.bat", "05": "1 BUILD CATALOG.bat"}

LANES = ("INBOX/00_PRIORITY", "INBOX/01_SERIES", "INBOX/02_GROUP", "OUTBOX")
OLD_IMPORT ="sys.path.insert(0, str(Path(__file__).resolve().parents[2]))"
NEW_IMPORT = 'sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_system"))'

LAUNCHER = """@echo off
setlocal
rem {what}
set "SYS=%~dp0..\\_system\\"
{key}where py >nul 2>nul && (py -3 "%SYS%engine\\menu.py" {number}{yes} %* & goto :done)
python "%SYS%engine\\menu.py" {number}{yes} %*
:done
pause
"""
KEY_CHECK = "if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1\n"


def front_name(row: dict) -> str:
    return f"0{row['number']}_{FRONT_NAMES.get(row['number'], row['name'])}"


def git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=MAIN, check=True)


def plan(numbers: set[str]) -> list[dict]:
    rows = json.loads(STATIONS_JSON.read_text(encoding="utf-8"))
    todo = []
    for row in rows:
        if row["number"] not in numbers or row["number"] in MENU_ONLY or row.get("retired"):
            continue
        if not row["folder"].startswith("stations/"):
            continue  # already out
        todo.append(row)
    return todo


def move(row: dict, apply: bool) -> list[str]:
    src = SYSTEM / row["folder"]
    front = MAIN / front_name(row)
    back = front / "BACKSIDE"
    meta = json.loads((src / "station.json").read_text(encoding="utf-8"))
    uses_api = bool(meta.get("uses_api"))
    bat = ASKS.get(row["number"]) or PLAIN.get(row["number"]) or "1 RUN ALL.bat"
    notes = [f"{row['label']:<32} -> {front.name}\\BACKSIDE   + {bat}" + ("" if uses_api else "   (no API)")]
    if front.exists() and not any(front.glob("*.bat")):
        raise SystemExit(f"STOP: {front} already exists; nothing moved")
    if back.exists():
        raise SystemExit(f"STOP: {back} already exists; nothing moved")
    if not apply:
        return notes
    front.mkdir(exist_ok=True)
    for box in LANES:
        (front / box).mkdir(parents=True, exist_ok=True)
        keep = front / box / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    git("mv", str(src.relative_to(MAIN)), str(back.relative_to(MAIN)))
    for py in back.glob("*.py"):
        text = py.read_text(encoding="utf-8")
        if OLD_IMPORT in text:
            py.write_text(text.replace(OLD_IMPORT, NEW_IMPORT), encoding="utf-8", newline="")
    launcher = front / bat
    if any(front.glob("*.bat")):  # a front folder that came with its own launchers keeps them (055 from LEAN)
        git("add", str(front.relative_to(MAIN)))
        return notes
    launcher.write_text(LAUNCHER.format(what=meta.get("description", row["name"]), number=row["number"],
                                        yes="" if row["number"] in ASKS else " --yes",
                                        key=KEY_CHECK if uses_api else "").replace("\n", "\r\n"),
                        encoding="utf-8", newline="")
    git("add", str(front.relative_to(MAIN)))
    return notes


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("family", choices=[*FAMILIES, "all"])
    p.add_argument("--apply", action="store_true", help="move for real (default: preview)")
    a = p.parse_args()
    ranges = FAMILIES.values() if a.family == "all" else [FAMILIES[a.family]]
    numbers = {f"{n:02d}" for r in ranges for n in r}
    todo = plan(numbers)
    # the two front folders that already existed under their old names
    for old, new in (("QUICK_CALL", "000_QUICK_CALL"), ("LEAN", "055_LEAN_PAPERS")):
        if (MAIN / old).exists() and (new == "000_QUICK_CALL" or any(r["number"] == "55" for r in todo)):
            print(("moved   " if a.apply else "preview ") + f"{old:<32} -> {new}")
            if a.apply:
                if (MAIN / new).exists():
                    raise SystemExit(f"STOP: {MAIN / new} already exists")
                git("mv", old, new)
    if not todo:
        print("nothing to move")
        return 0
    rows = json.loads(STATIONS_JSON.read_text(encoding="utf-8"))
    for row in todo:
        for line in move(row, a.apply):
            print(("moved   " if a.apply else "preview ") + line)
        if a.apply:
            for r in rows:
                if r["number"] == row["number"]:
                    r["folder"] = f"../{front_name(row)}/BACKSIDE"
    if a.apply:
        STATIONS_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        git("add", str(STATIONS_JSON.relative_to(MAIN)))
    else:
        print(f"\n{len(todo)} station(s). Add --apply to move them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
