# 30_EVIDENCE_INTAKE

Evidence in one station: the intake companion (support, claims, predicates, standing) and the three dials (kind, claimed vs earned strength), 2 calls per paper.

A bundle: one front folder, two passes per paper, papers run in parallel (`How many at once?` at the button, 1-30).
It sits in `020_CKG\OUTBOX` as a layer: run the CKG first, then pick this layer by number; it runs on the same notes.

Passes (each calls an existing, vendored script, unchanged, in a private scratch folder per paper):

- `turbo` (call 1): `vendor/evidence/SCRIPTS/turbo_pipeline_runner.py`, the v0.4.1 evidence companion.
- `dials` (call 2): `vendor/evidence/SCRIPTS/three_dials_annotate.py`, kind of each load-bearing statement, claimed vs earned strength.

Results: `<note> · 30_EVIDENCE.md` flat in the output folder (your choice at the button, default this OUTBOX), JSON in `_json\`,
the answer on the note. A paper that is already in the output folder is skipped. If one pass fails the other is kept and the
failure is written at the top of the file.

Two buttons, one engine: `1 RUN HERE` (the notes the CKG just ran, or this INBOX) and `2 RUN ON FOLDER` (pick input and output folder).
Or no questions: `python BACKSIDE\30_evidence_intake.py <folder> --out <folder> --workers 8`.
