@echo off
setlocal
pushd "%~dp0"

if not exist ".venv\Scripts\python.exe" call "SETUP.bat"
if errorlevel 1 goto :fail

".venv\Scripts\python.exe" "BACKSIDE\conversion_station.py" "INBOX"
set "RESULT=%ERRORLEVEL%"
echo.
if "%RESULT%"=="0" (
  echo Finished. Open OUTBOX to see the converted files.
) else (
  echo Finished with items requiring review. Open OUTBOX\90_NEEDS_REVIEW.
)
pause
popd
exit /b %RESULT%

:fail
echo Setup did not complete. Nothing was converted.
pause
popd
exit /b 1
