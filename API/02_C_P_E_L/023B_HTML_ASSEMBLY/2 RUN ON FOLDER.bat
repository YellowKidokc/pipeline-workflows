@echo off
title 23B HTML Assembly - on a folder
cd /d "%~dp0BACKSIDE"
echo.
set "TARGET=%~1"
if "%TARGET%"=="" set /p TARGET=Drag a folder or atom file here (or paste its path), then press Enter: 
if "%TARGET%"=="" exit /b 0
set "TARGET=%TARGET:"=%"
set "PY=python" & where py >nul 2>nul && set "PY=py -3"
%PY% 23b_assemble.py "%TARGET%"
echo.
pause