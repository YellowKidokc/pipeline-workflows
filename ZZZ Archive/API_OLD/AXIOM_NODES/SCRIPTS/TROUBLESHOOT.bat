@echo off
setlocal
set "ROOT=%~dp0..\.."
set "FAIL=0"
python --version >nul 2>&1 || (echo FAIL: Python is unavailable.& set "FAIL=1")
if not defined DEEPSEEK_API_KEY (echo FAIL: DEEPSEEK_API_KEY is not set.& set "FAIL=1") else echo OK: DeepSeek key is available.
if not exist "%ROOT%\_BACKSIDE\SHARED\PROVIDERS\candidate_station_api.py" (echo FAIL: Shared caller is missing.& set "FAIL=1") else echo OK: Shared caller exists.
if not exist "%ROOT%\_BACKSIDE\STATIONS\AXIOM_NODES\REFERENCES\reference_manifest.json" (echo FAIL: Reference manifest is missing.& set "FAIL=1") else echo OK: Reference manifest exists.
exit /b %FAIL%

