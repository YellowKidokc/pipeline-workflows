# Codex task: give every API front folder the same clean baseline

Repo: `pipeline-workflows`, folder `API/`. It holds numbered front folders (`001_YT_GRAB` … `060_OPENAI_STATIONS`) and the hidden engine `API/_system/`.
One folder is already done by hand and is the **reference**: `API/057_API_DEEP/`. Make every other front folder look and behave like it.
Do the grunt work. Where a folder does not fit, leave it working and write down why. "Mostly right" is fine: David and Claude will fix the rest.

## 1. The baseline: what a front folder is

```
API/0NN_NAME/
  1 RUN HERE.bat        runs the station in place on its own INBOX (a routine uses this); no questions asked
  2 RUN ON FOLDER.bat   asks where the notes are, which ones, and where the answers go (engine/ask.py)
  BACKSIDE/             everything else: the script, PROMPT.md, FOCUS.md, README.md, station.json, lib/, prompts/, vendor bits
  INBOX/                00_PRIORITY/ 01_SERIES/ 02_GROUP/
  OUTBOX/               results (git-ignored)
```

Front folders can sit in a **group folder**: `API/01_CKG/` holds 010, 011 and 020-022, and `API/02_YOUTUBE/` holds 001-009, 012 and 013. A group holds only front folders.
- In a grouped folder the launchers use `%~dp0..\..\_system\`.
- Scripts find `_system` by walking up: `next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir())`. Use that form everywhere.
- Do not create new groups; David decides those.

Known exception, left for Claude: `01_CKG/020_CKG/SYSTEM/` (the CKG engine's cache records).

Nothing else sits at the top of a front folder. Anything else there now (`SYSTEM/`, extra .bat files, READMEs, `input/`, `output/`) moves into `BACKSIDE/`. Fix every path that pointed at it.

Copy the two launchers from `057_API_DEEP` and change only the station number and the script name:

- `1 RUN HERE.bat` calls `BACKSIDE\<NN>_<name>.py "%~dp0INBOX" --publish`. If a station has no `--publish` (see section 3), it calls `_system\engine\menu.py NN --yes`, which is the old "1 RUN ALL.bat" behaviour.
- `2 RUN ON FOLDER.bat` calls `_system\engine\ask.py NN`.
- The old `1 RUN ALL.bat`, `1 RUN A TOPIC.bat` and similar files are replaced.
- If a station really needs a question of its own (01 asks for a channel URL, 48 for a topic), keep that question inside `1 RUN HERE.bat`, and say so in its README.
- Write the .bat files with CRLF line endings.

## 2. What the shared engine already gives you (do not rewrite it; call it)

- **`_system/engine/pick.py`**: the pick list.
  - `<folder>/_PICK.md` holds `- [ ] [[note]]` lines, and only ticked notes run. A line reading `ALL` runs the whole folder.
  - A folder with more than 10 notes and no list gets a list written, and nothing is run.
  - A channel folder (it has `Clean MD/`, `Channel Summary/`, `Prompts/`) keeps its `_PICK.md` in the channel folder, and that list covers `Clean MD/`.
  - An item written `@file.txt` is a list of note paths, one per line.
  - The entry point is `pick.resolve(items, default=None, limit=None) -> list[Path]`.
- **`_system/engine/ask.py NN`**: the interactive flow.
  - It asks for the source, then which notes: "122 ticked of 390, run those?" or "390 notes, how many?".
  - It asks where the answers go. The default is onto each note.
  - It asks for confirmation, then runs the station with `@<list file>`, plus `--publish` or `--out`.
  - Afterwards it asks up to 5 "anything else to look for" questions (passed as `--focus`), and offers follow-up passes from `_system/config/followups.json`.
- **`_system/engine/publish.py`** `publish_on_note(notes)` writes all analysis onto the source note (`_system/tools/publish_analysis.py`).
- **`_system/engine/items.py` `discover()`**, used by every `engine.station.Station`, already expands `@list` items and folders that have a `_PICK.md` or `Clean MD/`. Stations built on `Station` therefore obey the pick list with no change.
- `_system/engine/llm.py` now reports a reply cut off at the output cap (`finish_reason=length`) as an error `truncated: …`, never as a finished reply.

## 3. Per station: make the script take the same inputs

For every station script in `BACKSIDE/`:

1. **Inputs.** Positional items can be note files, folders or `@list.txt`.
   - If the script resolves its own inputs (it does not use `engine.station.Station`), route every non-special item through `pick.resolve([raw])`. See `resolve_items()` in `057_API_DEEP/BACKSIDE/57_api_deep.py`.
   - Keep the special item kinds each script already handles, such as paper folders with `paper.json`.
   - With no items, the default is its own `INBOX` (`Path(__file__).resolve().parent.parent / "INBOX"`).
2. **`--publish`**, but only where the station's output belongs on the note. Afterwards it calls `publish_on_note([...sources that succeeded...])`.
3. **`--out <folder>`**, if the script can write elsewhere.
4. **`stations.json`**: update `_system/config/stations.json` and `BACKSIDE/station.json`.
   - Set `options` to the flags the script really accepts, including `publish`, `out` and `focus`.
   - `ask.py` only passes a flag that is listed there.
5. **Local stations and utilities** (no API: 22, 37, 43, 46, 90, 91 and `000_QUICK_CALL`) still get the folder shape. For `2 RUN ON FOLDER.bat`, use `ask.py` if the station takes items; otherwise leave it out, and note that in the README.
6. **Do not change** prompts, rubrics, scoring logic or model settings.

## 4. How to check (no paid API calls)

- `python -m py_compile` on every changed .py file.
- `python API/_system/engine/menu.py NN --dry-run --yes` for every station that supports `--dry-run`.
- `python -m engine.pick <some folder>` (run from `API/_system`) writes a `_PICK.md`. Delete that test file afterwards.
- `python API/_system/engine/ask.py NN`, with stdin piped: a source folder, then `p` should write a pick list and stop without calling any API.
- For any station you cannot check, leave a line in `API/_system/FRONT_FOLDER_BASELINE.md` (the station, what is untested, and why).

## 5. Git

- Work on a new branch off `claude/api-front-folders`, and commit per family: youtube 001-013, ckg 020-022, evidence 030-039, papers 040-049, lean 050-055, bundles 060.
- The working tree may show deleted files at the repo root (`preferences/`, `prompts/`, `schemas/`, `scripts/`). Those are not yours: do not commit or restore them.
- Never commit anything under `INBOX/` or `OUTBOX/`, `_system/STATE`, or `_system/config/paths.json`.

## 6. Report back

Write `API/_system/FRONT_FOLDER_BASELINE.md` with one table row per front folder. The columns are:

- shape done
- the 2 launchers
- pick-aware
- `--publish`
- options registered
- checked how
- open issues

## Not in scope (David and Claude will do these)

- The top-line router: `API\START.bat` and a `routes.json` that detects YouTube / paper / Lean and hands the source to the right chain.
- New follow-up passes. `followups.json` is only edited if a station number changes.
