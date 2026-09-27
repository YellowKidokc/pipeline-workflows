@echo off
setlocal
rem Lists every action and workflow, asks which ones and which note or folder, then runs them.
rem Drag a folder onto this file to skip the folder question. Folders obey their _PICK.md.
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% "%~dp0act.py" %*
pause
