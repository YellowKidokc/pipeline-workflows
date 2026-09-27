@echo off
setlocal
rem Channel summary folder: a 3-sentence summary, 2-3 keywords and the COLUMNS.md answers per video, one call each; the channel sheet (.xlsx, .tsv, index note) is rebuilt after every video.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 13 --yes %* & goto :done)
python "%SYS%engine\menu.py" 13 --yes %*
:done
pause
