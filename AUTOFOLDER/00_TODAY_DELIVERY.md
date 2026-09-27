# Today's Delivery — Folder Watchers + Router Station

Date: 2026-09-24

## What's in this folder

### 1. `channel_watchers/`
Portable channel watcher for YouTube transcript folders.

Files:
- `watch.py` — watches a `subtitles/<Channel>/` folder, runs the Clean step, then calls DeepSeek indexing.
- `FolderWatcher.py` — reusable filesystem watcher (depends on `watchdog`).
- `deploy_watchers.py` — deploy `watch.py` + `FolderWatcher.py` to every channel folder with `.md` files.

### 2. `router_station/`
Central routing station plus portable relay watcher.

Files:
- `route.py` + `route.yaml` — multi-folder router.
- `relay_watch.py` + `relay.yaml` — single-folder relay watcher.
- `FolderWatcher.py` — shared watcher dependency.
- `deploy_relays.py` — deploys relay watchers to known research download folders.
- `README.md` — router usage reference.

### 3. `relay_deployed_configs/`
Snapshot of `relay.yaml` files dropped into each research download folder.

## Usage

Run `deploy_watchers.py` from `yt-transcript-downloader/subtitles/` to seed channel folders.
Run `deploy_relays.py` from `router_station/` to seed research download folders.
Update `relay.yaml` / `route.yaml` destination paths as needed.

### 4. `cocoindex_bridge_phase1/` (new)
CocoIndex Phase 1 bridge pipeline.

Reads `theophysics_pipeline.db` (424 papers, 3,166 truth predicates) and 356 axioms, emits a knowledge graph as JSON, then scans for contradiction candidates.

Run:
```bash
cd cocoindex_bridge_phase1
python -m pip install -e .
python main.py
python contradiction_radar.py
```

Latest output:
- 6,307 nodes (424 Paper, 3,166 TruthPredicate, 356 Axiom, 2,361 Entity)
- 8,526 edges (3,166 HAS_PREDICATE, 5,360 MENTIONS)
- 2,474 contradiction candidates
