@echo off
setlocal
cd /d "%~dp0"

echo === ME Station: local validation (no API calls) ===
echo.

py -3 scripts\me_lexicon_build.py
if errorlevel 1 (
  echo.
  echo Lexicon build failed. Check that paths.json keys me_pills and me_drift_rules are set.
  pause
  exit /b 1
)

for /f "usebackq delims=" %%i in (`py -3 scripts\station_paths.py gold_canon_source`) do set "ME_CANON=%%i"
if not defined ME_CANON (
  echo.
  echo Could not resolve gold_canon_source from paths.json.
  pause
  exit /b 1
)
set "ME_PAPER=%ME_CANON%\W3-master-equation.canonical.md"
if not exist "%ME_PAPER%" (
  echo.
  echo Pilot paper not found: %ME_PAPER%
  pause
  exit /b 1
)

py -3 scripts\lexicon_pass.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail
py -3 scripts\stats_engine.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail
py -3 scripts\stats_workbook.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

echo.
echo Validation passed. See grading_out\ for the .lexicon.json, .stats.json and .stats.xlsx.
pause
exit /b 0

:fail
echo.
echo Validation failed. Review the messages above.
pause
exit /b 1
