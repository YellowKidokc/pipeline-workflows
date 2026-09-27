# Contracts

`contracts/` is the repo's interface-promise layer. Use it when a future Codex
session needs to understand what a workflow, station, packet, approval, model
slot, or exported artifact is allowed to look like.

## Boundary rule

- **Contracts** describe stable interfaces between GitHub governor/spec files and
  NAS runtime/body processes.
- **Schemas** in `schemas/` remain the current compatibility location for code,
  tests, and docs that already import `schemas/*.schema.json`.
- Contract schema mirrors live under `contracts/schemas/` so new readers can
  start here without breaking old import paths.
- Do not put runtime configs, generated outputs, station bodies, model weights,
  vector indexes, databases, secrets, or NAS artifacts in this directory.

## Priority contract map

| Interface promise | Contract path | Compatibility path | Status |
| --- | --- | --- | --- |
| Workflow DAG | `contracts/schemas/workflow.schema.json` | `schemas/workflow.schema.json` | mirrored |
| Station config | `contracts/schemas/station.schema.json` | `schemas/station.schema.json` | mirrored |
| Model slot config | `contracts/schemas/model.schema.json` | `schemas/model.schema.json` | mirrored |
| BIL preference event | `contracts/schemas/preference-event.schema.json` | `schemas/preference-event.schema.json` | mirrored |
| Human correction | `contracts/schemas/correction.schema.json` | `schemas/correction.schema.json` | mirrored |
| Human approval gate | `contracts/schemas/approval.schema.json` | `schemas/approval.schema.json` | mirrored |
| Export manifest | `contracts/schemas/export-manifest.schema.json` | `schemas/export-manifest.schema.json` | mirrored |
| Packet/global manifest | `contracts/schemas/manifest.schema.json` | `schemas/manifest.schema.json` | mirrored |

## Compatibility doctrine

For this reorg phase, **do not move or delete `schemas/` files**. Add or update
contract mirrors, then keep tests validating both paths until runtime consumers
are deliberately migrated in a later approval-backed PR.
