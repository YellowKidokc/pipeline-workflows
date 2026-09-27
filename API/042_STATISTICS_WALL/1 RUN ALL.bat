@echo off
setlocal
rem Every academic + Obsidian metric in Python (same numbers every run), with corpus / series percentiles and change since last version.
rem Find _system by walking up, so this folder can be moved anywhere under API\.
set "SYS=%~dp0"
:findsys
if exist "%SYS%_system\engine\menu.py" goto :sysok
for %%I in ("%SYS%..") do set "UP=%%~fI"
if not "%UP:~-1%"=="\" set "UP=%UP%\"
if /i "%UP%"=="%SYS%" echo Cannot find the _system folder above %~dp0 & pause & exit /b 1
set "SYS=%UP%"
goto :findsys
:sysok
set "SYS=%SYS%_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 42 --yes %* & goto :done)
python "%SYS%engine\menu.py" 42 --yes %*
:done
pause
