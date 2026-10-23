"""68_FORMALIZE_TARGETS: one claim in (a markdown note from a canon docket; HOLD claims especially), one
proposed Lean 4 statement out.

  API-68.1 FORMALIZE_TARGETS   claim -> proposed compilable-looking Lean 4 statement -> <title> · 68_FORMALIZE[XX].md

Trust rule (the model proposes, code decides): every output is labelled PROPOSED — never VERIFIED, never
FLOOR. The compiler adjudicates later; a Lean build receipt is the only certification. Code stamps the status
on top of whatever the model said, and warns when the model overclaimed.

Inbox: this layer's own INBOX (00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>); one claim note (.md/.txt)
per item. Outbox: this layer's OUTBOX — one <title> · 68_FORMALIZE[XX].md per claim. Working folders stay in
lean_work/layers/68_FORMALIZE_TARGETS/.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine import inbox  # noqa: E402
from engine.output import markdown_to_html, page  # noqa: E402
from engine.paths import PathConfigurationError, external  # noqa: E402
from engine.station import ItemResult, Station  # noqa: E402

LABEL = "68_FORMALIZE_TARGETS"
HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
EXTENSIONS = {".md", ".txt"}
PROVIDER_TAGS = {"deepseek": "DS", "moonshot": "KIMI"}
STATUS = "PROPOSED"   # the only status this station ever writes; the compiler adjudicates later

DECL_KEYWORD = re.compile(r"\b(theorem|lemma|def|axiom|instance|structure|inductive|example)\b")


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


# ------------------------------------------------------------------ trust rules (the model proposes, code decides)
def enforce(reply: dict) -> tuple[dict, list[str]]:
    log = []
    offered = str(reply.get("status") or reply.get("grade") or reply.get("verification_status") or "")
    if offered and offered.upper() != STATUS:
        log.append(f"status {offered} -> PROPOSED (this station proposes; only the compiler certifies)")
    proposed = str(reply.get("proposed_lean", ""))
    if proposed and not DECL_KEYWORD.search(proposed):
        log.append("proposed_lean has no declaration keyword (theorem/def/...); kept, marked REVIEW")
        reply["needs_review"] = True
    reply["status"] = STATUS
    return reply, log


def render(item, meta, r: dict, tag: str, provider: str, model: str) -> str:
    slots = r.get("slot_refs") or []
    out = [f"# Formalization target: {item.title}", "",
           f"> {meta['lane']} / {meta['group']} · source `{meta['source_file']}` · {provider}:{model} [{tag}]", "",
           f"**Status: {STATUS}** — proposed by the model, labelled by code. The compiler adjudicates later; "
           "only a Lean build receipt certifies.", "",
           f"**Claim:** {r.get('claim_id', '')}", "",
           "## Proposed Lean 4", "",
           "```lean", str(r.get("proposed_lean", "")).strip(), "```", "",
           f"- **Confidence:** {r.get('confidence', '')}",
           f"- **Slot refs:** {', '.join(f'`{s}`' for s in slots) if slots else 'none'}", "",
           "## What it would prove", "", str(r.get("what_it_would_prove", "")), "",
           "## What it would NOT prove", "", str(r.get("what_it_would_not_prove", "")), ""]
    if r.get("needs_review"):
        out += ["> REVIEW: the proposed statement has no declaration keyword; read it before handing it to Lean.", ""]
    return "\n".join(out)


# ------------------------------------------------------------------ one claim
def process(ctx):
    item, meta = ctx.item, ctx.item.meta
    words = len(ctx.text.split())
    ctx.step(f"{meta['lane']} / {meta['group']} · {words:,} words · one claim, one call")
    body = ((HERE / "PROMPT.md").read_text(encoding="utf-8")
            + f"\n\nITEM: {item.id}\nSOURCE: {meta['source_file']}  ({meta['lane']} / {meta['group']})"
            + f"\nSHA256: {meta['source_hash']}\n\nCLAIM NOTE:\n{ctx.text}")
    reply = ctx.cached("formalize", lambda: ctx.call_json("formalize_targets", body))
    if not isinstance(reply, dict):
        return None
    receipt = ctx.receipts[-1] if ctx.receipts else {}
    reply, log = enforce(reply)
    for line in log:
        ctx.step(f"rule: {line}")
        ctx.warnings.append(line)
    tag = provider_tag(ctx)
    provider = receipt.get("provider") or ctx.args.provider
    model = receipt.get("model") or ctx.args.model
    md = render(item, meta, reply, tag, provider, model)
    report = item.folder / "03_REPORT"
    report.mkdir(exist_ok=True)
    (report / "FORMALIZE.md").write_text(md, encoding="utf-8")
    (report / "formalize.json").write_text(json.dumps(
        {**reply, "source_file": meta["source_file"], "source_hash": meta["source_hash"],
         "provider": provider, "model": model, "provider_tag": tag}, indent=2, ensure_ascii=False), encoding="utf-8")
    ctx.step(f"target PROPOSED (confidence {reply.get('confidence', '—')}) -> {report}")
    outbox = FRONT / "OUTBOX"
    outbox.mkdir(exist_ok=True)
    from engine.ytnames import safe
    (outbox / f"{safe(item.title, 90)} · 68_FORMALIZE[{tag}].md").write_text(md, encoding="utf-8")
    return ItemResult({**reply, "lane": meta["lane"], "group": meta["group"]},
                      page(f"Formalization target: {item.title}", markdown_to_html(md)),
                      {"formalize": [reply]}, md, {"formalize_status": STATUS})


# ------------------------------------------------------------------ items: this layer's own INBOX, or files named on the command line
def work_root() -> Path:
    return external("lean_work", create=True) / "layers" / LABEL


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
        print(f"{LABEL}: nothing in the inbox. Put claim notes (.md) in {FRONT / 'INBOX'} "
              "(00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>).")
        raise SystemExit(0)
    raise SystemExit(st.run(process, items=found))
