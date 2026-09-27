# Multi-SQLite AI Search Engine

Crawl folders (Obsidian, drives, API logs) into separate SQLite databases with FTS5 full-text search, then query one or all of them. Optionally ask an LLM to answer questions over the retrieved context.

## Files

- `indexer.py` — crawl a directory into a SQLite + FTS5 index.
- `api_call_indexer.py` — parse API-call conversation logs (DeepSeek-style Markdown) into a message index.
- `search.py` — search one or all indexes (files or messages).
- `ask.py` — retrieve relevant chunks and ask an LLM to answer.
- `theo.py` — unified CLI: `theo list`, `theo index-files`, `theo index-calls`, `theo search`, `theo ask`.
- `config.yaml` — example index targets.

## Quick start with the unified CLI

```bash
# List all indexes
python theo.py list

# Index a folder of files
python theo.py index-files --name obsidian --source "C:/Users/David/Documents/faiththruphysics.com/01_WORKING"

# Index API-call conversation logs
python theo.py index-calls --name deepseek_calls --source "D:/GitHub/Research-Acquisition/yt-transcript-downloader/pipeline-workflows/docs/deepseek-conversations"

# Index everything defined in config.yaml
python theo.py index-all

# Search all indexes
python theo.py search "resurrection evidence" --limit 10

# Ask across all indexes (requires LLM key)
python theo.py ask "What is the grace operator?" --limit 5

# Ask without calling an LLM, just show retrieved context
python theo.py ask "What is the grace operator?" --no-llm
```

## Index a folder with the standalone scripts

```bash
python indexer.py --name obsidian --source "C:/Users/David/Documents/faiththruphysics.com/01_WORKING"
```

Index a drive (slow the first time):

```bash
python theo.py index-files --name d_drive --source "D:/" \
  --exclude ".git,node_modules,__pycache__,.venv,venv,dist,build,target,*.mp4,*.mp3,*.wav,*.avi,*.mkv,*.mov,*.zip,*.tar,*.gz,*.rar,*.7z,*.exe,*.dll,*.pdb,*.bin,*.iso,*.img,*.dmg"
```

## Search

```bash
# One index
python theo.py search "resurrection evidence" --index obsidian --limit 10

# All indexes
python theo.py search "grace operator" --limit 20
```

## Ask (LLM-powered)

Requires `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` in environment.

```bash
python theo.py ask "What is the grace operator?" --index obsidian
python theo.py ask "Summarize the case for resurrection" --all
```

To only show retrieved context without calling an LLM:

```bash
python theo.py ask "..." --no-llm
```

## Indexes are stored in

`indexes/<name>.db`

Each database is independent. You can delete, rebuild, or move them individually.

## Supported index types

- **File index**: stores file metadata + content in `files` and `files_fts` tables.
- **API-call index**: stores parsed conversation messages in `messages` and `messages_fts` tables.

`search.py`, `ask.py`, and `theo.py` auto-detect which type each database is and query the right tables.

## Planned extensions

- Incremental updates for API-call indexes (currently deletes and re-inserts per file, which is fast enough for small logs).
- Vector search alongside FTS5.
- HTML tag stripping for cleaner file snippets.
