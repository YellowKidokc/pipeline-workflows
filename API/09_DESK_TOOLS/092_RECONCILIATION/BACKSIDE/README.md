# 092_RECONCILIATION — Desk Reconciliation

Interactive Stage 5 classification reconciliation.

## Files

- `station.json` — station metadata for the workbench.
- `92_reconciliation.py` — batch runner: reads atom JSON from INBOX, asks Forge for proposals, writes editable proposals to OUTBOX.
- `desk_reconciliation.html` — interactive panel: load an atom, ask Forge for proposals, edit resolutions, stage through canon engine.
- `templates/reconciliation_prompt.txt` — prompt template sent to Forge for proposals.

## Usage

- **Batch:** drop atom JSON files into `INBOX` and run `1 RUN HERE.bat`. Each file gets a proposal written to `OUTBOX`.
- **Interactive:** open `desk_reconciliation.html` in a panel. Load or paste an atom, click **Ask Forge for proposals**, edit, then stage.

## Rules

- AI-proposed classifications come from Forge (`FORGE_URL/v1/chat/completions`, local route).
- Output is badged **AI-PROPOSED** and remains editable.
- Nothing enters the canon graph except through the existing **Stage Candidate** button and its receipt.
- Canon engine calls (`http://127.0.0.1:8765`) are unchanged.
