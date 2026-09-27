@echo off
setlocal
rem 57_API_DEEP on any folder: asks where the notes are, which ones (pick list / how many),
rem where answers go (Enter = onto each note), then offers extra searches and extra passes.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% "%SYS%engine\ask.py" 57
pause
