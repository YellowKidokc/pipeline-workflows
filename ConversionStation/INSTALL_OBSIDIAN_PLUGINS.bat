@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL_OBSIDIAN_PLUGINS.ps1" "%~1"
exit /b %ERRORLEVEL%
