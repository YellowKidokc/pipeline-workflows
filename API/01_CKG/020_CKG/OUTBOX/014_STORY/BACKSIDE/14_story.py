"""14_STORY: Story Material System v1.0 (David, 2026-09-28) on each transcript: compact, traceable records for original
writing. A layer of the CKG; its cards go at the BOTTOM of the transcript page (the bottom is always the story).

  1 read   the transcript in overlapping sections of ~2,500 words (one call each, API-14.1), so no reply hits the cap
  2 spine  one small call over every record's gist, in order, for the whole-presentation spine (API-14.2)
  3 code   what the spec asks and a model cannot promise: stable IDs, duplicates merged (all spans kept), labels outside
           the vocabulary moved to notes, every transcript_wording checked character-for-character against the
           transcript (only a quote really there is source_checked), the transcript's sha256, honest coverage notes

Writes <note> · 14_STORY.md: the machine record (first fenced YAML block, schema 1.0) and readable cards by kind.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.output import markdown_to_html, page  # noqa: E402
from engine.station import ItemResult, Station  # noqa: E402

LABEL = "14_STORY"
HERE = Path(__file__).resolve().parent
SECTION_WORDS, OVERLAP_WORDS = 2500, 200

KINDS = {
    "fast_fact": ["unexpected_connection", "statistic", "scale_surprise", "origin_precursor", "concrete_detail",
                  "reversal_exception", "unexpected_consequence"],
    "human_moment": ["encounter", "desire_obstacle", "choice_cost", "failure", "adaptation", "turning_point", "loss",
                     "reconciliation"],
    "connection": ["cross_domain", "origin_precursor", "cause_consequence", "contradiction", "parallel", "theme_bridge"],
    "memorable_line": ["quotation", "aphorism", "slogan", "wordplay", "rhythmic_line"],
    "story_device": [],
    "story_spine": [],
}
DEVICES = {"cold_open", "in_medias_res", "reframe_inversion", "vivid_anchor", "scale_shock", "analogy_bridge",
           "dramatic_irony", "quotable", "permission_beat", "callback", "question_hook", "suspense_gap", "contrast",
           "rhyme", "rhythm_repetition", "humor_release", "thought_experiment"}
USES = {"opening", "explanation", "illustration", "evidence_lead", "transition", "humor", "emotional_turn", "ending"}
APPEAL = {"surprising", "vivid", "human_stakes", "tension", "humorous", "memorable_wording", "revealing_connection"}
BASIS = {"reported_fact", "fictional_event", "speaker_interpretation", "extractor_interpretation", "observed_wording",
         "observed_structure", "hypothetical"}
VERIFY = {"unchecked", "source_checked", "disputed", "unresolvable"}      # externally_checked needs a real outside check
REUSE = {"fact_after_check", "attributed_quote", "attributed_example", "pattern", "research_lead"}
ORDER = ["story_spine", "human_moment", "fast_fact", "memorable_line", "connection", "story_device"]
TITLES = {"story_spine": "Story spines", "human_moment": "Human moments", "fast_fact": "Fast facts",
          "memorable_line": "Memorable lines", "connection": "Connections", "story_device": "Story devices"}
STAMP = re.compile(r"^#{2,4} \[(\d{1,2}:\d{2}(?::\d{2})?)\]", re.M)


def hms(t: str | None) -> str | None:
    if not t:
        return None
    parts = [int(x) for x in re.findall(r"\d+", str(t))]
    if not parts:
        return None
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts[-3:]
    return f"{h:02d}:{m:02d}:{s:02d}"


def transcript_only(text: str) -> str:
    """The spoken transcript: from '## Transcript' on when the note has one, without its front matter."""
    m = re.search(r"^## Transcript\s*$", text, re.M)
    if m:
        return text[m.end():].strip()
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S).strip()


def sections(text: str) -> list[dict]:
    """Overlapping sections of about SECTION_WORDS words, cut at paragraph breaks."""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, cur, words, i = [], [], 0, 0
    while i < len(paras):
        cur.append(paras[i])
        words += len(paras[i].split())
        i += 1
        if words >= SECTION_WORDS or i == len(paras):
            body = "\n\n".join(cur)
            stamps = STAMP.findall(body)
            out.append({"text": body, "first": hms(stamps[0]) if stamps else None,
                        "last": hms(stamps[-1]) if stamps else None, "words": words})
            back, tail = [], 0                                # carry the last ~OVERLAP_WORDS into the next section
            for p in reversed(cur):
                if tail >= OVERLAP_WORDS or i == len(paras):
                    break
                back.insert(0, p)
                tail += len(p.split())
            cur, words = back, tail
            if i == len(paras):
                break
    return out


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def keep(values, allowed: set, where: str, notes: list) -> list:
    out = []
    for v in values or []:
        v = str(v).strip().lower().replace(" ", "_").replace("-", "_")
        if v in allowed:
            out.append(v)
        elif v:
            notes.append(f"vocabulary review: '{v}' ({where}) is not in the v1 list, left off the record")
    return list(dict.fromkeys(out))


def clean(raw: dict, notes: list) -> dict | None:
    kind = str(raw.get("kind", "")).strip()
    if kind not in KINDS or not str(raw.get("gist", "")).strip():
        if raw.get("gist"):
            notes.append(f"dropped a record with unknown kind '{kind}': {str(raw.get('gist'))[:80]}")
        return None
    sub = raw.get("subtype")
    if KINDS[kind] and sub not in KINDS[kind]:
        if sub:
            notes.append(f"vocabulary review: subtype '{sub}' for {kind} is not in the v1 list")
        sub = None
    pick = lambda v, allowed, default: v if v in allowed else default
    sources = []
    for s in raw.get("sources") or []:
        if isinstance(s, dict):
            sources.append({"start": hms(s.get("start")), "end": hms(s.get("end")), "lines": None,
                            "where": (s.get("where") or None)})
    details = raw.get("details") if isinstance(raw.get("details"), dict) else {}
    return {"kind": kind, "subtype": sub, "gist": str(raw["gist"]).strip(), "value": str(raw.get("value", "")).strip(),
            "topics": [str(t).strip() for t in raw.get("topics") or [] if str(t).strip()][:8],
            "uses": keep(raw.get("uses"), USES, "uses", notes), "appeal": keep(raw.get("appeal"), APPEAL, "appeal", notes),
            "devices": keep(raw.get("devices"), DEVICES, "devices", notes),
            "basis": pick(raw.get("basis"), BASIS, "speaker_interpretation"),
            "verification": pick(raw.get("verification"), VERIFY, "unchecked"),
            "reuse": pick(raw.get("reuse"), REUSE, "research_lead"),
            "sources": sources, "details": details, "related_ids": [],
            "checks": [str(c) for c in raw.get("checks") or [] if str(c).strip()]}


def check_quote(rec: dict, haystack: str) -> None:
    """transcript_wording must really be in the transcript; only then is the wording source_checked (the spec)."""
    w = (rec["details"] or {}).get("transcript_wording")
    if not w:
        return
    if norm(w) and norm(w) in haystack:
        if rec["basis"] == "observed_wording" and rec["verification"] == "unchecked":
            rec["verification"] = "source_checked"
    else:
        rec["verification"] = "unchecked" if rec["verification"] == "source_checked" else rec["verification"]
        rec["checks"].append("transcript_wording was NOT found verbatim in the transcript: treat as a paraphrase until checked")


def merge(records: list[dict]) -> list[dict]:
    """Same kind and the same gist or the same quoted wording = one record with every span kept."""
    out: list[dict] = []
    for r in records:
        key_w = norm((r["details"] or {}).get("transcript_wording", ""))
        twin = next((o for o in out if o["kind"] == r["kind"] and
                     (norm(o["gist"]) == norm(r["gist"]) or
                      (key_w and key_w == norm((o["details"] or {}).get("transcript_wording", ""))))), None)
        if twin:
            for s in r["sources"]:
                if s not in twin["sources"]:
                    twin["sources"].append(s)
            twin["topics"] = list(dict.fromkeys(twin["topics"] + r["topics"]))
            for f in ("uses", "appeal", "devices", "checks"):
                twin[f] = list(dict.fromkeys(twin[f] + r[f]))
        else:
            out.append(r)
    return out


def spine_prompt(item, recs: list[dict]) -> str:
    lines = [f"{r['id']} [{(r['sources'] or [{}])[0].get('start') or '?'}] {r['kind']}: {r['gist']}" for r in recs]
    return ((HERE / "STORY_MATERIAL_SYSTEM_v1.md").read_text(encoding="utf-8")
            + "\n\nEvery section of this transcript has been read. Below are ALL the records found, in presentation "
              "order. Using only these, write the PRESENTATION spine (scope: presentation): the order of setup, "
              "rupture, escalation, climax, resolution as the video actually unfolds. Roles may repeat or be absent; "
              "do not force a lecture into five beats; mark completeness 'partial' if the presentation is not a "
              "story. Each beat cites the record ids it rests on.\n"
              'Return ONLY JSON: {"spine": null} if there is no presentation story, else {"spine": {"subject": "", '
              '"completeness": "complete|partial", "shape": "short reusable description", "gist": "one sentence", '
              '"value": "one sentence", "beats": [{"role": "setup|rupture|escalation|climax|resolution", "gist": "", '
              '"record_ids": ["..."]}]}}'
            + f"\n\nVIDEO: {item.title}\n\nRECORDS:\n" + "\n".join(lines))


def process(ctx):
    item = ctx.item
    meta = item.meta
    text = transcript_only(ctx.text)
    parts = sections(text)
    ctx.step(f"{len(text.split()):,} words in {len(parts)} section(s) of ~{SECTION_WORDS:,}")
    spec = (HERE / "STORY_MATERIAL_SYSTEM_v1.md").read_text(encoding="utf-8")
    base = (HERE / "PROMPT.md").read_text(encoding="utf-8")
    notes: list[str] = []

    def one(k):
        p = parts[k]
        prompt = (f"{base}\n\nSTORY MATERIAL SYSTEM v1.0:\n{spec}\n\nVIDEO: {item.title}\nCHANNEL: {meta.get('channel', '')}"
                  f"\nSECTION {k + 1} of {len(parts)} (runs {p['first'] or '?'} to {p['last'] or '?'}; the first "
                  f"paragraphs may repeat the end of the previous section)\n\nSECTION TEXT:\n{p['text']}")
        h = hashlib.sha256(p["text"].encode()).hexdigest()[:12]
        rep = ctx.cached(f"section{k + 1}", lambda: ctx.call_json("story_section", prompt), extra=h)
        if isinstance(rep, dict):
            return rep
        # a section rich enough to overrun the output cap is read again as two halves (records merged afterwards)
        paras = [x for x in re.split(r"\n\s*\n", p["text"]) if x.strip()]
        if len(paras) < 2:
            return None
        ctx.step(f"section {k + 1}: no usable reply, reading it again as two halves")
        merged = {"items": [], "notes": []}
        for half, chunk in (("a", paras[:len(paras) // 2]), ("b", paras[len(paras) // 2:])):
            body = "\n\n".join(chunk)
            hp = prompt.split("SECTION TEXT:\n", 1)[0] + "SECTION TEXT:\n" + body
            r = ctx.cached(f"section{k + 1}{half}", lambda: ctx.call_json("story_section", hp),
                           extra=hashlib.sha256(body.encode()).hexdigest()[:12])
            if not isinstance(r, dict):
                return None
            merged["items"] += r.get("items") or []
            merged["notes"] += r.get("notes") or []
        ctx.errors[:] = [e for e in ctx.errors if "truncated" not in e]     # recovered: the halves covered it
        return merged

    replies = ctx.parallel(one, list(range(len(parts))), width=4)
    raw, read = [], []
    for k, rep in enumerate(replies):
        if not isinstance(rep, dict):
            ctx.warnings.append(f"section {k + 1} returned nothing usable")
            continue
        read.append(k)
        notes += [str(n) for n in rep.get("notes") or [] if str(n).strip()]
        for r in rep.get("items") or []:
            if isinstance(r, dict):
                c = clean(r, notes)
                if c:
                    raw.append(c)
    haystack = norm(text)
    for r in raw:
        check_quote(r, haystack)
    recs = merge(raw)
    recs.sort(key=lambda r: ((r["sources"] or [{}])[0].get("start") or "99"))
    sid = f"SRC-{item.id}" if re.fullmatch(r"[A-Za-z0-9_-]{6,20}", item.id or "") else "SRC-" + hashlib.sha256(
        item.title.encode()).hexdigest()[:10]
    for n, r in enumerate(recs, 1):
        r["id"] = f"{sid}-{n:03d}"
        for s in r["sources"]:
            s["source_id"] = sid
    spine = None
    if len(read) == len(parts) and recs:                       # the whole-video spine only once everything was read
        rep = ctx.cached("spine", lambda: ctx.call_json("story_spine", spine_prompt(item, recs), focus=False),
                         extra=hashlib.sha256(json.dumps([r["gist"] for r in recs]).encode()).hexdigest()[:12])
        s = (rep or {}).get("spine") if isinstance(rep, dict) else None
        if isinstance(s, dict) and s.get("beats"):
            ids = {r["id"]: r for r in recs}
            beats = []
            for b in s["beats"]:
                cited = [i for i in b.get("record_ids") or [] if i in ids]
                beats.append({"role": b.get("role"), "gist": b.get("gist"), "record_ids": cited,
                              "sources": [x for i in cited for x in ids[i]["sources"][:1]]})
            spine = {"id": f"{sid}-SPINE", "kind": "story_spine", "subtype": None, "gist": s.get("gist") or s.get("shape"),
                     "value": s.get("value", ""), "topics": [], "uses": [], "appeal": [], "devices": [],
                     "basis": "observed_structure", "verification": "source_checked", "reuse": "pattern",
                     "sources": [x for b in beats for x in b["sources"]][:1],
                     "details": {"scope": "presentation", "subject": s.get("subject") or item.title,
                                 "completeness": s.get("completeness", "partial"), "shape": s.get("shape"), "beats": beats},
                     "related_ids": sorted({i for b in beats for i in b["record_ids"]}), "checks": []}
    elif len(read) < len(parts):
        notes.append("presentation spine not written: not every section was read")
    all_recs = ([spine] if spine else []) + recs
    stamps = STAMP.findall(text)
    doc = {"schema_version": "1.0", "run_id": f"RUN-{ctx.receipts[-1]['finished_at'][:19] if ctx.receipts else 'cached'}",
           "source": {"id": sid, "title": item.title, "channel": meta.get("channel") or None, "url": meta.get("url") or None,
                      "transcript_path": meta.get("source_file") or None,
                      "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                      "coverage": {"status": "complete" if len(read) == len(parts) else "partial",
                                   "reviewed_ranges": [[parts[k]["first"], parts[k]["last"]] for k in read],
                                   "gaps": [[parts[k]["first"], parts[k]["last"]] for k in range(len(parts)) if k not in read],
                                   "time_range": [hms(stamps[0]), hms(stamps[-1])] if stamps else None}},
           "items": all_recs, "notes": list(dict.fromkeys(notes))}
    counts = {k: sum(1 for r in all_recs if r["kind"] == k) for k in ORDER}
    ctx.step("records: " + ", ".join(f"{v} {k}" for k, v in counts.items() if v))
    md = render(item, doc, counts)
    rows = [{"id": r["id"], "kind": r["kind"], "subtype": r["subtype"], "gist": r["gist"], "value": r["value"],
             "start": (r["sources"] or [{}])[0].get("start"), "uses": ", ".join(r["uses"]), "devices": ", ".join(r["devices"]),
             "basis": r["basis"], "verification": r["verification"], "reuse": r["reuse"]} for r in all_recs]
    return ItemResult(doc, page(f"Story material: {item.title}", markdown_to_html(md)), {"records": rows}, md,
                      {"story_records": len(all_recs)})


def card(r: dict) -> list[str]:
    d = r["details"] or {}
    at = ", ".join(s["start"] for s in r["sources"] if s.get("start")) or "—"
    labels = " · ".join(x for x in [r["subtype"] or "", ", ".join(r["devices"]), ", ".join(r["uses"])] if x)
    out = [f"#### {r['gist']}", f"`{r['id']}` · {at} · {labels}" if labels else f"`{r['id']}` · {at}", ""]
    if r["kind"] == "memorable_line" and d.get("transcript_wording"):
        out += [f"> \"{d['transcript_wording']}\"" + (f" — {d['speaker']}" if d.get("speaker") else ""), ""]
    if r["kind"] == "human_moment":
        bits = [f"**{k}:** {d[k]}" for k in ("actor", "desire", "obstacle", "choice", "consequence") if d.get(k)]
        if bits:
            out += [" · ".join(bits), ""]
    if r["kind"] == "story_spine":
        out += [f"*{d.get('scope', '')} · {d.get('completeness', '')}* · shape: **{d.get('shape') or '—'}**", ""]
        out += [f"{i}. **{b.get('role')}**: {b.get('gist')}" for i, b in enumerate(d.get("beats") or [], 1)] + [""]
    out += [f"**Writing value:** {r['value']}", f"*{r['basis']} · {r['verification']} · {r['reuse']}*"]
    out += [f"- check: {c}" for c in r["checks"]]
    return out + [""]


def render(item, doc, counts) -> str:
    src = doc["source"]
    out = [f"# Story material: {item.title}", "",
           f"Story Material System v1.0 · {sum(counts.values())} records · coverage **{src['coverage']['status']}** · "
           + " · ".join(f"{v} {k.replace('_', ' ')}" for k, v in counts.items() if v), ""]
    for kind in ORDER:
        recs = [r for r in doc["items"] if r["kind"] == kind]
        if recs:
            out += [f"### {TITLES[kind]} ({len(recs)})", ""]
            for r in recs:
                out += card(r)
    cov = src["coverage"]
    out += ["### Coverage notes", "",
            f"- Read: {len(cov['reviewed_ranges'])} section(s), {cov['time_range'][0] if cov['time_range'] else '?'} to "
            f"{cov['time_range'][1] if cov['time_range'] else '?'}; gaps: {cov['gaps'] or 'none'}.",
            "- Extraction and verification are separate: every factual record stays unchecked until checked outside "
            "the transcript. Quotations marked source_checked were found verbatim in the transcript by code.",
            *[f"- {n}" for n in doc["notes"]], "",
            "### Machine record (schema 1.0)", "", "```yaml",
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120).rstrip(), "```"]
    return "\n".join(out)


if __name__ == "__main__":
    raise SystemExit(Station(LABEL, kind="videos", prompt_files=["STORY_MATERIAL_SYSTEM_v1.md"]).run(process))
