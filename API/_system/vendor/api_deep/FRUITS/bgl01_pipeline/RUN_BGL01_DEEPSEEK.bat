@echo off
setlocal
set "ROOT=%~dp0..\..\_BACKSIDE\STATIONS\FRUITS"
python "%ROOT%\SCRIPTS\fruits_pipeline.py" "G:\faiththruphysics-site-v2\be-glad-youre-a-loser\bgl-01-be-glad-youre-a-loser.html" --output "%~dp0..\OUTBOX" --config "%ROOT%\CONFIG\deepseek.example.json"
pause
