@echo off
setlocal
rem Assemble every station's JSON in procedure order (aggregate.json/.md) and build report.html + report.xlsx.
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 46 --yes %* & goto :done)
python "%SYS%engine\menu.py" 46 --yes %*
:done
pause
