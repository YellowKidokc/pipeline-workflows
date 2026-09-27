@echo off
setlocal
rem Every academic + Obsidian metric in Python (same numbers every run), with corpus / series percentiles and change since last version.
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 42 --yes %* & goto :done)
python "%SYS%engine\menu.py" 42 --yes %*
:done
pause
