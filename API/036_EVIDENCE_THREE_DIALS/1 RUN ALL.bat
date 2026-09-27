@echo off
setlocal
rem Annotate one article with the three dials (kind, claimed vs earned strength).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 36 --yes %* & goto :done)
python "%SYS%engine\menu.py" 36 --yes %*
:done
pause
