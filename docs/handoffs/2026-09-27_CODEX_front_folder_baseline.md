# Codex task: bring every API folder up to the CKG baseline

**Repo:** `YellowKidokc/pipeline-workflows`, branch **`work`** (the only line; do not create others). Folder `API/`.

**Read `API/AGENTS.md` first.** It is the protocol. This file is the job, plus every lesson that was paid for while building the reference. The hard part (the design, and the mistakes) is done. Your part is careful, consistent application. Apply every rule below: each exists because breaking it cost real time or data.

## The reference: `API/01_CKG/020_CKG`

It was built and tested end to end with real runs on 2026-09-27. Copy its behaviour; do not invent a variant.

```
API/01_CKG/                    group folder (a container; David clicks into it)
  020_CKG/                     the station
    1 RUN HERE.bat             -> _system/engine/button.py here   "<this folder>"
    2 RUN ON FOLDER.bat        -> _system/engine/button.py folder "<this folder>"
    BACKSIDE/                  station.json, script, PROMPT.md, FOCUS.md, README.md (+ 022 inbox check, _deep work dir)
    INBOX/
    OUTBOX/
      <note> · ANALYSIS.md     newest full analysis of each note (CKG + every layer), rewritten every run
      CKG/<note> · CKG.md      base results
      010_CKG_THEOLOGY/        a LAYER: a whole station inside the OUTBOX (its own 2 buttons, BACKSIDE, INBOX, OUTBOX)
      011_CKG_PHYSICS/
      021_CLAIMS_PROOFS_EVIDENCE/
      _older/<date>/           anything replaced; never deleted
```

## The job

1. **`API/02_YOUTUBE/`**, and then the other numbered folders: give every station the same two buttons. Generate them with `python API/_system/tools/make_buttons.py <front folder> ["what RUN HERE does"] ["what RUN ON FOLDER does"]`. Each .bat is the walk-up block plus one `button.py` call. Remove the old `1 RUN ALL.bat`.
2. **`button.py` has one special case**: station 20 runs the deep CKG engine (`deep_ckg`). Every other engine station is run as `script @<list> --outbox <folder> --workers N [--focus ...]`, and a legacy station runs through `menu.py NN --yes`. If a station needs its own run step (a channel URL for 01, a topic for 48), add a small branch in `run_station`, the way 20 has one. Never write a second button script.
3. **Decide which stations are layers.** A station that only makes sense after another (a physics pass after the CKG) becomes a layer and moves into that station's `OUTBOX/`. Ask David before moving a station he has not placed. List your proposals in the report (see below).
4. **Make every engine station honour the shared flags:** `@list` inputs (via `engine/items.discover` or `engine/pick.resolve`), `--outbox`, `--workers`, and `--focus`. Any "focus findings" the model returns must be SHOWN in the report, using `engine/focus.findings_md`, as the first section.
5. **Keep `stations.json` truthful.** Its `options` list is exactly the flags the script accepts.

## Lessons already paid for: do not repeat these

### Things break when folders move
- **Never hard-code a folder's depth or position.** David moves folders by hand, and did so during the build.
  - Scripts find `_system` by walking up: `next(p for p in Path(__file__).resolve().parents if (p/"_system").is_dir())`.
  - `.bat` files use the walk-up block, copied verbatim.
  - `paths.station_dir()` finds a moved station and rewrites `stations.json`.
  - Use `station_dir()`, never `API_HOME / row["folder"]`.
- **A station placed inside an OUTBOX is code.** `.gitignore` re-includes `OUTBOX/<NNN_*>/`. Its own INBOX/OUTBOX and `__pycache__` stay ignored. After any move, verify with `git check-ignore`.

### Data got wiped or misplaced
- **Move data files with the code.** Station code was copied into MAIN without `taxonomy.json`. The first title run started an empty master record and **overwrote David's vault `00_CLASSIFICATION_MASTER.md`**. It was restored from the old copy. Always check that a tool's data files moved with it.
- **Publish must never wipe.** If an analysis already on a note is not found again, the note keeps it (`publish()` returns "kept …").
- **The analysis block goes after the YAML.** A note with no `# title` line once got the block ABOVE its YAML front matter, which breaks Obsidian. `insert_at()` handles this.
- **Names change; results must still be found.**
  - Every rename appends the old name to `previous_names`, which is a JSON list.
  - Names contain commas ("Historical Jesus, Resurrection Appearances"), so **never split name lists on commas**. Splitting did happen, and publish found nothing and emptied a note.
  - `original_file` keeps the very first name.
- **A title run must not title the standard name itself.** Titles come from YAML `title`, then the `# heading`, then `original_file`, never the current file name. A clean title that has been worked out is stored as `doc_title`.

### The model's output got lost or cut
- **DeepSeek stops at about 8k output tokens.** `llm.py` reports `finish_reason=length` as an ERROR, never as a result. The fix is to continue (the deep CKG does this automatically) or to split the work into its own call. For example, 010's scripture list overran the triage reply, so it now has its own call, API-10.2.
- **Register every new model call** as a goal in its `station.json` (`id`, `title`, `task`, `asks`), and give it a stand-in in `engine/mock.py` for the tests.
- **A request tacked onto the end of a prompt gets ignored.** Put new fields in the prompt's JSON schema itself. 010 ignored "also return scriptures" until the field was in the schema.
- **Answers to David's questions were silently dropped.** The model answered, but the station never put the answer in the report. Always render `focus_findings`.
- **Stations read the SOURCE only.** Strip our `<!-- analysis -->` and `<!-- scorecard -->` blocks before any model sees a note (`Item.text()` does this). Otherwise a layer analyses the previous layer's output instead of the transcript.
- **New questions mean a new run.** The deep engine skips notes it has already done unless there are new questions; keep that behaviour.

### The run itself
- **Finish each item before the next.** As soon as one note's result exists, that note is completed: its OUTBOX file, then its YAML, then the answer on the note, then its ANALYSIS file. Never hold results until the end of a run. A run was once interrupted and the notes did not get their answers, although the engine had finished.
- **A rerun skips finished items** (the file already exists in `OUTBOX/CKG/`).
- **Stray Ctrl+C.** David's dictation tool sends Ctrl+C ("copy") into the focused console, and that once killed a run.
  - Long steps run through `ask.run_guarded` or in their own process group.
  - `ask()` ignores Ctrl+C.
  - Only typing `stop` stops a run.
- **Always show work.** Print a timestamped line per step and per finished item (`[3/100] finished and on the note: …`). Silence means something is wrong.
- **Test input:** in bash, backslashes in a piped path are eaten (`D:\GitHub` became `D:GitHub`). Use forward slashes in test input.

### Inputs and preparation
- **X list first.** The button reads `_PICK.md`. A channel's list sits in the channel folder and covers `Clean MD/`. More than 10 notes with no list means ask "how many?", never "send everything".
- **Prepare only what is really raw.** A `.md` counts as raw only if it has a video id (`video_id:` or `**Video ID:**`) and no `cleaned:` field. Never re-clean a clean note. `Clean MD/`, `Prompts/` and `Channel Summary/` are created only for real channel folders.
- **Don't write loose files into `subtitles/`.** The cleaner treats loose files there as unsorted transcripts. David once chose that folder as the output; the results went to the OUTBOX instead. Warn if a chosen output folder is a transcript root.
- **Wrap existing tools; never rewrite them.** `clean_library.py`, ConversionStation and `file_actions.py` are called where they live, through `paths.json` keys (`yt_downloader`, `conversion_station`, `file_tools`, `vault_root`). There are two copies of `Codex-Powershell_GUI`; the one with `file_actions.py` is `D:\GitHub\Codex-Powershell_GUI`.

### Titles, series and scriptures
- **Title format:** `<AuthorCode> <YYYY-MM-DD> · [<SERIES> <NN> · ]<Title> · <Keyword>, <Keyword> · <Move>`.
  - Keywords are specific, never generic. A keyword on 40% or more of an author's notes goes last.
  - The title wins the space in the name; drop to one keyword before cutting the title.
  - A colon becomes " – ".
- **Series:** a `bgl-02-…` prefix gives `series_code` BGL, `part` 2, and a `series` name (the first name seen is kept in `taxonomy.json` under `series`). The note moves into a `<Series name>/` folder, created at the moment the note is titled.
- **Scriptures are found in code first** (`engine/scripture.py`: written and spoken forms, chapters checked, one-chapter books read by verse), then completed by the model (cited / mentioned / alluded, where, what is said). Nothing found in code may be dropped. Scripture analysis will be central to David's research.

## How to check (small real runs are fine; clean up after)

- `python -m pytest -q API/_system/tests`. Today one test fails: `020_CKG/SYSTEM` (the old engine's cache folder). Report it; do not "fix" it by deleting data.
- `python API/_system/engine/menu.py NN --dry-run --yes` for every station.
- For each station you converted, one real run on one or two short notes, through `2 RUN ON FOLDER`, with piped answers. Check four things:
  1. the OUTBOX layout above;
  2. the note's block, in the order CKG → layers → transcript;
  3. "Your questions" answered;
  4. a rerun skips the done notes.
- Remove your test files. Never commit INBOX, OUTBOX, `_system/STATE`, `paths.json` or keys (the repo is public).

## Report back

Write `API/_system/FRONT_FOLDER_BASELINE.md` with one row per station. The columns are:

- where it sits (and whether it is a layer)
- the 2 buttons
- which flags it honours (@list / --outbox / --workers / --focus)
- focus findings shown
- how it was checked
- open issues
- proposed moves (for David to approve)
