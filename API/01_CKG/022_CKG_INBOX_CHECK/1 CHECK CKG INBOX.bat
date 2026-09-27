@echo off
setlocal
rem Show what is waiting in the CKG inbox (no API).
set "SYS=%~dp0..\..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 22 --yes %* & goto :done)
python "%SYS%engine\menu.py" 22 --yes %*
:done
pause
