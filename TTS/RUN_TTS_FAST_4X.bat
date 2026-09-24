@echo off
setlocal
cd /d "%~dp0"
set "TTS_WORKERS=4"
call "%~dp0RUN_WITH_WORKERS.bat" %*
exit /b %ERRORLEVEL%
