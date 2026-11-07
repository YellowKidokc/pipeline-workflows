# FOLDER_SNAPSHOT

Point it at any folder → one HTML page showing what's in it: headline numbers, every doc as a circle (sized by length, colored by family), family overlap circles, a shared-vocabulary matrix, recurring terms, file types, subfolders, timeline, possible duplicates, and a searchable wall of every document. With DeepSeek on, each long doc gets a 2-line summary and the folder gets an overview at the top.

## Use
- **Double-click `Snapshot.bat`** → pick a folder in the dialog.
- **Drag a folder onto `Snapshot.bat`** → runs on that folder.
- Output: `_FOLDER_SNAPSHOT.html` inside the scanned folder; it opens automatically.

Command line:
```
python folder_snapshot.py "D:\some\folder" --ai --open
python folder_snapshot.py "D:\big folder" --ai --max-files 20000 --max-ai 200 -o out.html
```

## Needs
- Python 3 (stdlib only).
- `DEEPSEEK_API_KEY` env var for `--ai` (skipped with a note if missing).

## Limits (for huge folders)
5,000 files, first 2 MB of each, 60 AI summaries by default. Skips `.git`, `node_modules`, `.obsidian`, venvs.

## examples/
The two hand-built reference pages this tool grew from (`STATISTICS_MATRIX_PROTOTYPE.html`, `Paper_Information_Matrix.html`) and a sample run on `ONE_MENU_SOURCES`.

## Statistics to Excel
- **`STATS_TO_EXCEL.bat`** gathers every paper's `03_REPORT/statistics.json` (written by station
  `42_STATISTICS_WALL`) into `API\_data\ALL_STATISTICS.xlsx`: a Matrix sheet (paper x metric), a Long
  sheet (with percentiles and change since last run), a Guide sheet (what each metric is, which way is better)
  and a Sources sheet (exactly which files were read).
- **`SNAPSHOT_AND_STATS.bat`** does both: folder snapshot, then the Excel roll-up.
