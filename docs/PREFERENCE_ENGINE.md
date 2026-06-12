# Preference Engine

The preference layer observes and calibrates. It never blocks packet execution.

## Learning Chain

```text
Events → River (P06) → PPK (P05) → Implicit (P01) → Markovify (P07)
```

1. **River** (`P06_river`, slot 18) — online learning from immediate events and
   corrections. Runs ACTIVE inside the BIL server at `http://localhost:8420`,
   microsecond latency.
2. **PPK** (`P05_ppk`, slot 17) — Portable Preference Kernel. JSON weights only;
   copy to USB = portable identity, no personal data. The routing/preference spine.
3. **Implicit** (`P01_implicit`, slot 13) — recalculates collaborative/relevance
   patterns from accumulated behavior. Installed, needs wiring.
4. **Markovify** (`P07_markovify`, slot 19) — text prediction. Installed, needs a
   training corpus from clipboard + vault writing.

Slot folders live at `X:\Backside\_models\_Models\P01-P07` (renamed from
13-19 on 2026-06-10). Resolve paths via `models/MODEL_REGISTRY.json`.

## BIL Endpoints

- `http://localhost:8420` — BIL server (River). Start with
  `START_BIL.bat` in `X:\Backside\stations\preference-engine.station`.
- `POST /bil/correction` — correction events from `scripts/correction_logger.py`.

## BIL Signal Weights

Human correction is the strongest signal because it is an explicit override.
Passive behavior is useful but weaker.

| Signal | Weight |
| --- | --- |
| manual_approval | 1.0 |
| file_reused | 0.9 |
| copied_text | 0.8 |
| bookmark_save | 0.7 |
| long_dwell_scroll | 0.5 |
| opened_tab | 0.2 |
| accidental_visit | 0.0 |

These weights are mirrored in `models/MODEL_REGISTRY.json` → `bil_signal_weights`. Preference event shape is documented at `contracts/schemas/preference-event.schema.json` and mirrored at `schemas/preference-event.schema.json`.

## Correction Data

`scripts/correction_logger.py` writes structured JSONL
(`logs/corrections/corrections.jsonl`, compatibility schema: `schemas/correction.schema.json`, contract mirror: `contracts/schemas/correction.schema.json`)
and pushes each event to BIL. If BIL is offline, the local JSONL remains the
source of truth and can be replayed later. The correction log IS the training
data — without it, the system never gets smarter.


## BIL Source Snapshot

The repo-safe BIL source shape lives at `preferences/engines/bil/`. It maps
browser, folder, and manual observations into `contracts/schemas/preference-event.schema.json`
for the P06 River hot loop. This is source/spec only: live services, JSONL event
streams, learned River state, browser installation, and PPK persistence remain
runtime/NAS-side.

## Portable Identity

PPK's whole model is a JSON file
(`file-intelligence.station\_ppk_runtime\portable_preference_kernel.json`).
Copying that file moves David's learned preferences to any machine — no
retraining, no personal data, no infrastructure.
