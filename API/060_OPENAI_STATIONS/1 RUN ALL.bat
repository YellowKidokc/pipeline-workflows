@echo off
setlocal
rem The 23 api_call_NN prompts, grouped into bundles so one whole-document call answers several.
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 60 --yes %* & goto :done)
python "%SYS%engine\menu.py" 60 --yes %*
:done
pause
