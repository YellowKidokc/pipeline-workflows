@echo off
setlocal
rem One uniform name (Ch 159 - Title) and an Obsidian note (front matter, H1, transcript) per transcript, into yt_markdown/<Channel>/, one for one; --watch waits for a download to finish, then converts, tidies and summarizes (local).
set "SYS=%~dp0..\..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 12 --yes %* & goto :done)
python "%SYS%engine\menu.py" 12 --yes %*
:done
pause
