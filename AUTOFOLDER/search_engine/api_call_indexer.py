"""
Index API-call conversation logs (DeepSeek-style Markdown) into SQLite + FTS5.

Usage:
  python api_call_indexer.py --name deepseek_calls --source "D:/GitHub/Research-Acquisition/yt-transcript-downloader/pipeline-workflows/docs/deepseek-conversations"
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import re
import sqlite3
import sys
from typing import Any

os.environ.setdefault("PYTHONUTF8", "1")

DEFAULT_DB_DIR = pathlib.Path(__file__).resolve().parent / "indexes"
MAX_TEXT_BYTES = 5 * 1024 * 1024


def init_db(db_path: pathlib.Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT NOT NULL,
            conversation_id TEXT,
            message_index INTEGER NOT NULL,
            timestamp TEXT,
            model TEXT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            indexed_at TEXT
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
            role, content,
            content='messages',
            content_rowid='id'
        )
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
            INSERT INTO messages_fts(rowid, role, content)
            VALUES (new.id, new.role, new.content);
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
            INSERT INTO messages_fts(messages_fts, rowid, role, content)
            VALUES ('delete', old.id, old.role, old.content);
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
            INSERT INTO messages_fts(messages_fts, rowid, role, content)
            VALUES ('delete', old.id, old.role, old.content);
            INSERT INTO messages_fts(rowid, role, content)
            VALUES (new.id, new.role, new.content);
        END
    """)
    conn.commit()
    return conn


def parse_conversation(file_path: pathlib.Path) -> dict[str, Any]:
    """Parse a DeepSeek conversation Markdown file into structured messages."""
    raw = file_path.read_bytes()
    if len(raw) > MAX_TEXT_BYTES:
        return {"conversation_id": None, "model": None, "timestamp": None, "messages": []}
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1", errors="ignore")

    # Header: # DeepSeek exchange 20260923-190753 (deepseek-chat)
    conversation_id = None
    model = None
    timestamp = None
    header_match = re.search(r"#\s+DeepSeek exchange\s+(\S+)\s+\(([^)]+)\)", text)
    if header_match:
        timestamp_str = header_match.group(1)
        model = header_match.group(2).strip()
        # Try to format as ISO-ish timestamp.
        try:
            ts = dt.datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
            timestamp = ts.isoformat()
            conversation_id = timestamp_str
        except ValueError:
            conversation_id = timestamp_str

    messages: list[dict[str, Any]] = []
    # Split only on top-level ## David / ## DeepSeek headings, not on internal headings.
    parts = re.split(r"\n##\s+(David|DeepSeek)\s*\n", text)
    # parts[0] is header/front matter; then alternating role, content.
    msg_index = 0
    i = 1
    while i < len(parts):
        role = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if role.lower() in {"david", "user"}:
            role = "user"
        elif "deepseek" in role.lower():
            role = "assistant"
        else:
            role = role.lower()
        if content:
            messages.append({
                "index": msg_index,
                "role": role,
                "content": content,
            })
            msg_index += 1
        i += 2

    return {
        "conversation_id": conversation_id or file_path.stem,
        "model": model,
        "timestamp": timestamp,
        "messages": messages,
    }


def index_source(
    conn: sqlite3.Connection,
    source: pathlib.Path,
    commit_every: int = 100,
) -> dict[str, int]:
    cursor = conn.cursor()
    inserted = updated = skipped = errors = 0
    processed = 0

    files = sorted(source.rglob("*.md"))
    for file_path in files:
        if file_path.name.startswith("."):
            skipped += 1
            continue

        try:
            conv = parse_conversation(file_path)
            conv_id = conv["conversation_id"]
            model = conv["model"]
            timestamp = conv["timestamp"]
            source_file = str(file_path.resolve())
            indexed_at = dt.datetime.now().isoformat()

            # Wipe prior messages for this file to keep index idempotent.
            cursor.execute("DELETE FROM messages WHERE source_file = ?", (source_file,))
            deleted = cursor.rowcount
            if deleted:
                updated += 1
            else:
                inserted += 1

            for msg in conv["messages"]:
                cursor.execute(
                    """
                    INSERT INTO messages (source_file, conversation_id, message_index, timestamp, model, role, content, indexed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        source_file,
                        conv_id,
                        msg["index"],
                        timestamp,
                        model,
                        msg["role"],
                        msg["content"],
                        indexed_at,
                    ),
                )
        except Exception as e:
            errors += 1
            print(f"error indexing {file_path}: {e}", file=sys.stderr)

        processed += 1
        if processed % commit_every == 0:
            conn.commit()

    conn.commit()
    return {
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "files": processed,
        "messages": sum(1 for _ in conn.execute("SELECT 1 FROM messages")),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Index API-call conversation logs into SQLite.")
    ap.add_argument("--name", required=True, help="index name")
    ap.add_argument("--source", required=True, help="source directory containing .md conversation logs")
    ap.add_argument("--db-dir", type=pathlib.Path, default=DEFAULT_DB_DIR)
    args = ap.parse_args()

    source = pathlib.Path(args.source).expanduser().resolve()
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 1

    db_path = args.db_dir / f"{args.name}.db"
    print(f"indexing: {source}")
    print(f"database: {db_path}")

    conn = init_db(db_path)
    stats = index_source(conn, source)
    conn.close()

    print(f"files:    {stats['files']}")
    print(f"inserted: {stats['inserted']}")
    print(f"updated:  {stats['updated']}")
    print(f"skipped:  {stats['skipped']}")
    print(f"errors:   {stats['errors']}")
    print(f"messages in index: {stats['messages']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
