# 61_SERIES_SHEET

One run over a whole evidence series: the companions (`AX_GI_01_..._C3_<hash>.md`), the series notebook and the grand-synthesis master paper.
One INBOX, one OUTBOX, one script, no API call.

For every file: `<file> \u00b7 61_SHEET.md` (card, headline numbers, stable ids, outline, extracted tables) and `<file> \u00b7 61_SHEET.json` (everything parsed).
For the series: `<series> \u00b7 SERIES_SHEET.html` (one master page: stats, series documents, one sortable and filterable row per paper, click a row for its outline)
and `<series> \u00b7 SERIES_SHEET.json`. A run over several series also writes `ALL \u00b7 SERIES_SHEET.html`.

The series is the folder a file sits in. Sources are never changed and nothing is written onto the notes. The projected original at the bottom of a companion is counted, not parsed.

Buttons: `1 RUN HERE` (this INBOX) and `2 RUN ON FOLDER` (pick the series folder and the output folder). Or: `python BACKSIDE\\61_series_sheet.py <folder> --outbox <folder>`.
Parsing: `_system/engine/series_sheet.py`. Written without sample files from the NAS: check the first page against a real series.
