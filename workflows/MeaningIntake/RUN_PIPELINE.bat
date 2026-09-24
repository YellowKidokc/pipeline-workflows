@echo off
setlocal
cd /d "%~dp0\..\.."
python workflows\MeaningIntake\SCRIPTS\run_packet.py
pause

