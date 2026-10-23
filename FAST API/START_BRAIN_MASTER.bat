@echo off
rem Starts the Master API / Drive Brain dashboard on http://127.0.0.1:28280/
cd /d "%~dp0"
start "" http://127.0.0.1:28280/
python brain_server.py serve
pause
