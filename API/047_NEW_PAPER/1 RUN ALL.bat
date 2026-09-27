@echo off
setlocal
rem Create the per-paper working folder from templates/PAPER_FOLDER (then tags it).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 47 --yes %* & goto :done)
python "%SYS%engine\menu.py" 47 --yes %*
:done
pause
