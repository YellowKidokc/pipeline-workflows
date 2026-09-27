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

| Action | API | Gives you |
|---|---|---|
| scripture | free | `scriptures:` and `scripture_books:` in the YAML (every reference, found in code) |
| title | ~1.5k tokens | the standard name, keywords and move; renames the note |
| publish | free | every finished analysis onto the note |

| Workflow | Steps |
|---|---|
| new_note | title → scripture → publish |
| refresh | scripture → publish |
