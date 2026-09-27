# How this folder works: read this before changing anything

`pipeline-workflows\API` is David's API workbench. Every AI that works here (Codex, Claude, anyone) follows these rules. The working reference is `01_CKG\020_CKG`: copy what it does. Do not invent a new pattern.

## 1. Folder shape

- **A front folder is one station.** It holds:
  - `1 RUN HERE.bat`
  - `2 RUN ON FOLDER.bat`
  - `BACKSIDE\`, containing the script, `station.json`, `PROMPT.md`, `FOCUS.md` and `README.md`
  - `INBOX\`
  - `OUTBOX\`

  Nothing else sits at the top of a front folder.
- **Groups** such as `01_CKG\` and `02_YOUTUBE\` are containers you click into.
- **A layer is a station that sits inside another station's `OUTBOX\`.** For example, `010_CKG_THEOLOGY` sits inside `020_CKG\OUTBOX`. It runs after that station, on the same notes.
- **David moves folders by hand. Never hard-code a folder's position.**
  - Scripts find `_system` by walking up the folders.
  - Launchers use the walk-up block you can see in any `.bat`.
  - `paths.station_dir()` finds a moved station by its `station.json` and repairs `stations.json`.
- **Machine-specific paths** (the vault, the NAS, other repos) go in `_system\config\paths.json`, never in code.

## 2. Buttons

Both launchers call the one script, `_system\engine\button.py`, passing their own folder. Button behaviour is never duplicated in a station.

`2 RUN ON FOLDER` asks, in this order:
1. **Where is the folder?** Anything inside or outside `API\` can be dragged in.
2. **Which notes?**
   - If the folder has an X list (`_PICK.md`), it asks: "N ticked of M, run those?"
   - Otherwise it asks: "M notes, how many?" The answer can be a number, `all`, or `p` (write an X list and stop).
   - A folder with more than 10 notes and no X list never goes to the API by accident.
3. **Where do you want the output?** The default is the station's `OUTBOX`. Answers always go onto each note as well.
4. **How many at once?** From 1 to 30. This is the number of API calls running side by side.
5. **Anything else to look for?** Up to 5 extra questions. Each is answered in a "Your questions" section.
6. **Confirm**, then run. Every step prints a timestamped line, so David can always see work happening.
7. **Put a second layer on these notes?** Pick layers by number, then up to 5 questions for that layer.
8. **Publish:** everything goes onto each note.

`1 RUN HERE` works the same way on the station's `INBOX`. A layer's `1 RUN HERE` uses the notes its parent station just ran (`<parent>\OUTBOX\_last_run.txt`).

**Before any API call, in this order:**
1. **Prepare.** A YouTube channel folder gets `Clean MD\`, `Prompts\` and `Channel Summary\`. Raw transcripts are cleaned with `clean_library.py`, locally.
2. **X list.**
3. **Title**, but only for notes that do not carry their standard title yet. A titled note is recognised and skipped.

**A stray Ctrl+C never kills a run.** David's dictation tool can send one. Long steps run through `ask.run_guarded`; only typing `stop` stops them. Questions ignore Ctrl+C.

## 3. Where results go

- **On the note.** `publish_analysis.py` writes one block between `<!-- analysis:start -->` and `<!-- analysis:end -->`, above the transcript. Inside it, in order:
  1. the deep CKG;
  2. each layer (theology, physics, and so on);
  3. the rest.

  Rerunning replaces the block. No analysis is scattered into side files in the vault.
- **In the OUTBOX, flat.** The base station's results go straight into its `OUTBOX` root as `<note> · CKG.md`: no BY_DOMAIN, BY_TAG or BY_SERIES folders. A layer's results go into that layer's own `OUTBOX`, as `<note> · <NN_LABEL>.md`.
- **Stations read the source only.** Our analysis and scorecard blocks on a note are stripped before any station reads it. Analysis always comes from the transcript or paper, never from an earlier layer's output.

## 4. Standards every analysis follows

- **Title** (`_system\tools\standard_title.py`), in the form `<AuthorCode> <YYYY-MM-DD> · <Title> · <Keyword>, <Keyword> · <Move>`.
  - Keywords are specific, never "Theology" or "Apologetics".
  - The master record is `_system\tools\taxonomy.json`. It is copied to the vault as `00_CLASSIFICATION_MASTER.md`.
  - **Never** start a fresh taxonomy. Move the data file together with the code.
  - **A file-name title gets a real title.** For `bgl-02-who-did-jesus-save`, the same tagging call writes a proper title, stored as `doc_title`.
  - **A series prefix** (`bgl-02`) gives a series code, a part and a series name, stored as `series`, `series_code` and `part`. The first name seen is kept in the taxonomy's `series`. The name looks like `DLowe 2026-04-28 · BGL 02 · <Title> · …`, and the note moves into a `<Series name>\` folder.
  - A colon in a title becomes " – ".
  - **Every rename appends the old name to `previous_names`** (a JSON list), so results made under an earlier name are still found.
- **Publishing never wipes.** If an analysis already on the note is not found again, the note keeps it.
- **Scriptures.** Every CKG lists every passage used: found in code first (`engine\scripture.py`), then completed by the model (cited / mentioned / alluded, where, and what is said). Nothing found in code may be dropped.
- **Output cap.** DeepSeek stops at about 8k output tokens.
  - A reply cut off at the cap is an error, never a result.
  - Long outputs continue automatically (the deep CKG) or are split into their own calls (scriptures).
- **Scores** come from quoted checks computed in code, not from a model's self-grade.

## 5. Small jobs: `_ACTIONS\`

One job per file, in `_ACTIONS\actions\<name>.py`, with `ABOUT`, `API`, `SERIAL` and `run(note, text)` (or `SCOPE = "folder"` with `run_folder`). Actions are strung into `_ACTIONS\workflows\*.txt`.

**Wrap, don't rewrite.** An existing tool (`clean_library.py`, ConversionStation, `file_actions.py`, the converter plugins) is called where it lives, through `paths.json`.

## 6. Git

- **The repo is public.** Nothing under `INBOX\` or `OUTBOX\` is committed, and neither are `_system\STATE`, `_system\config\paths.json`, keys, or `__pycache__`. Station code that sits inside an OUTBOX is kept: `.gitignore` handles that.
- **One line only.** Work lands on the `work` branch; do not create new branches for routine work.
- **Test with real but small runs.** One or two notes is enough, and small API costs are fine. Remove your test files afterwards.
