@echo off
setlocal
rem CKG atom run over ckg_root/INBOX (map, S01-S10, audit).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 20 --yes %* & goto :done)
python "%SYS%engine\menu.py" 20 --yes %*
:done
pause
