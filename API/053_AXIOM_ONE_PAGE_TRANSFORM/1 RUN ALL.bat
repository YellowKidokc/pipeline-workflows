@echo off
setlocal
rem Transform axiom node pages into one-page form (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 53 --yes %* & goto :done)
python "%SYS%engine\menu.py" 53 --yes %*
:done
pause
