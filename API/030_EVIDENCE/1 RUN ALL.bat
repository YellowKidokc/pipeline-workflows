@echo off
setlocal
rem Turbo evidence intake: one call per paper fills the v0.4.1 companion; shelves + master index.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 30 --yes %* & goto :done)
python "%SYS%engine\menu.py" 30 --yes %*
:done
pause
