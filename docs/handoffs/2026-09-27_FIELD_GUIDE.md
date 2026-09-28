# Field Guide: what we built, how it works, what's left

*2026-09-27. David and Claude. Written for David, and for any AI that picks this up (Codex, Claude, Kimi).*

---

## 1. What got done today

| Where | What | State |
|---|---|---|
| `pipeline-workflows\API\01_CKG` | The CKG front folder became **the template** for every station: two buttons, the X list, output folder, how many at once, up to 5 questions, and each note finished the moment it's done | pushed, `work` |
| `API\AGENTS.md` | The **protocol**. Codex and Claude read it automatically. | pushed |
| Four bug fixes (Claude) | An API key could have been committed to the public repo. The Title station's "dry run" really renamed files. Stations 57/58 re-sent their own old analysis to the model. The title call read the analysis block instead of the paper. | pushed `fad3bda` |
| Codex PR #26 | Every station got the two buttons; 57/58 keep every focus point; 000 Quick Call became a normal station; 48/49 ask for a topic; stations can be moved; old stations say plainly that they don't read the INBOX. Tests pass 24/24. | merged `8c66a06` |
| YouTube review | 11 stations examined, and a plan decided (section 7) | plan saved; not built |
| `Documents\faiththruphysics.com` | Reorganised into a campus: 1,535 moves, nothing deleted (section 8) | 3 folders pending |
| `yt-transcript-downloader\ytgrab.py` | "Stuck on the main page" fixed. It was re-reading 10,600 files silently for 7 minutes; now it takes 3 seconds (cache). | local commit `de6262f` |

---

## 2. What still needs doing

**Your side**
1. **Finish the campus move.** Close the Habermas index in Notepad++. If `du.exe` is still running, end it in Task Manager. Then double-click `faiththruphysics.com\00_CAMPUS_REORG_FINISH.bat`. That moves `01_WORKING`, `30_FRAMEWORKS` and its `YOUTUBE` folder.
2. **Pick the live workbench vault.** `10_VAULTS\11_WORKBENCH` holds 01_Working, v3, v5 and Case_for_Christ; the others go to the archive.
3. **Run `retry_failed.bat`** in the downloader. **1,230 videos** are placeholders from earlier failures.
4. **Decide about your local repo.** `D:\GitHub\pipeline-workflows` is still on the old branch (`claude/api-front-folders`), with 110 unsaved changes, mostly deletions in `preferences`, `prompts`, `stations`, `templates` and `tests`. Git refused to switch it to `work` because untracked `AUTOFOLDER` files would be overwritten. Either back them up to a branch and then switch, or confirm they're clutter.

**Pipeline work still open** (listed at the end of `docs\handoffs\2026-09-27_CODEX_front_folder_baseline.md`)
- **The prompts are hidden.** 24 `PROMPT.md` files are only pointers; the real prompts live in `_system\vendor\…`. Copy them into each BACKSIDE so you can read and edit them there.
- **The 8k output cap.** 041 (a row per paragraph), 045 and 054 (a whole paper in one call), 055 (a markdown paper inside JSON) and 060 (GREAT_GRADER and the HTML page) can hit DeepSeek's ~8k output limit. Split those calls, or continue them.
- **57's tacked-on requests.** 57 still adds requests (lean4, coherence, `unmapped_claims`) to the end of the prompt. They must go into the prompt's JSON schema, or the model ignores them.
- **Two decisions.**
  - Where 022 lives: it's nested inside a BACKSIDE, and should move into 020's OUTBOX as a layer.
  - Whether 052 counts as an API station.

**Next builds (saved ideas)**
- **The YouTube group** (section 7).
- **The harvester:** reads every CKG analysis and pulls:
  - the YAML finding, the weakest claim and what to build next;
  - the falsifiers and "Unanswered";
  - the Scriptures and "Your questions".

  That gives you a list of what to chase next. It's local and free.
- **Vectorization:** local embeddings after cleaning, before the X list.
- **The `API_ALL` survey.**
- **Lean:** already running elsewhere (David). Don't start a second one.

---

## 3. How a station works (the API folder)

### Shape
```
API\01_CKG\                  a GROUP: a container you click into
  020_CKG\                   a STATION (front folder)
    1 RUN HERE.bat           runs on this station's INBOX
    2 RUN ON FOLDER.bat      runs on any folder you drag in
    BACKSIDE\                script, station.json, PROMPT.md, FOCUS.md, README.md
    INBOX\
    OUTBOX\
      <note> · ANALYSIS.md   newest full analysis of each note (CKG + every layer)
      CKG\<note> · CKG.md    base results
      010_CKG_THEOLOGY\      a LAYER: a whole station inside the OUTBOX
      _older\<date>\         anything replaced; never deleted
```
- **Nothing else sits at the top of a front folder.**
- **A layer** is a station that only makes sense after another one, like a theology pass after the CKG. It lives in that station's OUTBOX and runs on the same notes. Its `1 RUN HERE` uses the notes its parent just ran (`_last_run.txt`).

### The two buttons (one script: `_system\engine\button.py`)
`2 RUN ON FOLDER` asks, in this order:
1. Where is the folder?
2. **Which notes?**
   - With an X list (`_PICK.md`): "N ticked of M, run those?"
   - Without one: "M notes, how many?" You can answer a number, `all`, or `p` (write an X list and stop).
   - **A folder of more than 10 notes never goes to the API by accident.**
3. Where do you want the output? The default is the OUTBOX. Answers always go onto the note as well.
4. How many at once? 1 to 30 API calls side by side.
5. Anything else to look for? Up to 5 questions, answered under "Your questions".
6. Confirm, then run, with a timestamped line for every step.
7. Put a layer on these notes? Pick by number, plus up to 5 questions.
8. Publish onto each note.

**Before any API call:** prepare (clean raw transcripts locally), then the X list, then the title (only for untitled notes).

### INBOX lanes: priority, series, group
```
INBOX\
  00_PRIORITY\                 runs first
  01_SERIES\<Series name>\     the folder name IS the series
  02_GROUP\<Group name>\       like a series but not one (e.g. "One pagers")
  (loose files -> group "Ungrouped"; 02_GENERAL is read as the same lane)
```
- **Order:** priority, then series, then group. Inside a lane, by group name, then file name.
- **The group travels with every item into the outputs** (`<outbox>\<lane>\<group>\<item>\`), so a series stays together.

### Where results go
- **On the note:** one block between `<!-- analysis:start -->` and `<!-- analysis:end -->`.
  - Its order is: the CKG, then each layer, then the rest. The transcript stays below it.
  - A rerun replaces the block. **Publishing never wipes:** if an old analysis isn't found again, the note keeps it.
- **In the OUTBOX:** newest on top, one `ANALYSIS.md` per note. Old versions go to `_older\<date>\`.
- **All analysis goes on the original note,** never scattered into side files in the vault.

### Finish each note before the next
As soon as one note's result exists, the station writes, in this order:
1. its OUTBOX file;
2. its YAML;
3. the answer on the note;
4. its ANALYSIS file.

Nothing waits for the end of the run. An interrupted run loses nothing that was finished, and a rerun skips notes that are already done.

---

## 4. Titles, series, names, scriptures

- **Title format:** `<AuthorCode> <YYYY-MM-DD> · [<SERIES> <NN> · ]<Title> · <Keyword>, <Keyword> · <Move>`, for example `DLowe 2026-04-28 · BGL 02 · Who Did Jesus Save · Atonement, Election · Argument`.
  - Keywords are specific, never "Theology". A keyword on 40% or more of an author's notes goes last.
  - The title wins the space; drop to one keyword before cutting the title. A colon becomes " – ".
- **Master record:** `_system\tools\taxonomy.json`, copied to the vault as `00_CLASSIFICATION_MASTER.md`. **Never start a fresh one.** (It happened once: the code was copied without its data file, and the vault master got overwritten. It was restored.)
- **Series:** a file name like `bgl-02-who-did-jesus-save` gives `series_code` BGL, `part` 2 and a `series` name. The note moves into a `<Series name>\` folder, created the moment it's titled.
- **Names change, but results must still be found.**
  - Every rename appends the old name to `previous_names`, a JSON list. `original_file` keeps the very first name.
  - **Never split name lists on commas.** Titles contain commas ("Historical Jesus, Resurrection Appearances"). Splitting them once emptied a note.
- **Titles come from the YAML `title`, then the `# heading`, then `original_file`,** never from the current file name. Otherwise a rerun would title the title.
- **Scriptures:** every CKG lists every passage.
  - Code finds them first (`engine\scripture.py`), in written and spoken forms, checking chapters.
  - The model completes the list (cited, mentioned or alluded; where; what is said). Nothing code found may be dropped.

---

## 5. The hard lessons (read before changing anything)

**Folders move, so nothing may assume its position**
- **You move folders by hand**, and did so mid-build. So:
  - Scripts find `_system` by **walking up** the folders, never with a fixed `parents[2]`.
  - `.bat` files use the **walk-up block** below, copied verbatim.
  - `paths.station_dir()` finds a moved station by its `station.json`.
  ```bat
  set "SYS=%~dp0"
  :findsys
  if exist "%SYS%_system\engine\menu.py" goto :sysok
  for %%I in ("%SYS%..") do set "UP=%%~fI"
  if not "%UP:~-1%"=="\" set "UP=%UP%\"
  if /i "%UP%"=="%SYS%" echo Cannot find the _system folder & pause & exit /b 1
  set "SYS=%UP%"
  goto :findsys
  :sysok
  ```
- **Machine paths** (vault, NAS, other repos) go in `_system\config\paths.json`, never in code.
- **A station inside an OUTBOX is code.** `.gitignore` re-includes `OUTBOX\<NNN_*>\` but keeps each layer's own INBOX and OUTBOX out. Check with `git check-ignore` after any move.

**Two of things: which one is real**
- **Two CKG engines.** The deep companion (the 030 turbo runner, and the "deep CKG" used by station 20) is not the same as station 20's older CKG. Station 20's button runs `deep_ckg`.
- **Two copies of `Codex-Powershell_GUI`.** The one with `file_actions.py` is `D:\GitHub\Codex-Powershell_GUI`.
- **Two repos named like the downloader.** `youtube-transcript-ytdlp` (this session's folder) and `yt-transcript-downloader` (where `RUN_WITH_WEBSHARE.bat` and `ytgrab.py` live).
- **Two branches on GitHub.** `main` is the OLD layout (`API\API\…`); **`work`** is the real one. **Codex always calls its checkout "work", whatever it started from.** Pick branch `work` in Codex's dropdown, or it sees the old tree and says AGENTS.md is missing.
- **Two watchers for YouTube.** 006 WATCH and `012 --watch` do the same job; keep one.

**The model's output got lost or cut**
- **DeepSeek stops at about 8k output tokens.** A reply cut off with `finish_reason=length` is an **error**, never a result. Continue it, or split it into its own call. (Scriptures got their own call, API-10.2.)
- **A request tacked onto the end of a prompt gets ignored.** Put it in the JSON schema.
- **Answers to your questions were once silently dropped.** Always show `focus_findings`.
- **Stations read the source only.** Strip the `<!-- analysis -->` and `<!-- scorecard -->` blocks, and the YAML, before the model sees a note. Otherwise a layer analyses the last layer's output.
- The analysis block goes **after** the YAML. Above it, it broke Obsidian once.

**Windows and console traps**
- **A stray Ctrl+C.** Your dictation tool sends Ctrl+C ("copy") into whatever window has focus, and that once killed a run. Long steps now run guarded, and **only typing `stop` stops a run.**
- **Always show work.** A silent window looks frozen. The downloader "stuck on the main page" was really a 7-minute silent file scan.
- **Paths in bash lose their backslashes** (`D:\GitHub` becomes `D:GitHub`). Use forward slashes in test input.
- **Long paths.** Some files in `040_ANALYTICAL_ARMS\…\FRUITS` exceed Windows' 260-character limit. Clone and use worktrees with `core.longpaths=true` and short folder names.
- **Console encoding.** File names containing ↔ and other symbols crash Python's print on Windows. Scripts set `stdout` to UTF-8.
- **Don't write loose files into `subtitles\`.** The cleaner treats them as transcripts. (That's why the downloader's new cache sits next to the script.)
- **Only really raw notes get prepared.** A `.md` counts as raw only if it has a video id and no `cleaned:` field. Never re-clean a clean note.

**Git**
- **The repo is public.** Never commit INBOX, OUTBOX, `_system\STATE`, `paths.json`, keys or `.env`.
- **One line only:** work lands on `work`.
- **Wrap existing tools; never rewrite them.** `clean_library.py`, ConversionStation and `file_actions.py` are called where they live, via `paths.json`.

---

## 6. Where things live

| Thing | Path |
|---|---|
| The API workbench | `D:\GitHub\pipeline-workflows\API` (GitHub `YellowKidokc/pipeline-workflows`, branch `work`) |
| Protocol | `API\AGENTS.md` |
| Codex handoff + open list | `docs\handoffs\2026-09-27_CODEX_front_folder_baseline.md` |
| Button generator | `API\_system\tools\make_buttons.py <front folder> ["RUN HERE text"] ["RUN ON FOLDER text"]` |
| Titles + taxonomy | `API\_system\tools\standard_title.py`, `taxonomy.json` |
| Lean library | `API\_system\vendor\lean_atom\` (scanner, SQLite registry, `#print axioms` audit) |
| Transcript downloader | `D:\GitHub\Research-Acquisition\yt-transcript-downloader` (`RUN_WITH_WEBSHARE.bat`, `ytgrab.py`, `subtitles\`) |
| Vault campus | `C:\Users\David\Documents\faiththruphysics.com` (the map is `00_CAMPUS_MAP.md`) |
| Webshare login | the Windows user variables `WEBSHARE_USER` / `WEBSHARE_PASS` (set with `SET_WEBSHARE_CREDENTIALS.bat`) |

---

## 7. The YouTube plan (decided, not built)

Of the 11 stations, **6 were already pure Python**. Most of the 5 that call the API repeated each other or the CKG.
- **One local PREPARE flow:**
  1. grab (001);
  2. convert (007);
  3. clean (002);
  4. tidy (012);
  5. standard title (056; the only API call, about 1.5k tokens);
  6. catalog (005).

  Keep one watcher.
- **A YouTube CKG:** the summary stations (003 INDEX, 004 LENSES, 008 SUMMARY, 013 CHANNEL SUMMARY) are "pretty much CKG". They become a **copy of the CKG front folder named YouTube**, in the same format.
- **Deep (009)** gets its own layer or API call.
- **New layers:** conspiracy theory, end of the world, and one or two more to be named.
- It runs over the **whole downloaded corpus**.

---

## 8. The vault campus (`faiththruphysics.com`)

**The rule:** folders say what STAGE a thing is at; YAML says what it's ABOUT (`stage`, `type`, `domain`, `keywords`, `move`).

```
00_SYSTEM\     code, apps, data, operations          (not vaults)
10_VAULTS\     where you WRITE, one folder = one vault, no vault inside another
               11_WORKBENCH 12_CANONIZATION 13_FAITH_THROUGH_PHYSICS 14_MASTER_EQUATION
               15_FRAMEWORKS 16_BLUE_VAULT 17_PRODUCTION 18_SOCIAL_MEDIA
20_SUPPORT\    what you READ from, don't write in: 21_RESEARCH 22_YOUTUBE 23_BIBLE 24_SOURCES_INBOX
40_MEDIA\      by TYPE: 00_INBOX 01_IMAGES 02_AUDIO 03_VIDEO 04_SLIDES 05_DIAGRAMS
               06_THUMBNAILS 07_TRANSCRIPTS 08_DOCUMENTS 10_BY_STORY 80_REGISTRY
90_ARCHIVE\    OLD_VAULTS 999Z_VAULT_DEDUP EMPTY_SHELLS   (frozen)
```

- **Media:** one library. Topic goes in the file name (`axiom_A03_grace-field_01.png`), not in a second folder. Each vault can get a `_media` junction pointing at `40_MEDIA`. Full videos stay in the library; vaults get thumbnails and clip notes.
- **Kept in place:** `00_CLASSIFICATION_MASTER.md` (the pipeline writes it there), `10_AI_WORKSPACE` (a junction to `A:\`), and `SynologyDrive`.
- **Undo:** `00_CAMPUS_REORG_UNDO_20260927-183424.py` moves everything back from the receipt CSV.
- **Synology:** it syncs this folder, and it synced the moves as renames.
