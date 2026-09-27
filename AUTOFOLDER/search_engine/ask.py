"""
Ask a question across indexed files and API-call logs. Retrieves relevant chunks,
then optionally asks an LLM to synthesize an answer.

Usage:
  python ask.py --all --question "What does the Bible say about resurrection?"
  python ask.py --index obsidian --question "Explain the grace operator"
  python ask.py --index deepseek_calls --question "What output format does DeepSeek prefer?"
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sqlite3
import sys
from typing import Any

os.environ.setdefault("PYTHONUTF8", "1")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_DB_DIR = pathlib.Path(__file__).resolve().parent / "indexes"
MAX_CONTEXT_CHARS = 12000


def _escape_fts5(query: str) -> str:
    cleaned = query.replace('"', '""')
    return f'"{cleaned}"'


STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "as", "is", "was", "are", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "may", "might", "can", "what", "which", "who", "when", "where", "why", "how",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their", "this", "that", "these", "those",
}


def _question_terms(question: str) -> list[str]:
    """Extract search terms from a natural-language question."""
    words = re.findall(r"[a-zA-Z0-9_']+", question)
    terms = [w.lower().strip("'") for w in words if w.lower() not in STOP_WORDS and len(w) > 1]
    if not terms:
        terms = [w.lower() for w in words if len(w) > 1]
    # Deduplicate while preserving order.
    seen = set()
    unique = []
    for t in terms:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:12]


def _question_to_fts5(question: str) -> str:
    """Turn a natural-language question into an FTS5 OR query over its keywords."""
    terms = _question_terms(question)
    return " OR ".join(f'"{t.replace('"', '""')}"' for t in terms)


def _index_type(conn: sqlite3.Connection) -> str:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "messages" in tables:
        return "messages"
    return "files"


def _extract_snippet(text: str, terms: list[str], window: int = 600) -> str:
    """Extract a window of text around the first occurrence of any search term."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lower = text.lower()
    best_pos = -1
    for t in terms:
        pos = lower.find(t)
        if pos != -1 and (best_pos == -1 or pos < best_pos):
            best_pos = pos
    if best_pos == -1:
        # No term matched directly; return the start of the text.
        return text[: window * 2]
    start = max(0, best_pos - window)
    end = min(len(text), best_pos + window)
    snippet = text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def retrieve_file_chunks(db_path: pathlib.Path, question: str, limit: int) -> list[dict[str, Any]]:
    if not db_path.exists():
        return []
    terms = _question_terms(question)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """
        SELECT f.path, f.name, f.content
        FROM files_fts
        JOIN files f ON f.id = files_fts.rowid
        WHERE files_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (_question_to_fts5(question), limit),
    )
    results = []
    for row in cursor.fetchall():
        r = dict(row)
        r["snippet"] = _extract_snippet(r.get("content") or "", terms)
        r["kind"] = "file"
        results.append(r)
    conn.close()
    return results


def retrieve_message_chunks(db_path: pathlib.Path, question: str, limit: int) -> list[dict[str, Any]]:
    if not db_path.exists():
        return []
    terms = _question_terms(question)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        """
        SELECT m.source_file, m.conversation_id, m.role, m.content
        FROM messages_fts
        JOIN messages m ON m.id = messages_fts.rowid
        WHERE messages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (_question_to_fts5(question), limit),
    )
    results = []
    for row in cursor.fetchall():
        r = dict(row)
        r["snippet"] = _extract_snippet(r.get("content") or "", terms)
        r["kind"] = "message"
        results.append(r)
    conn.close()
    return results


def retrieve_chunks(db_path: pathlib.Path, question: str, limit: int) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    kind = _index_type(conn)
    conn.close()
    if kind == "messages":
        return retrieve_message_chunks(db_path, question, limit)
    return retrieve_file_chunks(db_path, question, limit)


def build_context(results: list[dict[str, Any]]) -> str:
    parts = []
    used = 0
    for r in results:
        snippet = r.get("snippet", "")
        if used + len(snippet) > MAX_CONTEXT_CHARS:
            break
        if r.get("kind") == "message":
            header = f"--- conversation: {r['conversation_id']} [{r['role']}] ---"
        else:
            header = f"--- {r['name']} ({r['path']}) ---"
        parts.append(f"{header}\n{snippet}\n")
        used += len(snippet)
    return "\n".join(parts)


def ask_llm(question: str, context: str) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "[No LLM API key found. Set DEEPSEEK_API_KEY or OPENAI_API_KEY.]"

    try:
        from openai import OpenAI
    except ImportError:
        return "[openai package not installed: pip install openai]"

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
    model = os.environ.get("LLM_MODEL", "deepseek-chat")

    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = (
        "You are a research assistant. Use only the provided context to answer. "
        "If the context does not contain the answer, say so.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\nAnswer:"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Answer based only on the provided context."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.3,
        )
        return resp.choices[0].message.content or "[empty response]"
    except Exception as e:
        return f"[LLM error: {e}]"


def list_indexes(db_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted(db_dir.glob("*.db"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Ask a question across indexed files and API calls.")
    ap.add_argument("--question", required=True, help="question to answer")
    ap.add_argument("--index", help="specific index name")
    ap.add_argument("--all", action="store_true", help="search all indexes")
    ap.add_argument("--db-dir", type=pathlib.Path, default=DEFAULT_DB_DIR)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--no-llm", action="store_true", help="only show retrieved context")
    args = ap.parse_args()

    if not args.index and not args.all:
        print("use --index <name> or --all", file=sys.stderr)
        return 1

    indexes = [args.db_dir / f"{args.index}.db"] if args.index else list_indexes(args.db_dir)

    all_results = []
    for db_path in indexes:
        all_results.extend(retrieve_chunks(db_path, args.question, args.limit))

    all_results = sorted(all_results, key=lambda r: len(r.get("snippet", "")), reverse=True)[: args.limit]

    if not all_results:
        print("No relevant files found.")
        return 0

    context = build_context(all_results)
    print("=" * 60)
    print("RETRIEVED CONTEXT")
    print("=" * 60)
    print(context)

    if not args.no_llm:
        print("=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(ask_llm(args.question, context))

    return 0


if __name__ == "__main__":
    sys.exit(main())
