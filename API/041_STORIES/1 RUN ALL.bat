@echo off
setlocal
rem Hook / sequence / coherence per paper -> series pass -> gated memorable lines (STORY_STATION_V2).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 41 --yes %* & goto :done)
python "%SYS%engine\menu.py" 41 --yes %*
:done
pause
