@echo off
setlocal
pushd "%~dp0"
if not exist ".venv\Scripts\python.exe" call "%CD%\SETUP.bat"
if errorlevel 1 exit /b 1
"%CD%\.venv\Scripts\python.exe" -m drop_pipeline.runner watch --workspace "%CD%\Workspace"
set "RESULT=%ERRORLEVEL%"
popd
exit /b %RESULT%
