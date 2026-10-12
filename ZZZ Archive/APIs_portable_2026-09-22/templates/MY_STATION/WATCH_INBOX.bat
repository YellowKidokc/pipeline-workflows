@echo off
setlocal
set "ROOT=%~dp0"
py -3 "%ROOT%SCRIPTS\workbench_cli.py" watch --root "%ROOT%"
exit /b %ERRORLEVEL%
