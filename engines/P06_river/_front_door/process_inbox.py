#!/usr/bin/env python3
"""Process inbox items for P06_river"""
import json, shutil
from pathlib import Path
from datetime import datetime

ENGINE_ROOT = Path(__file__).parent.parent
INBOX = ENGINE_ROOT / '_inbox'
OUTBOX = ENGINE_ROOT / '_outbox'
PROCESSED = ENGINE_ROOT / '_processed'

def process():
    items = [f for f in INBOX.iterdir() if f.name != 'README.md']
    if not items:
        print('Inbox empty — nothing to process.')
        return

    print(f'Found {len(items)} items in inbox:')
    for item in items:
        print(f'  → {item.name}')
        # TODO: Wire to actual engine processing
        # For now, move to processed with timestamp
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        dest = PROCESSED / f'{ts}_{item.name}'
        shutil.move(str(item), str(dest))
        print(f'    Moved to _processed/{dest.name}')

if __name__ == '__main__':
    process()
