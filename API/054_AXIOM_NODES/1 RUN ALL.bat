@echo off
setlocal
rem API_DEEP axiom-nodes runner over the atoms workspace (191-node registry).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 54 --yes %* & goto :done)
python "%SYS%engine\menu.py" 54 --yes %*
:done
pause
