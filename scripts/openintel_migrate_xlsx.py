#!/usr/bin/env python3
"""Migrate structured records from the OpenIntel master workbook."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openintel.ledger import Ledger
from openintel.xlsx import read_workbook


def migrate(workbook: Path, ledger_path: Path) -> dict[str, int]:
    sheets = read_workbook(workbook)
    ledger = Ledger(ledger_path)
    ledger.initialize()
    counts = {"cases": 0, "links": 0, "evidence_types": 0}
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    # The filled case sheets use labels in A and values in B.
    for name, rows in sheets.items():
        if not name.startswith("CASE —"):
            continue
        fields = {row.get("A", "").strip(): row.get("B", "").strip() for row in rows}
        legacy = fields.get("UUID (OI-CT-XXXX)")
        collection = fields.get("Short Code") or "GEN"
        title = fields.get("Full Case Name")
        if not title:
            continue
        case_id = ledger.next_id("CASE", collection)
        with ledger.db:
            ledger.db.execute("INSERT INTO cases(id,collection,legacy_ids,short_code,case_type,title,slug,rating,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)", (case_id, collection, json.dumps([legacy] if legacy else []), collection, fields.get("Case Type") or None, title, re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-"), "UNRATED", now, now))
        counts["cases"] += 1
        by_row = {int(row["_row"]): row for row in rows}
        for number, row_number in enumerate(range(36, 41), 1):
            row = by_row.get(row_number, {})
            if not row.get("B"):
                continue
            entity_id = f"ENT-UNK-{number:05d}"
            with ledger.db:
                ledger.db.execute("INSERT OR IGNORE INTO entities(id,entity_type,name,role,description,lifecycle) VALUES(?,'PERSON',?,?,?,'CANDIDATE')", (entity_id, row["B"], row.get("C"), row.get("D")))
                ledger.db.execute("INSERT OR IGNORE INTO case_entities(case_id,entity_id,relationship) VALUES(?,?,'INVOLVES')", (case_id, entity_id))
        for row_number in range(24, 34):
            row = by_row.get(row_number, {})
            if not row.get("C"):
                continue
            event_id = ledger.next_id("EVT", collection)
            with ledger.db:
                ledger.db.execute("INSERT INTO events(id,collection,case_id,event_date,title,description,lifecycle) VALUES(?,?,?,?,?,?,'CANDIDATE')", (event_id, collection, case_id, row.get("B"), row["C"][:200], row["C"]))
        for row_number in range(43, 51):
            row = by_row.get(row_number, {})
            if not row.get("B"):
                continue
            type_id = int(row.get("A") or row_number - 42)
            tier = row.get("E", "T3").upper()
            with ledger.db:
                existing = ledger.db.execute("SELECT 1 FROM evidence_types WHERE type_id=?", (type_id,)).fetchone()
                ledger.db.execute("INSERT OR IGNORE INTO evidence_types(type_id,tier,tier_label,name) VALUES(?,?,?,?)", (type_id, tier if tier in {"T1","T2","T3","T4","T5","NEGATIVE"} else "T3", tier, row["B"]))
                evidence_id = ledger.next_id("EVID", collection)
                ledger.db.execute("INSERT INTO evidence(id,collection,case_id,evidence_type,tier,title,description,lifecycle) VALUES(?,?,?,?,?,?,?,'CANDIDATE')", (evidence_id, collection, case_id, type_id, tier, row["B"], row.get("C")))
            if not existing:
                counts["evidence_types"] += 1
        for row_number in range(201, 211):
            row = by_row.get(row_number, {})
            if not row.get("C"):
                continue
            claim_id = ledger.next_id("CLM", collection)
            with ledger.db:
                ledger.db.execute("INSERT INTO claims(id,collection,case_id,claim_text,claim_type,rating) VALUES(?,?,?,?,?,?)", (claim_id, collection, case_id, row["C"], row.get("B"), row.get("D") or "UNRATED"))
    # Preserve the workbook's discovery URLs as source records and case-to-source links.
    for row in sheets.get("case_links_master", [])[1:]:
        url, title = row.get("E", "").strip(), row.get("C", "").strip()
        if not url:
            continue
        source_id = ledger.add_source("GEN", title=title or url, url=url, source_type=row.get("G", "web"), legacy_ids=())
        old_case = row.get("A", "").strip()
        with ledger.db:
            ledger.db.execute("INSERT OR IGNORE INTO links(from_id,to_id,link_type,source,created_at) VALUES(?,?,?,?,?)", (old_case, source_id, "SOURCE_DISCOVERY", "Open Intel.xlsx/case_links_master", now))
        counts["links"] += 1
    # Import an explicit lookup if a later workbook revision adds one in DROPDOWNS.
    dropdowns = sheets.get("DROPDOWNS", [])
    for row in dropdowns:
        name = row.get("J", "").strip()
        tier = row.get("I", "").strip().upper()
        type_id = row.get("H", "").strip()
        if name and type_id.isdigit() and tier in {"T1", "T2", "T3", "T4", "T5", "NEGATIVE"}:
            with ledger.db:
                ledger.db.execute("INSERT OR IGNORE INTO evidence_types(type_id,tier,tier_label,name) VALUES(?,?,?,?)", (int(type_id), tier, tier, name))
            counts["evidence_types"] += 1
    ledger.close()
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, default=Path("Open Intel.xlsx"))
    parser.add_argument("--ledger", type=Path, default=Path("openintel.sqlite"))
    args = parser.parse_args()
    print(json.dumps(migrate(args.workbook, args.ledger), indent=2))
