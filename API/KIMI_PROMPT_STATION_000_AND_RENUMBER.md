# PROMPT FOR KIMI — Renumber the API stations, then build Station 000 properly inside the pipeline
*Prepared by Claude (Opus) for David Lowe, POF 2828 · Oct 17, 2026 · paste this whole file*

Kimi, you are working in `D:\GitHub\pipeline-workflows\API` — David's research pipeline. Read this whole prompt before
touching anything. Work in the order given. Where this says STOP AND SHOW, stop and show David before continuing.

## Ground rules (non-negotiable)
1. **Look before touching.** Inventory first. Earlier tonight a duplicate folder tree was built next to an existing one
   because nobody looked first. Do not repeat that.
2. **Nothing is deleted.** Renames and moves only, each with a receipt line. Backups before editing any file the engine reads.
3. **The engine is the source of truth.** Every station is run by `_system\engine\` (bundle.py, station.py, gateway.py,
   focus.py, menu.py, paths.py). Read how a station is registered (station.json / labels / menu numbers) BEFORE renaming
   anything, because a renamed folder the engine still points at = a broken station.
4. **One config.** All paths come from `_system\config\paths.json`. Never hard-code a path anywhere else.
5. **All model calls go through the relay** (`engine/gateway.py`): one limiter, retries, receipts, GLOBAL_FOCUS, DEEPSEEK_NOTES.
   No station calls a model API directly.
6. **AI proposes, code validates.** Anything a model returns is checked by code before it is saved as fact.
7. **Receipts.** Every run writes what it did and why, whether anyone reads it or not.

## Read these first (they are the spec)
- `HTML_ASSEMBLY_SPEC_v0_1.md` — four layers, node record, identity rules, one shell / four modes
- `STATION_HOME_SPEC_v0_1.md` — breadth vs depth runs, series awareness, call counts, live log
- `SENTENCE_MARKER_SPEC_v0_1.md` — ⟦TYPE id⟧ … ⟦/⟧ markers + the marker-loss guard
- `YOUTUBE_ARGUMENT_CALL_v0_1.md` — argument/moves call (for later; know it exists)
- `000_QUICK_CALL\` — working prototype: `identity.py` (UUID registry), `nabla.py` (address builder + validator),
  `quick_call.py`, `series_run.py`. It works but calls DeepSeek DIRECTLY — Task 2 brings it inside the engine.
- `_system\config\GLOBAL_FOCUS.md` and `engine\focus.py` (global focus is deliberately excluded from the skip hash — keep it that way)
- NABLA spec v6 (address form `D/N/V/A/U/R :: GMESTKRQFC :: HASH`, binary 0/3, tie order E>C>G>K>M>T>R>F>S>Q)

---

## TASK 1 — Renumber the station folders

### 1a. Inventory (no changes)
List every top-level folder in `API\` with: current name, what it contains (sub-stations), whether the engine/menu
references it (search `_system\` and every `station.json`, `.bat`, `.py`, `.md` for the folder name), and its menu number.
Known problems to resolve:
- two folders share `02` (`02_C_P_E_L`, `02_YOUTUBE`)
- `ARUGMENT` is a misspelling and overlaps `07_ARGUMENTS`
- mixed digit widths (`000`, `01`, `041`, `047`, `048`, `049`, `060`)
- `Open-AI-CALL-OBS-Plugin-Final-Claude`, `TOPBAR`, `_ACTIONS`, `_data`, `_system` — classify: station, tool, or system

### 1b. Proposed map — STOP AND SHOW
Propose ONE consistent scheme (suggestion: three digits, gaps of 10 so stations can be inserted later):
`000_QUICK_CALL` · `010_CKG` · `020_CPEL` · `030_YOUTUBE` · `040_ACADEMIA` · `050_STORIES` · `060_ATOMS` ·
`070_ARGUMENTS` · `080_API_DEEP` · `090_NEW_PAPER` · `100_TOPIC_SYNTHESIS` · `110_GAP_MAP` · `120_OPENAI_STATIONS`
(adjust to what the inventory shows). For each row show: old name -> new name, every reference that must be updated.
Do not rename until David approves the table.

### 1c. Apply
Rename, update every reference, write `RENUMBER_RECEIPT_<date>.md` (old -> new, files edited, backups made).
Then run the engine's healthcheck station (`_system\stations\90_HEALTHCHECK`) and the menu, and show that every station
still loads. If any fails, revert that station from the backup and report.

---

## TASK 2 — Station 000 inside the pipeline (the first call every paper gets)

Station 000 runs once per paper (or per version) BEFORE every other station. It writes a **sidecar YAML** — tied to the
paper, never inside it — that becomes the header of every later API call.

### 2a. Register it as a real engine station
Same structure as the other stations (FRONT/BACKSIDE/FOCUS.md/station.json as they use it). Its model call goes through
`gateway.py` like every station. Reuse `identity.py` and `nabla.py` as libraries; do not rewrite their logic.

### 2b. What the sidecar must contain
```
identity:      paper_uuid (permanent, minted once by the registry)
               version_uuid = uuid5(8121b19c-b135-4b14-ae07-806757692169, "paper-version:" + sha256)
               version_n, source_sha256, source_file, original_copy (ORIGINALS path)
branch:        series name + code (e.g. MIM), position, of, sibling list (code, uuid, title)
master_equation_id
nabla:         address, filing D/N/V/A/U/R, vector (binary 0/3 ONLY), hash, confidence per variable,
               review_flags, minimal_decode, truth_modes, operators
               STABILITY: run the classification 3 times; majority vote per variable; any variable that flipped is
               listed in review_flags. (Measured tonight: single runs drifted up to 3 of 10 variables.)
classification (the four layers, for the paper as a whole): dominant speech acts, truth registers present,
               owner mix (FRAMEWORK / PERSONAL)
knowledge_graph: node_type candidates, 7Q dimension, edge types expected (filled fully by CKG; 000 seeds them)
arguments:     which debate questions (Q-IDs from _ARGUMENTS\DEBATE_MAP.md) this paper serves, side, confidence —
               max 5; anything weaker goes to a review list, not into a folder
lifecycle:     stations_done, stations_skipped, current_stage
ladder:        uuid -> nabla+title -> lossless summary (pending) -> paper
```
Validation by code (not by the model): enums, binary vector, Q-IDs exist in DEBATE_MAP.md, UUID formats, required fields.
INVALID results are saved and shown as INVALID, never silently fixed.

### 2c. Folders per paper — create all at once, prune at the end
Series-first layout:
```
API_PIPELINE\SERIES\<CODE>_<Name>\_SERIES\            series header, siblings, series aggregator output, series HTML
API_PIPELINE\SERIES\<CODE>_<Name>\<CODE-NN>_<paper>\
    000_QUICK_CALL\  010_CKG\JSON\  010_CKG\HTML_ASSEMBLY\  020_CPEL\JSON\  020_CPEL\HTML_ASSEMBLY\  ...
API_PIPELINE\STANDALONE\<paper>\                       same inside layout for papers with no series
```
HTML_ASSEMBLY under: CKG, CPEL, ACADEMIA, ATOMS, ARGUMENTS, API_DEEP, STORIES, NEW_PAPER.
At the end of a run, any station folder that received nothing is removed (empty folders only), and the removal is logged.

### 2d. The combined JSON
After the stations, one script merges every station's JSON for the paper into a single continuous file
(`<CODE-NN>_ALL.json`), in station order, each block tagged with station, version_uuid and timestamp. Also a series-level
`<CODE>_ALL.json` that concatenates the papers in order.

### 2e. Test on Math Is Moral — STOP AND SHOW before the full run
Source: `\\192.168.2.50\h_hp\Desktop\Folders\THEOPHYSICS_ORGANIZED (1)\O-09_Math_Is_Moral` (21 files; one exact
duplicate: preview-1526a4 == preview-c69183). The UUID registry already holds these papers from tonight's prototype run —
reuse their paper_uuids; do NOT mint new ones. Run 2 papers first, show the sidecars and folders, then run the rest.

---

## Deliverables
1. `RENUMBER_RECEIPT_<date>.md`
2. Station 000 registered in the engine, calling through the relay, passing healthcheck
3. Sidecars + folder trees for the MIM series, combined JSON files
4. A short report: what you changed, what you could not do, every assumption you made, and anything that looked wrong
   (say it plainly — David prefers a flagged problem to a hidden one)
