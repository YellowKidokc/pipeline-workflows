@echo off
echo Health check 03_JOB_CARDS...
cd /d X:\03_JOB_CARDS
python _front_door\health.py 2>nul || echo No health script yet
pause
