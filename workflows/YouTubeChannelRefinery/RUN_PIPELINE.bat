@echo off
py -3 "%~dp0SCRIPTS\run_pipeline.py" %*
if errorlevel 1 pause
