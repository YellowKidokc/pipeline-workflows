@echo off
setlocal
title Portable TTS Parallel
cd /d "%~dp0"
if not defined TTS_WORKERS set "TTS_WORKERS=4"
if not exist "INBOX" mkdir "INBOX"
if not exist "OUTBOX" mkdir "OUTBOX"

set "PYTHON=%~dp0.venv\Scripts\python.exe"
set "PYARGS="
if exist "%PYTHON%" goto :run
py -3 --version >nul 2>&1
if not errorlevel 1 (
  set "PYTHON=py"
  set "PYARGS=-3"
  goto :run
)
python --version >nul 2>&1
if not errorlevel 1 (
  set "PYTHON=python"
  goto :run
)
echo Python is missing. Run SETUP_OR_FIX.bat first.
pause
exit /b 1

:run
echo Running %TTS_WORKERS% TTS jobs in parallel.
echo Order: PRIORITY, then SERIES, then GENERAL.
if "%~1"=="" (
  "%PYTHON%" %PYARGS% "%~dp0portable_tts.py" --workers %TTS_WORKERS%
) else (
  "%PYTHON%" %PYARGS% "%~dp0portable_tts.py" "%~1" --workers %TTS_WORKERS%
)
set "RESULT=%ERRORLEVEL%"
echo.
if "%RESULT%"=="0" (echo Done. MP3 files are in OUTBOX.) else (echo A job failed. Run TROUBLESHOOT.bat.)
pause
exit /b %RESULT%
