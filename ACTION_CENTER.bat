@echo off
setlocal
cd /d "%~dp0"
where pyw >nul 2>nul
if %ERRORLEVEL%==0 (
  start "Pipeline Action Center" pyw -3 "%~dp0tools\action_center\action_center.py"
) else (
  python "%~dp0tools\action_center\action_center.py"
)
if errorlevel 1 pause

