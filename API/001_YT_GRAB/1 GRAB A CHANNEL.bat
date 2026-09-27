@echo off
setlocal
rem Download YouTube transcripts (channel, playlist or video URLs) into yt_subtitles. Then asks what to look for in this channel and whether to auto-process new videos.
set "SYS=%~dp0..\_system\"
where py >nul 2>nul && (py -3 "%SYS%engine\menu.py" 01 %* & goto :done)
python "%SYS%engine\menu.py" 01 %*
:done
pause
