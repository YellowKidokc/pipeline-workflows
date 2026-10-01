"""59_CHI_EVALUATOR: a bundle. Its passes are declared in station.json (steps) and run by engine/bundle.py.

Without questions, on any folder:
    python 59_chi_evaluator.py <folder or note> --out <folder> --workers 8
"""
import sys
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.bundle import main

if __name__ == "__main__":
    raise SystemExit(main("59_CHI_EVALUATOR"))
