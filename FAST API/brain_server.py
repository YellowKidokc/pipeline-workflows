#!/usr/bin/env python3
"""Drive Brain - baseline FastAPI kit (Master API, port 28280).

Layout
  <any drive>\\_BRAIN\\            one per drive (created by `install`)
      drive.json                 identity: brain_id, volume serial, label, root
      BRAIN.md                   the human-readable "note of the brain" (regenerated)
      registry\\fis.sqlite       this drive's FIS registry (fis_folder_memory.py --db)
      logs\\                     scan logs
  This folder (the kit)          one server for all drives; finds every _BRAIN itself.

Rules
  * Read-only by default. A scan writes only to the drive's registry. .fisnote files are
    written only when a scan is started with write=true (and FIS backs old notes up first).
  * Identity is the volume serial, not the drive letter: if a drive comes back as another
    letter, its brain_id is unchanged.

Commands
  python brain_server.py install D            create D:\\_BRAIN
  python brain_server.py install \\\\192.168.2.50\\h_hp
  python brain_server.py status               list brains + registry counts
  python brain_server.py serve [--port 28280] [--host 0.0.0.0]
"""
# (no `from __future__ import annotations`: FastAPI must resolve the request model defined
#  inside build_app(); Python 3.10+ handles the `X | None` hints natively.)

import argparse
import ctypes
import json
import os
import shutil
import socket
import sqlite3
import string
import subprocess
import sys
import threading
import uuid
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
KIT = Path(__file__).resolve().parent
BRAIN_DIRNAME = "_BRAIN"
DEFAULT_CONFIG = {
    "master_port": 28280,
    "host": "127.0.0.1",
    "fis_dir": r"D:\GitHub\David-OS\file-intelligence-system",
    "extra_roots": [],
    "skip_letters": ["A", "B"],
}


def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    p = KIT / "config.json"
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8-sig")))
    return cfg


CFG = load_config()


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


# --------------------------------------------------------------------------- identity
def norm_root(root: str) -> str:
    root = root.strip().strip('"')
    if len(root) == 1 and root.isalpha():
        root = root + ":"
    if len(root) == 2 and root[1] == ":":
        root = root + "\\"
    if not root.endswith("\\"):
        root += "\\"
    return root


def volume_info(root: str) -> dict:
    vol = ctypes.create_unicode_buffer(261)
    fs = ctypes.create_unicode_buffer(261)
    serial, maxlen, flags = ctypes.c_ulong(0), ctypes.c_ulong(0), ctypes.c_ulong(0)
    try:
        ok = ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(root), vol, 261, ctypes.byref(serial), ctypes.byref(maxlen),
            ctypes.byref(flags), fs, 261)
    except Exception:
        ok = 0
    if not ok:
        return {"label": "", "serial": "", "filesystem": ""}
    return {"label": vol.value, "serial": f"{serial.value:08X}", "filesystem": fs.value}


def disk_usage(root: str) -> dict:
    try:
        u = shutil.disk_usage(root)
        return {"total_gb": round(u.total / 1e9, 1), "free_gb": round(u.free / 1e9, 1)}
    except OSError:
        return {}


# ------------------------------------------------------------------------------ brains
def brain_dir(root: str) -> Path:
    return Path(norm_root(root)) / BRAIN_DIRNAME


def read_identity(root: str) -> dict | None:
    p = brain_dir(root) / "drive.json"
    if not p.exists():
        return None
    try:
        ident = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    ident["root"] = norm_root(root)          # current mount point wins over stored one
    return ident


def install(root: str) -> dict:
    root = norm_root(root)
    if not os.path.exists(root):
        raise SystemExit(f"root not found: {root}")
    b = brain_dir(root)
    for sub in ("registry", "logs"):
        (b / sub).mkdir(parents=True, exist_ok=True)
    vi = volume_info(root)
    old = read_identity(root) or {}
    base = vi["serial"] or uuid.uuid4().hex[:8].upper()
    if root.startswith("\\\\"):
        # shares on one NAS volume report the same serial; the share path is their stable name
        import hashlib
        base += "-" + hashlib.sha1(root.lower().encode()).hexdigest()[:4].upper()
    ident = {
        "brain_id": old.get("brain_id") or f"BRN-{base}",
        "root": root,
        "label": vi["label"],
        "volume_serial": vi["serial"],
        "filesystem": vi["filesystem"],
        "installed_at": old.get("installed_at") or now(),
        "kit_version": VERSION,
        "registry_db": "registry/fis.sqlite",
    }
    (b / "drive.json").write_text(json.dumps(ident, indent=2), encoding="utf-8")
    write_brain_note(ident)
    return ident


def discover() -> list[dict]:
    roots = [f"{L}:\\" for L in string.ascii_uppercase if L not in CFG.get("skip_letters", [])]
    roots += list(CFG.get("extra_roots", []))
    found, seen = [], set()
    for r in roots:
        try:
            ident = read_identity(r)
        except OSError:
            ident = None
        if ident and ident["brain_id"] not in seen:
            seen.add(ident["brain_id"])
            found.append(ident)
    return found


def get_brain(brain_id: str) -> dict:
    for b in discover():
        if b["brain_id"] == brain_id:
            return b
    raise KeyError(brain_id)


def db_path(ident: dict) -> Path:
    return brain_dir(ident["root"]) / ident.get("registry_db", "registry/fis.sqlite")


def ro(db: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=5)
    con.row_factory = sqlite3.Row
    return con


def registry_stats(ident: dict) -> dict:
    db = db_path(ident)
    if not db.exists():
        return {"registry": "not built yet - run a scan"}
    try:
        con = ro(db)
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        out: dict = {"registry_mb": round(db.stat().st_size / 1e6, 1)}
        if "file_memory" in tables:
            out["files"] = con.execute("SELECT COUNT(*) FROM file_memory").fetchone()[0]
            out["last_scanned"] = con.execute("SELECT MAX(last_scanned) FROM file_memory").fetchone()[0]
            out["doc_types"] = {r[0] or "UNCLASSIFIED": r[1] for r in con.execute(
                "SELECT doc_type, COUNT(*) FROM file_memory GROUP BY doc_type ORDER BY 2 DESC LIMIT 12")}
            out["canon_standing"] = {r[0] or "unset": r[1] for r in con.execute(
                "SELECT canon_standing, COUNT(*) FROM file_memory GROUP BY canon_standing ORDER BY 2 DESC LIMIT 8")}
        if "folder_memory" in tables:
            out["folders"] = con.execute("SELECT COUNT(*) FROM folder_memory").fetchone()[0]
        con.close()
        return out
    except sqlite3.Error as exc:
        return {"registry_error": str(exc)}


def write_brain_note(ident: dict) -> Path:
    st = registry_stats(ident)
    du = disk_usage(ident["root"])
    lines = [
        f"# Brain - {ident['root']}  ({ident.get('label') or 'no label'})",
        "",
        f"- brain_id: `{ident['brain_id']}`  (volume serial {ident.get('volume_serial') or 'n/a'})",
        f"- filesystem: {ident.get('filesystem', '')}   free: {du.get('free_gb', '?')} / {du.get('total_gb', '?')} GB",
        f"- installed: {ident.get('installed_at')}   kit {ident.get('kit_version')}",
        f"- registry: `{ident.get('registry_db')}`",
        f"- note regenerated: {now()}",
        "",
        "## Registry",
    ]
    if "files" in st:
        lines += [f"- files: {st['files']}   folders: {st.get('folders', '?')}   last scan: {st.get('last_scanned')}",
                  "- document types: " + ", ".join(f"{k} {v}" for k, v in st.get("doc_types", {}).items()),
                  "- canon standing: " + ", ".join(f"{k} {v}" for k, v in st.get("canon_standing", {}).items())]
    else:
        lines.append(f"- {next(iter(st.values()))}")
    lines += ["", "## How to use",
              "- Dashboard: http://127.0.0.1:28280/  (start with START_BRAIN_MASTER.bat in the kit)",
              "- This file is generated. Edit drive.json only through `brain_server.py install`.", ""]
    p = brain_dir(ident["root"]) / "BRAIN.md"
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


# -------------------------------------------------------------------------------- ports
def load_ports() -> dict:
    p = KIT / "PORTS.json"
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else {"services": []}


def port_open(host: str, port: int, timeout: float = 0.3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def services_status() -> list[dict]:
    out = []
    for s in load_ports().get("services", []):
        up = port_open(s.get("host", "127.0.0.1"), int(s["port"]))
        out.append({**s, "up": up})
    return out


# ------------------------------------------------------------------------------- search
SEARCH_COLS = ["name", "path", "keywords_text", "doc_type", "domain", "proposed_name"]


def search(q: str, brain_id: str | None = None, doc_type: str = "", limit: int = 50) -> list[dict]:
    q = (q or "").strip().lower()
    results = []
    for b in discover():
        if brain_id and b["brain_id"] != brain_id:
            continue
        db = db_path(b)
        if not db.exists():
            continue
        try:
            con = ro(db)
            cols = {r[1] for r in con.execute("PRAGMA table_info(file_memory)")}
            if not cols:
                continue
            use = [c for c in SEARCH_COLS if c in cols]
            where, params = [], []
            if q:
                where.append("(" + " OR ".join(f"lower(IFNULL({c},'')) LIKE ?" for c in use) + ")")
                params += [f"%{q}%"] * len(use)
            if doc_type and "doc_type" in cols:
                where.append("doc_type = ?")
                params.append(doc_type)
            pick = [c for c in ("path", "name", "doc_type", "domain", "canon_standing", "size_bytes",
                                "last_modified") if c in cols]
            sql = f"SELECT {', '.join(pick)} FROM file_memory"
            if where:
                sql += " WHERE " + " AND ".join(where)
            sql += f" LIMIT {int(limit)}"
            for r in con.execute(sql, params):
                results.append({"brain_id": b["brain_id"], "root": b["root"], **dict(r)})
            con.close()
        except sqlite3.Error as exc:
            results.append({"brain_id": b["brain_id"], "error": str(exc)})
    return results[:limit]


# --------------------------------------------------------------------------------- jobs
JOBS: dict[str, dict] = {}
JOBS_LOCK = threading.Lock()


def start_scan(brain_id: str, path: str | None = None, write: bool = False) -> dict:
    b = get_brain(brain_id)
    target = Path(path) if path else Path(b["root"])
    root = Path(b["root"]).resolve()
    try:
        target.resolve().relative_to(root)
    except ValueError:
        raise ValueError(f"{target} is not on drive {b['root']}")
    with JOBS_LOCK:
        if any(j["brain_id"] == brain_id and j["state"] == "running" for j in JOBS.values()):
            raise RuntimeError("a scan is already running on this drive")
    fis = Path(CFG["fis_dir"]) / "fis_folder_memory.py"
    if not fis.exists():
        raise FileNotFoundError(f"FIS scanner not found: {fis} (set fis_dir in config.json)")
    db = db_path(b)
    db.parent.mkdir(parents=True, exist_ok=True)
    job_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
    log = brain_dir(b["root"]) / "logs" / f"scan_{job_id}.log"
    cmd = [sys.executable, str(fis), str(target), "--tree", "--db", str(db)]
    if write:
        cmd.append("--write")
    job = {"job_id": job_id, "brain_id": brain_id, "target": str(target), "write": write,
           "state": "running", "started": now(), "finished": None, "returncode": None,
           "log": str(log), "cmd": cmd}
    with JOBS_LOCK:
        JOBS[job_id] = job

    def run():
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        with open(log, "w", encoding="utf-8", errors="replace") as fh:
            fh.write(f"# {now()}  {' '.join(cmd)}\n")
            fh.flush()
            proc = subprocess.run(cmd, cwd=str(fis.parent), stdout=fh, stderr=subprocess.STDOUT, env=env)
        with JOBS_LOCK:
            job.update(state="done" if proc.returncode == 0 else "failed",
                       returncode=proc.returncode, finished=now())
        try:
            write_brain_note(get_brain(brain_id))
        except Exception:
            pass

    threading.Thread(target=run, daemon=True).start()
    return job


def tail(path: str, n: int = 40) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return "".join(fh.readlines()[-n:])
    except OSError:
        return ""


# ---------------------------------------------------------------------------------- app
def build_app():
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel

    app = FastAPI(title="Drive Brain / Master API", version=VERSION)

    class ScanRequest(BaseModel):
        brain_id: str
        path: str | None = None
        write: bool = False

    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "Master API / Drive Brain", "version": VERSION, "time": now()}

    @app.get("/api/services")
    def services():
        return services_status()

    @app.get("/api/brains")
    def brains():
        return [{**b, **disk_usage(b["root"]), "registry": registry_stats(b)} for b in discover()]

    @app.post("/api/brains/{brain_id}/note")
    def refresh_note(brain_id: str):
        try:
            return {"note": str(write_brain_note(get_brain(brain_id)))}
        except KeyError:
            raise HTTPException(404, "unknown brain")

    @app.get("/api/search")
    def api_search(q: str = "", brain_id: str | None = None, doc_type: str = "", limit: int = 50):
        return search(q, brain_id, doc_type, min(limit, 500))

    @app.post("/api/scan")
    def api_scan(req: ScanRequest):
        try:
            job = start_scan(req.brain_id, req.path, req.write)
        except KeyError:
            raise HTTPException(404, "unknown brain")
        except (ValueError, RuntimeError, FileNotFoundError) as exc:
            raise HTTPException(400, str(exc))
        return {k: v for k, v in job.items() if k != "cmd"}

    @app.get("/api/jobs")
    def jobs():
        with JOBS_LOCK:
            return [{**{k: v for k, v in j.items() if k != "cmd"}, "tail": tail(j["log"], 8)}
                    for j in sorted(JOBS.values(), key=lambda j: j["started"], reverse=True)]

    @app.get("/", response_class=HTMLResponse)
    def dashboard():
        return DASHBOARD_HTML

    return app


DASHBOARD_HTML = r"""<!doctype html><html><head><meta charset="utf-8"><title>Drive Brain</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#111418;--panel:#1a1f26;--ink:#e6e6e6;--dim:#8b95a1;--ok:#3fb950;--off:#6e7681;--warn:#d29922;--acc:#58a6ff}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 Segoe UI,system-ui,sans-serif}
header{padding:14px 20px;border-bottom:1px solid #2a313a;display:flex;gap:12px;align-items:baseline}
h1{font-size:18px;margin:0} h2{font-size:14px;color:var(--dim);text-transform:uppercase;letter-spacing:.06em;margin:0 0 8px}
main{display:grid;grid-template-columns:minmax(300px,1fr) 2fr;gap:16px;padding:16px 20px}
section{background:var(--panel);border:1px solid #2a313a;border-radius:8px;padding:12px 14px;overflow-x:auto}
table{border-collapse:collapse;width:100%} td,th{padding:4px 6px;text-align:left;border-bottom:1px solid #232a32;vertical-align:top}
th{color:var(--dim);font-weight:600} .dot{display:inline-block;width:9px;height:9px;border-radius:50%}
.up{background:var(--ok)} .down{background:var(--off)} .muted{color:var(--dim)} .wide{grid-column:1/-1}
button,input,select{background:#0d1117;color:var(--ink);border:1px solid #30363d;border-radius:6px;padding:5px 9px;font:inherit}
button{cursor:pointer} button:hover{border-color:var(--acc)} pre{white-space:pre-wrap;color:var(--dim);margin:4px 0 0;font-size:12px}
@media(max-width:860px){main{grid-template-columns:1fr}}
</style></head><body>
<header><h1>Drive Brain</h1><span class="muted">Master API :28280 &middot; read-only unless you tick "write notes"</span></header>
<main>
<section><h2>Services</h2><table id="svc"></table></section>
<section><h2>Drives</h2><table id="brains"></table>
<p class="muted"><label><input type="checkbox" id="write"> write .fisnote files on scan (old notes are backed up first)</label></p></section>
<section class="wide"><h2>Search every drive</h2>
<input id="q" placeholder="name, path, keyword, doc type..." size="40"> <button onclick="doSearch()">Search</button>
<table id="res"></table></section>
<section class="wide"><h2>Jobs</h2><div id="jobs" class="muted">none yet</div></section>
</main>
<script>
const j=(u,o)=>fetch(u,o).then(r=>r.json());
const esc=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function loadSvc(){const s=await j('/api/services');
 document.getElementById('svc').innerHTML='<tr><th></th><th>port</th><th>service</th><th>status</th></tr>'+
 s.map(x=>`<tr><td><span class="dot ${x.up?'up':'down'}"></span></td><td>${x.port}</td><td>${esc(x.name)}</td><td class="muted">${esc(x.status)}</td></tr>`).join('');}
async function loadBrains(){const b=await j('/api/brains');
 document.getElementById('brains').innerHTML='<tr><th>drive</th><th>id</th><th>files</th><th>last scan</th><th></th></tr>'+
 (b.length?b.map(x=>`<tr><td>${esc(x.root)}<div class="muted">${esc(x.label)} &middot; ${x.free_gb??'?'} GB free</div></td><td class="muted">${esc(x.brain_id)}</td>
 <td>${x.registry.files??'-'}</td><td class="muted">${esc(x.registry.last_scanned??(x.registry.registry||''))}</td>
 <td><button onclick="scan('${x.brain_id}')">scan</button></td></tr>`).join(''):'<tr><td class="muted" colspan=5>No drives have a _BRAIN yet. Run INSTALL_BRAIN_ON_DRIVE.bat.</td></tr>');}
async function scan(id){const write=document.getElementById('write').checked;
 if(write&&!confirm('Write .fisnote files on this drive?'))return;
 const r=await j('/api/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({brain_id:id,write})});
 if(r.detail)alert(r.detail);loadJobs();}
async function loadJobs(){const r=await j('/api/jobs');if(!r.length)return;
 document.getElementById('jobs').innerHTML=r.map(x=>`<div><b>${esc(x.state)}</b> ${esc(x.brain_id)} ${esc(x.target)} ${x.write?'(writing notes)':'(registry only)'} <span class="muted">${esc(x.started)}</span><pre>${esc(x.tail)}</pre></div>`).join('');}
async function doSearch(){const q=document.getElementById('q').value;const r=await j('/api/search?q='+encodeURIComponent(q));
 document.getElementById('res').innerHTML='<tr><th>drive</th><th>name</th><th>type</th><th>canon</th><th>path</th></tr>'+
 r.map(x=>`<tr><td class="muted">${esc(x.root)}</td><td>${esc(x.name)}</td><td>${esc(x.doc_type)}</td><td>${esc(x.canon_standing)}</td><td class="muted">${esc(x.path)}</td></tr>`).join('');}
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter')doSearch()});
loadSvc();loadBrains();loadJobs();setInterval(loadJobs,4000);setInterval(loadSvc,15000);
</script></body></html>"""


# ---------------------------------------------------------------------------------- cli
def main() -> int:
    ap = argparse.ArgumentParser(description="Drive Brain / Master API")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("install", help="create <root>\\_BRAIN")
    i.add_argument("root", help="drive letter (D) or UNC root (\\\\server\\share)")
    sub.add_parser("status", help="list brains and registry counts")
    s = sub.add_parser("serve", help="run the Master API")
    s.add_argument("--port", type=int, default=CFG["master_port"])
    s.add_argument("--host", default=CFG["host"])
    args = ap.parse_args()

    if args.cmd == "install":
        print(json.dumps(install(args.root), indent=2))
    elif args.cmd == "status":
        for b in discover():
            print(f"{b['root']:<24} {b['brain_id']:<16} {json.dumps(registry_stats(b))}")
        if not discover():
            print("no _BRAIN folders found")
    elif args.cmd == "serve":
        import uvicorn
        print(f"Drive Brain on http://{args.host}:{args.port}/")
        uvicorn.run(build_app(), host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
