# 68_FORMALIZE_TARGETS

Layer of `55_LEAN_PAPERS`. One claim note in (markdown from the canon docket; HOLD claims especially), one
proposed Lean 4 statement out: complete, compilable-looking, with imports, slot refs, and an explicit
what-it-would-NOT-prove. Per claim: `<title> · 68_FORMALIZE[XX].md` in this layer's OUTBOX (XX = the answering
provider: DS, KIMI, ...).

- Script: `68_formalize_targets.py` (`ONE_MENU.bat 68`; or drop claim notes in this layer's INBOX and `1 RUN HERE`)
- Works on: its own INBOX (00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>), .md/.txt claim notes
- Menu options: limit, workers, provider, model, focus, redo
- Standing focus: `FOCUS.md`

## Rules enforced in code

- Everything is labelled `PROPOSED` — never VERIFIED, never FLOOR. If the model claims anything stronger, code
  stamps it back to PROPOSED with a logged warning. Only a Lean build receipt certifies.
- A proposed statement without a declaration keyword (theorem/def/...) is kept but marked REVIEW.

## API goals

| id | title | asks for |
|---|---|---|
| `API-68.1` | FORMALIZE_TARGETS | claim_id, proposed Lean 4 statement with imports, slot refs, confidence, what it would / would not prove |
