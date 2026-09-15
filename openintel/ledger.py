"""SQLite access and canonical OpenIntel ID allocation."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = {"CASE", "HNCH", "SRC", "STMT", "CLM", "EVID", "EVT", "ANOM", "SIG", "CONTRA", "FIN"}


def canonical_id(kind: str, collection: str, number: int, source_number: int | None = None) -> str:
    kind, collection = kind.upper(), collection.upper()
    if kind not in KINDS or not re.fullmatch(r"[A-Z0-9]{2,4}", collection):
        raise ValueError("invalid record kind or collection code")
    if kind == "STMT":
        if source_number is None:
            raise ValueError("statements require a source number")
        return f"STMT-{collection}-{source_number:04d}-{number:04d}"
    return f"{kind}-{collection}-{number:04d}"


class Ledger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")

    def close(self) -> None:
        self.db.close()

    def initialize(self) -> None:
        self.db.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
        # CREATE TABLE IF NOT EXISTS does not add columns to ledgers created by
        # earlier builds. Keep these additive migrations safe to run at startup.
        self._ensure_column("statements", "attribution_confidence", "TEXT")
        self._ensure_column("claims", "claimed_evidence", "TEXT")
        self._ensure_column("claims", "counterclaim", "TEXT")
        self.db.execute("INSERT OR REPLACE INTO metadata VALUES('schema_version','2.1-openintel')")
        for code in ("EVENT", "PROGRAM", "INSTITUTION", "PROPAGANDA", "PROPHETIC", "PHENOMENON", "PATTERN", "SYMBOL", "CULTURAL"):
            self.db.execute("INSERT OR IGNORE INTO case_types(code,label) VALUES(?,?)", (code, code.title()))
        self.db.commit()

    def _ensure_column(self, table: str, column: str, declaration: str) -> None:
        columns = {row[1] for row in self.db.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            self.db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")

    def next_id(self, kind: str, collection: str, source_number: int | None = None) -> str:
        kind, collection = kind.upper(), collection.upper()
        with self.db:
            row = self.db.execute("SELECT next_value FROM id_sequences WHERE kind=? AND collection=?", (kind, collection)).fetchone()
            value = row[0] if row else 1
            self.db.execute("INSERT INTO id_sequences VALUES(?,?,?) ON CONFLICT(kind,collection) DO UPDATE SET next_value=excluded.next_value", (kind, collection, value + 1))
        return canonical_id(kind, collection, value, source_number)

    def add_source(self, collection: str, *, title: str, url: str = "", source_type: str = "youtube", legacy_ids=()) -> str:
        record_id = self.next_id("SRC", collection)
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        with self.db:
            self.db.execute("INSERT INTO sources(id,collection,legacy_ids,title,source_type,url,acquired_at) VALUES(?,?,?,?,?,?,?)", (record_id, collection.upper(), json.dumps(list(legacy_ids)), title, source_type, url, now))
        return record_id

    def add_statement(self, collection: str, source_id: str, text: str, *, locator: str = "", sensitive: bool = False) -> str:
        source_number = int(source_id.rsplit("-", 1)[1])
        record_id = self.next_id("STMT", collection, source_number)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        with self.db:
            existing = self.db.execute("SELECT id FROM statements WHERE statement_hash=?", (digest,)).fetchone()
            if existing:
                return existing[0]
            self.db.execute("INSERT INTO statements(id,collection,source_id,statement_text,statement_hash,locator,sensitive) VALUES(?,?,?,?,?,?,?)", (record_id, collection.upper(), source_id, text, digest, locator, int(sensitive)))
        return record_id
