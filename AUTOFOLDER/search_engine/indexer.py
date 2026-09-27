"""
File indexer: crawl a directory and store metadata + searchable text in SQLite.

Usage:
  python indexer.py --name obsidian --source "C:/Users/David/Documents/faiththruphysics.com/01_WORKING"
  python indexer.py --name c_drive --source "C:/" --exclude "Windows,Program Files,ProgramData"
"""
from __future__ import annotations

import argparse
import datetime as dt
import mimetypes
import os
import pathlib
import re
import sqlite3
import sys
from typing import Any

# Force UTF-8 on Windows.
os.environ.setdefault("PYTHONUTF8", "1")

DEFAULT_DB_DIR = pathlib.Path(__file__).resolve().parent / "indexes"
TEXT_MIMES = {"text/plain", "text/markdown", "text/x-markdown"}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".log", ".csv", ".sql", ".html", ".htm",
    ".xml", ".css", ".sh", ".bat", ".ps1", ".rst", ".rtf",
}
MAX_TEXT_BYTES = 5 * 1024 * 1024  # 5 MB


def init_db(db_path: pathlib.Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            ext TEXT,
            size INTEGER,
            mtime REAL,
            mime_type TEXT,
            content TEXT,
            indexed_at TEXT
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS files_fts USING fts5(
            name, content,
            content='files',
            content_rowid='id'
        )
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS files_ai AFTER INSERT ON files BEGIN
            INSERT INTO files_fts(rowid, name, content)
            VALUES (new.id, new.name, new.content);
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS files_ad AFTER DELETE ON files BEGIN
            INSERT INTO files_fts(files_fts, rowid, name, content)
            VALUES ('delete', old.id, old.name, old.content);
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS files_au AFTER UPDATE ON files BEGIN
            INSERT INTO files_fts(files_fts, rowid, name, content)
            VALUES ('delete', old.id, old.name, old.content);
            INSERT INTO files_fts(rowid, name, content)
            VALUES (new.id, new.name, new.content);
        END
    """)
    conn.commit()
    return conn


def is_text_file(path: pathlib.Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(str(path))
    return mime in TEXT_MIMES


def strip_html(text: str) -> str:
    """Remove HTML tags and decode common entities for cleaner indexing."""
    import html

    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def read_text(path: pathlib.Path) -> str:
    try:
        stat = path.stat()
        if stat.st_size > MAX_TEXT_BYTES:
            return ""
        raw = path.read_bytes()
        # Try UTF-8 first; fall back to latin-1 (lossy but readable).
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="ignore")
        if path.suffix.lower() in {".html", ".htm"}:
            text = strip_html(text)
        return text
    except Exception:
        return ""


DEFAULT_EXCLUDES = {
    "__pycache__", "node_modules", ".git", ".venv", "venv",
    "$recycle.bin", "system volume information",
}


def should_skip(path: pathlib.Path, exclude: list[str], include: list[str] | None = None) -> bool:
    name = path.name
    if name.startswith("."):
        return True
    if name.lower() in DEFAULT_EXCLUDES:
        return True
    path_str = str(path).lower()
    for pat in exclude:
        if not pat:
            continue
        pat_lower = pat.lower()
        if pat_lower in name.lower() or pat_lower in path_str:
            return True
    if include:
        # include is a list of extensions like [".md", ".txt"]
        suffix = path.suffix.lower()
        if suffix not in include and name.lower() not in include:
            return True
    return False


def index_source(
    conn: sqlite3.Connection,
    source: pathlib.Path,
    exclude: list[str],
    include: list[str] | None = None,
    commit_every: int = 100,
) -> dict[str, int]:
    cursor = conn.cursor()
    inserted = updated = skipped = errors = 0
    processed = 0

    for root, dirs, files in os.walk(source, topdown=True):
        root_path = pathlib.Path(root)
        # Prune excluded directories.
        dirs[:] = [d for d in dirs if not should_skip(root_path / d, exclude)]

        for filename in files:
            file_path = root_path / filename
            if should_skip(file_path, exclude, include):
                skipped += 1
                continue
            if include is None and not is_text_file(file_path):
                skipped += 1
                continue

            try:
                stat = file_path.stat()
                content = read_text(file_path)
                rel_path = str(file_path.resolve())

                cursor.execute(
                    "SELECT id, mtime FROM files WHERE path = ?", (rel_path,)
                )
                row = cursor.fetchone()
                indexed_at = dt.datetime.now().isoformat()
                if row:
                    if row[1] != stat.st_mtime:
                        cursor.execute(
                            "UPDATE files SET name=?, ext=?, size=?, mtime=?, mime_type=?, content=?, indexed_at=? WHERE id=?",
                            (
                                file_path.name,
                                file_path.suffix.lower(),
                                stat.st_size,
                                stat.st_mtime,
                                mimetypes.guess_type(str(file_path))[0] or "",
                                content,
                                indexed_at,
                                row[0],
                            ),
                        )
                        updated += 1
                else:
                    cursor.execute(
                        "INSERT INTO files (path, name, ext, size, mtime, mime_type, content, indexed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            rel_path,
                            file_path.name,
                            file_path.suffix.lower(),
                            stat.st_size,
                            stat.st_mtime,
                            mimetypes.guess_type(str(file_path))[0] or "",
                            content,
                            indexed_at,
                        ),
                    )
                    inserted += 1
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
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Index files into SQLite for search.")
    ap.add_argument("--name", required=True, help="index name")
    ap.add_argument("--source", required=True, help="source directory")
    ap.add_argument("--db-dir", type=pathlib.Path, default=DEFAULT_DB_DIR)
    ap.add_argument("--exclude", default="", help="comma-separated substrings to exclude")
    ap.add_argument("--include", default="", help="comma-separated file extensions to include, e.g. '.md,.txt,.py'")
    args = ap.parse_args()

    source = pathlib.Path(args.source).expanduser().resolve()
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 1

    db_path = args.db_dir / f"{args.name}.db"
    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    include = [x.strip().lower() for x in args.include.split(",") if x.strip()] or None

    print(f"indexing: {source}")
    print(f"database: {db_path}")

    conn = init_db(db_path)
    stats = index_source(conn, source, exclude, include)
    conn.close()

    print(f"inserted: {stats['inserted']}")
    print(f"updated:  {stats['updated']}")
    print(f"skipped:  {stats['skipped']}")
    print(f"errors:   {stats['errors']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
