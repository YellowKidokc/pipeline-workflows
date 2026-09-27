# POF 2828 — Handoff to Codex: Watcher + Master API Architecture

## Goal

Build a distributed watcher system that reports file events to a central Master API. The Master API decides what to do and sends instructions back. Watchers never act on their own.

The API must be **always-on**, with the NAS as primary and the desktop as failover.

---

## Port Map (POF 2828)

| Port  | Service                    | Channel |
|-------|----------------------------|---------|
| 28280 | Master API (orchestrator)  | χ       |
| 28281 | PostgreSQL proxy           | G       |
| 28282 | FIS (File Intelligence System) | M   |
| 28283 | NLP Pipeline               | E       |
| 28284 | Dedup daemon               | S       |
| 28285 | TTS (Text to Speech)       | T       |
| 28286 | Lossless Compression       | K       |
| 28287 | Comms Hub                  | R       |
| 28288 | Clipboard                  | Q       |
| 28289 | Cross-service bridge       | F       |
| 28290 | Health dashboard           | C       |

**Network topology**

| Machine | LAN (1GbE)   | Direct (10GbE) |
|---------|--------------|----------------|
| Desktop | 192.168.1.76 | 192.168.2.51   |
| NAS     | 192.168.1.177| 192.168.2.50   |
| Laptop  | TBD          | —              |

**NAS brain stack**

- Qdrant: `:6333`
- Infinity: `:7997`
- PIL API: `:8420`
- Ollama: `:11434`
- PostgreSQL: `:2665`

**Design intent**: desktop is the GPU box. NAS runs always-on pure Python services (FIS, Clipboard, Comms, Health). Laptop is fallback. Master API at `:28280` discovers what's running where and proxies to the best route, preferring 10GbE.

---

## Watcher Agent Pattern

### Each watched folder gets

- `watcher_agent.py`
- `watcher_agent.yaml`

### What the watcher does

1. Watches the folder for created/modified files.
2. Inspects the file (extension, size, quick regex).
3. Guesses a type and proposed action.
4. POSTs a report to the Master API.
5. Does **only** what the API responds with.

### Report payload

```json
{
  "event": "created",
  "source_folder": "D:/GitHub/Research-Acquisition/yt-transcript-downloader/subtitles/Gary Habermas",
  "file_path": "D:/.../Gary Habermas/Chapter 100.md",
  "detected_type": "markdown_transcript",
  "proposed_action": "copy to CKG inbox",
  "timestamp": "2026-09-24T..."
}
```

### API response

```json
{
  "action": "copy",
  "destination": "//192.168.2.50/h_hp/Desktop/APIs/APIs/CKG/INBOX",
  "reason": "markdown transcript -> CKG"
}
```

or

```json
{
  "action": "hold",
  "queue": "human_review",
  "reason": "ambiguous file type"
}
```

---

## End-to-End Workflow Example

1. **Video downloads** into `D:/.../downloads/<channel>/`.
   - Watcher reports: `"type": "video"`
   - API responds: `"action": "move", "destination": "X:/conversion_center/inbox"`

2. **Conversion finishes** — `.srt` and `.md` appear in `X:/conversion_center/outbox/`.
   - Watcher reports: `"type": "transcript"`
   - API responds:
     - `"action": "copy", "destination": "D:/.../obsidian_transcripts/<channel>"` for the `.md`
     - `"action": "copy", "destination": "D:/.../srt_archive"` for the `.srt`

3. **Markdown arrives in Obsidian folder**.
   - Watcher reports: `"type": "markdown"`
   - API responds: `"action": "copy", "destination": "//192.168.2.50/.../CKG/INBOX"`

4. **API processing done** — output files appear.
   - Watcher reports: `"type": "processed"`
   - API responds: `"action": "move", "destination": "D:/.../consumed"`

5. **Consumed folder hits 20 files**.
   - Watcher reports: `"event": "batch_ready", "count": 20`
   - API responds: `"action": "zip_and_move", "destination": "//192.168.2.50/.../NAS/archive"`

---

## Master API Requirements

### Core endpoints

- `GET /health` — used by failover monitor and watchers.
- `POST /intake` — receive watcher reports.
- `GET /jobs/{job_id}` — check status of a file job.
- `POST /command/{job_id}` — external system (or human) can approve/reject/reroute a held job.
- `GET /dashboard` — simple JSON summary of recent events and queues.

### State tracking

Each file gets a job record in SQLite:

```json
{
  "job_id": "uuid",
  "file_path": "...",
  "current_state": "awaiting_conversion",
  "history": [
    {"state": "downloaded", "at": "..."},
    {"state": "moved_to_conversion", "at": "..."},
    {"state": "converted", "at": "..."}
  ]
}
```

### Routing policy

Start with rule-based routing by `detected_type` and file extension. Later add LLM classification.

### Actions the API can return

- `copy`
- `move`
- `hold`
- `delete`
- `zip_and_move`
- `run_command` (with a `command` string and placeholders)
- `none`

---

## Failover / Always-On Design

### Primary

Master API runs on the NAS at `http://192.168.2.50:28280`.

### Failover

A small monitor script `api_failover.py` runs on the desktop:

```python
while True:
    if not nas_api_is_healthy("http://192.168.2.50:28280/health"):
        start_local_api(port=28280)
    time.sleep(5)
```

Decision: **leave the local API running until reboot** when the NAS comes back (simpler). Watcher agents try NAS first, then `http://127.0.0.1:28280`.

---

## Obsidian Integration

Obsidian vaults are folders. Drop `watcher_agent.py` + `watcher_agent.yaml` into any Obsidian vault folder. On change, the watcher reports to the API, and the API can:

- Copy the note to CKG inbox.
- Trigger the CocoIndex bridge update.
- Queue it for claim/predicate extraction.
- Move the original to a consumed folder.

First version should use folder watchers. A custom Obsidian plugin can come later.

---

## Existing Code to Reuse

All of this is already in `AUTOFOLDER/`:

- `channel_watchers/` — `watch.py` + `FolderWatcher.py` + `deploy_watchers.py`
- `router_station/` — `route.py`, `relay_watch.py`, `FolderWatcher.py`, configs, deploy scripts
- `relay_deployed_configs/` — relay YAML snapshots
- `cocoindex_bridge_phase1/` — working CocoIndex pipeline that reads SQLite + axioms and emits a graph

**Do not rebuild from scratch.** Use `watcher_agent.py` as a thin wrapper around `FolderWatcher.py` that POSTs to the API instead of acting directly.

---

## Deliverables for Codex

1. `master_api.py` — FastAPI server on port `28280`.
2. `api_failover.py` — desktop monitor that starts local API if NAS is down.
3. `watcher_agent.py` — drop-in folder watcher.
4. `watcher_agent.yaml` — config template.
5. SQLite job/state schema.
6. Rule-based router.
7. Tests with temp folders.

---

## Notes from Current Session

- UTF-8 encoding must be explicit on every file open (`encoding="utf-8"`) or set `PYTHONUTF8=1`.
- CocoIndex vendored copy was removed from `Canonizationv1`; install from PyPI.
- Neo4j was not available in this environment, so the CocoIndex bridge targets JSON files for now. Neo4j target is next.
- Network share `\\192.168.2.50\h_hp\Desktop\____NEW_SUPER_FOLDER\API\AUTOFOLDER\` was unreachable at the end of this session; local copies are current.
