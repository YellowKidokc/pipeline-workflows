@echo off
rem Gathers every paper's statistics (station 42) into one Excel file and opens it.
rem Drag a folder onto this to aggregate only that folder; double-click for the whole pipeline (API\_data).
python "%~dp0stats_to_excel.py" %* --open
pause
