@echo off
setlocal
pushd "%~dp0"
if not exist ".venv\Scripts\python.exe" exit /b 0
"%CD%\.venv\Scripts\python.exe" -m drop_pipeline.runner stop --workspace "%CD%\Workspace"
set "RESULT=%ERRORLEVEL%"
popd
exit /b %RESULT%
