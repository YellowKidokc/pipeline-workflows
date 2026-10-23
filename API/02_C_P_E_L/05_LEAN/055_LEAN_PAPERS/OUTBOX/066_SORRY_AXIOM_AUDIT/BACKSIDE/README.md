# 66_SORRY_AXIOM_AUDIT

Layer of `55_LEAN_PAPERS`. Every `sorry` / `admit` / `axiom` / `native_decide` in a Lean source is found in
code first (free, no API, comments stripped), then one JSON call per file classifies each occurrence. Per file:
`<title> · 66_SORRYAUDIT[XX].md` in this layer's OUTBOX (XX = the answering provider: DS, KIMI, ...), plus
`00_REMEDIATION_DOCKET.md` rebuilt after every item, blockers first.

- Script: `66_sorry_axiom_audit.py` (`ONE_MENU.bat 66`; or drop .lean files in this layer's INBOX and `1 RUN HERE`)
- Works on: its own INBOX (00_PRIORITY, 01_SERIES/<series>, 02_GENERAL/<group>), or files/folders named on the command line
- Menu options: limit, workers, provider, model, focus, redo
- Standing focus: `FOCUS.md`

## Rules enforced in code

- The occurrences and their line numbers come from the code scan; a model entry that invents or renumbers one is dropped.
- `classification` outside placeholder | spec_by_design | hard_gap | copied_test | intended_axiom becomes `placeholder`.
- `severity` outside blocker | cosmetic | note becomes `note`.
- An occurrence the model skipped gets a code default (sorry/admit: placeholder/blocker; axiom: intended_axiom/note;
  native_decide: spec_by_design/note) and a logged warning.
- Nothing is compiled here: a classification is a triage note, not a verdict.

## API goals

| id | title | asks for |
|---|---|---|
| `API-66.1` | SORRY_AXIOM_AUDIT | classify each code-found occurrence, what closes it, severity |
