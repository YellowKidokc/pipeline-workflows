# Architecture

Three repos, one system. This repo is the wiring — it connects existing machines and
builds none of its own.

```text
┌─────────────────────────────────────────────────────────┐
│  FIS   file-intelligence-system      PERCEPTION          │
│        "What is this file?"                              │
│        X:\Backside\stations\file-intelligence.station    │
├─────────────────────────────────────────────────────────┤
│  BIL   behavioral-intelligence-layer  PREFERENCE         │
│        "Does David care?"                                │
│        X:\BIL  — River server on http://localhost:8420   │
├─────────────────────────────────────────────────────────┤
│  Pipeline  pipeline-workflows         ACTION             │
│        "What happens next?"                              │
│        This repo: configs + orchestrator                 │
└─────────────────────────────────────────────────────────┘
```

Pipeline orchestrates. FIS and BIL are called AS stations inside workflows
(`file-intelligence`, `preference-engine`). They stay separate repos.

## What lives where

| Thing | Location |
|---|---|
| Station code (the machines) | `X:\Backside\stations\*.station` |
| Model weights | `X:\Backside\_models\_Models\M01-M12, P01-P07` |
| Station configs (pointers + I/O contracts) | `stations/` in this repo |
| Model slot configs | `models/` in this repo |
| Workflow DAGs | `workflows/` in this repo |
| Orchestrator + tools | `scripts/` in this repo |
| Vault (destination) | `O:\_Theophysics_v4` |
| GTQ build | `T:\1111genesis-to-quantum` |

## Registries — single sources of truth

- `stations/STATION_REGISTRY.json` — every station, its real path, status, RUN.bat presence.
- `models/MODEL_REGISTRY.json` — all 19 model slots (M/P scheme). Reference the registry, never hardcode model paths.
- `workflows/WORKFLOW_REGISTRY.json` — every defined workflow.

## Packet contract (locked)

Every workflow packet has exactly these folders:
`INPUT/ OUTPUT/ REVIEW/ ARCHIVE/ ERROR/ CONFIG/ PREFS/ PROMPTS/ SCRIPTS/ LOGS/`
plus `STATUS.json` written by the orchestrator after every stage.

## Flow

```text
copied file → INPUT/ → stations (per workflow DAG) → OUTPUT|REVIEW|ERROR
                                  ↑ phi4 checkpoints (Ollama, local only)
                                  ↓ signals + STATUS.json + MANIFEST.json
            human approval gate → corrections logged → BIL learns
```

Rules that hold everywhere:
- Vectorize BEFORE classify (see STATION_DOCTRINE.md).
- Copies only. Nothing original is ever modified, moved, or deleted.
- All destructive actions require human approval (`CONFIG/approval.json`).
- LLM checkpoints run on local Ollama phi4 — never a cloud model.

## Two views

Internal schema (builders): `Intake -> Transform -> Validate -> Route -> Signals`.

Consumer front end (David): drop something in, see what it became, review what
needs a decision, see where it went. Workflows expose folders and scripts, not
the machine room.
