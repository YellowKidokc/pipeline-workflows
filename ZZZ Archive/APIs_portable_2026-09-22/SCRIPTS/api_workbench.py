"""Portable front door for the existing evidence and Lean review engines."""
from __future__ import annotations

import argparse
import contextlib
import csv
import getpass
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import venv

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = {"workers": 12, "deepseek_model": "deepseek-flash", "poll_seconds": 5,
            "settle_seconds": 15, "watch_lanes": ["EVIDENCE", "LEAN4"]}


def config(root=ROOT):
    values = dict(DEFAULTS)
    p = root / "CONFIG/settings.local.json"
    if p.exists():
        values.update(json.loads(p.read_text(encoding="utf-8-sig")))
    if not isinstance(values["workers"], int) or not 1 <= values["workers"] <= 30:
        raise ValueError("workers must be an integer from 1 to 30")
    if values["poll_seconds"] < 1 or values["settle_seconds"] < 5:
        raise ValueError("poll_seconds must be >= 1; settle_seconds must be >= 5")
    if not set(values["watch_lanes"]) <= {"EVIDENCE", "LEAN4"}:
        raise ValueError("watch_lanes may contain EVIDENCE and LEAN4 only")
    return values


def environment(root=ROOT):
    env = os.environ.copy()
    keyfile = root / "CONFIG/keys.local.json"
    if keyfile.exists():
        keys = json.loads(keyfile.read_text(encoding="utf-8-sig"))
        for name in ("DEEPSEEK_API_KEY", "OPENROUTER_API_KEY"):
            if keys.get(name):
                env[name] = str(keys[name]).strip()
    # A copied package must not inherit the old workstation's corpus locations.
    for name in ("LEAN4_EXTRA_SCAN", "LEAN4_RUN_ALL", "LEAN4_READER_PAPERS"):
        env.pop(name, None)
    env.update(LEAN4_ROOT=str(root / "LEAN4"),
               LEAN4_READING_LIBRARY=str(root / "LEAN4/OUTBOX/READING_LIBRARY"),
               PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    return env


def initialize(root=ROOT):
    for lane in ("EVIDENCE", "LEAN4"):
        for folder in ("INBOX/_PRIORITY", "INBOX/SERIES", "OUTBOX", "FAILED", "LOGS", "STATE", "PROCESSED_ORIGINALS"):
            (root / lane / folder).mkdir(parents=True, exist_ok=True)
    for folder in ("CONFIG", "LOGS", "STATE", "CANONIZATION/INBOX", "CANONIZATION/REVIEW",
                   "CANONIZATION/OUTBOX", "CANONIZATION/ADMITTED", "LEAN4/OUTBOX/READING_LIBRARY"):
        (root / folder).mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def lane_lock(lane, root=ROOT):
    """OS-released lock prevents a second launcher from billing the same queue."""
    path = root / "STATE" / (lane.lower() + ".lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    f = path.open("a+b")
    f.seek(0, 2)
    if not f.tell():
        f.write(b"0"); f.flush()
    f.seek(0)
    try:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.close()
        raise RuntimeError(f"{lane} is already running from another launcher.")
    try:
        yield
    finally:
        f.close()


def command(lane, mode="run", root=ROOT, values=None):
    values = values or config(root)
    if lane == "LEAN4":
        cmd = [sys.executable, "-u", str(root / "LEAN4/SCRIPTS/pipeline.py")]
        if mode in ("inventory", "verify"):
            return cmd + [mode]
        return cmd + ["deepseek", "--workers", str(values["workers"]), "--model", values["deepseek_model"],
                      "--reader-papers", "--auto" if mode == "watch" else "--count-only"]
    if lane == "EVIDENCE":
        return [sys.executable, "-u", str(root / "EVIDENCE/SCRIPTS/turbo_pipeline_runner.py"),
                "--workers", str(values["workers"]), "--provider", "deepseek", "--model", values["deepseek_model"], "--single-batch"]
    raise ValueError(f"Unknown lane: {lane}")


def run(lane, mode="run", root=ROOT):
    initialize(root)
    env = environment(root)
    if mode not in ("inventory", "verify") and not env.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("Set your DeepSeek key with 1_ADD_API_KEY.bat first.")
    with lane_lock(lane, root):
        return subprocess.call(command(lane, mode, root), env=env, cwd=root)


def snapshot(lane, root=ROOT):
    """All supported input files, including nested dropped folders."""
    extensions = {".lean"} if lane == "LEAN4" else {".md", ".txt", ".html", ".htm", ".tex"}
    rows = []
    inbox = root / lane / "INBOX"
    for directory, dirs, files in os.walk(inbox):
        dirs[:] = sorted(d for d in dirs if d not in {".git", ".lake", ".venv", "__pycache__", "node_modules"})
        for name in sorted(files):
            p = Path(directory) / name
            if p.suffix.lower() in extensions:
                try:
                    st = p.stat()
                    rows.append((str(p.relative_to(inbox)), st.st_size, st.st_mtime_ns))
                except FileNotFoundError:
                    pass
    return tuple(rows)


def watch(root=ROOT):
    initialize(root)
    values, env = config(root), environment(root)
    if not env.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("Set your DeepSeek key with 1_ADD_API_KEY.bat first.")
    print("Watching EVIDENCE and LEAN4 inboxes. API calls are enabled. Ctrl+C stops this watcher.", flush=True)
    print("Workers are per lane; two active lanes can use twice the configured worker count.", flush=True)
    state, children = {}, {}
    locks = contextlib.ExitStack()
    try:
        for lane in values["watch_lanes"]:
            locks.enter_context(lane_lock(lane, root))
        while True:
            for lane in values["watch_lanes"]:
                now = time.monotonic()
                sig = snapshot(lane, root)
                entry = state.setdefault(lane, {"signature": None, "changed": now, "submitted": None})
                if sig != entry["signature"]:
                    entry.update(signature=sig, changed=now)
                if lane in children:
                    process, log = children[lane]
                    if process.poll() is None:
                        continue
                    print(f"{lane} finished with status {process.returncode}. See {log.name}", flush=True)
                    log.close(); del children[lane]
                if sig and sig != entry["submitted"] and now - entry["changed"] >= values["settle_seconds"]:
                    name = lane.lower() + "-" + time.strftime("%Y%m%d-%H%M%S") + ".log"
                    log = (root / "LOGS" / name).open("a", encoding="utf-8")
                    try:
                        child = subprocess.Popen(command(lane, "watch", root, values), env=env,
                                                 cwd=root, stdout=log, stderr=subprocess.STDOUT)
                    except BaseException:
                        log.close(); raise
                    children[lane] = (child, log)
                    entry["submitted"] = sig
                    print(f"Started {lane}; progress: {log.name}", flush=True)
            time.sleep(values["poll_seconds"])
    except KeyboardInterrupt:
        print("Stopping. Waiting for active workers to close; saved receipts remain available.", flush=True)
    finally:
        for child, log in children.values():
            # Ctrl+C is also delivered to attached Windows child consoles.
            try:
                child.wait(timeout=15)
            except subprocess.TimeoutExpired:
                child.terminate(); child.wait()
            log.close()
        locks.close()
    return 0


def doctor(root=ROOT):
    env = environment(root)
    missing = [name for name in ("requests", "openpyxl") if importlib.util.find_spec(name) is None]
    print("Package:", root)
    print("Python:", sys.version.split()[0])
    print("Dependencies:", "missing " + ", ".join(missing) if missing else "ready")
    print("DeepSeek key:", "configured" if env.get("DEEPSEEK_API_KEY") else "not configured")
    print("Lean compiler:", "available" if shutil.which("lake") else "not installed (only needed for proof checks)")
    print("Workers per lane:", config(root)["workers"])
    for lane in ("EVIDENCE", "LEAN4"):
        print(lane, "input files:", len(snapshot(lane, root)))
    return int(bool(missing))


def setup(root=ROOT):
    target = root / ".venv"
    venv.EnvBuilder(with_pip=True).create(target)
    python = target / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(root / "requirements.txt")], check=True)
    initialize(root)
    print("Setup complete. Add an API key, then choose a launcher.")
    return 0


def add_key(root=ROOT):
    initialize(root)
    key = getpass.getpass("DeepSeek API key (hidden): ").strip()
    if not key:
        print("No key entered; existing configuration unchanged.")
        return 1
    path = root / "CONFIG/keys.local.json"
    keys = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    keys["DEEPSEEK_API_KEY"] = key
    path.write_text(json.dumps(keys, indent=2), encoding="utf-8")
    print("Saved locally in CONFIG/keys.local.json (excluded from Git and portable exports).")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["menu", "setup", "key", "doctor", "evidence", "lean", "inventory", "verify", "watch"])
    args = parser.parse_args()
    action = args.action
    if action == "menu":
        print("1 Evidence papers\n2 Lean reader papers\n3 Watch both inboxes\n4 Check setup\n5 Inventory Lean files\n6 Check Lean proofs\n0 Exit")
        action = {"1": "evidence", "2": "lean", "3": "watch", "4": "doctor", "5": "inventory", "6": "verify"}.get(input("Choose: ").strip())
        if not action:
            return 0
    if action in ("evidence", "lean", "inventory", "verify"):
        return run("EVIDENCE" if action == "evidence" else "LEAN4", action if action in ("inventory", "verify") else "run")
    return {"setup": setup, "key": add_key, "doctor": doctor, "watch": watch}[action]()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        raise SystemExit(1)
