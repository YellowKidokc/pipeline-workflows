@echo off
setlocal
rem Numbered focus lenses and lettered layers over indexed videos; --ask is free-text focus.
set "SYS=%~dp0..\..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 04 --yes %* & goto :done)
python "%SYS%engine\menu.py" 04 --yes %*
:done
pause
