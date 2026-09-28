"""How a CKG sits on the transcript page (David, 2026-09-28): the page stays readable, nothing is lost.

  Story Bank  -> its own file, <CKG OUTBOX>/STORY_BANK/<note> · STORIES.md, linked back to the note and its CKG;
                 the page keeps one line per story (title, kind, tags) linking to the full entry.
  Claim cards -> the "Warrant Control & Airtight Upgrade Formulations" section becomes one table row per claim
                 (strength, kill condition); the full cards go to the bottom of the page, below the transcript.

The CKG file itself (OUTBOX/CKG/<note> · CKG.md) is never changed: it stays the complete record, and the Story Bank
harvester (story_bank.py) reads the full entries from it.
"""
from __future__ import annotations

import re

STORY = "## Story Bank"
CLAIMS = "## Warrant Control & Airtight Upgrade Formulations"


def _section(body: str, heading: str) -> tuple[int, int] | None:
    """Start and end of a '## ' section in the raw companion (end = the next '## ' or '# ' heading)."""
    m = re.search(rf"^{re.escape(heading)}\s*$", body, re.M)
    if not m:
        return None
    nxt = re.compile(r"^#{1,2} (?!#)", re.M).search(body, m.end())
    return m.start(), nxt.start() if nxt else len(body)


def _field(block: str, label: str) -> str:
    m = re.search(rf"\*\*{re.escape(label)}:?\*\*:?\s*(.+?)(?=\n\s*[-|]\s*\*\*|\n\n|\Z)", block, re.S)
    if not m:
        return ""
    return " ".join(m.group(1).split()).strip(" |`")


def story_bank(body: str, stem: str) -> tuple[str, str | None]:
    """(body with a short Story Bank list, the full Story Bank file text or None)."""
    span = _section(body, STORY)
    if not span:
        return body, None
    part = body[span[0]:span[1]]
    entries = re.split(r"^### ", part, flags=re.M)[1:]
    if not entries:
        return body, None
    file = f"{stem} · STORIES"
    lines = [STORY, "", f"{len(entries)} stories and facts to retell. Full retellings, exact words and why each matters: "
                        f"[[{file}]]", ""]
    for e in entries:
        head = e.split("\n", 1)[0].strip()
        title = re.sub(r"^SB\d+\s*·\s*", "", head)
        kind, use = _field(e, "Kind"), _field(e, "Use it for")
        lines.append(f"- [[{file}#{head}|{title}]]" + (f" · *{kind}*" if kind else "") + (f" · {use}" if use else ""))
    full = "\n".join([f"# Story Bank · {stem}", "",
                      f"From the CKG of [[{stem}]] (the transcript) · full analysis: [[{stem} · CKG]]", "",
                      part.split("\n", 1)[1].strip(), ""])
    return body[:span[0]] + "\n".join(lines) + "\n\n" + body[span[1]:], full


def claim_cards(body: str) -> tuple[str, str | None]:
    """(body with a one-row-per-claim table, the full claim cards or None)."""
    span = _section(body, CLAIMS)
    if not span:
        return body, None
    part = body[span[0]:span[1]]
    cards = re.split(r"^### ", part, flags=re.M)[1:]
    if not cards:
        return body, None
    rows = [CLAIMS, "", "| # | Claim | Type | Strength | Kill condition |", "|---|---|---|---:|---|"]
    for c in cards:
        head = c.split("\n", 1)[0].strip()
        m = re.match(r"Claim\s*(\d+)\s*:?\s*(.*)", head)
        num, text = (m.group(1), m.group(2)) if m else ("", head)
        kind = _field(c, "Claim ID & Type").split("·")[-1].strip(" `") if "·" in _field(c, "Claim ID & Type") else ""
        cell = lambda s: s.replace("|", "\\|")
        rows.append(f"| {num} | {cell(text)} | {cell(kind)} | {cell(_field(c, 'Evidence strength'))} | "
                    f"{cell(_field(c, 'Kill condition'))} |")
    rows += ["", "The full claim cards (evidence, proof or test, the Airtight +8 formulation) are at the bottom of the page, "
                 "below the transcript.", ""]
    full = "\n".join(["## Claim cards (full)", "", *("### " + c.strip() + "\n" for c in cards)])
    return body[:span[0]] + "\n".join(rows) + "\n" + body[span[1]:], full
