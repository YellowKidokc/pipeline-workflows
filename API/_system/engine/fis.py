"""Glue between the 10_FIS stations and David-OSv3's FIS engine. No FIS logic lives here.

The engine (engine/understand.py, engine/path_write_policy.py) stays in David-OSv3 and is loaded from there by file
path: both repos have a package called `engine`, so a plain import would load the wrong one. Where David-OSv3 is on
this machine comes from paths.json key `david_osv3` (or the environment variable ONE_MENU_DAVID_OSV3).

What this module does:
  * load the engine modules;
  * read the FIS roots from David-OSv3's config/folder_registry.yaml (entries with a `fis:` field) plus root lists
    dropped in a station INBOX (.txt, one path per line, 00_PRIORITY first);
  * mark every root read-only through path_write_policy.protect_root and refuse any write inside one;
  * remember the scan a station made (OUTBOX/_last_scan.txt) so the next station works on the same scan.
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

from .paths import PathConfigurationError, expand, raw_value

ENGINE_FILES = ("engine/understand.py", "engine/path_write_policy.py")
LANES = ("00_PRIORITY", "01_SERIES", "02_GENERAL", "02_GROUP")
LAST_SCAN = "_last_scan.txt"


@dataclass
class Root:
    path: str
    treatment: str          # register | collection | skip
    collection: str = ""
    note: str = ""
    source: str = "folder_registry.yaml"


def osv3() -> Path:
    raw = raw_value("david_osv3")
    if not raw:
        raise PathConfigurationError("Set david_osv3 in _system/config/paths.json to your David-OSv3 folder "
                                     "(e.g. D:/GitHub/David-OSv3).")
    home = expand(raw)
    missing = [f for f in ENGINE_FILES if not (home / f).is_file()]
    if missing:
        raise PathConfigurationError(f"{home} has no {', '.join(missing)}: the FIS engine is not on this branch "
                                     "of David-OSv3 (check out the FIS snapshot branch).")
    return home


def _load(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def engine():
    """(understand, path_write_policy) from David-OSv3."""
    home = osv3()
    return _load("fis_understand", home / "engine" / "understand.py"), _load("fis_path_policy", home / "engine" / "path_write_policy.py")


def registry_roots() -> list[Root]:
    understand, _ = engine()
    out = [Root(e["path"], str(e["fis"]), str(e.get("collection") or ""), str(e.get("note") or ""))
           for e in understand.load_registry() if e.get("fis")]
    mirror = osv3() / "_FIS_ROOT_SIDECAR_ARCHIVE"   # the copy D:\_FIS_ROOT_SIDECAR_ARCHIVE is compared against
    if mirror.is_dir() and not any(Path(r.path) == mirror for r in out):
        out.append(Root(str(mirror), "register", note="David-OSv3's sidecar archive, scanned with the D: one so copies match",
                        source="david_osv3"))
    return out


def inbox_roots(front: Path) -> list[Root]:
    """Root lists dropped in the station INBOX: .txt files, one folder path per line, priority lane first."""
    box = front / "INBOX"
    files = []
    for lane in LANES:
        files += sorted((box / lane).rglob("*.txt")) if (box / lane).is_dir() else []
    files += sorted(p for p in box.glob("*.txt"))
    roots, seen = [], set()
    for f in files:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip().strip('"')
            if line and not line.startswith("#") and line not in seen:
                seen.add(line)
                roots.append(Root(line, "register", source=f.name))
    return roots


def chosen_roots(args_roots: list[str], front: Path) -> list[Root]:
    """Roots named on the command line, else the INBOX lists, else the registry."""
    if args_roots:
        known = {r.path.lower(): r for r in registry_roots()}
        return [known.get(p.lower(), Root(p, "register", source="command line")) for p in args_roots]
    return inbox_roots(front) or registry_roots()


def protect(roots: list[Root], *writes: Path) -> None:
    """Every scanned root becomes read-only for this process; refuse if any output would land inside one."""
    _, policy = engine()
    for r in roots:
        policy.protect_root(r.path)
    for w in writes:
        policy.require_write_allowed(w)


def default_db() -> Path:
    understand, _ = engine()
    return Path(understand.DB_PATH)


def save_scan(outbox: Path, scan_id: int) -> None:
    outbox.mkdir(parents=True, exist_ok=True)
    (outbox / LAST_SCAN).write_text(f"{scan_id}\n", encoding="utf-8")


def last_scan(con, *outboxes: Path) -> int:
    """The scan 101 made (its OUTBOX/_last_scan.txt), else the newest scan in the database."""
    for box in outboxes:
        f = box / LAST_SCAN
        if f.is_file() and f.read_text(encoding="utf-8").strip().isdigit():
            return int(f.read_text(encoding="utf-8").strip())
    row = con.execute("SELECT MAX(scan_id) FROM scans").fetchone()
    return int(row[0]) if row and row[0] else 0


def scan_roots(con, scan_id: int) -> list[str]:
    import json
    row = con.execute("SELECT roots FROM scans WHERE scan_id=?", (scan_id,)).fetchone()
    return json.loads(row[0]) if row else []


def collection_roots(con, scan_id: int) -> list[str]:
    return [f for (f,) in con.execute("SELECT folder FROM observations WHERE scan_id=? AND name='collection'", (scan_id,))]
