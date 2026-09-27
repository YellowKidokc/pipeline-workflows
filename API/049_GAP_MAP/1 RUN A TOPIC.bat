@echo off
setlocal
rem Overlay a topic synthesis on David's own work: expand / contract / holes, and who said it first (citations).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 49 %* & goto :done)
python "%SYS%engine\menu.py" 49 %*
:done
pause
