@echo off
setlocal
rem Split CKG outputs into claims / proofs / evidence (local).
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 21 --yes %* & goto :done)
python "%SYS%engine\menu.py" 21 --yes %*
:done
pause
