# Prompt-out: finish the bundle consolidation (for an online AI, not Claude Code on this machine)

Read `API/AGENTS.md` first, then `API/_system/engine/bundle.py` (the engine) and `01_CKG/020_CKG/OUTBOX/030_EVIDENCE` and
`045_ATOMS` (the two bundles built so far). Work on the `work` branch only; follow AGENTS.md section 6.

## What exists (built and tested offline with `--provider mock`; no live API call has been made)

A **bundle** is one front folder that runs 2-3 passes per note, notes in parallel (1-30 at once), on any input folder and
any output folder. It sits in `020_CKG\OUTBOX` as a layer, so the order is: CKG first, then pick layers by number.

| Bundle | Passes (calls per paper) | Replaces |
|---|---|---|
| `030_EVIDENCE` | `turbo` (1) intake companion, `dials` (1) three dials | 030, 036 |
| `045_ATOMS` | `atoms` (1) claim atoms, `axioms` (1) axiom nodes | 045, 054 |

Both buttons exist on each: `1 RUN HERE` (the notes the CKG just ran) and `2 RUN ON FOLDER` (asks for input folder, output
folder, how many at once). No-question form: `python BACKSIDE\30_evidence_intake.py <folder> --out <folder> --workers 8`.
Tests: `python -m unittest _system.tests.test_engine.Bundles`.

## Do next, in this order (each is a small adapter in `engine/bundle.py` `STEPS`, plus its name in the station.json `steps`)

1. **Run one real paper through each bundle** (`--limit 1`, DeepSeek key set) and read the output. Check the three vendored
   scripts really produce what the adapters look for: turbo `*_C1_*.md` under `OUTBOX`, dials `OUTBOX/ANNOTATED_THREE_DIALS/*.annotated.md`,
   atoms/axioms the appended `## Atom Classification (Axiom API)` / `## Axiom Node Mapping (Axiom Nodes API)` section. Fix adapters, not vendored code.
2. **Corpus passes for EVIDENCE** (they read many companions, so they run once per run on the output folder, after the per-paper passes):
   `031` merge originals, `032` best arguments and weaknesses, `035` series arcs, `037` sqlite sync, `038` sidecars; then API ones
   `033` build one argument and `034` series synthesis. Add a `post` list to station.json and a `run_post` in bundle.py. The
   scripts read `ONE_MENU_PATH_EVIDENCE_ROOT/OUTBOX/<shelf>/...`: point that variable at a folder shaped that way, or give the scripts a `--root`.
3. **`039` epistemic intake v2** as an optional third evidence pass (3 calls): it keeps shared state in its own `SCRIPTS/PROCESS`,
   `PROCESSED_ORIGINALS` and moves the source, so it cannot yet run per note in a scratch folder. Make those paths follow a root first.
4. **Lean/atoms side**: `052` Lean atom extractor, `053` axiom one-page transform (needs `{production_root}` folders: give it input/output flags),
   `050`/`051` Lean pairing. Decide whether they join `045_ATOMS` or become a `Lean` bundle (Lean sources are not notes).
5. **Publisher guard**: `tools/publish_analysis.py` refuses to publish when a layer was written to a custom output folder in an
   earlier run and is not in this run's `--look-in` ("kept ... not found again"). With default OUTBOXes it works. Remember each run's output folder (e.g. in the note's YAML) and look there.
6. Two tests fail on `work` before this change: `Portability.test_every_station_follows_the_naming_rule` (a BACKSIDE lacks FOCUS.md) and
   `EndToEnd.test_full_chain` (`report.xlsx` missing). Fix them.

Done = each bundle ran on 3 real papers with the output reviewed, the legacy stations it replaces are marked `superseded_by` in their
station.json (036 and 054 already are), and `_system/CONSOLIDATION.md` lists what was folded.
