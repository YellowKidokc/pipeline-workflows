@echo off
cd /d "%~dp0"
start "" http://localhost:8771/
python serve_backside.py 8771
