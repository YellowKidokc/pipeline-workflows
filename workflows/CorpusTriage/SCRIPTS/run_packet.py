"""Compatibility entry point for content-based corpus triage."""
from pathlib import Path
import argparse
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from workflows.CorpusTriage.SCRIPTS.triage_folder import triage, sha256
sha = sha256

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '--source', dest='source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    triage(args.source, args.output)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
