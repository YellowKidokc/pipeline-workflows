@echo off
rem STEP 2 - copies (never moves) every approved pick into obsidian_transcripts\<Channel> and into each matching question's 04_SOURCES.
cd /d "%~dp0"
python title_triage.py copy
pause
