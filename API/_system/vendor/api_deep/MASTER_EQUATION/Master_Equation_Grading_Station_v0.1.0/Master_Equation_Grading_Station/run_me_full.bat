@echo off
setlocal
cd /d "%~dp0"
set "PASS=setup (paper resolution)"

echo === ME Station: full run (all 7 passes) ===
echo.

if "%~1"=="" (
  echo Usage: run_me_full.bat "path\to\paper.md"
  echo.
  echo Runs every pass on one paper:
  echo   [1/7] lexicon build   ^(me_lexicon_build.py, local^)
  echo   [2/7] lexicon pass    ^(lexicon_pass.py, local^)
  echo   [3/7] stats engine    ^(stats_engine.py, local^)
  echo   [4/7] stats workbook  ^(stats_workbook.py, local^)
  echo   [5/7] span judge      ^(span_judge.py, DeepSeek API^)
  echo   [6/7] canon ledger    ^(canon_ledger_pass.py, DeepSeek API^)
  echo   [7/7] report page     ^(report_page.py, DeepSeek API^)
  pause
  exit /b 1
)
set "ME_PAPER=%~1"
if not exist "%ME_PAPER%" (
  echo Paper not found: %ME_PAPER%
  goto fail
)
echo Paper: %ME_PAPER%
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

set "PASS=span judge"
echo [%date% %time%] [5/7] span judge
py -3 scripts\span_judge.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

set "PASS=canon ledger"
echo [%date% %time%] [6/7] canon ledger
py -3 scripts\canon_ledger_pass.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

set "PASS=report page"
echo [%date% %time%] [7/7] report page
py -3 scripts\report_page.py --paper "%ME_PAPER%"
if errorlevel 1 goto fail

echo.
echo [%date% %time%] Full run complete. See grading_out\ for the .report.html and the rest of the artifact family.
pause
exit /b 0

:fail
echo.
echo [%date% %time%] Full run failed during pass: %PASS%
echo Review the messages above. Everything already graded is kept in grading_out\; rerun to continue.
pause
exit /b 1
