@echo off
setlocal
title Portable TTS
cd /d "%~dp0"

if not exist "INBOX" mkdir "INBOX"
if not exist "OUTBOX" mkdir "OUTBOX"

call :find_python
if errorlevel 1 goto :missing

echo.
echo ============================================================
echo   PORTABLE TTS - Text and Markdown to MP3
echo ============================================================
if "%~1"=="" (
  echo   Reading every .txt and .md file under INBOX
  "%PYTHON%" %PYARGS% "%~dp0portable_tts.py" --workers 2
) else (
  echo   Reading: %~1
  "%PYTHON%" %PYARGS% "%~dp0portable_tts.py" "%~1" --workers 2
)
set "RESULT=%ERRORLEVEL%"
echo.
if "%RESULT%"=="0" (
  echo Done. Open OUTBOX to find the MP3 files.
) else (
  echo Something failed. Double-click TROUBLESHOOT.bat for a report.
)
pause
exit /b %RESULT%

:find_python
set "PYTHON=%~dp0.venv\Scripts\python.exe"
set "PYARGS="
if exist "%PYTHON%" (
  "%PYTHON%" --version >nul 2>&1
  if not errorlevel 1 exit /b 0
)
py -3 --version >nul 2>&1
if not errorlevel 1 (
  set "PYTHON=py"
  set "PYARGS=-3"
  exit /b 0
)
python --version >nul 2>&1
if not errorlevel 1 (
  set "PYTHON=python"
  exit /b 0
)
exit /b 1

:missing
echo.
echo Python is missing or not working.
echo Double-click SETUP_OR_FIX.bat first.
pause
exit /b 1
