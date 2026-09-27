# Templates

This folder gathers the templates and prompt contracts that decide what each pipeline outputs. They are
**copies made on 2026-09-27**. The copy the runner actually reads is listed beside each one; edit that copy, then
copy it here again.

## CKG (regular paper CKG, station 20)

| File | What it is | Runner reads |
|---|---|---|
| `CKG/01_BLANK_TEMPLATE.md` | Empty form: map, S01-S10, audit | `API\_system\vendor\ckg\templates\` |
| `CKG/02_FULLY_EXPLAINED_TEMPLATE.md` | What every section and rule means | same |
| `CKG/CKG_ATOM_MASTER_TEMPLATE.md` | The prompt contract: the JSON each stage must return | same (this is the one sent to the API) |
| `CKG/COMPANION_LAYOUT.md` | How the finished companion prints, and the 2026-09-27 layout fixes | - |

NAS original: `Desktop\Folders\___Pipeline_Done_New\ONE_MENU_SOURCES\02_CKG\backside_CKG\templates\`.

## YouTube CKG (argument indexer, station 03)

| File | What it is | Runner reads |
|---|---|---|
| `YOUTUBE_CKG/CKGARGUMENT_TEMPLATE_V1.md` | Argument-first note template (David's A17 ARGUMENT_FIRST_V1 variant) | `D:\GitHub\nerve\source\html\atoms\Template\` (home.py sends its front half) |
| `YOUTUBE_CKG/STORY_TEMPLATE_V1.md` | Companion template for stories and testimonies | `yt-transcript-downloader\pipeline-workflows\API\deepseek-home\templates\` |

## API Deep: Fruits of Love and Truth (station 48)

| File | What it is | Runner reads |
|---|---|---|
| `API_DEEP/STATION_48_README.md` | The chain: Fruits, Axioms, Atoms, Lean, Stories, Master Equation, Coherence | `API_ALL\API_HOME\stations\48_API_DEEP\` |
| `API_DEEP/CHARACTER_PROFILES.md` | Love × Truth quadrants, the 10 character shapes, and the level types, in plain words | `...\48_API_DEEP\prompts\` |
| `API_DEEP/character_profiles.json` | The same rules as the scorer reads them (thresholds, `low_means`) | same |
| `API_DEEP/FRUITS_SENTENCES.md` | Per-sentence scoring prompt (papers) | same |
| `API_DEEP/FRUITS_TURNS.md` | Per-speaker-turn scoring prompt (YouTube transcripts) | same |
| `API_DEEP/FRUITS_SYSTEM_v0.3.0.md` | Fruits paper verdict, rubric v0.3.0 | same |

Station 48's other prompts are verbatim copies of `API_ALL\05_API_DEEP_STATIONS\*\PROMPT.md`, and are not repeated here.
Those cover atoms, axiom nodes, coherence, Lean 4, stories and master equation V2.

## Argument grade: strength × originality (station 49)

| File | What it is | Runner reads |
|---|---|---|
| `ARGUMENT_GRADE/STATION_49_README.md` | How the 0-8 scores are computed; human +1 and Lean +1 to 10 | `API_ALL\API_HOME\stations\49_ARGUMENT_GRADE\` |
| `ARGUMENT_GRADE/ARGUMENT_GRADE.md` | The checklist prompt: 8 strength checks and 4 originality checks, each needing a quote | `...\49_ARGUMENT_GRADE\prompts\` |
| `ARGUMENT_GRADE/CASE_MAP.md` | David's 18 key arguments (K01-K18) and 4 fronts (F1-F4) | same |

## EVD: Epistemic Intake Rubric v2.0.0 (station 39, the `evd_*` fields)

| File | What it is | Runner reads |
|---|---|---|
| `EVD/EVD_RUBRIC_v2.0.0.json` | 11 epistemic modes, 10 dimensions × 18 probes, 8 global gates | `API\_system\vendor\evidence_chain\SCRIPTS\SYSTEM_FILES\SCHEMAS\EPISTEMIC_INTAKE_V2_RUBRIC.json` |
| `EVD/README.md` | Each dimension in plain words, and how EVD relates to the CKG companion and station 49 | - |

## Paper Information Matrix (the circles page)

| File | What it is | Runner reads |
|---|---|---|
| `STATISTICS_MATRIX/Paper_Information_Matrix.html` | The approved statistics-matrix design (demo data) | `API\_system\templates\statistics_matrix.html` (station 46) |
| `STATISTICS_MATRIX/README.md` | Its encodings, and where every copy lives | - |
