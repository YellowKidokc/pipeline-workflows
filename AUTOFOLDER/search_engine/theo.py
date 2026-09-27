"""
Unified CLI for the multi-SQLite AI search engine.

Usage:
  theo list
  theo index-files --name obsidian --source "C:/Users/David/..."
  theo index-calls --name deepseek_calls --source "D:/.../deepseek-conversations"
  theo search "resurrection evidence" [--index obsidian] [--limit 10]
  theo ask "What is the grace operator?" [--index obsidian] [--limit 5] [--no-llm]
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sqlite3
import sys
from typing import Any

os.environ.setdefault("PYTHONUTF8", "1")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_DB_DIR = pathlib.Path(__file__).resolve().parent / "indexes"
DEFAULT_CONFIG = pathlib.Path(__file__).resolve().parent / "config.yaml"

# Import sibling modules.
import indexer as file_indexer
import api_call_indexer as call_indexer
import search as search_mod
import ask as ask_mod


def cmd_list(args: argparse.Namespace) -> int:
    import json

    indexes = search_mod.list_indexes(args.db_dir)
    if not indexes:
        if args.json:
            print(json.dumps({"indexes": []}))
        else:
            print("No indexes found.")
        return 0

    data = [{"name": p.stem, "size": p.stat().st_size if p.exists() else 0} for p in indexes]
    if args.json:
        print(json.dumps({"indexes": data}))
    else:
        print("Indexes:")
        for item in data:
            print(f"  {item['name']:30} {item['size']:>12,} bytes")
    return 0


def cmd_index_files(args: argparse.Namespace) -> int:
    source = pathlib.Path(args.source).expanduser().resolve()
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 1
    db_path = args.db_dir / f"{args.name}.db"
    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    include = [x.strip().lower() for x in args.include.split(",") if x.strip()] or None
    print(f"indexing files: {source}")
    print(f"database: {db_path}")
    conn = file_indexer.init_db(db_path)
    stats = file_indexer.index_source(conn, source, exclude, include)
    conn.close()
    print(f"inserted: {stats['inserted']}")
    print(f"updated:  {stats['updated']}")
    print(f"skipped:  {stats['skipped']}")
    print(f"errors:   {stats['errors']}")
    return 0


def cmd_index_calls(args: argparse.Namespace) -> int:
    source = pathlib.Path(args.source).expanduser().resolve()
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 1
    db_path = args.db_dir / f"{args.name}.db"
    print(f"indexing calls: {source}")
    print(f"database: {db_path}")
    conn = call_indexer.init_db(db_path)
    stats = call_indexer.index_source(conn, source)
    conn.close()
    print(f"files:    {stats['files']}")
    print(f"inserted: {stats['inserted']}")
    print(f"updated:  {stats['updated']}")
    print(f"skipped:  {stats['skipped']}")
    print(f"errors:   {stats['errors']}")
    print(f"messages in index: {stats['messages']}")
    return 0


def _load_config(path: pathlib.Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError:
        print("PyYAML is required for index-all. Install: pip install pyyaml", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def cmd_index_all(args: argparse.Namespace) -> int:
    cfg = _load_config(args.config)
    failed = 0

    file_indexes = cfg.get("indexes", {})
    for name, spec in file_indexes.items():
        print(f"\n=== index-files: {name} ===")
        sub = argparse.Namespace(
            name=name,
            source=spec["source"],
            exclude=spec.get("exclude", ""),
            include=spec.get("include", ""),
            db_dir=args.db_dir,
        )
        if cmd_index_files(sub) != 0:
            failed += 1

    call_indexes = cfg.get("call_indexes", {})
    for name, spec in call_indexes.items():
        print(f"\n=== index-calls: {name} ===")
        sub = argparse.Namespace(
            name=name,
            source=spec["source"],
            db_dir=args.db_dir,
        )
        if cmd_index_calls(sub) != 0:
            failed += 1

    print(f"\nindex-all finished with {failed} failures.")
    return 0 if failed == 0 else 1


def cmd_search(args: argparse.Namespace) -> int:
    import json

    indexes: list[pathlib.Path] = []
    if args.index:
        indexes = [args.db_dir / f"{args.index}.db"]
    else:
        indexes = search_mod.list_indexes(args.db_dir)

    output: list[dict[str, Any]] = []
    total = 0
    for db_path in indexes:
        results = search_mod.search_index(db_path, args.query, args.limit)
        if results:
            if args.json:
                output.append({"index": db_path.stem, "results": results})
            else:
                print(f"\n=== {db_path.stem} ({len(results)} results) ===")
                for r in results:
                    print(search_mod.format_result(r, db_path.stem))
            total += len(results)

    if args.json:
        print(json.dumps({"total": total, "indexes": output}, indent=2))
    else:
        print(f"\ntotal results: {total}")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    indexes: list[pathlib.Path] = []
    if args.index:
        indexes = [args.db_dir / f"{args.index}.db"]
    else:
        indexes = ask_mod.list_indexes(args.db_dir)

    all_results: list[dict[str, Any]] = []
    for db_path in indexes:
        all_results.extend(ask_mod.retrieve_chunks(db_path, args.question, args.limit))

    all_results = sorted(all_results, key=lambda r: len(r.get("snippet", "")), reverse=True)[: args.limit]

    if not all_results:
        print("No relevant results found.")
        return 0

    context = ask_mod.build_context(all_results)
    print("=" * 60)
    print("RETRIEVED CONTEXT")
    print("=" * 60)
    print(context)

    if not args.no_llm:
        print("=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(ask_mod.ask_llm(args.question, context))

    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Theophysics search engine CLI")
    ap.add_argument("--db-dir", type=pathlib.Path, default=DEFAULT_DB_DIR, help="directory for .db indexes")
    ap.add_argument("--config", type=pathlib.Path, default=DEFAULT_CONFIG, help="path to config.yaml")
    sub = ap.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list indexes")
    p_list.add_argument("--json", action="store_true", help="output JSON")

    p_idx = sub.add_parser("index-files", help="index a folder of files")
    p_idx.add_argument("--name", required=True)
    p_idx.add_argument("--source", required=True)
    p_idx.add_argument("--exclude", default="", help="comma-separated substrings to exclude")
    p_idx.add_argument("--include", default="", help="comma-separated file extensions to include, e.g. '.md,.txt,.py'")

    p_calls = sub.add_parser("index-calls", help="index API-call conversation logs")
    p_calls.add_argument("--name", required=True)
    p_calls.add_argument("--source", required=True)

    p_all = sub.add_parser("index-all", help="index all targets defined in config.yaml")

    p_search = sub.add_parser("search", help="search indexes")
    p_search.add_argument("query", help="search query")
    p_search.add_argument("--index", help="specific index name")
    p_search.add_argument("--limit", type=int, default=10)
    p_search.add_argument("--json", action="store_true", help="output JSON")

    p_ask = sub.add_parser("ask", help="ask a question across indexes")
    p_ask.add_argument("question", help="question to answer")
    p_ask.add_argument("--index", help="specific index name")
    p_ask.add_argument("--limit", type=int, default=5)
    p_ask.add_argument("--no-llm", action="store_true", help="only show retrieved context")

    args = ap.parse_args()

    handlers = {
        "list": cmd_list,
        "index-files": cmd_index_files,
        "index-calls": cmd_index_calls,
        "index-all": cmd_index_all,
        "search": cmd_search,
        "ask": cmd_ask,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
