# Station Source Mirror

`stations/source/` is a **repo-safe station snapshot area** for online prompting,
code review, and contract discussion. It is not the live station runtime.

## Boundary

- Live station paths stay in `stations/STATION_REGISTRY.json` and currently point
  to NAS/runtime locations such as `X:\Backside\stations\*.station`.
- This directory may contain sanitized source snapshots, station manifests,
  configs/examples, docs, prompts, and tests when those files are safe for GitHub.
- This directory must not contain model weights, generated outputs, vector
  indexes, databases, secrets, runtime logs, generated exports, or NAS artifacts.

## Current audit status

No station source snapshots are currently mirrored here. `AUDIT.json` records all
registry stations as missing snapshots so future cleanup can distinguish
"missing from mirror" from "missing from runtime."

## Adding a safe snapshot later

1. Keep the live path unchanged in `stations/STATION_REGISTRY.json`.
2. Add a sanitized folder named after the registry key, for example
   `stations/source/sbert-embedder/`.
3. Preserve source code, manifests, config examples, docs, prompts, and tests.
4. Exclude runtime outputs, logs, vector/database files, model weights, secrets,
   and generated exports.
5. Update `AUDIT.json` and run the station-source tests.

If a file is uncertain, document it in the audit instead of deleting or adding it.
