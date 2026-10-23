"""66_SORRY_AXIOM_AUDIT: every sorry / admit / axiom / native_decide in a Lean source, found in code first
(free, no API), then classified by one JSON call per file; the remediation docket puts blockers first.

  API-66.1 SORRY_AXIOM_AUDIT   classify each code-found occurrence -> <title> · 66_SORRYAUDIT[XX].md

Trust rules (the model proposes, code decides): the occurrences and their line numbers come from the code
scan, never from the model; classifications and severities outside the ruled vocabularies are coerced with a
logged warning; occurrences the model skipped get a code default. Nothing here compiles anything: a
classification is a triage note, not a verdict.

Inbox: this layer's own INBOX (00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>); one .lean file per item.
Outbox: this layer's OUTBOX — one docket per file plus 00_REMEDIATION_DOCKET.md, rebuilt after every item,
blockers first. Working folders stay in lean_work/layers/66_SORRY_AXIOM_AUDIT/.
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

LABEL = "66_SORRY_AXIOM_AUDIT"
HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
EXTENSIONS = {".lean"}
CLASSIFICATIONS = {"placeholder", "spec_by_design", "hard_gap", "copied_test", "intended_axiom"}
SEVERITIES = {"blocker", "cosmetic", "note"}
SEV_RANK = {"blocker": 0, "cosmetic": 1, "note": 2}
DEFAULTS = {"sorry": ("placeholder", "blocker"), "admit": ("placeholder", "blocker"),
            "native_decide": ("spec_by_design", "note"), "axiom": ("intended_axiom", "note")}
PROVIDER_TAGS = {"deepseek": "DS", "moonshot": "KIMI"}
MASTER_LOCK = threading.Lock()

TOKEN = re.compile(r"\b(sorry|admit|native_decide)\b")
AXIOM = re.compile(r"^\s*axiom\s+([A-Za-z_][\w'.]*)")
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


# ------------------------------------------------------------------ the free part: find every occurrence in code
def code_only(lines: list[str]) -> list[str]:
    """Each line with comments stripped (line comments -- and nested block comments /- -/)."""
    out, depth = [], 0
    for line in lines:
        kept, i = [], 0
        while i < len(line):
            two = line[i:i + 2]
            if depth == 0 and two == "--":
                break
            if two == "/-":
                depth += 1
                i += 2
                continue
            if two == "-/" and depth:
                depth -= 1
                i += 2
                continue
            if depth == 0:
                kept.append(line[i])
            i += 1
        out.append("".join(kept))
    return out


def scan(text: str) -> tuple[list[dict], list[str]]:
    lines = text.splitlines()
    code = code_only(lines)
    found, seen = [], set()
    for i, (src, cod) in enumerate(zip(lines, code), 1):
        kinds = [m.group(1) for m in TOKEN.finditer(cod)]
        if AXIOM.match(cod):
            kinds.append("axiom")
        for kind in kinds:
            if (i, kind) in seen:
                continue
            seen.add((i, kind))
            context = "\n".join(f"L{n}: {lines[n - 1]}" for n in range(max(1, i - 2), min(len(lines), i + 2) + 1))
            found.append({"line": i, "kind": kind, "code": src.strip(), "context": context})
    return found, lines


def declarations(text: str) -> list[str]:
    return DECL.findall(text)


# ------------------------------------------------------------------ trust rules (the model proposes, code decides)
def enforce(found: list[dict], replied: list[dict]) -> tuple[list[dict], list[str]]:
    log, by_line = [], {}
    real = {o["line"] for o in found}
    for r in replied:
        try:
            line = int(r.get("line"))
        except (TypeError, ValueError):
            log.append(f"entry without a usable line ({r.get('line')!r}); dropped")
            continue
        if line not in real:
            log.append(f"L{line}: not one of the code-found occurrences; dropped")
            continue
        if line in by_line:
            log.append(f"L{line}: classified twice; first answer kept")
            continue
        cls = str(r.get("classification", "")).lower()
        if cls not in CLASSIFICATIONS:
            log.append(f"L{line}: classification {cls or 'missing'} -> placeholder "
                       "(placeholder|spec_by_design|hard_gap|copied_test|intended_axiom only)")
            cls = "placeholder"
        sev = str(r.get("severity", "")).lower()
        if sev not in SEVERITIES:
            log.append(f"L{line}: severity {sev or 'missing'} -> note (blocker|cosmetic|note only)")
            sev = "note"
        by_line[line] = {"classification": cls, "severity": sev, "closes_with": str(r.get("closes_with", ""))}
    entries = []
    for o in found:
        if o["line"] in by_line:
            entries.append({k: v for k, v in {**o, **by_line[o["line"]]}.items() if k != "context"})
        else:
            cls, sev = DEFAULTS.get(o["kind"], ("placeholder", "note"))
            log.append(f"L{o['line']} ({o['kind']}): the model did not classify it; code default {cls}/{sev}")
            entries.append({k: v for k, v in o.items() if k != "context"} |
                           {"classification": cls, "severity": sev, "closes_with": ""})
    return entries, log


# ------------------------------------------------------------------ one source
def process(ctx):
    item, meta = ctx.item, ctx.item.meta
    found, lines = scan(ctx.text)
    ctx.step(f"{len(found)} occurrence(s) found in code ({meta['source_file']}, {len(lines)} lines)")
    receipt = {}
    if found:
        listing = "\n".join(f"OCC {o['line']} {o['kind']} | {o['code'][:120]}" for o in found)
        context = "\n\n".join(f"--- L{o['line']} ({o['kind']}):\n{o['context']}" for o in found)
        body = ((HERE / "PROMPT.md").read_text(encoding="utf-8")
                + f"\n\nFILE: {meta['source_file']}  ({meta['lane']} / {meta['group']})\nSHA256: {meta['source_hash']}"
                + f"\nDECLARATIONS: {', '.join(declarations(ctx.text)) or '(none found)'}"
                + f"\n\nOCCURRENCES (found in code; classify every one, match by line):\n{listing}\n\n{context}")
        reply = ctx.cached("audit", lambda: ctx.call_json("sorry_axiom_audit", body), extra=f"occ={len(found)}")
        if not isinstance(reply, dict):
            return None
        receipt = ctx.receipts[-1] if ctx.receipts else {}
        entries, log = enforce(found, [x for x in reply.get("occurrences") or [] if isinstance(x, dict)])
        for line in log:
            ctx.step(f"rule: {line}")
            ctx.warnings.append(line)
    else:
        entries = []
    tag = provider_tag(ctx)
    provider = receipt.get("provider") or ctx.args.provider
    model = receipt.get("model") or ctx.args.model
    blockers = sum(1 for e in entries if e["severity"] == "blocker")
    md = (f"# Sorry/axiom audit: {item.title}\n\n"
          f"> {meta['lane']} / {meta['group']} · source `{meta['source_file']}` · sha256 {meta['source_hash'][:8]} · "
          f"{provider}:{model} [{tag}]\n\n"
          f"**{len(entries)} occurrence(s), {blockers} blocker(s).** "
          "Occurrences and line numbers were found in code (free); the model only classified them. "
          "A classification is a triage note, not a verdict — nothing was compiled.\n\n"
          + table(sorted(entries, key=lambda e: (SEV_RANK[e["severity"]], e["line"])),
                  ["line", "kind", "classification", "severity", "closes_with", "code"]) + "\n")
    report = item.folder / "03_REPORT"
    report.mkdir(exist_ok=True)
    (report / "SORRYAUDIT.md").write_text(md, encoding="utf-8")
    (report / "sorryaudit.json").write_text(json.dumps(
        {"occurrences": entries, "source_file": meta["source_file"], "source_hash": meta["source_hash"],
         "provider": provider, "model": model, "provider_tag": tag}, indent=2, ensure_ascii=False), encoding="utf-8")
    ctx.step(f"{len(entries)} occurrence(s), {blockers} blocker(s) -> {report}")
    with MASTER_LOCK:
        outbox = FRONT / "OUTBOX"
        outbox.mkdir(exist_ok=True)
        from engine.ytnames import safe
        (outbox / f"{safe(item.title, 90)} · 66_SORRYAUDIT[{tag}].md").write_text(md, encoding="utf-8")
        rebuild_master(work_root(), outbox)
    ctx.step("master rebuilt: 00_REMEDIATION_DOCKET.md (blockers first)")
    return ItemResult({"occurrences": entries, "blockers": blockers, "lane": meta["lane"], "group": meta["group"]},
                      page(f"Sorry/axiom audit: {item.title}", markdown_to_html(md)),
                      {"occurrences": entries}, md,
                      {"sorry_occurrences": len(entries), "sorry_blockers": blockers})


# ------------------------------------------------------------------ the master docket, blockers first
def work_root() -> Path:
    return external("lean_work", create=True) / "layers" / LABEL


def done_items(work: Path) -> list[Path]:
    rank = {"priority": 0, "series": 1, "group": 2}
    folders = [p.parent for p in work.glob("*/*/*/lean.json") if (p.parent / "03_REPORT" / "sorryaudit.json").exists()]

    def key(f):
        meta = inbox.load_meta(f, "lean")
        return rank.get(meta.get("lane"), 3), str(meta.get("group", "")).lower(), str(meta.get("original_path", "")).lower()
    return sorted(folders, key=key)


def rebuild_master(work: Path, outbox: Path) -> None:
    rows, files, blockers = [], 0, 0
    for folder in done_items(work):
        meta = inbox.load_meta(folder, "lean")
        data = json.loads((folder / "03_REPORT" / "sorryaudit.json").read_text(encoding="utf-8"))
        files += 1
        for e in data.get("occurrences") or []:
            blockers += e.get("severity") == "blocker"
            rows.append({"file": meta["source_file"], "group": f"{meta['lane']}/{meta['group']}",
                         "line": e.get("line"), "kind": e.get("kind"), "classification": e.get("classification"),
                         "severity": e.get("severity"), "closes_with": e.get("closes_with"),
                         "provider_tag": data.get("provider_tag", "")})
    rows.sort(key=lambda r: (SEV_RANK.get(str(r["severity"]), 3), str(r["file"]).lower(), r["line"] or 0))
    md = [f"# Remediation docket — {LABEL}", "",
          f"{files} file(s) · {len(rows)} occurrence(s) · {blockers} blocker(s) — blockers first, then cosmetic, then notes.",
          "Code found the occurrences; the model classified them; nothing was compiled.", ""]
    for sev in ("blocker", "cosmetic", "note"):
        part = [r for r in rows if r["severity"] == sev]
        if part:
            md += [f"## {sev.title()}s ({len(part)})", "",
                   table(part, ["file", "line", "kind", "classification", "closes_with", "group"]), ""]
    (outbox / "00_REMEDIATION_DOCKET.md").write_text("\n".join(md), encoding="utf-8")


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
