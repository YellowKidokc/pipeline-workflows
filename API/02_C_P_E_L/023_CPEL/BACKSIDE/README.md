# 23_CPEL: Claims, Proofs, Evidence, Lean

Same layout as 020_CKG: **BACKSIDE** (prompts, script, settings), **INBOX** (00_PRIORITY, 01_SERIES, 02_GENERAL), **OUTBOX**, and the two buttons.

## The four calls

| Call | Job | Reads |
|---|---|---|
| `calls/001_CLAIMS` | Every claim the paper makes: class, lane, physics type, defense class, dependencies, load-bearing, kill condition; plus hidden premises | the paper |
| `calls/002_PROOFS` | The argument the paper gives for each claim: proof type, steps, gaps, circularity, equivocation; every equation with a verdict | paper + CLAIMS |
| `calls/003_EVIDENCE` | Every evidence item (all UNVERIFIED), what part of which claim it covers; evidence needed vs. present vs. gap per claim | paper + CLAIMS |
| `calls/004_LEAN` | Which claims can be stated in Lean 4, with PROPOSED statements ending in `sorry`, assumptions, and the gap between Lean and prose | paper + CLAIMS + PROOFS |

Each call folder has `prompt.md` (what the model is told; the note above the first `---` is for you and isn't sent) and `output.md` (the shape it fills). Order, model, and on/off switches are in `ckg.json`; set `"on": false` to skip a call. Rules come from the spec files in `02_C_P_E_L`.

## Running

- **1 RUN HERE**: everything in INBOX (priority first), through the shared engine like every other station.
- **2 RUN ON FOLDER**: any folder or note you point at.
- Directly: `python 23_cpel.py [notes or folders] [--workers N] [--focus "..."] [--dry-run]`.

Results land in OUTBOX: `<note> · CPEL.md` (the four sections, then the original) and `<note> · CPEL.run.json` (receipt: hashes, model, time and errors per call). A failed call is marked in the page and the receipt; the other calls still run.

It also shows on the web Run page (http://localhost:8771/run) as the variant **cpel**, through a folder link to this BACKSIDE. One copy; edit it here.

## Status

- Dry run tested 2026-10-16.
- **Prompts not yet tested against a model.** Run one paper live and read it before running a folder.
- Everything it writes is AI_PROPOSED. Nothing is ruled or compiled.
