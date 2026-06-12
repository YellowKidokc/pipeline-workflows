# Adding a Workflow

A workflow is a DAG defined in JSON. No code.

## 1. Define the DAG

Create `workflows/<name>.json` validating against `schemas/workflow.schema.json` (compatibility path) and its mirror `contracts/schemas/workflow.schema.json`:

```json
{
  "name": "<name>",
  "description": "What it does",
  "version": "0.1",
  "stages": [
    { "name": "intake", "station": "conversion-station", "on_error": "stop", "depends_on": [] },
    { "name": "vectorize", "station": "sbert-embedder", "on_error": "stop", "depends_on": ["intake"] },
    { "name": "classify", "station": "classify-documents", "on_error": "stop", "depends_on": ["vectorize"] },
    {
      "name": "framework-check",
      "station": "fruits-spirit-canon",
      "parallel": true,
      "stations": ["fruits-spirit-canon", "master-equation-canon", "trinity-canon"],
      "on_error": "continue",
      "depends_on": ["classify"]
    }
  ],
  "preference_profile": "defaults.json",
  "signals": ["quality", "ready"]
}
```

Rules:
- Every `station` must exist in `stations/STATION_REGISTRY.json` (or be a `_` built-in).
- Vectorize BEFORE classify. No exceptions in analysis workflows (STATION_DOCTRINE.md).
- `on_error`: `stop` | `skip` | `continue`.
- `llm_gate` on a stage runs an Ollama phi4 checkpoint. Local only.
- Human gates: add a stage with station `_await_approval`. The run HOLDs until
  someone writes `CONFIG/approval.json` `{"approved": true}` in the packet. The interface is documented at `contracts/schemas/approval.schema.json` and mirrored at `schemas/approval.schema.json`.

## 2. Register it

Add the workflow to `workflows/WORKFLOW_REGISTRY.json`.

## 3. Run it

```text
python scripts/orchestrator.py <name> path\to\packet --dry-run   # DAG/status check, no stations
python scripts/orchestrator.py <name> path\to\packet             # real run
```

The orchestrator writes `STATUS.json` after every stage and updates
`MANIFEST.json`. Resume is automatic: completed stages are skipped, held
stages re-run.
