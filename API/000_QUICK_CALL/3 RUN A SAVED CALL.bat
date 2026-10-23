@echo off
setlocal
rem Run one saved call from BACKSIDE\calls (each has its own prompt.txt, input\ and optional settings.txt).
rem The default prompt.txt / INBOX buttons are untouched. Answers land in OUTBOX\<call name>\.
cd /d "%~dp0BACKSIDE"
echo.
echo  SAVED CALLS:
for /d %%D in (calls\*) do echo    %%~nxD
echo.
set /p CALL=Type the call's number or name (e.g. 01): 
if "%CALL%"=="" exit /b 0
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% 00_quick_call.py --call %CALL%
echo.
pause
