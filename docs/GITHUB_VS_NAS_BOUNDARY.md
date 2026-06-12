# GitHub vs NAS Boundary

GitHub is the **governor/spec layer**. NAS is the **runtime/body layer**.

## GitHub owns

- Interface contracts in `contracts/`.
- Compatibility schemas in `schemas/` while existing consumers still use them.
- Registries such as `models/MODEL_REGISTRY.json`, `stations/STATION_REGISTRY.json`,
  and `workflows/WORKFLOW_REGISTRY.json`.
- Documentation, tests, prompts, and non-secret examples.

## NAS owns

- Model weights and runtime model folders.
- Live station bodies and executable station folders.
- Generated outputs, vector indexes, databases, logs, and secrets.
- Runtime packet contents unless explicitly represented by a schema/contract.

## Doctrine

- FIS = perception.
- BIL = preference.
- Pipeline = action.
- Vectorize before classify.
- Nothing destructive happens without an approval packet.
