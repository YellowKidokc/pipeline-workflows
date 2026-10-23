@echo off
title 23B HTML Assembly
cd /d "%~dp0BACKSIDE"
echo.
echo  23B HTML ASSEMBLY: every atom .json / .yaml in INBOX becomes a standalone HTML page in OUTBOX.
echo  No API calls. Unchanged atoms are skipped.
echo.
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% 23b_assemble.py
echo.
pause