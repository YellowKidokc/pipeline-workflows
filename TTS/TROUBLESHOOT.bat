@echo off
setlocal
title Portable TTS Troubleshooter
cd /d "%~dp0"
set "REPORT=%~dp0TTS_DIAGNOSTIC.txt"

(
echo PORTABLE TTS DIAGNOSTIC
echo Date: %DATE% %TIME%
echo Folder: %CD%
echo.
echo === FILES ===
if exist "portable_tts.py" (echo [OK] portable_tts.py) else (echo [MISSING] portable_tts.py)
if exist "INBOX" (echo [OK] INBOX) else (echo [MISSING] INBOX)
if exist "OUTBOX" (echo [OK] OUTBOX) else (echo [MISSING] OUTBOX)
echo.
echo === PYTHON ===
where py 2^>nul
py -3 --version 2^>^&1
where python 2^>nul
python --version 2^>^&1
echo.
echo === PRIVATE ENVIRONMENT ===
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" --version 2^>^&1
  ".venv\Scripts\python.exe" -c "import edge_tts; print('edge-tts:', edge_tts.__version__)" 2^>^&1
  ".venv\Scripts\python.exe" -m py_compile "portable_tts.py" 2^>^&1
) else (
  echo [MISSING] .venv - run SETUP_OR_FIX.bat
)
echo.
echo === INPUT COUNT ===
dir /s /b "INBOX\*.txt" "INBOX\*.md" 2^>nul ^| find /c /v ""
) > "%REPORT%"

type "%REPORT%"
echo.
echo Report saved as TTS_DIAGNOSTIC.txt
pause
