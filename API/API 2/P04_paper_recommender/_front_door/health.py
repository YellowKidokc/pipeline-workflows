#!/usr/bin/env python3
"""Health check for P04_paper_recommender"""
import json, importlib, sys
from pathlib import Path

def check():
    status = {'engine': 'P04', 'name': 'paper_recommender', 'checks': {}}

    # Check library import
    try:
        importlib.import_module('custom')
        status['checks']['library_custom'] = 'OK'
    except ImportError:
        status['checks']['library_custom'] = 'MISSING'

    # Check state files
    state_dir = Path(__file__).parent.parent / '_state'
    pkl_files = list(state_dir.glob('*.pkl'))
    status['checks']['trained_models'] = len(pkl_files)

    # Check inbox
    inbox = Path(__file__).parent.parent / '_inbox'
    pending = list(inbox.glob('*')) if inbox.exists() else []
    pending = [p for p in pending if p.name != 'README.md']
    status['checks']['inbox_pending'] = len(pending)

    status['healthy'] = status['checks'].get(f'library_{engine["library"]}') == 'OK'
    return status

if __name__ == '__main__':
    result = check()
    print(json.dumps(result, indent=2))
