@echo off
setlocal
rem Lean atom extractor (scan / classify / verify / audit / enrich / export / pills / briefs / serve).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 52 --yes %* & goto :done)
python "%SYS%engine\menu.py" 52 --yes %*
:done
pause
