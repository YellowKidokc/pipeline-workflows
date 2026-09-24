@echo off
setlocal
pushd "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Not installed. Run SETUP.bat first.
  exit /b 1
)
"%CD%\.venv\Scripts\python.exe" -m drop_pipeline.runner status --workspace "%CD%\Workspace"
set "RESULT=%ERRORLEVEL%"
popd
exit /b %RESULT%
