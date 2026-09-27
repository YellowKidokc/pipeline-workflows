@echo off
setlocal
rem Pair GOD IS unproven claims with Lean targets (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 51 --yes %* & goto :done)
python "%SYS%engine\menu.py" 51 --yes %*
:done
pause
