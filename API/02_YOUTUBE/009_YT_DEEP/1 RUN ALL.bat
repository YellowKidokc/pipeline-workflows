@echo off
setlocal
rem Detailed, rigorous layer on top of the base summary (reads 08's output + the whole transcript).
set "SYS=%~dp0..\..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 09 --yes %* & goto :done)
python "%SYS%engine\menu.py" 09 --yes %*
:done
pause
