@echo off
setlocal
set "HERE=%~dp0"
set "REPO=%HERE%..\..\..\.."
set "PAPER=bgl-01-be-glad-youre-a-loser"
set "SOURCE=G:\faiththruphysics-site-v2\be-glad-youre-a-loser\%PAPER%.html"
set "OUT=%HERE%..\OUTBOX\%PAPER%"

python "%REPO%\API\API\_BACKSIDE\STATIONS\FRUITS\SCRIPTS\inject_fruits_html.py" ^
  "%SOURCE%" ^
  "%OUT%\%PAPER%.fruits.json" ^
  "%OUT%\%PAPER%.run.json" ^
  "%OUT%\%PAPER%.fruits-integrated.html"

if errorlevel 1 (
  echo Fruits page build failed.
  exit /b 1
)

echo Open: %OUT%\%PAPER%.fruits-integrated.html
endlocal
