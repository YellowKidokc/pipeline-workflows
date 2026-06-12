# Reorganization Packet

- Generated: 2026-06-12T19:07:15.568211+00:00
- Findings: 1
- Suggested moves: 4

## Doctrine

- GitHub is the governor/spec layer.
- NAS is the runtime/body layer.
- Models are top-level contracts under `models/`; weights stay on NAS.
- Station bodies may be mirrored under `stations/source/`, but live paths stay in `stations/STATION_REGISTRY.json`.
- No move executes until the approval file is edited.

## Suggested Moves

| Status | From | To | Reason |
|---|---|---|---|
| needs_review | `schemas/model.schema.json` | `contracts/model.schema.json` | Schemas are contracts. Keep compatibility alias if code imports old path. |
| needs_review | `schemas/workflow.schema.json` | `contracts/workflow.schema.json` | Workflow schema belongs with contracts. |
| needs_review | `schemas/station.schema.json` | `contracts/station.schema.json` | Station schema belongs with contracts. |
| needs_review | `models/preference/*.json` | `preferences/engines/` | Preference engine configs should live with preferences; model registry stays in models/. |

## Findings

| Kind | Path | Recommendation | Target | Reason |
|---|---|---|---|---|
| noncanonical_root | `logs` | move_or_explain | `david/DOES_NOT_FIT.md` | Top-level folder is outside the current architecture. |
