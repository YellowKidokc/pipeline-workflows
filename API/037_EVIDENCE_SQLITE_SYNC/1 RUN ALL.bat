@echo off
setlocal
rem Sync companions into the pipeline SQLite database (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 37 --yes %* & goto :done)
python "%SYS%engine\menu.py" 37 --yes %*
:done
pause
