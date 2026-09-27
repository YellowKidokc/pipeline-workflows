# Session summary, 2026-09-27: API chain, deep CKG, argument grades, analysis on the note, standard titles

A complete record of one long working session with David, to be carried into the next conversation. Every path is
real. "API_HOME" means `D:\GitHub\Research-Acquisition\API_ALL\API_HOME`, and "MAIN" means `D:\GitHub\pipeline-workflows\API`.

## 0. Where to start next time

David wants to go through the APIs **one at a time**, starting with titling. He also said: "It's OK to make mistakes;
act, don't wait for permission; small costs are fine." Memory (`~/.claude/projects/...ytdlp/memory/`) carries the
same facts. This file is the long version.

## 1. What was built, in order

### 1.1 Station 48 `48_API_DEEP` (API_HOME\stations\48_API_DEEP)
- **Problem found:** the older stations 40 and 41 sent DeepSeek one-line instructions instead of the real station
  prompts, and without a `max_tokens` setting (DeepSeek's default of about 4k truncates).
- **Fix:** one chain per source: Fruits → Axioms → Atoms → Lean → Stories → Master Equation → Coherence.
  - Prompts are **verbatim copies** of `API_ALL\05_API_DEEP_STATIONS\*\PROMPT.md` and ME V2, kept in `prompts\`.
  - The tested builders `atom_prompt.py`, `axiom_prompt.py` and `fruits_grade.py` are copied into `lib\`.
  - Every call uses JSON mode and max_tokens 8192. The source is numbered locally ([P01]/S001) so every station
    cites the same ids.
  - A reply that is truncated or invalid is retried once, with the problem stated.
  - Master equation Part A runs twice at temperature 0.7, and the two runs are compared (agreed / contested slots).
  - Cache: a rerun reuses every successful call whose prompt hash is unchanged. `run_uuid` is stable, so the cache works.
  - `--copy` writes the prompts to files and puts ALL_IN_ONE.md on the clipboard for pasting into a chat.
- `engine\llm.py` gained `json_mode`, `max_tokens` and `temperature`; `finish_reason=length` is now an error. There is a backup `llm.py.bak`.
- Two new prompts had to be written, because nothing on disk existed for them: `FRUITS_SYSTEM_v0.3.0.md` (the
  grader's config named a file that had never been copied) and `FRUITS_SENTENCES.md`.

### 1.2 Fruits of Love and Truth (inside station 48)
- **Truth Engine v2.0.** The lexicons and weights were extracted from `\\NAS\h_hp\Desktop\Folders\ALL EXCEL\Fruits Template (1) (1).xlsx`
  into `prompts\truth_engine_v2_lexicons.json`. The TRUTH formula and the workbook's 10 characterizations are applied locally (`lib\love_truth.py`).
- **Character profiles** (V0 draft, for David to correct) are in `prompts\CHARACTER_PROFILES.md` + `character_profiles.json`:
  - 4 Love × Truth quadrants: Grace and Truth, Sentimentalist, Clanging Cymbal, Propagandist.
  - 10 shapes: Shepherd, Prophet, Pharisee, Stoic, Zealot, Peacemaker, Peacekeeper, Enthusiast, Servant, Witness.
  - Levels: Mature Fruit, Anti-Fruit, No Signal.
- **David's decision:** the profile is scored **automatically from the per-sentence pass**, as net points per 100
  sentences. The paper verdict (rubric 0-4) is only a second opinion, because it came back 2 for nearly everything.
- **Absent vs negative:** Pharisee, Zealot and Enthusiast only match if their "low" fruits actually score below zero
  (`low_means`). "I AM" changed from Pharisee to Stoic / Prophet.
- **YouTube transcripts** are scored per **speaker turn** (split at `>>`, at most 15 sentences; `prompts\FRUITS_TURNS.md`).
  Per sentence, 7 of 10 Habermas chapters were "No Signal" (1-10% of sentences engaged); per turn, 48-100% engaged.
  Habermas is consistently Grace and Truth, Stoic / Prophet, with faithfulness highest.

### 1.3 Outputs of station 48
- `RUNS\48_API_DEEP\<source>\<stamp>\` contains:
  - `API_DEEP.html`: self-contained, in the circles house style. KPI strip, Love × Truth plot, fruit lollipops,
    sentence heat strip, spikes, verdict, axioms, atoms, Lean, stories, ME slot circles, coherence, searchable sentences, audit.
  - `API_DEEP.md` and `API_DEEP.json`, plus one JSON per station and `love_truth.json`.
  - `fruits_sentences.xlsx`, with sheets Sentences (colour-coded, Truth Engine trigger words), Turns, Profile and Paragraphs.
- `RUNS\48_API_DEEP\INDEX.html` lists every paper and is rebuilt after each run.
- Default input is `API_HOME\INBOX\48_API_DEEP\`. Run it with `ONE_MENU.bat 48`.

### 1.4 YouTube CKG (station 03) repairs
- deepseek-home moved to `yt-transcript-downloader\pipeline-workflows\API\deepseek-home`, and stations 03-06 were re-pointed there.
- `REPO` in index_video.py and watch_pipeline.py is now found by walking up to the folder that holds `obsidian_indexed`.
- `meta()` reads the YAML `channel:` field. Vault folders named "CHANNEL - X - date" were breaking the cleaned-note lookup.
- The halving retry had never worked on ~21-line chunks; its threshold changed from 20 lines to 4.
- It now exits 1 on FAIL / wait / empty and prints a summary line, so the menu stops reporting "done" when items failed.
- All 10 Habermas chapters were indexed, and the catalog was rebuilt (station 05).

### 1.5 The two CKG engines, and the big finding
- **Station 20 `run_ckg.py`** (`MAIN\_system\vendor\ckg`) uses `CKG_ATOM_MASTER_TEMPLATE.md`: free-form S01-S10. It is thin; David called it "surface".
  - Fixed: the map renders as a table, headings are no longer doubled, and the source goes at the end.
  - Fixed: each claim is extracted once (it had been extracted twice, from two copies of the companion).
- **The EVIDENCE engine `turbo_pipeline_runner.py`** (`MAIN\_system\vendor\evidence\SCRIPTS`, station 030) is **the deep CKG
  David means**: MASTER PAPER COMPANION v0.4.1 from `TEMPLATES\02_MASTER_PAPER_RENDERED_FORMAT.md`.
  - **Bug:** it writes everything in one reply, so DeepSeek's 8,192-token output cap cut it off around S03-S06, silently.
  - **508 of 509 companions in the NAS EVIDENCE OUTBOX are cut off.** None reaches S10.
  - **Fix:** a reply that hits the cap continues automatically (up to 4 more parts). The skip rule now requires `## S10`,
    so cut-off companions are redone.
  - Habermas 001-010 were all regenerated complete (S01-S11, 13-38k words each). Each needed 3-5 parts.
  - **The rerun of the 508 NAS companions was NOT done.** It needs David's go-ahead: it runs on the live NAS
    pipeline, costs about $30-50, and needs the originals copied back into the INBOX.
- The NAS launcher `2_RUN_DEEPSEEK_PIPELINE.bat` is broken: its wrapper points to `Desktop\APIs\APIs\_BACKSIDE\EVIDENCE`, which no longer exists.

### 1.6 Station 49 `49_ARGUMENT_GRADE` (API_HOME\stations\49_ARGUMENT_GRADE)
- **Why:** the model's own section scores were boilerplate (S01 always 8). David wants a statistical score of whether
  an argument is good and whether it is original.
- **How it works:**
  - One call extracts the arguments.
  - Two independent gradings (temperature 0.7) follow, in batches of 6 arguments. A single batch of 19 overflowed the 8k cap.
  - **Strength 0-8:** 8 checks (conclusion, premises, support, inference, objection, scope, falsifiable, convergence),
    each 0/1/2. A check with no quote from the source scores 0.
  - **Originality 0-8:** the model first names the closest prior art, then answers 4 checks (not restated, new
    support, new bridge, new structure).
  - Machine ceiling 8. David's human review adds +1 and a Lean receipt adds +1, for 10.
  - Each argument is tagged to David's **case map**, `prompts\CASE_MAP.md`: K01-K18 key arguments and F1-F4 fronts,
    from his conversation "Key arguments for defending Christ's resurrection".
- **Ledger:** `RUNS\49_ARGUMENT_GRADE\ARGUMENT_LEDGER.xlsx`, with sheets Arguments, Develop next (the case needs it
  and strength is below 5) and Case coverage, plus `LEDGER.html` (strength × originality scatter). The human and Lean
  columns survive rebuilds.
- **Known weakness:** case-map tagging is too generous.
- Routine D in API_HOME is now 00 → 48 → 49.

### 1.7 Analysis on the note (David: "all the analysis always goes on the original transcripts")
- `API_HOME\tools\publish_analysis.py <note|folder>` writes one block between `<!-- analysis:start/end -->`, after the scorecard.
  Rerunning replaces the block. The block contains, in order:
  1. a summary callout;
  2. the full deep CKG, S01-S11 (its YAML and its copy of the source cut out; an open code fence is closed);
  3. the argument grades;
  4. Fruits of Love and Truth;
  5. the YouTube argument catalogue.
- The transcript stays last. Only the HTML report sits beside the note, in `_ANALYSIS\`.
- The script falls back to the YAML `original_file`, so renamed notes still find their runs.
- All 10 Habermas notes in `faiththruphysics.com\30_FRAMEWORKS\YOUTUBE\CHANNEL - Gary Habermas - 2026-09-15\` were published.

### 1.8 Standard titles and the master classification record
- `API_HOME\tools\standard_title.py <note|folder> [--apply]`; also menu station **00_TITLE**, first in routine D.
- The format is `<AuthorCode> <YYYY-MM-DD> · <Title> · <Keyword>, <Keyword> · <Move>`.
  - Author code: "GHabermas"; David's papers get "DLowe".
  - Date: the YouTube upload date (yt-dlp, free) replaces the chapter number. Papers use their own date field, then the file date.
  - Keywords: specific, never generic. David: "Theology / Apologetics are banal". The file name gets 2; the YAML gets 3.
  - Move: Evidence, Argument, Objection-reply, Scholarly-survey, Method, Application, Testimony or Debate.
- YAML fields written: `std_title, author_code, upload_date, keywords, move, original_file`. `[[links]]` in the same folder are updated.
- The **master record** lives in `tools\taxonomy.json` and in the vault as `faiththruphysics.com\00_CLASSIFICATION_MASTER.md`
  (rules, every keyword with counts and links, moves, author codes). The tagger reuses known keywords, so the vocabulary settles.
- Cost: about 1,500 tokens per note.
- The 10 Habermas chapters were renamed. Backups are in the session scratchpad.

### 1.9 Docs and handoffs
- `MAIN\..\docs\templates\` (that is, `D:\GitHub\pipeline-workflows\docs\templates\`) holds copies of:
  - CKG (3 templates + COMPANION_LAYOUT.md);
  - YOUTUBE_CKG;
  - API_DEEP;
  - ARGUMENT_GRADE;
  - EVD (rubric v2.0.0 + README);
  - STATISTICS_MATRIX (the circles page + where every copy lives).
  - README.md is the index. Each runner still reads its own copy.
- The Kimi handoff is `docs\handoffs\2026-09-27_KIMI_corpus_report\`, zipped to the Desktop as `KIMI_corpus_report_2026-09-27.zip`.
  It asks Kimi for the unifying CKG parameters (a data contract), a per-source HTML layout, and what to drop, merge or add in the CKG.
- The circles page (Paper Information Matrix) is at `C:\Users\David\Desktop\Paper_Information_Matrix.html`,
  `MAIN\_system\templates\statistics_matrix(_live).html`, and `MAIN\API 3\08_NEW_STATION_SPECS\STATISTICS_MATRIX_PROTOTYPE.html`.
  It was not rewired; the real-data version depends on stations 42 and 46, which were untested today.

## 2. Problems and their fixes (quick reference)

| Problem | Fix |
|---|---|
| Stations sent one-line prompts, and output was truncated at 4k | Verbatim prompts, max_tokens 8192, JSON mode, truncation detected |
| Model scores drift to about 8 | Compute scores in code from quoted yes / partly / no checks (station 49) |
| Deep companions cut off at S03-S06 (508/509 on the NAS) | Continue on `finish_reason=length`; the skip rule requires `## S10` |
| Sentence-level fruits flat on interviews | Score per speaker turn |
| "Pharisee" for mere absence of love | `low_means: negative` for vice shapes |
| Analysis never visible in the vault | publish_analysis.py writes it onto the note |
| Channel from the folder name broke index_video | Read the YAML `channel:` |
| Menu said "done" on failures | index_video exits 1 and prints a summary |
| Each claim extracted twice | Dedupe by paper_uuid |
| 19 arguments overflowed one grading call | Batches of 6 |
| Heredoc Python patches kept breaking on backslashes | Use the Edit tool or a full-file Write for code containing `\` |

## 3. Open items

1. **Rerun the 508 cut-off NAS companions** with the fixed engine (David's go-ahead needed).
2. **Stage the deep CKG properly.** Instead of one mega-reply, make one call per section group, using the station-20
   stages and checkpoints with the deep template. David agreed this is better.
3. **Drop "God Is" from other people's sources.** Show the Axiomatic Contract preamble only on David's own papers,
   never on other people's sources.
4. **Treat not-applicable sections as N/A** rather than scoring them low (for example, S07 math on history talks).
5. **Router after the base CKG:** base CKG → domain pass by `domain_primary`. MAIN already has `010_CKG_THEOLOGY` and
   `011_CKG_PHYSICS`; math needs its own CKG, closer to Lean.
6. **Wire 00_TITLE first** in MAIN's CKG/EVIDENCE launchers. It is only in API_HOME routine D so far.
7. **Front-folder inbox names:** MAIN's front folders use `00_PRIORITY/01_SERIES/02_GROUP`, but the CKG reads `01_PRIORITY/02_SERIES/03_GENERAL`.
8. **Unify file names** of the station-20 CKG outputs (YT_ / APOLO_ / THEO_ prefixes vary).
9. **Tighten station 49's case-map tagging.**
10. **Station 39 (EVD):** compute dimension scores from probe results, and check it for 8k truncation.
11. **Kimi's answer** → build a per-video HTML in each video's folder, then iterate (about 10 versions expected).
12. **Jev Router** (OpenRouter `typesafe/jev-router`; 1M context; audio/video in; routes by difficulty). David feels
    it has an essential place. Candidates: one provider for all calls, whole-channel series passes, audio/video input.
    To test, add a route to `engine\llm.py` and compare it with DeepSeek on a known task.
13. **Commit status:** none of the MAIN edits are committed. `pipeline-workflows` is a PUBLIC repo on the other
    session's branch `claude/api-front-folders`, and David's approval is needed before any push. Changed files:
    - `_system\vendor\ckg\workbench\ckg.py`
    - `_system\vendor\ckg\workbench\extract_cpe.py`
    - `_system\vendor\evidence\SCRIPTS\turbo_pipeline_runner.py`
    - `docs\templates\**`
    - `docs\handoffs\**`

## 4. How David works (keep this)

- **Intuition first; errors get caught afterwards.** "It's OK to make mistakes; it's OK not to claim everything right."
- **Act without asking,** except for destructive, live or public actions.
- **Small API costs are fine,** so verify with real runs.
- **One source = one page.** Titles are uniform and classifications specific; the master record is the vocabulary.
- **He loves the circles house style.** Reuse it for every report.
- **"I try to make it a co-partnership, not a dictatorship."** He is generous with thanks and wants honest pushback.
