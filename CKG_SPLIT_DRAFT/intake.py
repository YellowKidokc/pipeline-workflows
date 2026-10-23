"""Stage 1 · Intake, per ID_AND_YAML_SPEC v0.2 (deep-research-hub/docs/paper-lifecycle).

scan(folder)          read-only: hash every file, check exact / near duplicates, propose titles.
commit(items, dflt)   mints UUID + readable ID (TOPIC-ORIGIN-TYPE-NNNN), freezes the original,
                      writes <ID>.meta.yaml (sidecar) and .norm.md, appends the registry.
topics() / add_topic  the topic registry (spec §3), seeded with the ME tree and WC-01..WC-18.

The original file is never edited or moved. Everything lands in INTAKE/:
  registry.jsonl                     append-only events: "intake" (new identity), "location" (same bytes, new path)
  topics.json                        topic registry
  files/<uuid>/original<ext>         frozen untouched bytes
  files/<uuid>/<uuid>.norm.md        normalized working copy (UTF-8, LF) that spans will point into
  files/<uuid>/<ID or uuid>.meta.yaml  the sidecar
"""
import hashlib
import json
import re
import shutil
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "INTAKE"
REG = BASE / "registry.jsonl"
TOPICS = BASE / "topics.json"
LOCK = threading.Lock()  # one allocator: concurrent commits can't mint the same number
EXTS = {".md", ".txt", ".docx", ".html", ".htm", ".tex", ".lean", ".pdf"}
TEXT = {".md", ".txt", ".html", ".htm", ".tex", ".lean"}
FORMAT = {".md": "markdown", ".txt": "text", ".docx": "docx", ".html": "html", ".htm": "html",
          ".tex": "latex", ".lean": "lean", ".pdf": "pdf"}
ID_RE = re.compile(r"^[A-Z]{2,4}(\.[A-Z]{2,6}){0,2}-[DAX]-[PNWBJYH]-\d{4}(\.v\d+)?(\.(m|q|L|x)\d+)?$")
ROOT_RE = re.compile(r"^[A-Z]{2,4}$")
PATH_RE = re.compile(r"^[A-Z]{2,4}(\.[A-Z]{2,6}){0,2}$")
SEED = [("ME", "Master Equation", None)] + [(f"ME.{c}", n, "ME") for c, n in [
    ("GRAV", "Gravitation"), ("MOT", "Motion"), ("EM", "Electromagnetism"), ("STR", "Strong force"),
    ("THERM", "Thermodynamics"), ("INFO", "Information"), ("QM", "Quantum"), ("REL", "Relativity"),
    ("WEAK", "Weak force"), ("COH", "Coherence")]] + [("MIM", "Math Is Moral", None)]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------- topic registry ----------
def topics():
    if not TOPICS.exists():
        BASE.mkdir(exist_ok=True)
        t = [{"code": c, "name": n, "parent": p, "kind": "topic", "created": now()[:10], "aliases": []} for c, n, p in SEED]
        t += [{"code": f"WC-{i:02d}", "name": f"Whole-case argument {i}", "parent": None, "kind": "whole_case",
               "created": now()[:10], "aliases": []} for i in range(1, 19)]
        TOPICS.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return json.loads(TOPICS.read_text(encoding="utf-8"))


def add_topic(code, name, parent=None):
    code, name = code.strip().upper(), name.strip()
    t = topics()
    if not name:
        raise ValueError("a topic needs a full name")
    if parent:
        if not any(x["code"] == parent and x["kind"] == "topic" for x in t):
            raise ValueError(f"parent {parent} is not in the registry")
        code = f"{parent}.{code}" if not code.startswith(parent + ".") else code
        if not PATH_RE.match(code):
            raise ValueError("child codes are 2–6 capital letters, three levels at most")
    elif not ROOT_RE.match(code):
        raise ValueError("root codes are 2–4 capital letters")
    if any(code == x["code"] or code in x["aliases"] for x in t):
        raise ValueError(f"{code} is already in the registry")
    t.append({"code": code, "name": name, "parent": parent or None, "kind": "topic", "created": now()[:10], "aliases": []})
    TOPICS.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return t


# ---------- registry (events folded into records) ----------
def registry():
    recs = {}
    if REG.exists():
        for line in REG.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e.get("event", "intake") == "intake":
                recs[e["uuid"]] = e
            elif e["event"] == "location" and e["uuid"] in recs:
                recs[e["uuid"]].setdefault("where", []).append(e["path"])
    return list(recs.values())


def counts():
    """Live counts per topic (spec §3: counts live in the registry, never in IDs)."""
    c = {}
    for r in registry():
        k = r.get("topic") or "(no topic)"
        c.setdefault(k, {})
        key = f"{r['origin']}-{r['type']}"
        c[k][key] = c[k].get(key, 0) + 1
    return c


def _append(event):
    BASE.mkdir(exist_ok=True)
    with REG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


# ---------- scan ----------
def _text(raw):
    try:
        return raw.decode("utf-8-sig").replace("\r\n", "\n")
    except UnicodeDecodeError:
        return None


def near_key(raw):
    """Same text once case, whitespace and YAML front matter are ignored. A candidate link only."""
    t = _text(raw)
    if t is None:
        return None
    t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)
    return hashlib.sha256(re.sub(r"\s+", " ", t).strip().lower().encode()).hexdigest()


def title_of(path, raw):
    t = _text(raw)
    if t is None:
        return path.stem
    m = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", t[:3000], re.M) or re.search(r"^#\s+(.+)$", t, re.M)
    return m.group(1).strip() if m else path.stem


def scan(folder):
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError(f"folder not found: {folder}")
    reg = registry()
    by_sha = {r["source_sha256"]: r for r in reg}
    by_near = {r["near_key"]: r for r in reg if r.get("near_key")}
    seen_sha, seen_near, items = {}, {}, []
    for p in sorted(folder.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        raw = p.read_bytes()
        sha, nk = hashlib.sha256(raw).hexdigest(), near_key(raw)
        dup, dup_of, action = "", "", "new"
        if sha in by_sha:
            r = by_sha[sha]
            known_here = str(p) in r.get("where", [])
            dup, dup_of = "exact (already in)", r.get("id") or r["title"]
            action = "already" if known_here else "location"
        elif sha in seen_sha:
            dup, dup_of, action = "exact (in this folder)", seen_sha[sha], "location"
        elif nk and nk in by_near:
            dup, dup_of = "near (already in)", by_near[nk].get("id") or by_near[nk]["title"]
        elif nk and nk in seen_near:
            dup, dup_of = "near (in this folder)", seen_near[nk]
        seen_sha.setdefault(sha, p.name)
        if nk:
            seen_near.setdefault(nk, p.name)
        pm = re.match(r"^part[_\s-]*(\d+)", p.stem, re.I)
        items.append({"path": str(p), "name": p.name, "title": title_of(p, raw), "sha256": sha,
                      "part": int(pm.group(1)) if pm else None,
                      "role": "part" if pm else ("index" if re.match(r"^0*_?index", p.stem, re.I) else "companion"),
                      "size": len(raw), "format": FORMAT.get(p.suffix.lower(), p.suffix),
                      "written": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).date().isoformat(),
                      "duplicate": dup, "duplicate_of": dup_of, "action": action,
                      "take": action != "already"})
    return {"folder": str(folder), "items": items, "registry_count": len(reg),
            "topics": [t for t in topics() if t["kind"] == "topic"]}


# ---------- commit ----------
def _q(s):
    return json.dumps(s, ensure_ascii=False) if s not in (None, "") else "null"


def _list(xs):
    return "[" + ", ".join(_q(x) for x in xs) + "]"


def sidecar(rec):
    return "\n".join([
        'schema_version: "0.2"',
        "# ---- identity (fixed at intake) ----",
        f"id: {_q(rec['id'])}",
        f'uuid: "{rec["uuid"]}"',
        "aliases: []",
        f"title: {_q(rec['title'])}",
        f"standard_title: {_q(rec['title'])}",
        "previous_names: []",
        f"topic: {_q(rec['topic'])}",
        "also_in: []",
        f"origin: {rec['origin']}                  # D house · A analysis · X external",
        f"type: {rec['type']}                    # P paper · N note · W web · B book · J journal · Y video · H hub",
        "authors: [David Lowe]",
        "co_authors: []",
        f"register: {_q(rec['register'])}             # declaration | canon",
        f"source_sha256: \"{rec['source_sha256']}\"",
        f"norm_sha256: {_q(rec['norm_sha256'])}",
        "source_uri: null",
        f"acquired: {rec['ingested'][:10]}",
        f"where: {_list(rec['where'])}",
        f"frozen_copy: {_q(rec['frozen_copy'])}",
        f"source_format: {rec['format']}",
        f"written: {rec['written']}",
        f"ingested: {rec['ingested'][:10]}",
        f"lane: {rec['lane']}",
        *_collection_yaml(rec.get("collection")),
        "version_of: null",
        "successor_of: []",
        f"near_duplicate_of: {_q(rec['near_duplicate_of'])}   # candidate link only; David decides",
        "disposition: null",
        "",
        "# ---- found (proposed by the scan; accepted by David) ----",
        "tags: []", "occurrences: []", "claims: []", "axioms: []", "definitions: []", "evidence: []",
        "predictions: []", "isomorphisms: []", "lean: []", "me_nodes: []", "scripture: []", "witnesses: []",
        "equations: null", "whole_case: {helps: [], hurts: [], neutral: []}", "edges: []",
        "",
        "# ---- status (generated cache; regenerate, never edit) ----",
        "workflow_state: EXTRACTED",
        "last_scan: null",
        f"intake_receipt: {rec['receipt']}",
        f"generated_at: {rec['ingested']}",
        "generated_by: CKG_SPLIT_DRAFT/intake.py",
        "",
        "# ---- local (unlimited) ----",
        "local: []",
        "",
    ])


def _collection(defaults, it):
    """Series (ordered parts) or grouping (kept together, no order). Same record either way."""
    name = (defaults.get("collection_name") or "").strip()
    if not name:
        return None
    kind = defaults.get("collection_kind", "series")
    return {"kind": kind, "name": name, "code": re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-"),
            "part": it.get("part") if kind == "series" else None, "role": it.get("role") or "companion"}


def _collection_yaml(c):
    if not c:
        return ["series: null", "grouping: null"]
    body = f"{{code: {_q(c['code'])}, name: {_q(c['name'])}, part: {_q(c['part'])}, role: {c['role']}}}"
    return ([f"series: {body}", "grouping: null"] if c["kind"] == "series"
            else ["series: null", f"grouping: {{code: {_q(c['code'])}, name: {_q(c['name'])}, role: {c['role']}}}"])


def collections():
    out = {}
    for r in registry():
        c = r.get("collection")
        if c:
            g = out.setdefault(c["code"], {"code": c["code"], "name": c["name"], "kind": c["kind"], "members": []})
            g["members"].append({"id": r.get("id"), "uuid": r["uuid"], "title": r["title"], "part": c.get("part"), "role": c.get("role")})
    for g in out.values():
        g["members"].sort(key=lambda m: (m["part"] is None, m["part"] or 0, m["title"]))
    return list(out.values())


def _next_number(reg, topic, origin, typ):
    pre = f"{topic}-{origin}-{typ}-"
    nums = [int(r["id"][len(pre):len(pre) + 4]) for r in reg if (r.get("id") or "").startswith(pre)]
    return max(nums, default=0) + 1


def commit(items, defaults):
    valid_topics = {t["code"] for t in topics() if t["kind"] == "topic"}
    done, located, skipped = [], [], []
    with LOCK:
        reg = registry()
        by_sha = {r["source_sha256"]: r for r in reg}
        for it in items:
            src = Path(it["path"])
            raw = src.read_bytes()
            sha = hashlib.sha256(raw).hexdigest()
            if sha != it["sha256"]:
                skipped.append({"name": src.name, "why": "file changed since scan; scan again"})
                continue
            if sha in by_sha:  # same bytes: one identity, another location
                r = by_sha[sha]
                if str(src) in r.get("where", []):
                    skipped.append({"name": src.name, "why": f"already in as {r.get('id') or r['uuid']}"})
                    continue
                _append({"event": "location", "uuid": r["uuid"], "path": str(src), "at": now()})
                r.setdefault("where", []).append(str(src))
                _write_sidecar(r)
                located.append({"name": src.name, "id": r.get("id"), "uuid": r["uuid"]})
                continue
            topic = (it.get("topic") or defaults.get("topic") or "").strip().upper() or None
            if topic and topic not in valid_topics:
                skipped.append({"name": src.name, "why": f"topic {topic} is not in the registry; add it first"})
                continue
            origin = it.get("origin") or defaults.get("origin", "D")
            typ = it.get("type") or defaults.get("type", "P")
            rid = f"{topic}-{origin}-{typ}-{_next_number(reg, topic, origin, typ):04d}" if topic else None
            if rid and not ID_RE.match(rid):
                raise ValueError(f"minted ID fails the spec grammar: {rid}")
            uid = str(uuid.uuid4())
            home = BASE / "files" / uid
            home.mkdir(parents=True)
            frozen = home / f"original{src.suffix.lower()}"
            shutil.copy2(src, frozen)
            norm_sha = None
            text = _text(raw) if src.suffix.lower() in TEXT else None
            if text is not None:
                (home / f"{uid}.norm.md").write_text(text, encoding="utf-8", newline="\n")
                norm_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            ingested = now()
            rec = {"event": "intake", "uuid": uid, "id": rid, "title": it.get("title") or src.stem,
                   "topic": topic, "origin": origin, "type": typ,
                   "register": defaults.get("register") or None, "lane": defaults.get("lane", "general"),
                   "collection": _collection(defaults, it), "source_sha256": sha, "norm_sha256": norm_sha,
                   "near_key": near_key(raw), "format": it["format"], "where": [str(src)],
                   "frozen_copy": str(frozen.relative_to(ROOT)), "written": it["written"], "ingested": ingested,
                   "near_duplicate_of": it.get("duplicate_of") if (it.get("duplicate") or "").startswith("near") else None,
                   "receipt": f"intake-{ingested[:19].replace(':', '').replace('-', '')}-{uid[:8]}"}
            _append(rec)
            reg.append(rec)
            by_sha[sha] = rec
            _write_sidecar(rec)
            done.append({"name": src.name, "id": rid, "uuid": uid})
    return {"done": done, "located": located, "skipped": skipped}


def _write_sidecar(rec):
    home = BASE / "files" / rec["uuid"]
    for old in home.glob("*.meta.yaml"):
        old.unlink()  # regenerated view; the registry is the truth
    (home / f"{rec.get('id') or rec['uuid']}.meta.yaml").write_text(sidecar(rec), encoding="utf-8")


def sidecar_text(uid):
    home = BASE / "files" / uid
    f = next(home.glob("*.meta.yaml"), None)
    return f.read_text(encoding="utf-8") if f else ""
