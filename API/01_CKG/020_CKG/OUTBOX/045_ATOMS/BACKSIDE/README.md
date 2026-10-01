# 45_CLAIM_ATOMS

Atoms and axioms in one station: claim atoms and axiom-node mapping, 2 calls per paper.

A bundle: one front folder, two passes per paper, papers run in parallel (`How many at once?` at the button, 1-30).
It sits in `020_CKG\OUTBOX` as a layer: run the CKG first, then pick this layer by number; it runs on the same notes.

Passes (each calls an existing, vendored script, unchanged, in a private scratch folder per paper):

- `atoms` (call 1): `vendor/api_deep/ATOMS/SCRIPTS/run_atoms.py`, claim atoms.
- `axioms` (call 2): `vendor/api_deep/AXIOM_NODES/SCRIPTS/run_axiom_nodes.py`, axiom-node mapping.

Results: `<note> · 45_ATOMS.md` flat in the output folder (your choice at the button, default this OUTBOX), JSON in `_json\`,
the answer on the note. A paper that is already in the output folder is skipped. If one pass fails the other is kept and the
failure is written at the top of the file.

Two buttons, one engine: `1 RUN HERE` (the notes the CKG just ran, or this INBOX) and `2 RUN ON FOLDER` (pick input and output folder).
Or no questions: `python BACKSIDE\45_claim_atoms.py <folder> --out <folder> --workers 8`.
