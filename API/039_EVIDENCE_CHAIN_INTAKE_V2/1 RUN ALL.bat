@echo off
setlocal
rem Epistemic intake v2: extract, evaluate against the rubric, adversarial synthesis (3 JSON calls).
set "SYS=%~dp0..\_system\"
if not defined DEEPSEEK_API_KEY echo DEEPSEEK_API_KEY is not set. Run SETUP.bat once. & pause & exit /b 1
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 39 --yes %* & goto :done)
python "%SYS%engine\menu.py" 39 --yes %*
:done
pause
