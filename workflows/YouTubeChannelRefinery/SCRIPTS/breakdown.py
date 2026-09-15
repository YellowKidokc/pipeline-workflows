#!/usr/bin/env python3
"""Run the S0-S10 OpenIntel refinery chain or one station for one video."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
from station_common import PACKET, STATIONS, Ledger, run_station

def run_video(ledger,video,stations=None,force=False):
 selected=stations
 if selected is None:
  db=Ledger(ledger); db.initialize(); row=db.db.execute("SELECT profile FROM videos WHERE id=?",(video,)).fetchone(); prefs=json.loads((PACKET/'PREFS/preferences.json').read_text()); db.close()
  selected=prefs.get('profile_stations',{}).get(row[0] if row else 'general',prefs.get('stations',STATIONS))
 return {name:run_station(ledger,video,name,force) for name in selected}
def main():
 p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True)
 station=sub.add_parser('station'); station.add_argument('name',choices=STATIONS); station.add_argument('--video',required=True); station.add_argument('--ledger',type=Path,required=True); station.add_argument('--force',action='store_true')
 run=sub.add_parser('run'); run.add_argument('--video',required=True); run.add_argument('--ledger',type=Path,required=True); run.add_argument('--force',action='store_true')
 a=p.parse_args()
 if a.command=='station': print(run_station(a.ledger,a.video,a.name,a.force))
 else: print(json.dumps(run_video(a.ledger,a.video,force=a.force),indent=2))
if __name__=='__main__': main()
