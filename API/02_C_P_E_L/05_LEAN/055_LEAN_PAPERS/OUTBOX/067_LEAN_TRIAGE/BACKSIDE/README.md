# 67_LEAN_TRIAGE

Layer of `55_LEAN_PAPERS`. Whole-corpus triage: one compact JSON call per Lean file — what kind of file it is,
one-line purpose, quality, duplicate hint, and the action to take. Files up to ~2000 lines go in whole; longer
files go in as the first 400 lines plus the declaration list, marked PARTIAL. Per file:
`<title> · 67_TRIAGE[XX].md` in this layer's OUTBOX (XX = the answering provider: DS, KIMI, ...), plus
`00_TRIAGE.md` rebuilt after every item, sorted by action.

- Script: `67_lean_triage.py` (`ONE_MENU.bat 67`; or drop .lean files in this layer's INBOX and `1 RUN HERE`)
- Works on: its own INBOX (00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>), or files/folders named on the command line
- Menu options: limit, workers, provider, model, focus, redo
- Standing focus: `FOCUS.md`

## Rules enforced in code

- `file_kind` / `quality` / `action` outside their ruled vocabularies are coerced (scratch / draft / keep) with a logged warning.
- `nominate_floor` only travels with `floor_candidate` quality.
- `delete_candidate` is a label for David; this station never deletes anything.
- `floor_candidate` is a nomination: only a build receipt puts a file on the floor.

## API goals

| id | title | asks for |
|---|---|---|
| `API-67.1` | LEAN_TRIAGE | file kind, purpose, quality, duplicate hint, action |
