@echo off
setlocal
if "%~1"=="" (
  echo Usage: %~nx0 "path\to\paper.html"
  exit /b 2
)
set "HERE=%~dp0"
set "ROOT=%HERE%..\.."
for %%F in ("%~1") do set "PAPER=%%~nF"
set "OUT=%ROOT%\AXIOM_NODES\OUTBOX\%PAPER%\%PAPER%.axiom_nodes.json"
python "%ROOT%\_BACKSIDE\SHARED\PROVIDERS\candidate_station_api.py" axiom_nodes "%~1" --station-dir "%ROOT%\_BACKSIDE\STATIONS\AXIOM_NODES" --output "%OUT%" %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

