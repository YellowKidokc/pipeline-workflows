@echo off
setlocal
rem Find the apps this pipeline needs on this machine (David-OS, the FIS scanner, Nerve, Python, git ...).
rem Only looks; writes OUTBOX\FOUND_APPS.md and OUTBOX\found_apps.json. Edit BACKSIDE\apps.json to look for more.
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% "%~dp0BACKSIDE\find_apps.py" %*
pause
