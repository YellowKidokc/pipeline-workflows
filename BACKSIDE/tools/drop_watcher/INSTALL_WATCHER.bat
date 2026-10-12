@echo off
set /p DEST="Folder to install watcher into: "
if not exist "%DEST%" mkdir "%DEST%"
copy /Y "%~dp0drop_watcher.py" "%DEST%\" >nul
copy /Y "%~dp0watch_rules.yaml" "%DEST%\" >nul
copy /Y "%~dp0WATCH.bat" "%DEST%\" >nul
echo Installed in %DEST%
pause
