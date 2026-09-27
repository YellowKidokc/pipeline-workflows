#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openintel.ledger import Ledger

parser = argparse.ArgumentParser(description="Create an empty OpenIntel SQLite ledger")
parser.add_argument("ledger")
args = parser.parse_args()
ledger = Ledger(args.ledger)
ledger.initialize()
ledger.close()
print(f"Initialized {args.ledger}")
