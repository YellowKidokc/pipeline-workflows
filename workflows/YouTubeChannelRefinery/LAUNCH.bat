@echo off
:menu
cls
echo OpenIntel Refinery
py -3 -c "import json,pathlib; d=json.loads(pathlib.Path(r'%~dp0STATE\queue.json').read_text()) if pathlib.Path(r'%~dp0STATE\queue.json').exists() else {'jobs':[]}; print('\n'.join('%s: %s'%%(x['id'],x['status']) for x in d['jobs']) or 'Queue empty')"
echo [R] Run scheduler once  [O] Open output  [Q] Quit
choice /c ROQ /n
if errorlevel 3 exit /b
if errorlevel 2 start "" "%~dp0OUTPUT" & goto menu
py -3 "%~dp0SCRIPTS\scheduler.py" --once
goto menu
