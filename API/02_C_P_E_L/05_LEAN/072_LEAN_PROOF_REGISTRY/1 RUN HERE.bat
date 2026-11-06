@echo off
setlocal
cd /d "%~dp0BACKSIDE"
py -3.13 -m uvicorn app.main:app --host 127.0.0.1 --port 8424
endlocal

