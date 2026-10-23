@echo off
rem STEP 1 - DeepSeek reads the TITLES only (cheap) and writes a pick list per channel into PICKLISTS\. Nothing is copied.
cd /d "%~dp0"
python title_triage.py plan
echo.
echo Pick lists are in %~dp0PICKLISTS  - read the .md files. To reject a pick, set "approved": false in that channel's .json.
echo Then run 2 COPY APPROVED.bat
pause
