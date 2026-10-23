"""091_CHAT — Desk Chat batch runner.

Reads every .md/.txt file in the station INBOX, sends it as a user message
to Forge (FORGE_URL, default http://127.0.0.1:8790), and writes the assistant
reply to OUTBOX. Each call is recorded as a receipt in OUTBOX/_receipts.

Usage:
    python 91_chat.py
    python 91_chat.py --outbox D:/some/folder
    python 91_chat.py --model llama3.1
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
FORGE_URL = os.environ.get("FORGE_URL", "http://127.0.0.1:8790").rstrip("/")
TEXT = {".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm", ".py", ".lean", ".tex", ".bib", ".yaml", ".yml", ".toml", ".ini", ".log", ".sql", ".rst", ".js", ".ts", ".srt", ".vtt"}


def system_message() -> str:
    p = HERE / "templates" / "chat_system.txt"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return "You are a helpful research assistant."


def inputs() -> list[Path]:
    folder = FRONT / "INBOX"
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in TEXT and not p.name.startswith("."))


def forge_chat(messages: list[dict], model: str | None) -> tuple[str, dict]:
    body = {
        "model": model or "default",
        "messages": messages,
        "stream": False,
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{FORGE_URL}/v1/chat/completions", data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Forge HTTP {e.code}: {e.read()[:500].decode(errors='replace')}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Forge unreachable: {e.reason}. Is Forge running at {FORGE_URL}?") from None

    if "choices" not in resp or not resp["choices"]:
        raise RuntimeError(f"Forge returned no choices: {json.dumps(resp)[:500]}")
    return resp["choices"][0]["message"]["content"], resp


def write_receipt(out: Path, note: Path, resp: dict) -> None:
    receipts = out / "_receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rec = {
        "station": "091_CHAT",
        "note": note.name,
        "forge_url": FORGE_URL,
        "model": resp.get("model"),
        "usage": resp.get("usage"),
        "created_at": resp.get("created"),
        "local_time": stamp,
    }
    (receipts / f"{note.stem}_{stamp}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="*")
    ap.add_argument("--outbox")
    ap.add_argument("--model", default=os.environ.get("FORGE_CHAT_MODEL", "default"))
    ap.add_argument("--focus", action="append", default=[])
    a = ap.parse_args()

    out = Path(a.outbox) if a.outbox else FRONT / "OUTBOX"
    out.mkdir(parents=True, exist_ok=True)

    files = []
    for item in a.items:
        p = Path(item)
        if p.is_file(): files.append(p)
        elif p.is_dir(): files += [x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in TEXT]
    files = files or inputs()
    if not files:
        print("No input files found. Drop a .md/.txt into INBOX or pass a path.")
        return 0

    system = system_message()
    focus = "\n\n".join(a.focus) if a.focus else ""
    if focus:
        system += "\n\n## STANDING FOCUS\n" + focus

    for note in files:
        print(f"[{datetime.now():%H:%M:%S}] 091_CHAT → {note.name}")
        user_text = note.read_text(encoding="utf-8", errors="replace")
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user_text}]
        try:
            answer, resp = forge_chat(messages, a.model)
        except RuntimeError as e:
            print(f"  FAILED: {e}")
            (out / f"{note.stem}_ERROR.txt").write_text(str(e), encoding="utf-8")
            continue

        out_file = out / f"{note.stem} · CHAT.md"
        out_file.write_text(answer, encoding="utf-8")
        write_receipt(out, note, resp)
        print(f"  saved {out_file.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
