@echo off
setlocal
rem Theology triage after the CKG index: 17 probes (CLEAN / NOTE / FLAG / CLAIM / ??), rules enforced in code, argument layer for the claim graph, YouTube platform notes.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 10 --yes %* & goto :done)
python "%SYS%engine\menu.py" 10 --yes %*
:done
pause
