#!/usr/bin/env python3
"""Report legacy IDs and unresolved Obsidian links without modifying a vault."""
from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

ID_RE = re.compile(r"\b(?:OI-CT-\d{4}|CASE-(?:\d{4}|\d{3}-[A-Z]\d+|YYYY-NNN)|CT\d{3}|SRC-(?:YYYY-NNN|\d{3}-[A-Z]\d+-\d{3})|STMT-(?:YYYY-NNN|[A-Z]\d+-\d{3})|CLM-YYYY-NNN|(?:EV|EVID)-(?:[A-Z]+\d+-\d+|YYYY-NNN)|ENTITY-[a-z0-9-]+|ENT-TYPE-NNN)\b", re.I)
WIKI_RE = re.compile(r"\[\[([^\]|#]+)")
PREFIX = {"OI-CT": "CASE", "CT": "CASE", "CASE": "CASE", "SRC": "SRC", "STMT": "STMT", "CLM": "CLM", "EV": "EVID", "EVID": "EVID", "ENTITY": "ENT", "ENT": "ENT"}


def collection_for(path: Path, text: str) -> str:
    known = {"mkultra": "MKU", "candace owens": "COW", "habermas": "HAB", "epstein": "EPS"}
    haystack = (str(path) + " " + text[:2000]).lower()
    return next((code for word, code in known.items() if word in haystack), "GEN")


def scan(vault: Path, output: Path) -> tuple[int, int]:
    files = list(vault.rglob("*.md"))
    stems = defaultdict(list)
    for path in files:
        stems[path.stem.lower()].append(path)
    found, broken, counters = [], [], defaultdict(int)
    for path in files:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        coll = collection_for(path, text)
        for old in dict.fromkeys(ID_RE.findall(text)):
            raw_prefix = old.upper().split("-", 1)[0]
            if old.upper().startswith("OI-CT-"):
                raw_prefix = "OI-CT"
            kind = PREFIX.get(raw_prefix, "CASE")
            counters[(kind, coll)] += 1
            width = 5 if kind == "ENT" else 4
            new = f"{kind}-{coll}-{counters[(kind, coll)]:0{width}d}" if kind != "ENT" else f"ENT-UNK-{counters[(kind, coll)]:05d}"
            found.append((old, new, str(path.relative_to(vault))))
        for target in WIKI_RE.findall(text):
            key = Path(target.strip()).name.lower()
            if key not in stems:
                broken.append((str(path.relative_to(vault)), target.strip(), "missing target"))
    output.mkdir(parents=True, exist_ok=True)
    with (output / "id_map.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle); writer.writerow(("legacy_id", "new_id", "source_file")); writer.writerows(found)
    with (output / "broken_links.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle); writer.writerow(("source_file", "target", "reason")); writer.writerows(broken)
    return len(found), len(broken)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", type=Path)
    parser.add_argument("--output", type=Path, default=Path("openintel-reports"))
    args = parser.parse_args()
    mapped, broken = scan(args.vault, args.output)
    print(f"Reported {mapped} legacy IDs and {broken} broken links; vault unchanged")
