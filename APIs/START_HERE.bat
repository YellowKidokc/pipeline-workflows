@echo off
setlocal
set "PYTHONIOENCODING=utf-8"
set "API_PYTHON=%~dp0.venv\Scripts\python.exe"
if exist "%API_PYTHON%" goto run
set "API_PYTHON=python"
:run
"%API_PYTHON%" "%~dp0SCRIPTS\api_workbench.py" menu
set "API_EXIT=%ERRORLEVEL%"
if not "%API_EXIT%"=="0" echo The operation did not complete successfully. Read the message above.
pause
exit /b %API_EXIT%
