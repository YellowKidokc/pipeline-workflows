"""PICKER - pick a folder, check off files, choose a preset, run DeepSeek.
Answers are saved NEXT TO each source file:  <file>.<preset>.md
Presets = folders in ..\BACKSIDE\calls\<name>\ with prompt.txt (+ optional example.txt, settings.txt).
Run:  py -3.12 picker.py   then open http://127.0.0.1:8790
Standard library only.
"""
import json, os, threading, time, urllib.request, pathlib, concurrent.futures as cf
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = pathlib.Path(__file__).resolve().parent
CALLS = HERE.parent / "BACKSIDE" / "calls"
PORT = 8790
EXTS = {".md", ".txt", ".json"}
JOB = {"running": False, "done": 0, "total": 0, "failed": 0, "log": [], "tokens": 0}


def key():
    k = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("DEEPSEEKAPI")
    if not k and os.name == "nt":
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as h:
            for n in ("DEEPSEEK_API_KEY", "DEEPSEEKAPI"):
                try:
                    return winreg.QueryValueEx(h, n)[0]
                except OSError:
                    pass
    return k


def settings(p):
    s = {"MODEL": "deepseek-chat", "MAX_TOKENS": "4000", "TEMPERATURE": "0.2", "WORKERS": "20"}
    f = p / "settings.txt"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                a, b = line.split("=", 1)
                s[a.strip().upper()] = b.strip()
    return s


def preset_names():
    return [d.name for d in CALLS.glob("*") if (d / "prompt.txt").exists()]


def presets():
    out = []
    for name in sorted(preset_names()):
        d = CALLS / name
        ex = d / "example.txt"
        out.append({"name": name,
                    "prompt": (d / "prompt.txt").read_text(encoding="utf-8"),
                    "example": ex.read_text(encoding="utf-8") if ex.exists() else ""})
    return out


def is_answer(p, names):
    n = p.name
    return n.endswith(".objections.json") or any(n.endswith(f".{x}.md") for x in names)


def ask(prompt, text, s):
    body = json.dumps({"model": s["MODEL"], "temperature": float(s["TEMPERATURE"]),
                       "max_tokens": int(s["MAX_TOKENS"]),
                       "messages": [{"role": "system", "content": prompt},
                                    {"role": "user", "content": text}]}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", body,
                                 {"Content-Type": "application/json", "Authorization": "Bearer " + key()})
    r = json.load(urllib.request.urlopen(req, timeout=600))
    return r["choices"][0]["message"]["content"], r.get("usage", {}).get("total_tokens", 0)


def run_job(files, preset, overwrite):
    d = CALLS / preset
    s = settings(d)
    prompt = (d / "prompt.txt").read_text(encoding="utf-8")
    ex = d / "example.txt"
    if ex.exists() and ex.read_text(encoding="utf-8").strip():
        prompt += "\n\nHere is an example of exactly the output wanted:\n" + ex.read_text(encoding="utf-8")
    JOB.update(running=True, done=0, total=len(files), failed=0, log=[], tokens=0)

    def one(f):
        src = pathlib.Path(f)
        out = src.with_name(src.name + f".{preset}.md")
        if out.exists() and not overwrite:
            return f"skip  {src.name} (already answered)", 0
        text = f"FILE: {src.name}\n\n" + src.read_text(encoding="utf-8", errors="replace")
        ans, tok = ask(prompt, text, s)
        stamp = time.strftime("%Y-%m-%d %H:%M")
        out.write_text(f"<!-- preset: {preset} | source: {src.name} | {stamp} -->\n{ans}\n", encoding="utf-8")
        return f"ok    {src.name}", tok

    with cf.ThreadPoolExecutor(int(s["WORKERS"])) as pool:
        futs = {pool.submit(one, f): f for f in files}
        for fu in cf.as_completed(futs):
            try:
                msg, tok = fu.result()
                JOB["tokens"] += tok
            except Exception as e:
                msg = f"FAIL  {pathlib.Path(futs[fu]).name}: {e}"
                JOB["failed"] += 1
            JOB["done"] += 1
            JOB["log"].append(msg)
    JOB["running"] = False


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, obj, ctype="application/json"):
        data = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            return self.send((HERE / "picker.html").read_bytes(), "text/html; charset=utf-8")
        if u.path == "/api/presets":
            return self.send(presets())
        if u.path == "/api/files":
            root = pathlib.Path(q.get("folder", [""])[0].strip().strip('"'))
            if not root.is_dir():
                return self.send({"error": "folder not found"})
            names = preset_names()
            files = []
            for p in root.rglob("*"):
                if p.is_file() and p.suffix.lower() in EXTS and not p.name.startswith(".") and not is_answer(p, names):
                    done = [x for x in names if p.with_name(p.name + f".{x}.md").exists()]
                    files.append({"path": str(p), "rel": str(p.relative_to(root)),
                                  "kb": round(p.stat().st_size / 1024, 1), "done": done})
                    if len(files) >= 20000:
                        break
            return self.send({"files": files})
        if u.path == "/api/status":
            return self.send({**JOB, "log": JOB["log"][-40:]})
        if u.path == "/api/preview":
            p = pathlib.Path(q.get("path", [""])[0])
            return self.send({"text": p.read_text(encoding="utf-8", errors="replace")[:8000] if p.exists() else ""})
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/api/run":
            if JOB["running"]:
                return self.send({"error": "a job is already running"})
            if not key():
                return self.send({"error": "no DeepSeek key found (DEEPSEEK_API_KEY or DEEPSEEKAPI)"})
            threading.Thread(target=run_job, args=(body["files"], body["preset"], body.get("overwrite", False)),
                             daemon=True).start()
            return self.send({"started": len(body["files"])})
        if self.path == "/api/preset":
            name = "".join(c for c in body.get("name", "") if c.isalnum() or c in "_-").strip()
            if not name:
                return self.send({"error": "name needed"})
            d = CALLS / name
            d.mkdir(parents=True, exist_ok=True)
            (d / "prompt.txt").write_text(body.get("prompt", ""), encoding="utf-8")
            (d / "example.txt").write_text(body.get("example", ""), encoding="utf-8")
            if not (d / "settings.txt").exists():
                (d / "settings.txt").write_text("MODEL=deepseek-chat\nMAX_TOKENS=4000\nTEMPERATURE=0.2\nWORKERS=20\n",
                                                encoding="utf-8")
            return self.send({"saved": name})
        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    print(f"PICKER running: http://127.0.0.1:{PORT}   (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
