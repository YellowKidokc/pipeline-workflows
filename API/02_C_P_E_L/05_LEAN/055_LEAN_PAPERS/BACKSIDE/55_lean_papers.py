"""55_LEAN_PAPERS: every Lean source (or claim written for Lean) in the Lean inbox becomes two papers, its claims in
the claim template, and a separate assumptions paper to review before anything is run.

One source = the whole file in every call (no chunking); 30+ sources side by side, each getting the same calls:
  API-55.1 LEAN_ASSUMPTIONS   every assumption, with line, kind, load-bearing          -> 4_ASSUMPTIONS.md
  API-55.2 LEAN_CLAIMS        the claims (at most 12) filled into templates/lean        -> 3_CLAIMS.md
  API-55.3 LEAN_FORMAL_PAPER  paper 1, for Lean readers           } side by side        -> 1_FORMAL.md
  API-55.4 LEAN_READER_PAPER  paper 2, for someone new to Lean    }                     -> 2_READER.md
  API-55.5 LEAN_CLAIM_LEDGER  theorem->claim reverse ledger, grades proposed           -> 5_CLAIMLEDGER.md
Claims never carry their assumptions: they point to them by id. Code enforces the trust rules (no LEAN_CERTIFIED from
the model; PASS only with a cited source line). The ledger's grades are suggestions: the model may never mark a
declaration FLOOR/VERIFIED without a cited build-receipt line (coerced to DRAFT), and ledger line numbers must
exist in the source.

Inbox (lean_inbox): 00_PRIORITY/, 01_SERIES/<series>/, 02_GENERAL/<group>/, run in that order (engine/inbox.py).
Outbox (lean_outbox): one flat folder. Every paper is printed into its root:
  <title> - 1 Formal.md, <title> - 2 Reader.md, <title> - 3 Claims.md, <title> - 4 Assumptions.md,
  <title> - 5 ClaimLedger[XX].md   (XX = the provider that answered: deepseek DS, moonshot KIMI, else uppercased)
and, rebuilt after every item:
  00_ALL_CLAIMS.md             every claim through the template, in inbox order
  00_ALL_ASSUMPTIONS.md        every assumptions paper, in the same order
  00_ALL_CLAIM_LEDGERS.md      every claim ledger, in the same order
  00_ASSUMPTIONS_REVIEW.xlsx   one row per assumption with a `review` column (your marks are kept on rebuild)
Working folders (receipts, every call, steps.log) stay out of sight in lean_work/<lane>/<group>/<item>/.
"""
import csv
import hashlib
import json
import re
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine import inbox  # noqa: E402
from engine.output import markdown_to_html, page, write_xlsx  # noqa: E402
from engine.paths import PathConfigurationError, external, inside  # noqa: E402
from engine.station import ItemResult, Station  # noqa: E402

LABEL = "55_LEAN_PAPERS"
HERE = Path(__file__).resolve().parent
EXTENSIONS = {".lean", ".md", ".txt", ".tex"}
READER_HEADINGS = ["What we claimed", "What we asked the computer to check", "What we went through",
                   "What the recorded result means", "What it does not mean", "Why it matters"]
FORMAL_HEADINGS = ["Scope", "Formal objects", "Main results", "Proof structure", "Trust boundary",
                   "What would change the result"]
ALLOWED_STATUS = {"NOT_ATTEMPTED", "CANDIDATE", "IN_PROGRESS", "FAILED"}
LEDGER_GRADES = {"FLOOR", "VERIFIED", "DRAFT", "PROSE"}
LEDGER_KINDS = {"theorem", "lemma", "def", "instance", "structure", "inductive"}
PROVIDER_TAGS = {"deepseek": "DS", "moonshot": "KIMI"}
MASTER_LOCK = threading.Lock()


def provider_tag(ctx) -> str:
    """The [XX] in output names: from the provider that actually answered (last receipt), else the one asked for."""
    provider = ""
    for receipt in reversed(ctx.receipts):
        provider = receipt.get("provider") or ""
        if provider:
            break
    provider = provider or getattr(ctx.args, "provider", "") or ""
    return PROVIDER_TAGS.get(provider, provider.upper() or "API")


def args(p):
    p.add_argument("--lane", choices=["priority", "series", "group"], help="only this lane of the inbox")
    p.add_argument("--group", help="only this series / group (folder name)")


def template(name: str) -> str:
    return inside("templates", "lean", name).read_text(encoding="utf-8")


def fill(text: str, values: dict) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), "") or "—"), text)


def table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "—"
    cell = lambda v: str(v if v not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
                     + ["| " + " | ".join(cell(r.get(c)) for c in cols) + " |" for r in rows])


# ------------------------------------------------------------------ trust rules (the model proposes, code decides)
def enforce(claims: list[dict], assumption_ids: set[str]) -> list[str]:
    log = []
    for c in claims:
        status = str(c.get("verification_status", "")).upper()
        if status not in ALLOWED_STATUS:
            log.append(f"{c.get('claim_id')}: status {status or 'missing'} -> CANDIDATE (only the compiler certifies)")
            c["verification_status"] = "CANDIDATE"
        for ctl in c.get("controls") or []:
            if str(ctl.get("status", "")).upper() == "PASS" and not re.search(r"\bL\d+", str(ctl.get("command_or_evidence", ""))):
                ctl["status"] = "NOT_RUN"
                log.append(f"{c.get('claim_id')}: control '{ctl.get('check')}' PASS without a cited source line -> NOT_RUN")
        used = [a for a in (c.get("uses_assumptions") or []) if a in assumption_ids]
        if len(used) != len(c.get("uses_assumptions") or []):
            log.append(f"{c.get('claim_id')}: dropped unknown assumption ids")
        c["uses_assumptions"] = used
    return log


DECL_LINE = re.compile(r"^\s*(?:theorem|lemma|def|instance|structure|inductive|abbrev|axiom)\s+([A-Za-z_][\w'.]*)")


def enforce_ledger(entries: list[dict], lines: list[str]) -> list[str]:
    """The model proposes grades; only a cited build receipt certifies. FLOOR/VERIFIED without one -> DRAFT,
    and a ledger line that does not exist in the source is repaired by name or dropped."""
    log = []

    def declared_at(name) -> int | None:
        want = str(name or "")
        for i, ln in enumerate(lines, 1):
            m = DECL_LINE.match(ln)
            if m and m.group(1).split(".")[-1] == want.split(".")[-1]:
                return i
        return None

    for e in entries:
        grade = str(e.get("grade_suggestion", "")).upper()
        if grade not in LEDGER_GRADES:
            log.append(f"{e.get('name')}: grade {grade or 'missing'} -> DRAFT (FLOOR|VERIFIED|DRAFT|PROSE only)")
            grade = "DRAFT"
        if grade in ("FLOOR", "VERIFIED"):
            cited = re.search(r"\bL(\d+)\b", str(e.get("grade_evidence", "")))
            if not cited or not (1 <= int(cited.group(1)) <= len(lines)):
                log.append(f"{e.get('name')}: {grade} without a cited build-receipt line -> DRAFT "
                           "(only a build receipt certifies)")
                grade = "DRAFT"
        e["grade_suggestion"] = grade
        kind = str(e.get("kind", "")).lower()
        if kind not in LEDGER_KINDS:
            log.append(f"{e.get('name')}: kind {kind or 'missing'} -> def (theorem|lemma|def|instance|structure|inductive only)")
            kind = "def"
        e["kind"] = kind
        try:
            line = int(e.get("line"))
        except (TypeError, ValueError):
            line = None
        if line is None or not (1 <= line <= len(lines)):
            found = declared_at(e.get("name"))
            if found:
                log.append(f"{e.get('name')}: line {e.get('line')} not in source -> L{found} (declaration found by name)")
                line = found
            else:
                log.append(f"{e.get('name')}: line {e.get('line')} not in source, no declaration of that name -> line dropped")
                line = None
        e["line"] = line
    return log


def headings_ok(text: str, wanted: list[str]) -> bool:
    return re.findall(r"^## (.+?)\s*$", text or "", re.M) == wanted


# ------------------------------------------------------------------ one source
def process(ctx):
    item, meta = ctx.item, ctx.item.meta
    words = len(ctx.text.split())
    limit = ctx.station.settings.get("context_words", 60000)
    if words > limit:
        ctx.errors.append(f"{words:,} words is more than one call takes ({limit:,}); split the file yourself "
                          "or raise context_words in settings.json (it is never chunked)")
        return None
    numbered = "\n".join(f"L{i}: {line}" for i, line in enumerate(ctx.text.splitlines(), 1))
    head = f"SOURCE: {meta['source_file']}  ({meta['lane']} / {meta['group']})\nSHA256: {meta['source_hash']}\n"
    ctx.step(f"{meta['lane']} / {meta['group']} · {words:,} words · whole file in every call")

    a = ctx.cached("assumptions", lambda: ctx.call_json(
        "lean_assumptions", (HERE / "ASSUMPTIONS_PROMPT.md").read_text(encoding="utf-8") + f"\n\n{head}\n{numbered}"))
    if not isinstance(a, dict):
        return None
    assumptions = [x for x in a.get("assumptions") or [] if isinstance(x, dict)]
    ids = {str(x.get("id")) for x in assumptions}
    listing = "\n".join(f"{x.get('id')} [{x.get('kind')}] {x.get('statement')} ({x.get('where')})" for x in assumptions)

    c = ctx.cached("claims", lambda: ctx.call_json(
        "lean_claims", (HERE / "PROMPT.md").read_text(encoding="utf-8")
        + f"\n\nASSUMPTIONS:\n{listing or '(none listed)'}\n\n{head}\n{numbered}"), extra=f"a={len(assumptions)}")
    if not isinstance(c, dict):
        return None
    claims = [x for x in c.get("claims") or [] if isinstance(x, dict)]
    for line in enforce(claims, ids):
        ctx.step(f"rule: {line}")
        ctx.warnings.append(line)
    brief = json.dumps({"claims": claims, "assumptions": assumptions}, ensure_ascii=False)

    le = ctx.cached("claim_ledger", lambda: ctx.call_json(
        "lean_claim_ledger", (HERE / "CLAIM_LEDGER_PROMPT.md").read_text(encoding="utf-8")
        + f"\n\nCLAIMS AND ASSUMPTIONS:\n{brief}\n\n{head}\n{numbered}"), extra=f"a={len(assumptions)};c={len(claims)}")
    if not isinstance(le, dict):
        return None
    ledger = [x for x in le.get("ledger") or [] if isinstance(x, dict)]
    for line in enforce_ledger(ledger, ctx.text.splitlines()):
        ctx.step(f"rule: {line}")
        ctx.warnings.append(line)
    tag = provider_tag(ctx)
    le_receipt = ctx.receipts[-1] if ctx.receipts else {}
    ledger_md = (f"# Claim ledger: {item.title}\n\n"
                 f"> source `{meta['source_file']}` · sha256 {meta['source_hash'][:8]} · "
                 f"{le_receipt.get('provider') or ctx.args.provider}:{le_receipt.get('model') or ctx.args.model} [{tag}]\n\n"
                 "Grades are suggestions: FLOOR/VERIFIED stand only with a cited build receipt, everything else "
                 "is DRAFT until the compiler rules.\n\n"
                 + table(ledger, ["name", "line", "kind", "grade_suggestion", "receipts_claim",
                                  "plain_statement", "does_not_prove"]) + "\n")

    def paper(job):
        task, prompt_file, with_source = job
        body = (HERE / prompt_file).read_text(encoding="utf-8") + f"\n\nCLAIMS AND ASSUMPTIONS:\n{brief}"
        body += f"\n\n{head}\n{numbered}" if with_source else ""
        return ctx.cached(task, lambda: ctx.call_text(task, body), extra=str(len(brief)))
    formal, reader = ctx.parallel(paper, [("lean_formal_paper", "FORMAL_PAPER_PROMPT.md", True),
                                          ("lean_reader_paper", "READER_PROMPT.md", False)], width=2)
    for text, wanted, name in ((formal, FORMAL_HEADINGS, "formal paper"), (reader, READER_HEADINGS, "reader paper")):
        if text and not headings_ok(text, wanted):
            ctx.warnings.append(f"{name}: headings differ from the required ones; kept, marked REVIEW")

    values = {"title": item.title, "lane": meta["lane"], "group": meta["group"], "source_file": meta["source_file"],
              "sha8": meta["source_hash"][:8]}
    claim_md = "\n\n".join(fill(template("CLAIM_TEMPLATE.md"), {
        **values, **cl, "symbols": table(cl.get("symbols") or [], ["term", "formal_definition", "reader_meaning"]),
        "controls": table(cl.get("controls") or [], ["check", "command_or_evidence", "status", "interpretation"]),
        "uses_assumptions": ", ".join(cl.get("uses_assumptions") or []) or "none"}) for cl in claims)
    if c.get("other_declarations"):
        claim_md += "\n\n**Other declarations in this source:** " + ", ".join(f"`{d}`" for d in c["other_declarations"])
    assumption_md = fill(template("ASSUMPTIONS_TEMPLATE.md"), {
        **values, "review_status": "PENDING REVIEW",
        "table": table(assumptions, ["id", "kind", "statement", "where", "load_bearing", "why"]),
        "paper": a.get("assumptions_paper", "")})

    report = item.folder / "03_REPORT"
    report.mkdir(exist_ok=True)
    files = {"1_FORMAL.md": formal or "", "2_READER.md": reader or "", "3_CLAIMS.md": f"# Claims: {item.title}\n\n{claim_md}\n",
             "4_ASSUMPTIONS.md": assumption_md, "5_CLAIMLEDGER.md": ledger_md}
    for name, text in files.items():
        (report / name).write_text(text, encoding="utf-8")
    (report / "claims.json").write_text(json.dumps({"claims": claims, "other": c.get("other_declarations", [])},
                                                   indent=2, ensure_ascii=False), encoding="utf-8")
    (report / "assumptions.json").write_text(json.dumps(assumptions, indent=2, ensure_ascii=False), encoding="utf-8")
    (report / "claimledger.json").write_text(json.dumps(
        {"ledger": ledger, "source_file": meta["source_file"], "source_hash": meta["source_hash"],
         "provider": le_receipt.get("provider") or ctx.args.provider,
         "model": le_receipt.get("model") or ctx.args.model, "provider_tag": tag},
        indent=2, ensure_ascii=False), encoding="utf-8")
    ctx.step(f"{len(claims)} claim(s), {len(assumptions)} assumption(s), {len(ledger)} ledger entrie(s) -> {report}")
    with MASTER_LOCK:
        outbox = external("lean_outbox", create=True)
        stamp = f"> {meta['lane']} / {meta['group']} · source `{meta['source_file']}`\n\n"
        for name, text in files.items():
            (outbox / flat_name(item, name, tag if name == "5_CLAIMLEDGER.md" else "")).write_text(stamp + text, encoding="utf-8")
        rebuild_masters(external("lean_work"), outbox)
    ctx.step("master files rebuilt: 00_ALL_CLAIMS.md, 00_ALL_ASSUMPTIONS.md, 00_ALL_CLAIM_LEDGERS.md, 00_ASSUMPTIONS_REVIEW.xlsx")
    data = {"claims": claims, "assumptions": assumptions, "ledger": ledger, "lane": meta["lane"], "group": meta["group"]}
    md = "\n\n---\n\n".join(files.values())
    return ItemResult(data, page(item.title, markdown_to_html(md)),
                      {"claims": [{k: v for k, v in cl.items() if k not in ("symbols", "controls")} for cl in claims],
                       "assumptions": assumptions}, md,
                      {"lean_claims": len(claims), "lean_assumptions": len(assumptions),
                       "lean_ledger_entries": len(ledger)})


# ------------------------------------------------------------------ the masters, in inbox order
PAPER_NAMES = {"1_FORMAL.md": "1 Formal", "2_READER.md": "2 Reader", "3_CLAIMS.md": "3 Claims",
               "4_ASSUMPTIONS.md": "4 Assumptions", "5_CLAIMLEDGER.md": "5 ClaimLedger"}


def flat_name(item, name: str, tag: str = "") -> str:
    """<title> - 1 Formal.md in the outbox root; the source hash keeps two same-titled sources apart.
    The claim ledger carries the answering provider: <title> - 5 ClaimLedger[DS].md"""
    from engine.ytnames import safe
    title = safe(item.title, 90)
    paper = PAPER_NAMES[name] + (f"[{tag}]" if tag else "")
    taken = external("lean_outbox") / f"{title} - {paper}.md"
    if taken.exists() and item.meta["source_file"] not in taken.read_text(encoding="utf-8", errors="replace")[:4000]:
        title = f"{title} ({item.meta['source_hash'][:6]})"
    return f"{title} - {paper}.md"


def done_items(work: Path) -> list[Path]:
    rank = {"priority": 0, "series": 1, "group": 2}
    folders = [p.parent for p in work.glob("*/*/*/lean.json") if (p.parent / "03_REPORT" / "claims.json").exists()]
    def key(f):
        meta = inbox.load_meta(f, "lean")
        return rank.get(meta.get("lane"), 3), str(meta.get("group", "")).lower(), str(meta.get("original_path", "")).lower()
    return sorted(folders, key=key)


def read_reviews(path: Path) -> dict[str, str]:
    try:
        from openpyxl import load_workbook
        ws = load_workbook(path, read_only=True).worksheets[0]
    except Exception:  # no workbook yet, or openpyxl missing
        return {}
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return {}
    head = [str(h) for h in rows[0]]
    if "key" not in head or "review" not in head:
        return {}
    k, r = head.index("key"), head.index("review")
    return {str(row[k]): str(row[r]) for row in rows[1:] if row[r] not in (None, "")}


def rebuild_masters(work: Path, outbox: Path) -> None:
    claims_md, assumptions_md, ledgers_md, rows = ["# All claims", ""], ["# All assumptions", ""], ["# All claim ledgers", ""], []
    xlsx = outbox / "00_ASSUMPTIONS_REVIEW.xlsx"
    reviews = read_reviews(xlsx)
    current = None
    for folder in done_items(work):
        meta = inbox.load_meta(folder, "lean")
        heading = f"{meta['lane'].title()} · {meta['group']}"
        if heading != current:
            claims_md += [f"# {heading}", ""]
            assumptions_md += [f"# {heading}", ""]
            ledgers_md += [f"# {heading}", ""]
            current = heading
        claims_md += [re.sub(r"^# ", "## ", (folder / "03_REPORT" / "3_CLAIMS.md").read_text(encoding="utf-8"), count=1), ""]
        assumptions_md += [(folder / "03_REPORT" / "4_ASSUMPTIONS.md").read_text(encoding="utf-8"), ""]
        ledger_file = folder / "03_REPORT" / "5_CLAIMLEDGER.md"
        if ledger_file.exists():  # items from before the ledger goal have none
            ledgers_md += [re.sub(r"^# ", "## ", ledger_file.read_text(encoding="utf-8"), count=1), ""]
        for a in json.loads((folder / "03_REPORT" / "assumptions.json").read_text(encoding="utf-8")):
            key = f"{meta['id']}:{a.get('id')}:{hashlib.sha256(str(a.get('statement')).encode()).hexdigest()[:8]}"
            rows.append({"key": key, "lane": meta["lane"], "group": meta["group"], "source": meta["source_file"],
                         "id": a.get("id"), "kind": a.get("kind"), "statement": a.get("statement"),
                         "where": a.get("where"), "load_bearing": a.get("load_bearing"), "why": a.get("why"),
                         "review": reviews.get(key, "")})
    (outbox / "00_ALL_CLAIMS.md").write_text("\n".join(claims_md), encoding="utf-8")
    (outbox / "00_ALL_ASSUMPTIONS.md").write_text("\n".join(assumptions_md), encoding="utf-8")
    (outbox / "00_ALL_CLAIM_LEDGERS.md").write_text("\n".join(ledgers_md), encoding="utf-8")
    if not write_xlsx(xlsx, {"assumptions": rows}):
        with open(outbox / "00_ASSUMPTIONS_REVIEW.tsv", "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["key"], delimiter="\t")
            w.writeheader()
            w.writerows(rows)


def items(station):
    a = station.args
    try:
        box = external("lean_inbox", create=True)
        out = external("lean_work", create=True)
    except PathConfigurationError as exc:
        print(f"{LABEL}: {exc}", file=sys.stderr)
        return []
    inbox.ensure_layout(box)
    entries = [e for e in inbox.scan(box, EXTENSIONS)
               if (not a.lane or e.lane == a.lane) and (not a.group or e.group.lower() == a.group.lower())]
    if a.items:
        wanted = {Path(i).name for i in a.items}
        entries = [e for e in entries if e.path.name in wanted]
    entries = entries[: a.limit] if a.limit else entries
    return [inbox.ensure_item(e, out, "lean") for e in entries]


if __name__ == "__main__":
    st = Station(LABEL, kind="lean", extra_args=args,
                 prompt_files=["ASSUMPTIONS_PROMPT.md", "PROMPT.md", "FORMAL_PAPER_PROMPT.md", "READER_PROMPT.md",
                               "CLAIM_LEDGER_PROMPT.md"])
    found = items(st)
    if not found:
        print(f"{LABEL}: nothing in the Lean inbox. Put .lean / .md files in lean_inbox "
              "(00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>).")
        raise SystemExit(0)
    raise SystemExit(st.run(process, items=found))
