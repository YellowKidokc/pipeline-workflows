@echo off
setlocal
rem Opens the live API workspace (the working version of index.html in this folder).
rem It runs the stations in ..\API through ONE_MENU.bat. Leave the window open while you use the page.
if not exist "%~dp0..\API\ONE_MENU.bat" echo Cannot find ..\API\ONE_MENU.bat next to this folder. & pause & exit /b 1
call "%~dp0..\API\ONE_MENU.bat" workspace %*
