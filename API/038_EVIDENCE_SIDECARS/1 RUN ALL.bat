@echo off
setlocal
rem Write / search evidence sidecars (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 38 --yes %* & goto :done)
python "%SYS%engine\menu.py" 38 --yes %*
:done
pause
