@echo off
setlocal
cd /d "%~dp0\..\.."
python -m py_compile workflows\MeaningIntake\SCRIPTS\run_packet.py
if errorlevel 1 exit /b 1
echo MeaningIntake syntax check passed.

