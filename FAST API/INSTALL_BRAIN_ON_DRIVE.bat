@echo off
rem Creates <drive>:\_BRAIN (identity + empty registry + logs + BRAIN.md). Writes nothing else.
cd /d "%~dp0"
set /p ROOT=Drive letter (e.g. D) or network share (e.g. \\192.168.2.50\h_hp): 
python brain_server.py install "%ROOT%"
pause
