"""Write the two standard buttons into a front folder (and remove its old "1 RUN ALL.bat").

    python _system/tools/make_buttons.py <front folder> ["what 1 RUN HERE does"] ["what 2 RUN ON FOLDER does"]

Each .bat is the same: find _system by walking up (so the folder can be moved anywhere under API), then call
_system/engine/button.py with `here` or `folder` and the folder the .bat sits in. Only the description line differs.
Written with CRLF line endings. Never touches anything else in the folder.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FINDSYS = (
    'rem Find _system by walking up, so this folder can be moved anywhere under API\\.\r\n'
    'set "SYS=%~dp0"\r\n'
    ':findsys\r\n'
    'if exist "%SYS%_system\\engine\\menu.py" goto :sysok\r\n'
    'for %%I in ("%SYS%..") do set "UP=%%~fI"\r\n'
    'if not "%UP:~-1%"=="\\" set "UP=%UP%\\"\r\n'
    'if /i "%UP%"=="%SYS%" echo Cannot find the _system folder above %~dp0 & pause & exit /b 1\r\n'
    'set "SYS=%UP%"\r\n'
    'goto :findsys\r\n'
    ':sysok\r\n'
    'set "SYS=%SYS%_system\\"\r\n'
)


def bat(mode: str, about: str) -> bytes:
    return ("@echo off\r\nsetlocal\r\n" + f"rem {about}\r\n" + FINDSYS
            + 'set "PY=python" & where py >nul 2>nul && set "PY=py -3"\r\n'
            + f'%PY% "%SYS%engine\\button.py" {mode} "%~dp0."\r\n'
            + "pause\r\n").encode("utf-8")


def make(front: Path, here: str = "", folder: str = "") -> None:
    meta = json.loads((front / "BACKSIDE" / "station.json").read_text(encoding="utf-8"))
    what = meta.get("description", meta.get("label", front.name))
    for old in front.glob("1 RUN ALL.bat"):
        old.unlink()
    (front / "1 RUN HERE.bat").write_bytes(bat("here", here or f"{what} On this folder's INBOX (or the notes its parent station just ran)."))
    (front / "2 RUN ON FOLDER.bat").write_bytes(bat("folder", folder or f"{what} On any folder or note you point at (X list applies)."))
    print(f"buttons: {front}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    make(Path(sys.argv[1]).resolve(), *(sys.argv[2:4]))
