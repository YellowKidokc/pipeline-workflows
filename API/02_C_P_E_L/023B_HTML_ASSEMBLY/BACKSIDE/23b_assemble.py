r"""23B_HTML_ASSEMBLY: atom JSON (or YAML) -> one standalone HTML page per atom. No API calls.

Takes atom files that follow the atom contract (Faith-through-physics-atoms\_template\schemas\
atom-api-contract.md) and builds the black atom card for each one. Every output page is
self-contained: the CSS, the renderer, the lens grammar and the atom's data are all inside the
one .html file, so it opens by double-click, works offline, and can be published as-is.

    python 23b_assemble.py                    everything in ..\INBOX (00_PRIORITY first)
    python 23b_assemble.py file.json folder\  those files / folders
    python 23b_assemble.py @list.txt          files listed in a text file
    --outbox DIR     where pages go (default ..\OUTBOX)
    --force          rebuild pages even if the atom and shell are unchanged

Shell: uses the live template in Faith-through-physics-atoms\_template\html if it exists
(set SHELL_DIR in settings.txt to change it), otherwise the snapshot in BACKSIDE\shell.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
INBOX, OUTBOX = FRONT / "INBOX", FRONT / "OUTBOX"
LANES = ["00_PRIORITY", "01_SERIES", "02_GENERAL", "02_GROUP"]
EXTS = {".json", ".yaml", ".yml"}
SHELL_FILES = ["atom-shell.html", "atom-shell.css", "atom-shell.js", "grammar.json"]
DEFAULT_SHELL = ""  # override in settings.txt; empty means use BACKSIDE\shell snapshot
EMPTY_BLOCK = '<script type="application/json" id="atom-data"></script>'


def settings() -> dict:
    out = {"SHELL_DIR": DEFAULT_SHELL}
    f = HERE / "settings.txt"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip().upper()] = v.strip()
    return out


def shell_dir() -> Path:
    cfg = settings().get("SHELL_DIR", "").strip()
    if cfg:
        live = Path(cfg)
        if all((live / f).exists() for f in SHELL_FILES):
            return live
    return HERE / "shell"


def load_shell() -> tuple[str, str]:
    """The template with its CSS, JS and grammar pulled inside, ready for one atom's data."""
    d = shell_dir()
    page = (d / "atom-shell.html").read_text(encoding="utf-8")
    css = (d / "atom-shell.css").read_text(encoding="utf-8")
    js = (d / "atom-shell.js").read_text(encoding="utf-8")
    grammar = json.loads((d / "grammar.json").read_text(encoding="utf-8"))
    # Opened from disk, the page can't fetch grammar.json, so the grammar goes into the script itself.
    hook = "let GRAMMAR = DEFAULT_GRAMMAR;"
    if hook not in js:
        raise RuntimeError(f"atom-shell.js no longer contains '{hook}'; the grammar can't be built in")
    js = js.replace(hook, "let GRAMMAR = { ...DEFAULT_GRAMMAR, ..." + json.dumps(grammar, ensure_ascii=False) + " };", 1)
    for needle, repl in [('<link rel="stylesheet" href="atom-shell.css">', "<style>\n" + css + "\n</style>"),
                         ('<script src="atom-shell.js"></script>', "<script>\n" + js.replace("</script", "<\\/script") + "\n</script>")]:
        if needle not in page:
            raise RuntimeError(f"atom-shell.html no longer contains: {needle}")
        page = page.replace(needle, repl, 1)
    if EMPTY_BLOCK not in page:
        raise RuntimeError("atom-shell.html has no empty atom-data block to fill")
    stamp = hashlib.sha256((page).encode("utf-8")).hexdigest()[:12]
    return page, stamp


def read_atom(p: Path) -> dict:
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("not an atom: the file's top level must be an object")
    return data


def check(atom: dict) -> list[str]:
    """Warnings only. The page still builds; the shell shows TODO for anything missing."""
    warn = []
    a = atom.get("atom") or {}
    if not a:
        warn.append("no 'atom' block")
    for k in ("id", "type", "title"):
        if a and not a.get(k):
            warn.append(f"atom.{k} missing")
    if a.get("type") and a["type"] not in ("claim", "evidence", "proof", "lean", "bridge", "definition"):
        warn.append(f"unknown atom.type '{a['type']}' (lens will show TODO)")
    lens = atom.get("lens") or {}
    missing = [k for k in ("m05", "m06", "m07", "m08") if not lens.get(k)]
    if missing:
        warn.append("lens empty: " + ", ".join(missing))
    return warn


def build_page(shell: str, atom: dict) -> str:
    data = json.dumps(atom, ensure_ascii=False, indent=1).replace("<", "\\u003c")   # can't close the tag early
    page = shell.replace(EMPTY_BLOCK, '<script type="application/json" id="atom-data">\n' + data + "\n</script>", 1)
    title = (atom.get("atom") or {}).get("title")
    if title:
        page = page.replace("<title>", "<title>" + html.escape(str(title)) + " · ", 1)
    return page


def gather(items: list[str]) -> list[Path]:
    def scan(d: Path) -> list[Path]:
        return sorted(p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in EXTS
                      and not p.name.startswith(("_", ".")))
    if not items:
        out = []
        for lane in LANES:
            if (INBOX / lane).is_dir():
                out += scan(INBOX / lane)
        return out
    files: list[Path] = []
    for raw in items:
        if raw.startswith("@"):
            files += [Path(l.strip()) for l in Path(raw[1:]).read_text(encoding="utf-8-sig").splitlines() if l.strip()]
        elif Path(raw).is_dir():
            files += scan(Path(raw))
        elif Path(raw).is_file():
            files.append(Path(raw))
        else:
            print(f"  ! not found, skipped: {raw}")
    return [f for f in dict.fromkeys(files) if f.suffix.lower() in EXTS]


def write_index(out: Path) -> None:
    rows = []
    for rec in sorted(out.glob("*.receipt.json")):
        r = json.loads(rec.read_text(encoding="utf-8"))
        rows.append(f"<tr><td><a href=\"{html.escape(r['page'])}\">{html.escape(r['title'] or r['page'])}</a></td>"
                    f"<td>{html.escape(r['type'] or '')}</td><td>{html.escape(r['id'] or '')}</td>"
                    f"<td>{len(r['warnings'])}</td><td>{html.escape(r['built'])}</td></tr>")
    (out / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>Atom pages</title>"
        "<style>body{font:14px system-ui;background:#0b0b0d;color:#e8e6e1;margin:24px}a{color:#d4af37}"
        "table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #333;padding:6px;text-align:left}</style>"
        f"<h1>Atom pages ({len(rows)})</h1><table><tr><th>Atom</th><th>Type</th><th>ID</th><th>Warnings</th><th>Built</th></tr>"
        + "".join(rows) + "</table>", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(prog="23B_HTML_ASSEMBLY")
    ap.add_argument("items", nargs="*")
    ap.add_argument("--outbox", default=str(OUTBOX))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", default="1")      # accepted for the shared buttons; assembly is instant
    ap.add_argument("--focus", default="")         # accepted for the shared buttons; not used
    ap.add_argument("--dry-run", action="store_true", help="list inputs without writing pages")
    a = ap.parse_args()

    files = gather(a.items)
    if a.dry_run:
        print(f"23B HTML assembly dry run: {len(files)} atom file(s); no files written")
        for source in files:
            print(source)
        return 0
    shell, shell_stamp = load_shell()
    out = Path(a.outbox)
    out.mkdir(parents=True, exist_ok=True)
    print(f"[{datetime.now():%H:%M:%S}] 23B HTML assembly: {len(files)} atom file(s), shell from {shell_dir()}")
    if not files:
        print("  nothing to build: put atom .json or .yaml files in INBOX\\00_PRIORITY, 01_SERIES or 02_GENERAL")
        return 0
    built = skipped = failed = 0
    used: set[str] = set()
    for f in files:
        try:
            atom = read_atom(f)
            src_hash = hashlib.sha256(f.read_bytes()).hexdigest()
            name = f.stem if f.stem.lower() not in used else f"{f.stem}.{f.suffix.lstrip('.').lower()}"
            used.add(name.lower())                  # claim.json and claim.yaml in one run don't overwrite each other
            page_path = out / f"{name}.html"
            rec_path = out / f"{name}.receipt.json"
            if not a.force and rec_path.exists() and page_path.exists():
                old = json.loads(rec_path.read_text(encoding="utf-8"))
                if old.get("source_sha256") == src_hash and old.get("shell") == shell_stamp:
                    skipped += 1
                    continue
            warn = check(atom)
            page_path.write_text(build_page(shell, atom), encoding="utf-8")
            a_ = atom.get("atom") or {}
            rec_path.write_text(json.dumps({
                "station": "23B_HTML_ASSEMBLY", "source": str(f), "source_sha256": src_hash,
                "shell": shell_stamp, "page": page_path.name, "id": a_.get("id"), "type": a_.get("type"),
                "title": a_.get("title"), "warnings": warn, "built": datetime.now().isoformat(timespec="seconds"),
            }, indent=2, ensure_ascii=False), encoding="utf-8")
            built += 1
            print(f"[{datetime.now():%H:%M:%S}] built  {page_path.name}" + (f"  ({len(warn)} warning(s): {'; '.join(warn)})" if warn else ""))
        except Exception as e:                      # one bad file never stops the rest
            failed += 1
            print(f"[{datetime.now():%H:%M:%S}] FAILED {f.name}: {e}")
    write_index(out)
    print(f"[{datetime.now():%H:%M:%S}] done: {built} built, {skipped} unchanged (skipped), {failed} failed -> {out}")
    print(f"  open {out / 'index.html'} to see them all")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
