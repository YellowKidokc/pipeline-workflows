@echo off
setlocal
pushd "%~dp0"
if "%~1"=="" (
  set /p "SOURCE=Enter a file path or URL: "
) else (
  set "SOURCE=%~1"
)
if not exist ".venv\Scripts\python.exe" call "%CD%\SETUP.bat"
if errorlevel 1 exit /b 1
"%CD%\.venv\Scripts\python.exe" -m theophysics_conversion.convert "%SOURCE%" --export-root "%CD%\Workspace\CONVERTED" --state-root "%CD%\Workspace\STATE\conversion"
set "RESULT=%ERRORLEVEL%"
popd
exit /b %RESULT%
