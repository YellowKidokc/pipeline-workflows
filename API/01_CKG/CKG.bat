@echo off
title CKG
color 0E
set "API=D:\GitHub\pipeline-workflows\API\01_CKG"
:menu
cls
echo.
echo   ==========================================
echo    CKG
echo   ==========================================
echo.
echo    1  CKG V4 on a paper or folder   (drag it in)
echo    2  CKG V4 on everything in its INBOX
echo    3  Original CKG (station 20) on its INBOX
echo.
echo    4  Open CKG V4 results  (OUTBOX)
echo    5  Open CKG V4 INBOX    (drop papers here)
echo    6  Open the V4 prompts  (BACKSIDE\calls)
echo.
echo    Q  Quit
echo.
set "C="
set /p C=  Choose: 
if /i "%C%"=="1" goto one
if /i "%C%"=="2" goto two
if /i "%C%"=="3" goto three
if /i "%C%"=="4" start "" "%API%\025_CKG_V4\OUTBOX" & goto menu
if /i "%C%"=="5" start "" "%API%\025_CKG_V4\INBOX" & goto menu
if /i "%C%"=="6" start "" "%API%\025_CKG_V4\BACKSIDE\calls" & goto menu
if /i "%C%"=="q" exit /b 0
goto menu

:one
echo.
set "T="
set /p T=  Drag a paper or folder here, then press Enter: 
if "%T%"=="" goto menu
set "T=%T:"=%"
set /p W=  How many papers at once? (Enter = 3): 
if "%W%"=="" set W=3
cd /d "%API%\025_CKG_V4\BACKSIDE"
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% 25_ckg_v4.py "%T%" --workers %W%
echo.
echo  Results are in 025_CKG_V4\OUTBOX.
pause
goto menu

:two
call "%API%\025_CKG_V4\1 RUN HERE.bat"
goto menu

:three
call "%API%\020_CKG\1 RUN HERE.bat"
goto menu
