# _ACTIONS: one small job per file

Every Python job that is not a whole station lives here: detecting scriptures, titling, publishing, and later tag words, classification, coherence, renaming and converting. Each one does one thing well.

A **workflow** strings actions together in order. Many small pieces chained into a workflow produce the end result.

## Run

- `1 RUN AN ACTION.bat` lists everything, asks which action(s) or workflow and which note or folder, then runs.
- `python act.py scripture <folder>` runs a single action.
- `python act.py title scripture <folder>` runs several actions, in that order.
- `python act.py new_note <folder>` runs a workflow.

Folders obey their `_PICK.md`, so only the ticked notes run. That tick list is the same one every station uses.

## Add an action

Create `actions/<name>.py`:

```python
ABOUT = "one line: what it gives you"
API = False            # True if it calls a model (the menu says so before running)
SERIAL = False         # True if notes must go one at a time (shared state)

def run(note, text):   # note: Path, text: its contents
    return {"yaml": {"my_field": [...]},   # small results, stored in the note's YAML (Obsidian can search them)
            "say": "12 found"}             # one line for the screen
    # also possible: {"note": new_path} if the action renamed the note
```

Shared code (a detector, a prompt builder) goes in `_system/engine/`, and the action stays a thin wrapper around it. For example, `actions/scripture.py` calls `engine/scripture.py`, which the CKG stations use too.

## Add a workflow

Create `workflows/<name>.txt` with one action name per line, in order. `#` starts a comment.

## What's here

Actions come in two kinds:
- **Note actions** run on each (ticked) note.
- **Folder actions** (`SCOPE = "folder"`, with `run_folder(folder)`) run once on the folder, before the note actions.

Actions that wrap an existing tool call it where it lives, through `_system/config/paths.json`. Nothing is rewritten.

| Action | Kind | API | Gives you | Calls |
|---|---|---|---|---|
| clean | folder | free | raw YouTube transcripts → `<Channel>/Clean MD` | yt-transcript-downloader `clean_library.py --in-place` |
| convert | folder | free | PDF/DOCX/HTML/XLSX/PPTX → `<folder>/Converted MD` | ConversionStation `theophysics_conversion.convert` |
| html2md | folder | free | every .html → .md beside it | Reusable Tools `convert_html_to_markdown` |
| combine | folder | free | all .md → one `<folder>__combined.md` beside it | Codex-Powershell_GUI `file_actions.py combine-markdown` |
| scripture | note | free | `scriptures:` and `scripture_books:` in the YAML | `_system/engine/scripture.py` |
| title | note | ~1.5k tokens | standard name, keywords and move; renames the note | `_system/tools/standard_title.py` |
| md2html | note | free | the note → .html beside it | Reusable Tools `convert_markdown_to_html` |
| publish | note | free | every finished analysis onto the note | `_system/tools/publish_analysis.py` |

| Workflow | Steps |
|---|---|
| new_channel | clean → title → scripture → publish |
| new_note | title → scripture → publish |
| refresh | scripture → publish |

## Tools not wired yet

- **Moving and copying files** (AUTOFOLDER `router_station/route.py`) is rule-driven: it watches folders listed in `route.yaml`. It is not a one-shot "move this there" command, so it is not an action yet. Its NAS rules point at `//192.168.2.50/h_hp/Desktop/APIs/APIs/CKG/INBOX`.
- **ConversionStation's drop pipeline** (`drop_pipeline.runner`) routes files with DeepSeek, so it would be a paid action.
