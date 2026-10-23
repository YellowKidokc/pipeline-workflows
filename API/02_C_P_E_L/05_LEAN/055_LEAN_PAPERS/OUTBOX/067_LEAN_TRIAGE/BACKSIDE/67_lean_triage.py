"""67_LEAN_TRIAGE: whole-corpus triage, one compact JSON call per Lean file.

  API-67.1 LEAN_TRIAGE   file kind, one-line purpose, quality, duplicate hint, action -> 00_TRIAGE.md

Files up to ~2000 lines go in whole; a longer file goes in as its first 400 lines plus the declaration list,
marked "partial". The prompt is short and the per-call tokens small on purpose: this is the pass that runs over
the whole vault.

Trust rules (the model proposes, code decides): file_kind / quality / action outside the ruled vocabularies are
coerced with a logged warning. `delete_candidate` is a label for David; code never deletes anything. Floor
nominations are nominations: only a build receipt puts a file on the floor.

Inbox: this layer's own INBOX (00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>); one .lean file per item.
Outbox: this layer's OUTBOX — <title> · 67_TRIAGE[XX].md per file plus 00_TRIAGE.md, rebuilt after every item,
sorted by action. Working folders stay in lean_work/layers/67_LEAN_TRIAGE/.
"""
import json
import re
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine import inbox  # noqa: E402
from engine.output import markdown_to_html, page  # noqa: E402
from engine.paths import PathConfigurationError, external  # noqa: E402
from engine.station import ItemResult, Station  # noqa: E402

LABEL = "67_LEAN_TRIAGE"
HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
EXTENSIONS = {".lean"}
WHOLE_LIMIT = 2000     # lines; longer files go in as a head plus the declaration list
HEAD_LINES = 400
FILE_KINDS = {"proof", "spec", "scratch", "test", "docs_extract", "duplicate"}
QUALITIES = {"floor_candidate", "solid", "draft", "noise"}
ACTIONS = {"nominate_floor", "keep", "archive", "delete_candidate"}
ACTION_RANK = {"nominate_floor": 0, "keep": 1, "archive": 2, "delete_candidate": 3}
PROVIDER_TAGS = {"deepseek": "DS", "moonshot": "KIMI"}
MASTER_LOCK = threading.Lock()

DECL = re.compile(r"^\s*(?:theorem|lemma|def|instance|structure|inductive|abbrev|axiom|namespace|class)"
                  r"\s+([A-Za-z_][\w'.]*)", re.M)


def args(p):
    p.add_argument("--lane", choices=["priority", "series", "group"], help="only this lane of the inbox")
    p.add_argument("--group", help="only this series / group (folder name)")


def provider_tag(ctx) -> str:
    """The [XX] in output names: from the provider that actually answered (last receipt), else the one asked for."""
    provider = ""
    for receipt in reversed(ctx.receipts):
        provider = receipt.get("provider") or ""
        if provider:
            break
    provider = provider or getattr(ctx.args, "provider", "") or ""
    return PROVIDER_TAGS.get(provider, provider.upper() or "API")


def table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "—"
    cell = lambda v: str(v if v not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
                     + ["| " + " | ".join(cell(r.get(c)) for c in cols) + " |" for r in rows])


def payload(text: str) -> tuple[str, bool]:
    """(what the model sees, partial?). Long files: head + declaration list, so the call stays cheap."""
    lines = text.splitlines()
    if len(lines) <= WHOLE_LIMIT:
        return text, False
    head = "\n".join(lines[:HEAD_LINES])
    decls = DECL.findall(text)
    return (head + f"\n\n[PARTIAL FILE: first {HEAD_LINES} of {len(lines)} lines; declarations of the whole file:]\n"
            + "\n".join(decls)), True


# ------------------------------------------------------------------ trust rules (the model proposes, code decides)
def enforce(reply: dict) -> tuple[dict, list[str]]:
    log = []
    kind = str(reply.get("file_kind", "")).lower()
    if kind not in FILE_KINDS:
        log.append(f"file_kind {kind or 'missing'} -> scratch (proof|spec|scratch|test|docs_extract|duplicate only)")
        kind = "scratch"
    quality = str(reply.get("quality", "")).lower()
    if quality not in QUALITIES:
        log.append(f"quality {quality or 'missing'} -> draft (floor_candidate|solid|draft|noise only)")
        quality = "draft"
    action = str(reply.get("action", "")).lower()
    if action not in ACTIONS:
        log.append(f"action {action or 'missing'} -> keep (nominate_floor|keep|archive|delete_candidate only)")
        action = "keep"
    if action == "nominate_floor" and quality != "floor_candidate":
        log.append("nominate_floor without floor_candidate quality -> quality floor_candidate (they travel together)")
        quality = "floor_candidate"
    return {"file_kind": kind, "one_line_purpose": str(reply.get("one_line_purpose", "")),
            "quality": quality, "duplicate_of_hint": str(reply.get("duplicate_of_hint", "")), "action": action}, log


# ------------------------------------------------------------------ one source
def process(ctx):
    item, meta = ctx.item, ctx.item.meta
    body_text, partial = payload(ctx.text)
    n_lines = len(ctx.text.splitlines())
    ctx.step(f"{meta['lane']} / {meta['group']} · {n_lines} line(s)" + (" · PARTIAL (head + declarations)" if partial else ""))
    body = ((HERE / "PROMPT.md").read_text(encoding="utf-8")
            + f"\n\nFILE: {meta['source_file']}  ({meta['lane']} / {meta['group']})"
            + f"\nLINES: {n_lines}  PARTIAL: {'yes' if partial else 'no'}\n\n{body_text}")
    reply = ctx.cached("triage", lambda: ctx.call_json("lean_triage", body), extra=f"partial={partial}")
    if not isinstance(reply, dict):
        return None
    receipt = ctx.receipts[-1] if ctx.receipts else {}
    verdict, log = enforce(reply)
    for line in log:
        ctx.step(f"rule: {line}")
        ctx.warnings.append(line)
    tag = provider_tag(ctx)
    provider = receipt.get("provider") or ctx.args.provider
    model = receipt.get("model") or ctx.args.model
    verdict.update({"file": meta["source_file"], "lane": meta["lane"], "group": meta["group"],
                    "lines": n_lines, "partial": partial, "provider": provider, "model": model, "provider_tag": tag})
    md = (f"# Triage: {item.title}\n\n"
          f"> {meta['lane']} / {meta['group']} · source `{meta['source_file']}` · {n_lines} line(s)"
          f"{' · PARTIAL' if partial else ''} · {provider}:{model} [{tag}]\n\n"
          f"**{verdict['action']}** · {verdict['file_kind']} · {verdict['quality']} — {verdict['one_line_purpose']}"
          + (f"\n\nPossible duplicate of: {verdict['duplicate_of_hint']}" if verdict["duplicate_of_hint"] else "")
          + "\n\n`delete_candidate` is a label, never a deletion. `nominate_floor` is a nomination: "
            "only a build receipt puts a file on the floor.\n")
    report = item.folder / "03_REPORT"
    report.mkdir(exist_ok=True)
    (report / "TRIAGE.md").write_text(md, encoding="utf-8")
    (report / "triage.json").write_text(json.dumps(verdict, indent=2, ensure_ascii=False), encoding="utf-8")
    ctx.step(f"{verdict['action']} · {verdict['file_kind']} · {verdict['quality']} -> {report}")
    with MASTER_LOCK:
        outbox = FRONT / "OUTBOX"
        outbox.mkdir(exist_ok=True)
        from engine.ytnames import safe
        (outbox / f"{safe(item.title, 90)} · 67_TRIAGE[{tag}].md").write_text(md, encoding="utf-8")
        rebuild_master(work_root(), outbox)
    ctx.step("master rebuilt: 00_TRIAGE.md (sorted by action)")
    return ItemResult(verdict, page(f"Triage: {item.title}", markdown_to_html(md)), {"triage": [verdict]}, md,
                      {"triage_action": verdict["action"]})


# ------------------------------------------------------------------ the master table, sorted by action
def work_root() -> Path:
    return external("lean_work", create=True) / "layers" / LABEL


def done_items(work: Path) -> list[Path]:
    rank = {"priority": 0, "series": 1, "group": 2}
    folders = [p.parent for p in work.glob("*/*/*/lean.json") if (p.parent / "03_REPORT" / "triage.json").exists()]

    def key(f):
        meta = inbox.load_meta(f, "lean")
        return rank.get(meta.get("lane"), 3), str(meta.get("group", "")).lower(), str(meta.get("original_path", "")).lower()
    return sorted(folders, key=key)


def rebuild_master(work: Path, outbox: Path) -> None:
    rows = []
    for folder in done_items(work):
        rows.append(json.loads((folder / "03_REPORT" / "triage.json").read_text(encoding="utf-8")))
    rows.sort(key=lambda r: (ACTION_RANK.get(str(r.get("action")), 4), str(r.get("file", "")).lower()))
    md = [f"# Triage — {LABEL}", "",
          f"{len(rows)} file(s), sorted by action. Nominations are nominations: only a build receipt certifies. "
          "delete_candidate is a label for David; nothing is deleted here.", "",
          table(rows, ["file", "action", "file_kind", "quality", "one_line_purpose", "duplicate_of_hint",
                       "partial", "provider_tag", "group"]), ""]
    (outbox / "00_TRIAGE.md").write_text("\n".join(md), encoding="utf-8")


# ------------------------------------------------------------------ items: this layer's own INBOX, or files named on the command line
def selected_files(raw_items) -> list[Path]:
    out = []
    for raw in raw_items:
        if raw.startswith("@"):
            listfile = Path(raw[1:])
            if listfile.is_file():
                out += [Path(l.strip().strip('"')) for l in listfile.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
        else:
            out.append(Path(raw))
    files = []
    for p in out:
        if p.is_file() and p.suffix.lower() in EXTENSIONS:
            files.append(p)
        elif p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.suffix.lower() in EXTENSIONS
                            and not f.name.startswith(("_", ".")) and not {".git", ".lake", "__pycache__"} & set(f.parts))
    return list(dict.fromkeys(files))


def items(station):
    a = station.args
    box = FRONT / "INBOX"
    inbox.ensure_layout(box)
    try:
        out = work_root()
    except PathConfigurationError as exc:
        print(f"{LABEL}: {exc}", file=sys.stderr)
        return []
    picked = selected_files(a.items)
    if picked:
        entries = [inbox.Entry(p, "group", "Selected") for p in picked]
    else:
        entries = [e for e in inbox.scan(box, EXTENSIONS)
                   if (not a.lane or e.lane == a.lane) and (not a.group or e.group.lower() == a.group.lower())]
    entries = entries[: a.limit] if a.limit else entries
    return [inbox.ensure_item(e, out, "lean") for e in entries]


if __name__ == "__main__":
    st = Station(LABEL, kind="lean", extra_args=args, prompt_files=["PROMPT.md"])
    found = items(st)
    if not found:
        print(f"{LABEL}: nothing in the inbox. Put .lean files in {FRONT / 'INBOX'} "
              "(00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>).")
        raise SystemExit(0)
    raise SystemExit(st.run(process, items=found))
