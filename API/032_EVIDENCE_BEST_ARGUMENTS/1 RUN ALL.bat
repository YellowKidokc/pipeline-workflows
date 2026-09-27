@echo off
setlocal
rem Cluster primary arguments and weaknesses across companions (local TF-IDF).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 32 --yes %* & goto :done)
python "%SYS%engine\menu.py" 32 --yes %*
:done
pause
