@echo off
setlocal
rem Theophysics congruence matrix: evidence status x Lean status per paper (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 50 --yes %* & goto :done)
python "%SYS%engine\menu.py" 50 --yes %*
:done
pause
