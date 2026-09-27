@echo off
setlocal
rem Base layer for a video: the summary questions in QUESTIONS.md, whole transcript in one call.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 08 --yes %* & goto :done)
python "%SYS%engine\menu.py" 08 --yes %*
:done
pause
