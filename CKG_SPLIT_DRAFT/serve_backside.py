"""Local server for backside.html: serves this folder and saves edits back into it.

    python serve_backside.py [port]        (default 8771, 127.0.0.1 only)

GET  /data  -> ckg.json with each call's prompt.md / output.md text filled in (always fresh from disk)
POST /save  -> {calls:[...], model, ...}: writes ckg.json and every changed prompt.md / output.md.
Every file it replaces is copied first to _older/<timestamp>/ ; nothing is deleted.
"""
import json
import os
import re
import shutil
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import runner  # noqa: E402
import intake  # noqa: E402
import subprocess  # noqa: E402

JOB = {"job": None}
OSV3 = Path(r"D:\GitHub\David-OSv3")
CLASSIFY = {  # the only programs /launch will start
    "PROFILE": OSV3 / "01_PROFILE" / "PROFILE.bat",
    "REVIEW": OSV3 / "03_CLASSIFY" / "REVIEW.bat",
    "VALIDATE": OSV3 / "03_CLASSIFY" / "VALIDATE.bat",
    "REPORT": OSV3 / "03_CLASSIFY" / "REPORT.bat",
    "ADAPT": OSV3 / "04_ADAPT" / "ADAPT.bat",
}
CALLS = (ROOT / "calls").resolve()


def load():
    m = json.loads((ROOT / "ckg.json").read_text(encoding="utf-8"))
    for c in m["calls"]:
        f = ROOT / c["folder"]
        for key, name in (("prompt", "prompt.md"), ("template", "output.md")):
            p = f / name
            c[key] = p.read_text(encoding="utf-8") if p.exists() else ""
    return m


def call_folder(rel):
    f = (ROOT / rel).resolve()
    if f.parent != CALLS or not f.is_dir():
        raise ValueError(f"not a call folder: {rel}")
    return f


def save(incoming):
    current = json.loads((ROOT / "ckg.json").read_text(encoding="utf-8"))
    known = {c["folder"]: c for c in current["calls"]}
    backup = ROOT / "_older" / time.strftime("%Y-%m-%d_%H%M%S")
    written = []

    def write(path, text):
        if path.exists():
            if path.read_text(encoding="utf-8") == text:
                return
            dest = backup / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
        elif not text:
            return
        path.write_text(text, encoding="utf-8", newline="")
        written.append(str(path.relative_to(ROOT)))

    calls = []
    for c in incoming["calls"]:
        if c.get("folder") not in known:
            raise ValueError(f"unknown call folder: {c.get('folder')}")
        f = call_folder(c["folder"])
        if "prompt" in c:
            write(f / "prompt.md", c["prompt"])
        if "template" in c:
            write(f / "output.md", c["template"])
        calls.append({k: v for k, v in c.items() if k not in ("prompt", "template")})
    if len(calls) != len(current["calls"]):
        raise ValueError("call count changed; adding or removing calls is not supported here")
    manifest = {**current, **{k: v for k, v in incoming.items() if k != "calls"}, "calls": calls}
    write(ROOT / "ckg.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return {"written": written, "backup": str(backup.relative_to(ROOT)) if backup.exists() else None}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/data":
            return self._json(200, load())
        if self.path == "/variants":
            return self._json(200, {"variants": list(runner.variants()),
                                    "has_key": bool(os.environ.get("DEEPSEEK_API_KEY"))})
        if self.path == "/progress":
            return self._json(200, JOB["job"].status() if JOB["job"] else {"items": []})
        if self.path == "/run":
            self.path = "/run.html"
        if self.path == "/intake/registry":
            return self._json(200, {"items": intake.registry()[-200:][::-1], "topics": intake.topics(),
                                    "counts": intake.counts(), "classify": {k: v.exists() for k, v in CLASSIFY.items()}})
        if self.path.startswith("/intake/sidecar/"):
            uid = self.path.rsplit("/", 1)[-1]
            if not re.fullmatch(r"[0-9a-f-]{36}", uid):
                return self._json(400, {"error": "bad uuid"})
            return self._json(200, {"text": intake.sidecar_text(uid)})
        if self.path == "/intake":
            self.path = "/intake.html"
        if self.path in ("/verify", "/research", "/ruling", "/rebuild", "/publish", "/feedback", "/settings"):
            self.path = "/soon.html"
        if self.path in ("/", ""):
            self.path = "/home.html"
        return super().do_GET()

    def do_POST(self):
        if self.path not in ("/save", "/run", "/stop", "/intake/scan", "/intake/commit", "/intake/topic", "/launch"):
            return self._json(404, {"error": "not found"})
        if self.headers.get("Origin") not in (None, "null", f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"):
            return self._json(403, {"error": "origin not allowed"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            if self.path == "/intake/scan":
                return self._json(200, intake.scan(body["folder"]))
            if self.path == "/intake/topic":
                return self._json(200, {"topics": intake.add_topic(body.get("code", ""), body.get("name", ""), body.get("parent") or None)})
            if self.path == "/intake/commit":
                r = intake.commit(body["items"], body.get("defaults", {}))
                print(f"intake: {len(r['done'])} in, {len(r['located'])} new location(s), {len(r['skipped'])} skipped", flush=True)
                return self._json(200, r)
            if self.path == "/launch":
                bat = CLASSIFY.get(body.get("name"))
                if not bat or not bat.exists():
                    return self._json(404, {"error": f"not found: {body.get('name')}"})
                args = ["cmd", "/c", "start", "", str(bat)] + ([body["arg"]] if body.get("arg") else [])
                subprocess.Popen(args, cwd=str(bat.parent))
                return self._json(200, {"ok": True})
            if self.path == "/stop":
                if JOB["job"]:
                    JOB["job"].stopped = True
                return self._json(200, {"ok": True})
            if self.path == "/run":
                cur = JOB["job"]
                if cur and not cur.status()["finished"]:
                    return self._json(409, {"error": "a run is already going"})
                job = runner.Job(body["folder"], body["variants"], body.get("mode", "per_note"),
                                 body.get("workers", 4), body.get("dry_run", True))
                JOB["job"] = job
                job.start()
                print(f"run: {len(job.items)} item(s), dry_run={job.dry}, workers={job.workers}", flush=True)
                return self._json(200, {"ok": True, "total": len(job.items)})
            result = save(body)
            print("saved:", ", ".join(result["written"]) or "(no changes)", flush=True)
            return self._json(200, result)
        except Exception as e:  # report to the page, keep serving
            return self._json(400, {"error": str(e)})


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
if __name__ == "__main__":
    print(f"CKG backside: http://localhost:{PORT}/  (folder {ROOT})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
