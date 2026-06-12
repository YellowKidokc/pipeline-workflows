@echo off
REM === BIL Preference Engine — Auto-Start ===
REM Drop a shortcut to this file in: shell:startup
REM (Win+R → shell:startup → paste shortcut)

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
set BIL_HOME=D:\BIL\behavioral-intelligence-layer-OBS-Plugin-Final-Claude

echo [BIL] Starting preference engine server...
start /min "BIL-Server" cmd /c "cd /d %BIL_HOME% && %PYTHON% -m bil.bil_server"

REM Give server 3 seconds to bind the port
timeout /t 3 /nobreak >nul

if "%BIL_START_CLIPBOARD_WATCHER%"=="1" (
    echo [BIL] Starting clipboard watcher fallback...
    start /min "BIL-Clipboard" cmd /c "%PYTHON% D:\BIL\clipboard_watcher.py"
) else (
    echo [BIL] Clipboard watcher skipped. ClipSync bridge owns clipboard-to-BIL feed.
    echo [BIL] To enable fallback watcher, set BIL_START_CLIPBOARD_WATCHER=1 before launch.
)

echo [BIL] Startup complete.
echo [BIL] Server: http://localhost:8420/bil/status
echo [BIL] To stop: close the minimized windows or kill python.exe
timeout /t 5
exit
