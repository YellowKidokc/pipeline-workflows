@echo off
setlocal
set "API_PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%API_PYTHON%" set "API_PYTHON=python"
"%API_PYTHON%" "%~dp0SCRIPTS\export_portable.py"
set "API_EXIT=%ERRORLEVEL%"
pause
exit /b %API_EXIT%
