@echo off
setlocal
rem Automatic chain for channels in WATCH_CHANNELS: convert, clean, index, channel focus, catalog.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 06 --yes %* & goto :done)
python "%SYS%engine\menu.py" 06 --yes %*
:done
pause
