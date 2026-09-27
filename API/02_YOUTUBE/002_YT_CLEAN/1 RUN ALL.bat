@echo off
setlocal
rem Clean raw transcripts into readable notes (local Python, never an API).
set "SYS=%~dp0..\..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 02 --yes %* & goto :done)
python "%SYS%engine\menu.py" 02 --yes %*
:done
pause
