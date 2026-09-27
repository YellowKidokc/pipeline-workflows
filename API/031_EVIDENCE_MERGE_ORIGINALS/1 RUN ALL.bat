@echo off
setlocal
rem Match companions to their originals by sha256 and merge (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 31 --yes %* & goto :done)
python "%SYS%engine\menu.py" 31 --yes %*
:done
pause
