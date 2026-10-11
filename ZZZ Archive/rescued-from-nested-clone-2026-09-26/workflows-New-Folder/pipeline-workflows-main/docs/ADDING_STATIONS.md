# Adding a Station

Stations are machines that live on `X:\Backside`. This repo only points at them.
If you are writing NLP code, training loops, or inference logic here — stop.
Write a config that points to the existing code instead.

## 1. Confirm the station exists on disk

```text
X:\Backside\stations\<name>.station\
```

It needs an entry point: `RUN.bat`, a `prompt.md`/`station.json` (prompt-based),
or a package entry (`*.ps1`, `pyproject.toml`, `package.json`).

## 2. Create the config

Add `stations/<category>/<name>.json` (categories: analysis, framework,
processing, media, graph, intelligence). It must validate against
`schemas/station.schema.json` (compatibility path) and its mirror `contracts/schemas/station.schema.json`:

```json
{
  "name": "<name>",
  "version": "1.0",
  "path": "X:\\Backside\\stations\\<name>.station",
  "type": "local",
  "has_run_bat": true,
  "status": "active",
  "input":  { "accepts": ["md", "txt"], "source": "INPUT/" },
  "output": { "produces": ["json"], "destination": "OUTPUT/" },
  "llm_checkpoint": { "enabled": false, "engine": "ollama:phi4", "prompt": null },
  "dependencies": [],
  "idempotency": { "method": "input_hash", "cache": "ARCHIVE/" }
}
```

## 3. Register it

Add the same name to `stations/STATION_REGISTRY.json` with `path`, `type`,
`has_run_bat`, `status`, `category`. One entry per station — workflows resolve
paths from the registry, never from hardcoded strings.

## 4. Verify

```text
python scripts/canary.py            # must report the station active
python scripts/station_runner.py <name> path\to\test_packet
```

## 5. Wire it into a workflow

Reference the station by registry name in a workflow stage. See
ADDING_WORKFLOWS.md.

Names starting with `_` (`_manifest`, `_await_approval`, `_log_correction`,
`_archive_input`) are orchestrator built-ins, not disk stations — don't reuse
the prefix.
