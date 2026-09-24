@echo off
echo Processing inbox for 03_JOB_CARDS...
cd /d X:\03_JOB_CARDS
python _front_door\process_inbox.py 2>nul || echo No processor yet
pause
