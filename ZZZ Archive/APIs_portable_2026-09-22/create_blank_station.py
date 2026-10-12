#!/usr/bin/env python3
import argparse
from pathlib import Path
from workbench.cli import create
p=argparse.ArgumentParser(description="Create a clean, uniquely identified portable station")
p.add_argument("destination",type=Path)
a=p.parse_args()
created=create(Path(__file__).parent/"templates"/"MY_STATION",a.destination)
print(created.resolve())
