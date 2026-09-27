#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description="Install the first-class hunch templates into an OpenIntel vault")
parser.add_argument("vault", type=Path)
args = parser.parse_args()
source = Path(__file__).parents[1] / "openintel" / "templates"
targets = [(source / "00_SCHEMA_TEMPLATES/HUNCH.md", args.vault / "00_SCHEMA_TEMPLATES/HUNCH.md"), (source / "HUNCH.md", args.vault / "CASE_TEMPLATE/HUNCH.md")]
for src, dest in targets:
    dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dest); print(dest)
