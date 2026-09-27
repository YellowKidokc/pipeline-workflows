@echo off
setlocal
rem Physics mirror pass after the CKG index: which physics process a theological event mirrors (or the reverse), stage by stage, in order, and whether it is identity, structural isomorphism or only analogy (rules enforced in code).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 11 --yes %* & goto :done)
python "%SYS%engine\menu.py" 11 --yes %*
:done
pause
