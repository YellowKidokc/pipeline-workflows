@echo off
start "OpenIntel watcher" /min py -3 "%~dp0SCRIPTS\watcher.py"
start "OpenIntel scheduler" /min py -3 "%~dp0SCRIPTS\scheduler.py"
