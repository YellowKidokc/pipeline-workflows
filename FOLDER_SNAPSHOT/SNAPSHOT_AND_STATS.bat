@echo off
rem Does both: (1) HTML snapshot of a folder, (2) every paper's statistics gathered into one Excel file.
rem Drag a folder onto this file, or double-click to snapshot via the picker.
rem Stats always come from the pipeline (API\_data) and land in API\_data\ALL_STATISTICS.xlsx.
echo === 1/2  Folder snapshot ===
python "%~dp0folder_snapshot.py" "%~1" --open
echo.
echo === 2/2  All statistics to Excel ===
python "%~dp0stats_to_excel.py" --open
pause
