# Troubleshooting

## First move: run the canary

```text
python scripts/canary.py
```

| Verdict | Meaning | Fix |
|---|---|---|
| active | path exists, entry point found | nothing |
| degraded | path exists but claimed RUN.bat is missing, or folder empty | check the station folder; fix `has_run_bat` in the registry if the claim is wrong |
| dead | path does not exist | station moved or drive not mounted — see Path problems |

Known-good baseline: at least 23 active (52/52 as of 2026-06-10).

## Path problems

- Station paths use `X:\Backside\...`. `X:` is the mapped drive for
  `\\dlowenas\brain`. Services and scheduled tasks don't see per-user drive
  mappings — scripts fall back to the UNC root automatically; override with
  the `FORGE_BRAIN_ROOT` environment variable.
- `models_root` moved to the M/P scheme on 2026-06-10
  (`M01_summarizer`…`P07_markovify`). Anything still pointing at
  `01_summarizer`/`13_preference_implicit`-style folders is stale — resolve
  through `models/MODEL_REGISTRY.json`.

## Workflow stuck on "hold"

That is the human approval gate working. Write
`CONFIG/approval.json` → `{"approved": true}` into the packet and re-run the
same orchestrator command. To reject, use `{"approved": false, "reason": "..."}`.

## Stage keeps failing

- Read `LOGS/orchestrator.log` and `LOGS/<station>.run.log` in the packet.
- Run the station alone: `python scripts/station_runner.py <name> <packet>`.
- `on_error: stop` halts the run; `skip` records the failure and continues.

## Ollama gate returns "review" every time

The phi4 checkpoint couldn't reach Ollama. Check `http://localhost:11434` is
up and the `ollama_model` in `pipeline.config.json` is pulled
(`ollama pull phi4`). Gates never call cloud models — offline Ollama means
the gate degrades to "review", it does not fail the packet.

## BIL not learning from corrections

- BIL server must be on `http://localhost:8420` (`START_BIL.bat` in
  preference-engine.station).
- Corrections still land in `logs/corrections/corrections.jsonl` when BIL is
  offline — the local log is the source of truth and can be replayed.

## MANIFEST.json out of sync

Rebuild from the packets on disk:

```text
python scripts/manifest_tracker.py <packet-root> [...more roots]
```

## STATUS.json from a previous run blocks a fresh start

Run with `--no-resume` to ignore it (the file is overwritten, inputs are not
touched), or delete the STATUS.json — never anything in INPUT/.
