# CLAUDE CODE PROMPT: FIS stations in the API workbench (v0.1)
**Date:** 2026-10-23 | **Author:** Claude (Fable) with David | **Status:** ready for a builder, read receipt first

## Read receipt (first message back, before any edit)
Restate in your own words: (1) why you must not copy or move any source data, (2) why the stations are
thin wrappers and not copies of FIS logic, (3) what "I can't see engine/understand.py" means you must do.
If any restatement is wrong, stop and ask.

## 0. Stop-check (do this first)
You run in a cloud container and can only see GitHub. David's FIS engine lives in `David-OSv3`
(`engine/understand.py`, `engine/path_write_policy.py`, `engine/flatten_dedupe.py`, the GUIs, tests).
As of 2026-10-23 that code was **uncommitted and on a local-only branch** (`claude/03-classify-renamer`
is not on GitHub; about 40 files modified and about 90 untracked). If you cannot read
`engine/understand.py` on the branch David names, **STOP and tell David the snapshot has not been
pushed.** Do not rewrite it from the spec.

## 1. What FIS is (spec: `David-OSv3/docs/FIS_UNDERSTAND_PIPELINE.md`)
Eight stages, in this order: 1 Inventory, 2 Identify+extract, 3 Exact copies (size, then SHA-256),
4 Classify documents (rules first, LLM only for unresolved), 5 Analyze folders, 6 Relationships,
7 Completeness+authority, 8 Propose actions. Results go to `.data/fis_understand.sqlite`.
Rules that bind you: **R1 nothing is moved, renamed or deleted.** Observations, inferences, judgments and
authorizations are four separate data classes (R3). Predictions run in shadow mode (R7).
Canon comes only from explicit evidence (approval tied to a file hash, canon pins), never from names.

## 2. The data David wants "aggregated" (all on his PC; you cannot see any of it)
Aggregate means **register the roots, inventory them, hash them into the SQLite.** It does NOT mean copy.
"Which copy is best" is decided later, by code, from the inventory.
| Root | What it is (checked 2026-10-23) | Treatment |
|---|---|---|
| `D:\_FIS_STATE` | one file, `keyword_registry.json`, byte-identical to the one in David-OSv3 | skip |
| `D:\_FIS_ROOT_SIDECAR_ARCHIVE` | 12,756 files; every path also exists in `David-OSv3\_FIS_ROOT_SIDECAR_ARCHIVE` (90,534 files) | register; expect exact copies |
| `D:\_FISNOTE_ARCHIVE_20260820_213241` | 12,553 `.fisnote` snapshots + `_manifest.txt` of original `D:\GitHub\...` paths | register; the one distinct dataset |
| `D:\CHI PARTS` | 508 MB of Lean build output (.lean/.olean/.hash/.trace) | register as ONE collection `lean_build_artifacts`; skip stages 2+ |
| `D:\FIS_REPORTS` | only David's argument-match dry-run reports (not FIS data) | skip |
Put these in `config/folder_registry.yaml` with `confirmed: false` (never mark `confirmed: true`; only David does).

## 3. What to build
In `pipeline-workflows/API`, a new group `10_FIS` with three stations, in the shape Kimi used for
`09_DESK_TOOLS` (copy `091_CHAT`: `station.json`, `PROMPT.md`, `FOCUS.md`, `README.md`, `BACKSIDE/`,
`INBOX/` and `OUTBOX/` with `.gitkeep`, `1 RUN HERE.bat`, `2 RUN ON FOLDER.bat`). Read `API/AGENTS.md` first.
- `101_FIS_INVENTORY`: stages 1-2. `uses_api: false`.
- `102_FIS_EXACT_COPIES`: stage 3. `uses_api: false`. Reports copy groups with every location kept.
- `103_FIS_CLASSIFY`: stage 4. Rules first; the LLM only for what rules leave unresolved, through
  **Forge** `POST {FORGE_URL}/v1/chat/completions` (default `http://127.0.0.1:8790`). No provider URLs or
  keys anywhere. Send folder name, file names, extension mix; never file contents by default.
Each station is a **thin wrapper** that calls David-OSv3's engine (import or CLI). **Do not copy engine
logic into pipeline-workflows.** Two copies of FIS is the exact drift problem this whole cleanup is fixing.
Register the group in `API/_system/config/stations.json` and in `API/api-workspace.html` the same way
`09_DESK_TOOLS` was registered (read that diff first).

## 4. Safety
- Default `--dry-run`. Assert read-only on every root; use `engine/path_write_policy.py`.
- Never write inside a scanned root. Output goes to the SQLite and the station OUTBOX only.
- Treat unreadable files as findings (reported with the reason), never as silent skips.
- Tests in `tests/`: identical files with different names found; a revised document stays distinct from an
  exact duplicate; unreadable files reported; authority left unresolved without approval evidence; no source
  file changes (hash before and after).

## 5. Branches and acceptance
- pipeline-workflows: branch from `wip/api-restructure-2026-10-23` (it holds the current stations). Draft PR.
- David-OSv3: only the minimum needed so the stations can call the engine; on the branch David names.
- Never push to main or master anywhere.
- Acceptance happens on David's machine and is PENDING: run 101 and 102 over the five roots in section 2;
  expect `D:\_FIS_ROOT_SIDECAR_ARCHIVE` to come back as almost entirely exact copies of the David-OSv3 archive.
  Say "acceptance pending on target machine" in the PR description.

## 6. Out of scope
Stages 5-8, the GUIs, moving or deleting files, debate-map matching, TikTok material, Rust.
