# Retired 2026-10-11

Top-level folders moved here from the repo root because nothing in API uses them.

- `contracts/`, `models/`, `openintel/`, `PIPELINE/` — early scaffolding.
- `drop_pipeline/` — older copy; the live one is `ConversionStation/drop_pipeline/`. Its test (`test_drop_pipeline.py`) moved with it.
- `openintel/openintel_install_templates.py` — was `scripts/`; it only installed these templates.

`../APIs_portable_2026-09-22/` is the old portable APIs workbench. Its unique parts moved into API:
`Reusable_Tools_From_Theophysics` -> `API/_system/vendor/reusable_tools/`,
`LEAN4/TEMPLATES` -> `API/05_LEAN/055_LEAN_PAPERS/BACKSIDE/templates/review/`,
`stations/Stories/PROMPTS` -> `API/041_STORIES/BACKSIDE/extra_prompts/`.
Everything else there is an older copy of scripts already in API (newer versions dated 2026-09-27).
