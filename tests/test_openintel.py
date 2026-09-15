import importlib.util
import sqlite3
from pathlib import Path

import pytest

from openintel.ledger import Ledger, canonical_id
from openintel.xlsx import read_workbook


def load_script(name):
    path = Path("scripts") / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ids_and_hunch_invariants(tmp_path):
    assert canonical_id("CASE", "MKU", 1) == "CASE-MKU-0001"
    assert canonical_id("STMT", "COW", 2, 7) == "STMT-COW-0007-0002"
    ledger = Ledger(tmp_path / "ledger.sqlite")
    ledger.initialize()
    now = "2026-09-15T00:00:00+00:00"
    with ledger.db:
        ledger.db.execute("INSERT INTO hunches(id,collection,written_by,written_at,gut_statement) VALUES('HNCH-MKU-0001','MKU','David',?,'The timeline feels rehearsed')", (now,))
    with pytest.raises(sqlite3.IntegrityError):
        with ledger.db:
            ledger.db.execute("UPDATE hunches SET hunch_status='DROPPED' WHERE id='HNCH-MKU-0001'")
    with pytest.raises(sqlite3.IntegrityError):
        with ledger.db:
            ledger.db.execute("UPDATE hunches SET sensitive=1,public_projection=1 WHERE id='HNCH-MKU-0001'")
    with pytest.raises(sqlite3.IntegrityError):
        with ledger.db:
            ledger.db.execute("UPDATE hunches SET written_at='later' WHERE id='HNCH-MKU-0001'")
    with pytest.raises(sqlite3.IntegrityError):
        with ledger.db:
            ledger.db.execute("DELETE FROM hunches WHERE id='HNCH-MKU-0001'")
    ledger.close()


def test_workbook_reader_and_migration(tmp_path):
    sheets = read_workbook("Open Intel.xlsx")
    assert {"DROPDOWNS", "DB Schema v2.0", "CASE — MKUltra (OI-CT-0001)"} <= sheets.keys()
    migrate = load_script("openintel_migrate_xlsx")
    counts = migrate.migrate(Path("Open Intel.xlsx"), tmp_path / "ledger.sqlite")
    assert counts["cases"] == 1
    db = sqlite3.connect(tmp_path / "ledger.sqlite")
    row = db.execute("SELECT id,legacy_ids,rating FROM cases").fetchone()
    assert row[0] == "CASE-MKU-0001" and "OI-CT-0001" in row[1] and row[2] == "UNRATED"
    assert db.execute("SELECT count(*) FROM sources").fetchone()[0] > 0
    assert db.execute("SELECT count(*) FROM claims").fetchone()[0] == 10
    assert db.execute("SELECT count(*) FROM evidence").fetchone()[0] == 8
    assert db.execute("SELECT count(*) FROM events").fetchone()[0] == 10


def test_id_mapper_reports_without_editing(tmp_path):
    vault = tmp_path / "vault"; vault.mkdir()
    note = vault / "MKUltra.md"
    original = "case_id: OI-CT-0001\nSee [[Missing Note]].\n"
    note.write_text(original)
    mapper = load_script("openintel_id_mapper")
    mapped, broken = mapper.scan(vault, tmp_path / "reports")
    assert (mapped, broken) == (1, 1)
    assert note.read_text() == original
    assert "CASE-MKU-0001" in (tmp_path / "reports/id_map.csv").read_text()


def test_recheck_is_idempotent(tmp_path):
    ledger = Ledger(tmp_path / "ledger.sqlite"); ledger.initialize()
    now = "2026-09-15T00:00:00+00:00"
    with ledger.db:
        ledger.db.execute("INSERT INTO hunches(id,collection,written_by,written_at,gut_statement,lifecycle) VALUES('HNCH-MKU-0001','MKU','David',?,'timeline date conflict','ACCEPTED')", (now,))
    source = ledger.add_source("MKU", title="Test")
    statement = ledger.add_statement("MKU", source, "The timeline has a date conflict.")
    with ledger.db:
        ledger.db.execute("UPDATE statements SET lifecycle='ACCEPTED' WHERE id=?", (statement,))
    ledger.close()
    recheck = load_script("openintel_recheck_hunches")
    assert recheck.recheck(tmp_path / "ledger.sqlite", .1) == 1
    assert recheck.recheck(tmp_path / "ledger.sqlite", .1) == 0


def test_refinery_ledger_candidates_and_sensitive_gate(tmp_path):
    path = Path("workflows/YouTubeChannelRefinery/SCRIPTS/run_pipeline.py")
    spec = importlib.util.spec_from_file_location("refinery_ledger", path)
    refinery = importlib.util.module_from_spec(spec); spec.loader.exec_module(refinery)
    video = {"chapter": 1, "title": "Test", "video_id": "abc", "url": "https://youtu.be/abc", "transcript": "John Smith lied in 2020 and 2021."}
    _, _, count = refinery.ledger_extract(tmp_path / "ledger.sqlite", "COW", "Channel", video)
    assert count == 1
    db = sqlite3.connect(tmp_path / "ledger.sqlite")
    assert db.execute("SELECT sensitive,lifecycle FROM statements").fetchone() == (1, "CANDIDATE")
    assert db.execute("SELECT written_by,sensitive FROM hunches").fetchone() == ("system extraction", 1)
