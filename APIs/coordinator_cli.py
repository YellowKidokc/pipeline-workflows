#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from workbench.coordinator import aggregate, discover
p=argparse.ArgumentParser(description="Inspect only explicitly selected station roots")
p.add_argument("roots",type=Path,nargs="+")
p.add_argument("--inventory",type=Path,default=Path(__file__).parent/"coordinator"/"inventory.json")
p.add_argument("--activity",type=Path,default=Path(__file__).parent/"activity"/"activity.csv")
a=p.parse_args(); inventory=discover(a.roots); a.inventory.parent.mkdir(parents=True,exist_ok=True); a.inventory.write_text(json.dumps(inventory,indent=2)+"\n"); aggregate(inventory,a.activity); print(json.dumps(inventory,indent=2))
