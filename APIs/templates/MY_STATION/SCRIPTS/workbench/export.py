from __future__ import annotations
import shutil
from pathlib import Path
ALLOW=("START_HERE.bat","SETUP.bat","RUN_ONCE.bat","WATCH_INBOX.bat","CHECK_SETUP.bat","README.md","CONFIG/station.json","PROMPTS","SCRIPTS")
def clean_export(source: Path,destination: Path):
    if destination.exists(): raise FileExistsError(destination)
    destination.mkdir(parents=True)
    for name in ALLOW:
        src=source/name
        if src.is_dir(): shutil.copytree(src,destination/name,ignore=shutil.ignore_patterns("__pycache__","*.pyc","private.local.json","*.key","*.pem"))
        elif src.exists(): (destination/name).parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,destination/name)
    from .cli import setup
    setup(destination)
    return destination
