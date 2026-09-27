# CODEX PROMPT: number every API inside pipeline-workflows\API

**Repo:** `YellowKidokc/pipeline-workflows`. **Work on branch `claude/api-front-folders`** (create your own branch off
it if you prefer). Never push to `main` or `V2`. Open a draft PR at the end.

**Touch only the `API\` folder.** Everything else in the repo stays exactly as it is.

Read first, in this order:
1. `API\_system\FRONT_FOLDER_PLAN.md`: the inventory and the numbered list. Where it says MAIN = `API_HOME`,
   read MAIN = `API\` (David's decision, top of that file).
2. `API\_system\README.md`: how the engine works.
3. `API\_system\engine\` (`station.py`, `menu.py`, `inbox.py`, `gateway.py`, `paths.py`, `health.py`, `goals.py`,
   `legacy.py`) and `API\_system\stations\55_LEAN_PAPERS\` (the reference station), `API\LEAN\` (the reference
   front folder).

---

## 1. Where things are now (commit 1cb6a19)

```
API\
  ONE_MENU.bat  SETUP.bat          the engine's two entry points
  _system\                          engine, stations\NN_NAME\ (45 stations), config, vendor, tools, tests
  LEAN\                             front folder of station 55
  QUICK_CALL\                       self-contained DeepSeek copy-me folder
  API\                              OLD container: empty scaffold (only .gitkeep + README + one config)
  API 2\                            NLP engines: DO NOT TOUCH (goes to the NLP stack later)
  API 3\                            OLD container: copies already vendored into _system\vendor
  Open-AI-CALL-OBS-Plugin-Final-Claude\   OLD quick-call; its 23 prompts already run under station 60
```

## 2. Target (what David sees when he opens `API\`)

```
API\
  ONE_MENU.bat
  SETUP.bat
  000_QUICK_CALL\
  001_YT_GRAB\ ... 013_YT_CHANNEL_SUMMARY\
  020_CKG\  021_CLAIMS_PROOFS_EVIDENCE\  022_CKG_INBOX_CHECK\
  030_EVIDENCE\  031_ ... 039_
  040_ANALYTICAL_ARMS\  041_STORIES\  042_ ... 044_  045_ATOMS\  046_ ... 049_
  050_ ... 053_  054_AXIOM_NODES\  055_LEAN_PAPERS\
  060_OPENAI_STATIONS\
  API 2\                 (left alone until David names the NLP stack)
  _system\               hidden: shared engine only
  _data\                 hidden: created at run time, not in git
```

Exact folder names, INBOX yes/no, which OUTBOX each reads, and launcher names: `FRONT_FOLDER_PLAN.md` section B.
Rule: three digits; keep the ONE_MENU number; use David's CODEX-sketch name where it names the same API
(`020_CKG`, `021_CLAIMS_PROOFS_EVIDENCE`, `030_EVIDENCE`, `041_STORIES`, `045_ATOMS`, `054_AXIOM_NODES`).
90 HEALTHCHECK and 91 RELOCATE stay menu-only (no folder). The menu numbers do not change.

Every `NNN_` folder holds exactly: **1-4 numbered .bat launchers, `INBOX\` (only if it takes files), `OUTBOX\`,
`BACKSIDE\`.** Nothing else: no README, config, logs or loose scripts at that level.

```
055_LEAN_PAPERS\
  1 RUN ALL.bat
  2 RUN PRIORITY ONLY.bat
  INBOX\00_PRIORITY\  INBOX\01_SERIES\<series>\  INBOX\02_GROUP\<group>\
  OUTBOX\                     flat: "<title> - <kind>.md", first line stamps lane / group / source
  BACKSIDE\                   station.json, the script(s), PROMPT.md, FOCUS.md, README.md, templates,
                              work\ (JSON, receipts, calls) and logs\ (both git-ignored)
```

`000_QUICK_CALL` is `QUICK_CALL` moved unchanged (no BACKSIDE). `055_LEAN_PAPERS` is `LEAN` + station 55.

## 3. Engine changes FIRST, with tests (one commit)

1. `config\stations.json` gets `"folder": "../NNN_NAME/BACKSIDE"` per station (relative to `_system`).
   `station.py`, `menu.py`, `health.py`, `goals.py`, `legacy.py` resolve the station folder from it instead of
   `_system\stations\<label>`. `paths.inside()` still refuses anything outside `API\`.
2. `engine\inbox.py`: add `--from NNN` (resolves to `../NNN_NAME/OUTBOX`; several allowed). A flat OUTBOX is read
   as group "Ungrouped" unless a paper's first-line stamp names lane / group. Nothing is copied between folders.
3. Per-station work folders and receipts â†’ `BACKSIDE\work\`, logs â†’ `BACKSIDE\logs\` (a `paths.json` key per
   station, relative default). Add `**/BACKSIDE/work/` and `**/BACKSIDE/logs/` to the repo `.gitignore`.
4. Tests: a station found in its BACKSIDE; a run reading another API's OUTBOX via `--from`; a **layout test**
   (every `NNN_` folder holds only launchers, INBOX, OUTBOX, BACKSIDE); every launcher is `%~dp0`-relative.
5. `vendor\` stays in `_system` (shared legacy code). Vendored paths a station uses keep working after the move.

## 4. Move the stations, one family per commit, with `git mv`

Order: `000` + `055` (reference) â†’ YouTube `001-013` â†’ CKG `020-022` â†’ evidence `030-039` â†’ papers `040-049` â†’
Lean `050-054` â†’ `060`.

For each station: `git mv _system\stations\NN_NAME API\NNN_NAME\BACKSIDE` (contents), create `INBOX\` / `OUTBOX\`
with a `.gitkeep`, write the launchers, set `folder` in `stations.json`. After **each** family commit run:

```
python API\_system\engine\health.py
python -m unittest discover -s API\_system\tests
ONE_MENU.bat <NN> --mock --limit 1      (every station in that family)
```

Launchers (the rigor bar, 5-10 lines each): `%~dp0`-relative, check `DEEPSEEK_API_KEY` (only when the station
uses the API), call `python "%~dp0..\_system\engine\menu.py" <NN> --yes` (+ `--station-args "..."` for options),
end with `pause`. Plain names ("1 RUN ALL.bat"). Copy `API\LEAN\*.bat` as the model.

## 5. Retire the old containers (never delete)

After all stations are out, one commit per container, `git mv` into `_system\vendor\_retired\`:
- `API\API` â†’ `_retired\API_API_SCAFFOLD` (its README = the six-station grading-bundle contract; keep it).
- `API\API 3` â†’ `_retired\API_3_SOURCES`. **Before**: hash-check every file under `_system\vendor` against its API 3
  original and list mismatches in `CONSOLIDATION.md`. `API 3\02_CKG\backside_workbench` â†’ `_system\vendor\_duplicates\`.
  `API 3\08_NEW_STATION_SPECS` â†’ `_system\docs\specs\`.
- `API\Open-AI-CALL-OBS-Plugin-Final-Claude` â†’ `_retired\QUICK_CALL_OLD` (code, prompts, `consolidated\`).
  Its `stations_raw\*\` old outputs (~75 MB of .md/.json/.html) also go there; they are already in git history,
  so moving is fine, but do not duplicate them.
- `API 2`: **do not touch.**

## 6. Settled rules (do not reopen)

- **DeepSeek only** (`settings.json` `allowed_providers` = deepseek + mock). Key only from env `DEEPSEEK_API_KEY`.
  Never write a key to any file. Every `config.txt` is git-ignored because one holds a live key; never copy one.
- One item = one whole-document call; never chunk input. Default 30 calls in parallel, one limiter in `gateway.py`.
- One for one: save each item when done; reruns skip finished items; interrupted runs resume.
- The model proposes, code decides. API goal ids `API-NN.n TITLE`; `python API\_system\engine\goals.py` regenerates
  `API_GOALS.md`.
- Never delete, never overwrite an existing file or folder (stop and report instead).

## 7. Stop and ask David (do NOT build these)

- `061_FRUITS`, `062_COHERENCE_SCORE`, `063_GRADING_BUNDLE`, `023_CANONIZATION` (plan section C): not approved yet.
- Where the NLP stack is (for `API 2`).
- Anything in the plan that turns out wrong on disk.

## 8. Done means

- `API\` top level: `ONE_MENU.bat`, `SETUP.bat`, the `NNN_` folders, `API 2\`, `_system\`. Nothing else in git.
- Every `NNN_` folder passes the layout test; tests, health and a `--mock --limit 1` per station are green.
- `ONE_MENU.bat` numbers unchanged and every station still runs from the menu.
- `_system\README.md`, `CONSOLIDATION.md`, `MIGRATION_REPORT.md`, `API_GOALS.md`, `FRONT_FOLDER_PLAN.md` updated
  (the plan lists every old folder and where it went).
- Draft PR against `V2` with a table: old path â†’ new path, per family, and the test / health output.
