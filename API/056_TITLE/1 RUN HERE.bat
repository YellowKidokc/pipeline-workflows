@echo off
setlocal
rem 56_TITLE in place: every note in INBOX (lanes 00_PRIORITY / 01_SERIES / 02_GROUP), results in OUTBOX,
rem and the analysis written onto each note. Folders inside INBOX obey their _PICK.md.
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
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% "%~dp0BACKSIDE\56_title.py" "%~dp0INBOX" %*
pause
