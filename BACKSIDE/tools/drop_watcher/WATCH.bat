@echo off
cd /d "%~dp0"
py -3 drop_watcher.py --path "%~dp0"
if errorlevel 1 pause
