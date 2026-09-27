@echo off
setlocal
rem Convert SRT / VTT / JSON transcripts to ytgrab-style .md; originals kept in <Channel>/_originals (local).
set "SYS=%~dp0..\..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 07 --yes %* & goto :done)
python "%SYS%engine\menu.py" 07 --yes %*
:done
pause
