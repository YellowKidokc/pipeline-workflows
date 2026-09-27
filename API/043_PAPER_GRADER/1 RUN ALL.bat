@echo off
setlocal
rem July deterministic paper audit: metrics, sections, claim candidates, 7Q checks (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 43 --yes %* & goto :done)
python "%SYS%engine\menu.py" 43 --yes %*
:done
pause
