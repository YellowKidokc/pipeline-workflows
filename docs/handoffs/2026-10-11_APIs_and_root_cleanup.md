# Handoff — 2026-10-11: APIs folder retired, root cleanup

Work lands directly on `main` and is pushed (owner's rule). Commit for this session: `1139b6a`.

## What was done

**`APIs/` (the old portable workbench, dated 2026-09-22) was compared file-by-file against `API/`.**
Most of it was an older copy of scripts already in API with newer versions (2026-09-27) in
`API/_system/vendor/evidence/SCRIPTS/` and `API/Open-AI-CALL-OBS-Plugin-Final-Claude/consolidated/`.
Only these three parts were unique, and they were moved into API:

| From | To |
|---|---|
| `APIs/Reusable_Tools_From_Theophysics/` (253 files) | `API/_system/vendor/reusable_tools/` |
| `APIs/LEAN4/TEMPLATES/` (8 Lean review docs) | `API/05_LEAN/055_LEAN_PAPERS/BACKSIDE/templates/review/` |
| `APIs/stations/Stories/PROMPTS/` (4 prompts) | `API/041_STORIES/BACKSIDE/extra_prompts/` |

The rest of APIs went to `ZZZ Archive/APIs_portable_2026-09-22/`.

**Root folders `contracts`, `drop_pipeline`, `models`, `openintel`, `PIPELINE`** went to
`ZZZ Archive/retired_2026-10-11/` (see its README). `tests/test_drop_pipeline.py` and
`scripts/openintel_install_templates.py` moved with them, because they only work with those folders.
All moves were `git mv` (510 renames). Nothing was deleted.

## Decided: ConversionStation stays in place

**Decision (2026-10-11, owner): keep `ConversionStation/` at the repo root.** Don't move it, make it a station, or archive it.
`paths.json` and `convert` stay as they are. The background below is kept for reference.

### Background

`ConversionStation/` is still in use. The local, untracked `API/_system/config/paths.json` sets
`conversion_station` to `D:\GitHub\pipeline-workflows\ConversionStation`, and `API/_ACTIONS/actions/convert.py`
runs `.venv\Scripts\python.exe -m theophysics_conversion.convert` from there. It also holds the live
`drop_pipeline` (the root copy that was archived was the older one).
It is about 1.7 GB, mostly `.venv`. It also holds 47 MB of git-ignored data in `BACKSIDE/PRESERVED_ORIGINALS`,
plus `Workspace/` and OUTBOX transcripts.

The owner was asked to choose: keep it in place, make it an API station, or archive it.
If it moves: move the whole folder on the filesystem so the ignored data goes too (`git mv` only moves tracked files),
update `paths.json`, and test that `convert` still works. A moved venv may break, and rebuilding it is the fix.

## Things to follow up

The owner deferred all of these on 2026-10-11. Pick them up only when asked.

- `API/_system/vendor/reusable_tools/` is reference material that has never been run (see its `START_HERE.md` and `INVENTORY.csv`).
  Each tool needs its config, imports and paths fixed before use. Destructive or in-place operations should copy first.
  `merger.py` can re-merge its own earlier output and overwrite it, so fix that before using it.
- `API/041_STORIES/BACKSIDE/extra_prompts/` is not wired into `41_story.py`. It sits next to PASS1–3 and is unused.
- `API/05_LEAN/.../templates/review/` is not referenced by any station prompt yet.
- Unrelated uncommitted work was in the tree and was left alone: Master Equation Grading Station edits under
  `API/_system/vendor/api_deep/MASTER_EQUATION/` and `API/_system/config/paths.example.json`. Don't sweep it into an unrelated commit.
- `API/_system/config/path_keys.json` (`apis_root`) and some scripts mention `Desktop\APIs\APIs`. Those are NAS paths, not the
  repo's old `APIs/` folder, so they were left as they are.
