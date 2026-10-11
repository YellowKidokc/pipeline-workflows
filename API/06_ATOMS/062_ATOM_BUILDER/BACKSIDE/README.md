# 62_ATOM_BUILDER

Claim atoms and axiom companions for each paper, from David's ATOM BUILDER (September 2026).

| Pass | Script (vendored, unchanged) | What it writes | API |
|---|---|---|---|
| atoms | `vendor/atom_builder/scripts/process_atom_pipeline.py` | CLAIM, EVIDENCE, PROOF, PROCESS + the 10-section Atom Meaning Block; a nerve-draft JSON | OpenRouter (default `deepseek/deepseek-v4-flash`) |
| axioms | `vendor/atom_builder/scripts/process_axiom_deepseek.py` | the axiom companion: every axiom, theorem, definition or claim the paper states | DeepSeek |

Each pass runs in a private scratch folder: the source note is never moved or archived.

**Output** (flat, in the folder chosen at the button; default this OUTBOX):
- `<note> · 62_ATOM_BUILDER.md`: the meaning block, then the axiom companion
- `_json\<note> · nerve-draft.json`: open `tools\atom-builder.html` and use **Import JSON**

**Buttons:** `1 RUN HERE` (this INBOX: `00_PRIORITY`, `01_SERIES\<series>`, `02_GENERAL\<group>`) and `2 RUN ON FOLDER` (asks for folder and output).
No questions: `python BACKSIDE\62_atom_builder.py <papers or folder> --outbox <folder> --workers 8`.

**Tools** (`tools\`, open in a browser): `atom-builder.html` (Claim Atom Builder), `workbench.html`, `consilience-atlas.html`, `AtomBALCK.html`.

**Templates** (`templates\`): `CKG_ATOM_MASTER_TEMPLATE.md` (CKG Atom Record V3.2, the full record), `CLAIM_ATOM_EXPANSION_AI_INTAKE_TEMPLATE_v1_1.md`,
`LEAN4_ATOM_MASTER_TEMPLATE.md` + field guide, `axiom-packet.schema.json`. Source: NAS `ONE_MENU_SOURCES\02_CKG\backside_TEMPLATES` (23 Sep 2026).

`045_ATOMS` (the 2-call layer inside `020_CKG\OUTBOX`) stays as it is, for running atoms right after a CKG.
