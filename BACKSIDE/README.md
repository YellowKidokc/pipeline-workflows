# BACKSIDE

Behind-the-scenes material for the repo root. Nothing in here is something you click or drop files into.
Put anything here that the system needs but a person doesn't use directly.

The things you use stay at the root: `API/`, `ConversionStation/`, `workflows/`, `ACTION_CENTER.bat`, `SYSTEM.bat`, `docs/`.

| Folder | What it is |
|---|---|
| `preferences/` | Workflow defaults, profiles and the BIL preference engine |
| `prompts/` | Loose prompts and personas |
| `schemas/` | JSON schemas for workflows, stations, manifests |
| `scripts/` | The older root pipeline: `unified.py` (`SYSTEM.bat`), orchestrator, station runner, packet maker |
| `signals/` | Signal folders (duplicate, gap, quality, ready, upstream) |
| `stations/` | The older root station registry and definitions (not the API stations) |
| `templates/` | Workflow packet and sandbox test templates |
| `tests/` | Tests for the above. Run with `python -m pytest BACKSIDE/tests` from the repo root |
| `tools/` | Action Center (`ACTION_CENTER.bat`), drop watcher, prompt box |

Paths: code in here treats `BACKSIDE/` as its root for these sibling folders. For `workflows/` and
`pipeline.config.json` it uses the folder above (the repo root).

Moved here on 2026-10-11. Before the move, `scripts/unified.py` (`SYSTEM.bat`) and 18 of the test files already failed
because the `engines/` and `openintel/` packages they import are gone. That was already true and the move didn't change it.
