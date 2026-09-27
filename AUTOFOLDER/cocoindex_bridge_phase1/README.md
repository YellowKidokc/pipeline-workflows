# Phase 1 CocoIndex Bridge — Faith Through Physics

A deterministic, zero-API-cost CocoIndex v1 pipeline that reads existing extracted
data and emits a knowledge graph as JSON.

## What it does

- Reads 424 papers and 3,166 truth predicates from
  `D:/GitHub/Canonizationv1/theophysics_pipeline.db`.
- Reads 356 axiom-candidate packets from
  `D:/GitHub/Canonizationv1/Canonization-integration-20260904/workbench/axiom-all-nodes.js`.
- Emits `nodes.json` and `edges.json` to the output directory.
- A standalone `contradiction_radar.py` then scans the graph and reports
  contradiction candidates based on predicate modality polarity.

## Install

Run these commands **inside** `bridge/cocoindex-pipeline/`:

```bash
python -m pip install -e .
```

> Important: run from the pipeline subfolder, not the repo root, so that
> `import cocoindex` resolves to the installed package and is not shadowed by any
> stale `cocoindex/` directory.

## Run the pipeline

### Option A — `cocoindex` CLI

```bash
cocoindex update main.py
```

For a full reprocess:

```bash
cocoindex update main.py --full-reprocess
```

### Option B — plain Python

```bash
python main.py
```

Both write:

- `output/nodes.json`
- `output/edges.json`

## Run the contradiction radar

```bash
python contradiction_radar.py
```

This reads `output/nodes.json` and `output/edges.json`, writes
`output/contradictions.json`, and prints a top-20 summary to stdout.

## Configure paths

Set environment variables to override defaults:

| Variable | Default |
|---|---|
| `THEOPHYSICS_DB` | `D:/GitHub/Canonizationv1/theophysics_pipeline.db` |
| `AXIOM_NODES_JS` | `D:/GitHub/Canonizationv1/Canonization-integration-20260904/workbench/axiom-all-nodes.js` |
| `OUTPUT_DIR` | `D:/GitHub/Canonizationv1/bridge/cocoindex-pipeline/output` |

Example:

```bash
export THEOPHYSICS_DB="D:/some/other.db"
cocoindex update main.py
```

On Windows PowerShell use `$env:THEOPHYSICS_DB = "..."`.

## UTF-8

The scripts set `PYTHONUTF8=1` at the top of each file. If you run into encoding
issues, also set it in your shell before running:

```bash
export PYTHONUTF8=1
```

## Project layout

```
bridge/cocoindex-pipeline/
├── pyproject.toml
├── schema.py              # dataclasses for nodes/edges
├── main.py                # CocoIndex v1 app
├── contradiction_radar.py # standalone contradiction scanner
├── README.md
└── output/                # generated JSON files
    ├── nodes.json
    ├── edges.json
    └── contradictions.json
```
