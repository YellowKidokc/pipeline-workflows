@echo off
setlocal
title Portable TTS Setup or Fix
cd /d "%~dp0"
echo ============================================================
echo   PORTABLE TTS - SETUP / REPAIR
echo ============================================================
echo.

set "BASEPY="
set "BASEARGS="
py -3 --version >nul 2>&1
if not errorlevel 1 (
  set "BASEPY=py"
  set "BASEARGS=-3"
) else (
  python --version >nul 2>&1
  if not errorlevel 1 set "BASEPY=python"
)

if not defined BASEPY (
  echo [FAIL] Python 3 was not found.
  echo Install Python from https://www.python.org/downloads/
  echo During installation, select "Add Python to PATH".
  pause
  exit /b 1
)

echo [1/3] Python found
%BASEPY% %BASEARGS% --version

if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" --version >nul 2>&1
  if errorlevel 1 (
    echo [2/3] Existing environment does not work in this location.
    setlocal EnableDelayedExpansion
    set "BACKUP=.venv_broken_%RANDOM%"
    echo       Preserving it as !BACKUP! and rebuilding...
    move ".venv" "!BACKUP!" >nul
    endlocal
  )
)

if not exist ".venv\Scripts\python.exe" (
  echo [2/3] Creating this folder's private Python environment...
  %BASEPY% %BASEARGS% -m venv ".venv"
  if errorlevel 1 goto :failed
) else (
  echo [2/3] Private Python environment already exists
)

echo [3/3] Installing or repairing Edge TTS...
".venv\Scripts\python.exe" -m pip install --upgrade pip edge-tts
if errorlevel 1 goto :failed

if not exist "INBOX" mkdir "INBOX"
if not exist "OUTBOX" mkdir "OUTBOX"
if not exist "INBOX\PRIORITY" mkdir "INBOX\PRIORITY"
if not exist "INBOX\SERIES" mkdir "INBOX\SERIES"
if not exist "INBOX\GENERAL" mkdir "INBOX\GENERAL"
".venv\Scripts\python.exe" -c "import edge_tts; print('[OK] edge-tts', edge_tts.__version__)"
if errorlevel 1 goto :failed

echo.
echo READY. Put files under INBOX, then choose a RUN_TTS launcher.
pause
exit /b 0

:failed
echo.
echo [FAIL] Setup did not finish. Check your internet connection, then run
echo SETUP_OR_FIX.bat again. TROUBLESHOOT.bat can make a diagnostic report.
pause
exit /b 1
