@echo off
setlocal
cd /d "%~dp0"
set "PASS=setup (paper resolution)"

echo === ME Station: pilot run (all 7 passes, LLM passes limited to 12) ===
echo.

if "%~1"=="" (
  for /f "usebackq delims=" %%i in (`py -3 scripts\station_paths.py gold_canon_source`) do set "ME_CANON=%%i"
  if not defined ME_CANON (
    echo Could not resolve gold_canon_source from paths.json.
    goto fail
  )
  set "ME_PAPER=%ME_CANON%\W3-master-equation.canonical.md"
) else (
  set "ME_PAPER=%~1"
)
if not exist "%ME_PAPER%" (
  echo Paper not found: %ME_PAPER%
  goto fail
)
echo Paper: %ME_PAPER%
echo The two LLM passes run with --limit 12, so the pilot only judges the
echo first 12 spans and processes the first 12 claims. Everything else is full.
echo.

set "PASS=lexicon build"
echo [%date% %time%] [1/7] lexicon build
py -3 scripts\me_lexicon_build.py
if errorlevel 1 goto fail

set "PASS=lexicon pass"
echo [%date% %time%] [2/7] lexicon pass
py -3 scripts\lexicon_pass.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

set "PASS=stats engine"
echo [%date% %time%] [3/7] stats engine
py -3 scripts\stats_engine.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

set "PASS=stats workbook"
echo [%date% %time%] [4/7] stats workbook
py -3 scripts\stats_workbook.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

set "PASS=span judge (limit 12)"
echo [%date% %time%] [5/7] span judge ^(limit 12^)
py -3 scripts\span_judge.py --paper "%ME_PAPER%" --limit 12
if errorlevel 1 goto fail

set "PASS=canon ledger (limit 12)"
echo [%date% %time%] [6/7] canon ledger ^(limit 12^)
py -3 scripts\canon_ledger_pass.py --paper "%ME_PAPER%" --limit 12
if errorlevel 1 goto fail

set "PASS=report page"
echo [%date% %time%] [7/7] report page
py -3 scripts\report_page.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

echo.
echo [%date% %time%] Pilot complete. The .spans.json and .canon.json only cover the
echo first 12 spans / claims -- run run_me_full.bat for the full grading.
pause
exit /b 0

:fail
echo.
echo [%date% %time%] Pilot failed during pass: %PASS%
echo Review the messages above.
pause
exit /b 1
