"""1 FIND APPS: find the apps this pipeline needs on this machine (David-OS, the FIS scanner, Nerve, Python ...).

    python find_apps.py            look, then write OUTBOX\\found_apps.json and OUTBOX\\FOUND_APPS.md
    python find_apps.py --quick    hints and PATH only (no drive search)

What to look for is BACKSIDE\\apps.json: a folder is the app when every 'marker' file is inside it. Known places
('hints') are checked first, then every drive a few folders deep. Nothing is changed anywhere: it only looks and
writes its own report, so other scripts (the drive's SQLite builder, the Station Console) can read where things are.
API keys are reported as set or missing, never their values.
"""
from __future__ import annotations

import json
import os
import shutil
import string
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
OUT = FRONT / "OUTBOX"
SPEC = json.loads((HERE / "apps.json").read_text(encoding="utf-8"))
SKIP = {s.lower() for s in SPEC.get("skip_dirs", [])}
DEPTH = int(SPEC.get("depth", 3))
DRIVE_SECONDS = 60          # a network drive that is slow to list gives up after this


def drives() -> list[str]:
    return [f"{d}:/" for d in string.ascii_uppercase if d not in "AB" and os.path.exists(f"{d}:/")]


def fill(hint: str, drive: str) -> Path:
    return Path(hint.replace("{LOCALAPPDATA}", os.environ.get("LOCALAPPDATA", ""))
                .replace("{USERPROFILE}", os.environ.get("USERPROFILE", "")).replace("{DRIVE}", drive))


def is_app(folder: Path, app: dict) -> bool:
    if "exe" in app:
        return (folder / app["exe"]).is_file()
    return all((folder / m).exists() for m in app["marker"])


def where(app: dict) -> Path | None:
    for hint in app.get("hints", []):
        for d in (drives() if "{DRIVE}" in hint else [""]):
            p = fill(hint, d)
            if p.is_dir() and is_app(p, app):
                return p
    if "exe" in app:
        found = shutil.which(app["exe"])
        if found and "WindowsApps" not in found:
            return Path(found).parent
    return None


def walk(root: Path, depth: int, deadline: float):
    """Folders under root, breadth first, at most `depth` deep, skipping system and build folders."""
    level = [root]
    for _ in range(depth):
        nxt = []
        for folder in level:
            if time.monotonic() > deadline:
                return
            try:
                with os.scandir(folder) as it:
                    for e in it:
                        if e.is_dir(follow_symlinks=False) and e.name.lower() not in SKIP and not e.name.startswith("$"):
                            p = Path(e.path)
                            yield p
                            nxt.append(p)
            except OSError:
                continue
        level = nxt


def search(missing: list[dict]) -> dict[str, list[Path]]:
    hits: dict[str, list[Path]] = {a["name"]: [] for a in missing}
    for d in drives():
        deadline = time.monotonic() + DRIVE_SECONDS
        started = time.monotonic()
        seen = 0
        for folder in walk(Path(d), DEPTH, deadline):
            seen += 1
            for app in missing:
                if is_app(folder, app):
                    hits[app["name"]].append(folder)
        late = " (stopped: slow drive)" if time.monotonic() > deadline else ""
        print(f"  searched {d} {seen:,} folders in {time.monotonic() - started:.0f}s{late}", flush=True)
    return hits


def main() -> int:
    quick = "--quick" in sys.argv
    print(f"Looking for {len(SPEC['apps'])} apps on {', '.join(drives())}")
    rows = []
    for app in SPEC["apps"]:
        p = where(app)
        rows.append({"name": app["name"], "need": app.get("need", False), "path": str(p) if p else "",
                     "how": "known place" if p else "", "also": []})
    missing = [a for a, r in zip(SPEC["apps"], rows) if not r["path"]]
    if missing and not quick:
        print(f"Not in the known places: {', '.join(a['name'] for a in missing)}. Searching drives {DEPTH} folders deep...")
        hits = search(missing)
        for r in rows:
            found = hits.get(r["name"]) or []
            if found and not r["path"]:
                r["path"], r["how"], r["also"] = str(found[0]), "drive search", [str(x) for x in found[1:6]]
    keys = {k: bool(os.environ.get(k)) for k in SPEC.get("keys", [])}

    OUT.mkdir(exist_ok=True)
    report = {"computer": os.environ.get("COMPUTERNAME", ""), "checked_at": datetime.now().isoformat(timespec="seconds"),
              "drives": drives(), "apps": rows, "api_keys_set": keys}
    (OUT / "found_apps.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = [f"# Found apps · {report['computer']} · {report['checked_at'].replace('T', ' ')}", "",
          "| App | Needed | Where | Found by |", "|---|---|---|---|"]
    for r in rows:
        mark = r["path"] or ("**MISSING**" if r["need"] else "not found")
        md.append(f"| {r['name']} | {'yes' if r['need'] else ''} | {mark} | {r['how']} |")
        md += [f"|  | | also: {x} | |" for x in r["also"]]
    md += ["", "API keys: " + ", ".join(f"{k} {'set' if v else 'missing'}" for k, v in keys.items())]
    (OUT / "FOUND_APPS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print()
    for r in rows:
        print(f"  {'OK ' if r['path'] else ('!! ' if r['need'] else '-- ')} {r['name']:<34} {r['path'] or ('MISSING' if r['need'] else 'not found')}")
    print("  keys: " + ", ".join(f"{k} {'set' if v else 'MISSING'}" for k, v in keys.items()))
    print(f"\nReport: {OUT / 'FOUND_APPS.md'}")
    return 1 if any(r["need"] and not r["path"] for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
