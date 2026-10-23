"""092_RECONCILIATION — Desk Reconciliation batch runner.

Reads atom JSON files from INBOX, asks Forge's local route for classification
proposals, and writes editable proposals to OUTBOX. Each call is recorded as a
receipt in OUTBOX/_receipts.

Usage:
    python 92_reconciliation.py
    python 92_reconciliation.py --outbox D:/some/folder
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

AXES = ["object_type", "register", "proof_label", "one_axiom_classification", "lean_state", "adequacy"]


def prompt_template() -> str:
    p = HERE / "templates" / "reconciliation_prompt.txt"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return "Classify this atom against the Claim Atom Canon v1.1. Reply ONLY with JSON: {\"object_type\":\"\",\"register\":\"\",\"one_axiom_classification\":\"\",\"lean_state\":\"\",\"adequacy\":\"\",\"reasoning\":\"\"}.\n\nAtom:\n{atom_json}"


def inputs() -> list[Path]:
    folder = FRONT / "INBOX"
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".md", ".txt"} and not p.name.startswith("."))


def forge_propose(atom: dict, model: str | None = "local") -> tuple[dict, dict]:
    tmpl = prompt_template()
    body = {
        "model": model or "local",
        "messages": [{"role": "user", "content": tmpl.format(atom_json=json.dumps(atom, indent=2))}],
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
    raw = resp["choices"][0]["message"]["content"]
    try:
        sug = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Could not parse proposal JSON: {e}") from None
    return sug, resp


def write_receipt(out: Path, note: Path, resp: dict) -> None:
    receipts = out / "_receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rec = {
        "station": "092_RECONCILIATION",
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
    ap.add_argument("--model", default=os.environ.get("FORGE_LOCAL_MODEL", "local"))
    ap.add_argument("--focus", action="append", default=[])
    a = ap.parse_args()

    out = Path(a.outbox) if a.outbox else FRONT / "OUTBOX"
    out.mkdir(parents=True, exist_ok=True)

    files = []
    for item in a.items:
        p = Path(item)
        if p.is_file(): files.append(p)
        elif p.is_dir(): files += [x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in {".json", ".md", ".txt"}]
    files = files or inputs()
    if not files:
        print("No input files found. Drop an atom JSON into INBOX or pass a path.")
        return 0

    for note in files:
        print(f"[{datetime.now():%H:%M:%S}] 092_RECONCILIATION → {note.name}")
        try:
            atom = json.loads(note.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError as e:
            print(f"  FAILED: not valid JSON: {e}")
            continue
        try:
            sug, resp = forge_propose(atom, a.model)
        except RuntimeError as e:
            print(f"  FAILED: {e}")
            (out / f"{note.stem}_ERROR.txt").write_text(str(e), encoding="utf-8")
            continue

        proposal = {
            "atom_id": atom.get("atom_id") or atom.get("id"),
            "proposal_source": "AI-PROPOSED",
            "proposed": {k: sug.get(k, "") for k in AXES if k in sug},
            "reasoning": sug.get("reasoning", ""),
            "forge_model": resp.get("model"),
        }
        out_file = out / f"{note.stem} · RECONCILIATION_PROPOSAL.json"
        out_file.write_text(json.dumps(proposal, indent=2), encoding="utf-8")
        write_receipt(out, note, resp)
        print(f"  saved {out_file.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
