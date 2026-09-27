@echo off
setlocal
rem Channel overviews, debate pages, catalog.xlsx and catalog.sqlite from the index (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 05 --yes %* & goto :done)
python "%SYS%engine\menu.py" 05 --yes %*
:done
pause
