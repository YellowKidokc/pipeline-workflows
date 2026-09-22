#!/usr/bin/env python3
import argparse
from pathlib import Path
from workbench.export import clean_export
p=argparse.ArgumentParser(description="Export only the documented station allowlist with a fresh identity")
p.add_argument("source",type=Path); p.add_argument("destination",type=Path)
a=p.parse_args(); print(clean_export(a.source,a.destination).resolve())
