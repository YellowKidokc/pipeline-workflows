@echo off
rem Drag any folder onto this file (or double-click to pick one). Makes _FOLDER_SNAPSHOT.html in that folder and opens it.
python "%~dp0folder_snapshot.py" %1 --ai --open
pause
