"""The workspace page: a home page for every API group, served on this machine only.

    ONE_MENU.bat workspace     starts this and opens the page (or API PIPELINE\\OPEN WORKSPACE.bat)
    python workspace.py        [--port 8765] [--no-open]

The page (_system/workspace/index.html) never runs anything itself. It asks this server, and the server uses what
the buttons use:

  Run             button.py plan <station> <plan.json>: the same code as 2 RUN ON FOLDER, with the answers (notes,
                  output folder, how many at once, extra questions, layers) picked on the page. A sequence runs its
                  stations one after another on the same notes. Every call goes through one relay (engine/gateway.py),
                  so concurrency is global across everything running from the page.
  Piece by piece  one call at a time (engine/llm.py): a station's template broken into pieces (BACKSIDE/pieces.json,
                  else the S/A sections of BACKSIDE/templates/*.md, else PROMPT.md). Each answer is saved the moment
                  it is accepted, to <output>/PIECES/<note>/.

Only 127.0.0.1 is served, and every /api request must carry the token printed into the page, so another web page
cannot drive it. Keys stay in environment variables; nothing here reads or logs them.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SYSTEM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SYSTEM))
from engine import llm, pick                                         # noqa: E402
from engine.gateway import Gateway                                   # noqa: E402
from engine.paths import load_paths, expand                          # noqa: E402
from engine.text import strip_front_matter                           # noqa: E402

MAIN = SYSTEM.parent
PAGE = SYSTEM / "workspace" / "index.html"
BUTTON = SYSTEM / "engine" / "button.py"
TOKEN = secrets.token_urlsafe(24)
TEXT_EXT = {".md", ".txt", ".json", ".jsonl", ".csv", ".html", ".htm", ".tex", ".lean", ".log", ".tsv"}
NOT_GROUPS = {"_system", "_ACTIONS", "ZZZ Archive"}
ACRONYMS = {"CKG", "API", "YT", "AI", "HTML", "OPENAI"}
EDITABLE = {"PROMPT.md", "FOCUS.md", "pieces.json"}                 # the only files the page may write in a BACKSIDE
OURS = re.compile(r"<!-- (analysis|analysis-detail|scorecard):start -->.*?<!-- \1:end -->\n?", re.S)


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


# ------------------------------------------------------------------ catalog: groups, stations, layers

def station_info(front: Path) -> dict:
    """One front folder: its station.json plus what the page needs (folders, prompt files, layers)."""
    back = front / "BACKSIDE"
    st = read_json(back / "station.json", {}) or {}
    layers = []
    outbox = front / "OUTBOX"
    if outbox.is_dir():
        for d in sorted(outbox.iterdir()):
            if d.is_dir() and (d / "BACKSIDE" / "station.json").is_file():
                layers.append(station_info(d))
    files = [f.name for f in sorted(back.iterdir()) if f.is_file() and f.suffix.lower() in (".md", ".txt", ".json")] \
        if back.is_dir() else []
    return {
        "folder": front.name,
        "path": str(front),
        "rel": os.path.relpath(front, MAIN).replace(os.sep, "/"),
        "number": st.get("number", ""),
        "label": st.get("label", front.name),
        "name": st.get("name", front.name),
        "kind": st.get("kind") or "native",
        "items": st.get("items"),
        "description": st.get("description", ""),
        "uses_api": bool(st.get("uses_api")),
        "on_note": st.get("on_note", True),
        "chain": st.get("chain") or [],
        "options": st.get("options") or [],
        "inbox": str(front / "INBOX"),
        "outbox": str(outbox),
        "files": files,
        "has_pieces": (back / "pieces.json").is_file() or bool(template_files(back)),
        "needs_topic": st.get("number") in ("48", "49"),
        "own_inbox": st.get("items") == "lean",
        "layers": layers,
    }


def is_station(d: Path) -> bool:
    return (d / "BACKSIDE" / "station.json").is_file()


def catalog() -> dict:
    """Groups as David sees them in API\\: a group folder holds stations; a station at the top is its own group."""
    groups = []
    for d in sorted(MAIN.iterdir()):
        if not d.is_dir() or d.name in NOT_GROUPS or d.name.startswith((".", "_")):
            continue
        if is_station(d):
            groups.append({"id": d.name, "title": pretty(d.name), "path": str(d), "stations": [station_info(d)]})
            continue
        stations = [station_info(s) for s in sorted(d.iterdir()) if s.is_dir() and is_station(s)]
        if stations:
            groups.append({"id": d.name, "title": pretty(d.name), "path": str(d), "stations": stations})
    settings = llm.settings()
    routines = read_json(SYSTEM / "config" / "routines.json", {}) or {}
    return {
        "main": str(MAIN),
        "groups": groups,
        "settings": {k: settings.get(k) for k in ("max_concurrent_calls", "turbo_presets", "default_provider", "models",
                                                    "allowed_providers", "output_token_cap",
                                                    "estimated_tokens_per_item", "estimated_seconds_per_call")},
        "routines": routines,
        "roots": roots(),
        "keys": {p: bool(os.environ.get(spec.get("key", ""))) for p, spec in llm.PROVIDERS.items()
                 if spec.get("key")},
    }


def pretty(folder: str) -> str:
    words = re.sub(r"^\d+_", "", folder).split("_")
    return " ".join(w if w in ACRONYMS else w.title() for w in words)


def roots() -> list[dict]:
    """Starting places for the folder browser: API itself and every folder named in paths.json that exists."""
    out = [{"name": "API", "path": str(MAIN)}]
    try:
        for key, raw in load_paths().items():
            if raw and not key.startswith("_"):
                p = expand(raw)
                if p.is_dir():
                    out.append({"name": key, "path": str(p)})
    except Exception:                                   # paths.json missing or broken: the API folder still works
        pass
    if sys.platform == "win32":
        import string
        out += [{"name": f"{c}:", "path": f"{c}:\\"} for c in string.ascii_uppercase if Path(f"{c}:\\").exists()]
    return out


def known_front(path: str) -> Path:
    """A front folder the catalog knows (so the page can only run or edit real stations)."""
    p = Path(path).resolve()
    if not is_station(p):
        raise ValueError(f"not a station folder: {p}")
    p.relative_to(MAIN.resolve())                       # ValueError when outside API
    return p


# ------------------------------------------------------------------ folders and notes

def browse(path: str) -> dict:
    p = Path(path).expanduser() if path else MAIN
    if p.is_file():
        p = p.parent
    if not p.is_dir():
        raise ValueError(f"not a folder: {p}")
    dirs = []
    try:
        for d in sorted(p.iterdir(), key=lambda x: x.name.lower()):
            if d.is_dir() and not d.name.startswith((".", "__")):
                dirs.append({"name": d.name, "path": str(d)})
    except PermissionError:
        pass
    notes = len(pick.notes(p)) if p.is_dir() else 0
    return {"path": str(p), "parent": str(p.parent) if p.parent != p else "", "dirs": dirs, "notes": notes}


def inbox_units(inbox: Path) -> list[Path]:
    """The same folders button.units() runs: loose notes, lanes, channel folders (not Clean MD / Prompts...)."""
    from engine.button import units
    return units(inbox) if inbox.is_dir() else []


def list_notes(path: str) -> dict:
    """The notes 2 RUN ON FOLDER would see, newest first, with date, words, ticks (_PICK.md) and priority."""
    p = Path(path).expanduser()
    if p.is_file():
        sources = [p]
    elif p.name == "INBOX" and is_station(p.parent):
        sources = inbox_units(p)
    elif p.is_dir():
        sources = [p]
    else:
        raise ValueError(f"not found: {p}")
    rows, seen = [], set()
    for src in sources:
        found = [src] if src.is_file() else pick.by_date(pick.notes(src))
        listing = pick.read_pick(src) if src.is_dir() else None
        for n in found:
            if n in seen:
                continue
            seen.add(n)
            date, title, words = pick._describe(n)
            rows.append({"path": str(n), "name": n.name, "date": date, "title": title, "words": words,
                         "folder": os.path.relpath(n.parent, p) if p.is_dir() else "",
                         "priority": "00_PRIORITY" in n.parts,
                         "ticked": bool(listing and (listing[1] or n.stem in listing[0]))})
    rows.sort(key=lambda r: not r["priority"])          # 00_PRIORITY first, as the buttons run it
    return {"path": str(p), "notes": rows, "has_pick": any(src.is_dir() and (src / pick.PICK).is_file() for src in sources),
            "pick_free": pick.PICK_FREE}


def read_file(path: str) -> dict:
    p = Path(path)
    if p.suffix.lower() not in TEXT_EXT or not p.is_file():
        raise ValueError(f"not a text file: {p}")
    text = p.read_text(encoding="utf-8", errors="replace")
    return {"path": str(p), "text": text[:2_000_000], "cut": len(text) > 2_000_000,
            "modified": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")}


def archive(path: Path, folder: Path) -> None:
    """A file about to be replaced moves to <folder>/_older/<date>/ (never deleted)."""
    if not path.is_file():
        return
    dest = folder / "_older" / datetime.now().strftime("%Y-%m-%d")
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / path.name
    if target.exists():
        target = dest / f"{path.stem} · {datetime.now():%H%M%S}{path.suffix}"
    shutil.move(str(path), str(target))


def save_backside(front: str, name: str, text: str) -> dict:
    """PROMPT.md, FOCUS.md or pieces.json of a station; the version it replaces goes to BACKSIDE/_older/."""
    back = known_front(front) / "BACKSIDE"
    if name not in EDITABLE:
        raise ValueError(f"the page may only edit {sorted(EDITABLE)}")
    if name.endswith(".json"):
        json.loads(text)                                # refuse broken JSON rather than save it
    target = back / name
    archive(target, back)
    target.write_text(text, encoding="utf-8")
    return {"saved": str(target)}


def results(front: str) -> dict:
    """What a station has written: its OUTBOX (and one folder down), newest first, without _older."""
    box = known_front(front) / "OUTBOX"
    rows = []
    if box.is_dir():
        for f in box.rglob("*"):
            rel = f.relative_to(box).parts
            if not f.is_file() or f.suffix.lower() not in TEXT_EXT or any(x == "_older" or x == "BACKSIDE" for x in rel):
                continue
            if any(is_station(box.joinpath(*rel[:i + 1])) for i in range(len(rel) - 1)):
                continue                                # a layer's files show on the layer's own page
            rows.append({"path": str(f), "rel": "/".join(rel), "size": f.stat().st_size, "mtime": f.stat().st_mtime})
    rows.sort(key=lambda r: -r["mtime"])
    for r in rows:
        r["modified"] = datetime.fromtimestamp(r.pop("mtime")).strftime("%Y-%m-%d %H:%M")
    return {"outbox": str(box), "files": rows[:500], "total": len(rows)}


# ------------------------------------------------------------------ pieces (prompt by prompt)

SECTION = re.compile(r"^## +((?:S|A)\d+)\s*[·:-]\s*(.+?)\s*$", re.M)


def template_files(back: Path) -> list[Path]:
    t = back / "templates"
    return sorted(f for f in t.glob("*.md") if SECTION.search(f.read_text(encoding="utf-8", errors="replace"))) \
        if t.is_dir() else []


def pieces(front: str) -> dict:
    """The calls a station breaks into: pieces.json if David saved one, else the S/A sections of its template (a draft
    breakdown, not final calls), else one piece from PROMPT.md."""
    back = known_front(front) / "BACKSIDE"
    saved = read_json(back / "pieces.json")
    if saved:
        return {"source": "pieces.json", "pieces": saved.get("pieces", saved)}
    for tpl in template_files(back):
        text = tpl.read_text(encoding="utf-8", errors="replace")
        marks = list(SECTION.finditer(text))
        out = []
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            nxt = re.search(r"^## ", text[m.end():end], re.M)          # stop at the next ## that is not an S/A section
            body = text[m.start(): m.end() + nxt.start() if nxt else end].strip()
            out.append({"id": m.group(1), "title": m.group(2),
                        "prompt": (f"Fill only section {m.group(1)} · {m.group(2)} of the {tpl.stem.replace('_', ' ')} "
                                   "for the source below. Follow the output template exactly: keep every heading, "
                                   "table and field, and write 'Not applicable' rather than dropping one. Quote the "
                                   "source where you rely on it."),
                        "output": body})
        if out:
            return {"source": f"templates/{tpl.name} (draft breakdown, not saved yet)", "pieces": out}
    prompt = (back / "PROMPT.md").read_text(encoding="utf-8") if (back / "PROMPT.md").is_file() else ""
    return {"source": "PROMPT.md (one piece)", "pieces": [{"id": "P1", "title": "Whole prompt", "prompt": prompt, "output": ""}]}


def source_text(note: Path) -> str:
    """The source only: our analysis and scorecard blocks never go back to a model."""
    return OURS.sub("", note.read_text(encoding="utf-8", errors="replace"))


def piece_messages(piece: dict, note: Path, focus: list[str]) -> list[dict]:
    body = piece.get("prompt", "").strip()
    if piece.get("output", "").strip():
        body += "\n\n## Output template\n\n" + piece["output"].strip()
    if focus:
        body += "\n\n## Also look for\n\n" + "\n".join(f"- {q}" for q in focus[:5])
    body += f"\n\n## Source: {note.stem}\n\n" + strip_front_matter(source_text(note))
    return [{"role": "user", "content": body}]


def call_piece(req: dict) -> dict:
    """One piece on one note, now. Truncated replies come back as errors (llm.py), never as answers."""
    note = Path(req["note"])
    if not note.is_file():
        raise ValueError(f"note not found: {note}")
    front = known_front(req["front"])
    provider = req.get("provider") or llm.settings().get("default_provider", "deepseek")
    model = req.get("model") or llm.settings().get("models", {}).get(provider, "")
    messages = piece_messages(req["piece"], note, req.get("focus") or [])
    task = f"piece:{req['piece'].get('id', '')}"
    result = llm.call(messages, provider=provider, model=model, max_tokens=llm.settings().get("output_token_cap"),
                      task=task, station=front.name)
    row = llm.receipt(result, station=front.name, note=note.name, piece=req["piece"].get("id"), source="workspace")
    log = SYSTEM / "LOGS" / f"workspace-pieces-{datetime.now():%Y-%m-%d}.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return {"text": result.text, "error": result.error, "provider": result.provider, "model": result.model,
            "prompt_tokens": result.prompt_tokens, "completion_tokens": result.completion_tokens,
            "seconds": round(result.elapsed_seconds, 1), "finish_reason": result.extra.get("finish_reason")}


def piece_folder(req: dict) -> tuple[Path, Path]:
    front = known_front(req["front"])
    out = Path(req["out"]) if req.get("out") else front / "OUTBOX"
    note = Path(req["note"])
    return out / "PIECES" / note.stem, out


def safe(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()[:80]


def save_piece(req: dict) -> dict:
    """An accepted answer is saved now, before the next piece (the version it replaces goes to _older/)."""
    folder, out = piece_folder(req)
    folder.mkdir(parents=True, exist_ok=True)
    piece = req["piece"]
    dest = folder / f"{int(req.get('position', 0)):02d} {safe(piece.get('id', 'P'))} · {safe(piece.get('title', ''))}.md"
    for old in folder.glob(f"* {safe(piece.get('id', 'P'))} · *.md"):   # the same piece at an earlier position
        archive(old, out)
    head = (f"---\nnote: \"[[{Path(req['note']).stem}]]\"\npiece: {json.dumps(piece.get('id'))}\n"
            f"title: {json.dumps(piece.get('title', ''))}\nsaved: {datetime.now():%Y-%m-%d %H:%M}\n---\n\n")
    dest.write_text(head + req["text"].strip() + "\n", encoding="utf-8")
    return {"saved": str(dest)}


def saved_pieces(req: dict) -> dict:
    folder, _ = piece_folder(req)
    files = sorted(folder.glob("*.md")) if folder.is_dir() else []
    return {"folder": str(folder), "files": [{"name": f.name, "path": str(f)} for f in files]}


def assemble_pieces(req: dict) -> dict:
    """The saved pieces of one note, in position order, as <output>/<note> · PIECES.md."""
    folder, out = piece_folder(req)
    files = sorted(folder.glob("*.md")) if folder.is_dir() else []
    if not files:
        raise ValueError("no saved pieces for this note yet")
    stem = Path(req["note"]).stem
    parts = [strip_front_matter(f.read_text(encoding="utf-8")).strip() for f in files]
    dest = out / f"{stem} · PIECES.md"
    archive(dest, out)
    dest.write_text(f"---\nnote: \"[[{stem}]]\"\npieces: {len(files)}\nupdated: {datetime.now():%Y-%m-%d %H:%M}\n---\n\n"
                    f"# {stem}\n\n" + "\n\n".join(parts) + "\n", encoding="utf-8")
    return {"saved": str(dest), "pieces": len(files)}


# ------------------------------------------------------------------ runs (the buttons, answers given up front)

class Run:
    def __init__(self, req: dict, gateway: Gateway):
        self.id = datetime.now().strftime("%Y%m%d-%H%M%S-") + secrets.token_hex(2)
        self.fronts = [known_front(p) for p in req["sequence"]]
        if not self.fronts:
            raise ValueError("pick at least one station")
        self.req = req
        self.notes = list(req.get("notes") or [])     # renamed by titling as the run goes; each step gets the new names
        self.gateway = gateway
        self.lines: list[str] = []
        self.status = "running"
        self.step = 0
        self.current = ""
        self.proc: subprocess.Popen | None = None
        self.stopping = False
        self.codes: list[dict] = []
        self.started = time.time()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def say(self, line: str) -> None:
        with self.lock:
            self.lines.append(line.rstrip("\n"))

    def _plan_for(self, front: Path) -> Path:
        r = self.req
        layers = [l for l in (r.get("layers") or {}).get(str(front), [])]
        plan = {"notes": self.notes, "out": r.get("out") or "", "workers": r.get("workers") or 8,
                "focus": r.get("focus") or [], "layers": layers, "topic": r.get("topic") or ""}
        f = SYSTEM / "STATE" / "workspace" / f"plan-{self.id}-{front.name}.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        return f

    def _run(self) -> None:
        mock = bool(self.req.get("mock"))
        self.say(f"[{now()}] run {self.id}: {len(self.fronts)} station(s), {len(self.req.get('notes') or [])} note(s), "
                 f"{self.req.get('workers')} at once" + (" · MOCK (fake replies, nothing leaves this machine)" if mock else ""))
        for i, front in enumerate(self.fronts, 1):
            if self.stopping:
                break
            self.step, self.current = i, front.name
            label = (read_json(front / "BACKSIDE" / "station.json", {}) or {}).get("label", front.name)
            self.say(f"\n[{now()}] ===== step {i}/{len(self.fronts)}: {front.name} =====")
            env = {**os.environ, **self.gateway.env_for(label), "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8",
                   "ONE_MENU_RUN_ID": self.id}
            if mock:                                    # legacy scripts skip a route without a key; the relay never sends it
                for key in ("DEEPSEEK_API_KEY", "OPENROUTER_API_KEY", "OPENAI_API_KEY", "MOONSHOT_API_KEY"):
                    env.setdefault(key, "mock-key-not-sent")
                env["ONE_MENU_PROVIDER"] = "mock"
            cmd = [sys.executable, "-u", str(BUTTON), "plan", str(front), str(self._plan_for(front))]
            started = time.time()
            kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if sys.platform == "win32" else {"start_new_session": True}
            self.proc = subprocess.Popen(cmd, cwd=MAIN, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", **kw)
            for line in self.proc.stdout:
                self.say(line)
            code = self.proc.wait()
            last = front / "OUTBOX" / "_last_run.txt"     # the notes this step ran, under their names after titling
            if last.is_file() and last.stat().st_mtime >= started - 1:
                self.notes = [str(n) for n in pick.read_list(last) if n.is_file()] or self.notes
            self.codes.append({"station": front.name, "returncode": code})
            self.say(f"[{now()}] {front.name}: {'OK' if code == 0 else f'exit {code}'}")
        stats = self.gateway.stats.snapshot()
        self.status = "stopped" if self.stopping else ("failed" if any(c["returncode"] for c in self.codes) else "done")
        self.say(f"\n[{now()}] {self.status} · {round(time.time() - self.started)} s · relay so far: calls {stats['calls']}, "
                 f"failed {stats['failed']}, tokens {stats['tokens']:,}")
        record = {"run_id": self.id, "request": {k: v for k, v in self.req.items() if k != "notes"},
                  "notes": self.req.get("notes"), "results": self.codes, "status": self.status,
                  "finished_at": datetime.now(timezone.utc).isoformat()}
        log = SYSTEM / "LOGS" / f"workspace-run-{self.id}.json"
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    def stop(self) -> None:
        """Stop after what is finished: every note already done keeps its results (they are saved one at a time)."""
        self.stopping = True
        p = self.proc
        if p and p.poll() is None:
            self.say(f"[{now()}] stop pressed: ending {self.current}; finished notes keep their results")
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
            else:
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def view(self, since: int) -> dict:
        with self.lock:
            lines = self.lines[since:]
            total = len(self.lines)
        return {"id": self.id, "status": self.status, "step": self.step, "steps": len(self.fronts),
                "current": self.current, "lines": lines, "next": total, "results": self.codes,
                "seconds": round(time.time() - self.started), "stats": self.gateway.stats.snapshot(),
                "sequence": [f.name for f in self.fronts], "notes": self.notes}


class Workspace:
    def __init__(self):
        self.runs: dict[str, Run] = {}
        self.gateways: dict[bool, Gateway] = {}
        self.lock = threading.Lock()

    def gateway(self, mock: bool) -> Gateway:
        """One relay for real calls and one for mock, shared by every run: concurrency never multiplies."""
        with self.lock:
            if mock not in self.gateways:
                limit = int(llm.settings().get("max_concurrent_calls", 30))
                run_id = f"workspace-{datetime.now():%Y%m%dT%H%M%S}" + ("-mock" if mock else "")
                self.gateways[mock] = Gateway(limit, run_id, mock=mock).start()
            return self.gateways[mock]

    def start(self, req: dict) -> dict:
        run = Run(req, self.gateway(bool(req.get("mock"))))
        self.runs[run.id] = run
        run.thread.start()
        return {"id": run.id}


WS = Workspace()


# ------------------------------------------------------------------ HTTP

ROUTES_GET = {
    "/api/catalog": lambda q: catalog(),
    "/api/browse": lambda q: browse(q.get("path", "")),
    "/api/notes": lambda q: list_notes(q["path"]),
    "/api/file": lambda q: read_file(q["path"]),
    "/api/results": lambda q: results(q["front"]),
    "/api/pieces": lambda q: pieces(q["front"]),
    "/api/runs": lambda q: {"runs": [r.view(len(r.lines)) | {"lines": []} for r in WS.runs.values()]},
}
ROUTES_POST = {
    "/api/run": lambda b: WS.start(b),
    "/api/backside": lambda b: save_backside(b["front"], b["name"], b["text"]),
    "/api/piece/call": call_piece,
    "/api/piece/save": save_piece,
    "/api/piece/saved": saved_pieces,
    "/api/piece/assemble": assemble_pieces,
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        return

    def _send(self, status: int, body: bytes, ctype: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, data) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _authorised(self) -> bool:
        return secrets.compare_digest(self.headers.get("X-Workspace-Token", ""), TOKEN)

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        if url.path in ("/", "/index.html"):
            page = PAGE.read_text(encoding="utf-8").replace("__WORKSPACE_TOKEN__", TOKEN)
            return self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
        q = dict(urllib.parse.parse_qsl(url.query))
        run = re.fullmatch(r"/api/runs/([\w-]+)", url.path)
        if not self._authorised():
            return self._json(403, {"error": "missing workspace token: reopen the page from ONE_MENU.bat workspace"})
        try:
            if run:
                r = WS.runs.get(run.group(1))
                return self._json(200, r.view(int(q.get("since", 0)))) if r else self._json(404, {"error": "no such run"})
            if url.path in ROUTES_GET:
                return self._json(200, ROUTES_GET[url.path](q))
            return self._json(404, {"error": "not found"})
        except (ValueError, KeyError, OSError) as exc:
            return self._json(400, {"error": str(exc)})

    def do_POST(self):
        url = urllib.parse.urlsplit(self.path)
        if not self._authorised():
            return self._json(403, {"error": "missing workspace token: reopen the page from ONE_MENU.bat workspace"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0) or 0)) or b"{}")
            stop = re.fullmatch(r"/api/runs/([\w-]+)/stop", url.path)
            if stop:
                r = WS.runs.get(stop.group(1))
                if not r:
                    return self._json(404, {"error": "no such run"})
                r.stop()
                return self._json(200, {"stopping": True})
            if url.path in ROUTES_POST:
                return self._json(200, ROUTES_POST[url.path](body))
            return self._json(404, {"error": "not found"})
        except (ValueError, KeyError, OSError) as exc:
            return self._json(400, {"error": str(exc)})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-open", action="store_true", help="do not open the browser")
    args = ap.parse_args(argv)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.daemon_threads = True
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"[{now()}] API workspace: {url}\n  Leave this window open while you use the page. Close it to stop.", flush=True)
    if not args.no_open:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    while True:                                         # a stray Ctrl+C never closes it; only typing stop does
        try:
            line = input("  (type stop and Enter to close the workspace)\n") if sys.stdin.isatty() else None
        except KeyboardInterrupt:
            print("  (Ctrl+C ignored: type stop to close)", flush=True)
            continue
        except EOFError:
            line = None
        if line is None:                                # no console (started in the background): serve until killed
            threading.Event().wait()
        if line.strip().lower() == "stop":
            running = [r for r in WS.runs.values() if r.status == "running"]
            if running and input(f"  {len(running)} run(s) still going. Stop them and close? [y/N] ").lower() not in ("y", "yes"):
                continue
            for r in running:
                r.stop()
            server.shutdown()
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
