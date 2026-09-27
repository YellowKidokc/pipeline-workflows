from pathlib import Path
import sys

system = next(p for p in Path(__file__).resolve().parents if p.name == "_system")
sys.path.insert(0, str(system))
from engine.paths import station_dir
root = station_dir("20_CKG_RUN").parent
backside = system / "vendor" / "ckg"
sys.path.insert(0, str(backside))
from workbench.series_tools import main

sys.argv[1:1] = ["--root", str(root)]
main()
