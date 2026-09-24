@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0IMPORT_TO_DROP.ps1" "%~1"
exit /b %ERRORLEVEL%
