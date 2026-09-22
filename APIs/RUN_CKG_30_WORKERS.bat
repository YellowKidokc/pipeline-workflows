@echo off
set "CKG_ROOT=%~dp0"
powershell -NoProfile -Command "$env:PYTHONPATH=$env:CKG_ROOT; python -m workbench.ckg --root $env:CKG_ROOT --workers 30"
pause
