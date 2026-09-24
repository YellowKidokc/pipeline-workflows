@echo off
setlocal
pushd "%~dp0"

echo [ConversionStation] Installing in: %CD%

if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    python -m venv .venv
  )
  if errorlevel 1 goto :fail
)

set "PYTHON=%CD%\.venv\Scripts\python.exe"
"%PYTHON%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :fail
"%PYTHON%" -m pip install -r "%CD%\drop_pipeline\requirements.txt"
if errorlevel 1 goto :fail
"%PYTHON%" -m pip install -e "%CD%\conversion_engine[all]"
if errorlevel 1 goto :fail
"%PYTHON%" -m pip install tubescribe
if errorlevel 1 goto :fail

"%PYTHON%" -m drop_pipeline.runner init --workspace "%CD%\Workspace"
if errorlevel 1 goto :fail

echo.
echo Setup complete. This folder can be moved or renamed.
echo After moving it, run SETUP.bat again to rebuild local paths.
popd
exit /b 0

:fail
echo.
echo Setup failed with error %ERRORLEVEL%.
popd
exit /b 1
