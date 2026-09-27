"""
Search across one or all SQLite indexes.

Supports two index types:
  - file indexes (created by indexer.py): files/files_fts tables
  - API-call indexes (created by api_call_indexer.py): messages/messages_fts tables

Usage:
  python search.py --index obsidian --query "resurrection evidence"
  python search.py --all --query "grace operator" --limit 20
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import sqlite3
import sys
from typing import Any

os.environ.setdefault("PYTHONUTF8", "1")

DEFAULT_DB_DIR = pathlib.Path(__file__).resolve().parent / "indexes"


def _escape_fts5(query: str) -> str:
    """Wrap a raw query in double quotes so FTS5 treats it as a literal phrase."""
    cleaned = query.replace('"', '""')
    return f'"{cleaned}"'


def _index_type(conn: sqlite3.Connection) -> str:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "messages" in tables:
        return "messages"
    return "files"


def search_files(db_path: pathlib.Path, query: str, limit: int) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """
        SELECT f.path, f.name, f.ext, f.size, f.mtime,
               rank AS score
        FROM files_fts
        JOIN files f ON f.id = files_fts.rowid
        WHERE files_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (_escape_fts5(query), limit),
    )
    results = []
    for row in cursor.fetchall():
        r = dict(row)
        r["kind"] = "file"
        results.append(r)
    conn.close()
    return results


def search_messages(db_path: pathlib.Path, query: str, limit: int) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """
        SELECT m.source_file, m.conversation_id, m.message_index, m.timestamp, m.model, m.role,
               rank AS score
        FROM messages_fts
        JOIN messages m ON m.id = messages_fts.rowid
        WHERE messages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (_escape_fts5(query), limit),
    )
    results = []
    for row in cursor.fetchall():
        r = dict(row)
        r["kind"] = "message"
        results.append(r)
    conn.close()
    return results


def search_index(db_path: pathlib.Path, query: str, limit: int) -> list[dict[str, Any]]:
    if not db_path.exists():
        return []
    conn = sqlite3.connect(db_path)
    kind = _index_type(conn)
    conn.close()
    if kind == "messages":
        return search_messages(db_path, query, limit)
    return search_files(db_path, query, limit)


def list_indexes(db_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted(db_dir.glob("*.db"))


def format_file_result(r: dict[str, Any], db_name: str) -> str:
    mtime = r.get("mtime") or 0
    mtime_str = ""
    if mtime:
        mtime_str = dt.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    return (
        f"[{db_name}] file: {r['name']}\n"
        f"  path: {r['path']}\n"
        f"  size: {r['size'] or 0} bytes  modified: {mtime_str}\n"
    )


def format_message_result(r: dict[str, Any], db_name: str) -> str:
    ts = r.get("timestamp") or ""
    return (
        f"[{db_name}] message: {r['role']}#{r['message_index']}\n"
        f"  conversation: {r['conversation_id']}  model: {r['model']}  timestamp: {ts}\n"
        f"  source: {r['source_file']}\n"
    )


def format_result(r: dict[str, Any], db_name: str) -> str:
    if r.get("kind") == "message":
        return format_message_result(r, db_name)
    return format_file_result(r, db_name)


def main() -> int:
    ap = argparse.ArgumentParser(description="Search indexed files and API calls.")
    ap.add_argument("--query", required=True, help="search query")
    ap.add_argument("--index", help="specific index name")
    ap.add_argument("--all", action="store_true", help="search all indexes")
    ap.add_argument("--db-dir", type=pathlib.Path, default=DEFAULT_DB_DIR)
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    if not args.index and not args.all:
        print("use --index <name> or --all", file=sys.stderr)
        return 1

    indexes = []
    if args.index:
        indexes = [args.db_dir / f"{args.index}.db"]
    else:
        indexes = list_indexes(args.db_dir)

    total = 0
    for db_path in indexes:
        name = db_path.stem
        results = search_index(db_path, args.query, args.limit)
        if results:
            print(f"\n=== {name} ({len(results)} results) ===")
            for r in results:
                print(format_result(r, name))
            total += len(results)

    print(f"\ntotal results: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
