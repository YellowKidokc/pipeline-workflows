# GitHub Prompt: Preference Loop Wiring

Goal: wire preference learning as a visible system, not scattered scripts.

Core stack:

```text
P06_river       hot loop
P05_ppk         identity loop
P01_implicit    pattern loop
P03_lightfm     hybrid loop
P07_markovify   voice loop
```

Tasks:

1. Make `contracts/preference-event.schema.json` match `scripts/correction_logger.py`.
2. Make `preferences/signal-weights.json` the canonical source for BIL signal weights.
3. Ensure `workflows/preference-learning.json` matches `models/preference-chain.json`.
4. Add a replay path for offline correction logs into BIL.
5. Make approval/rejection/correction events feed the same schema.

Constraints:

- Human correction is strongest signal.
- BIL offline is allowed; local JSONL remains source truth.
- No real learned PPK weights in GitHub.

Expected output:

- Schema/code/doc alignment.
- A small replay script if needed.
- Tests or smoke checks for correction event shape.
