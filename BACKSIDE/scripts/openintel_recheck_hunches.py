#!/usr/bin/env python3
"""Re-check OPEN/PARKED hunches against new accepted ledger text."""
from __future__ import annotations
import argparse, datetime as dt, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openintel.ledger import Ledger

STOP = {"the","a","an","and","or","to","of","in","is","it","that","this","was","for","with","on"}
def tokens(text): return {x for x in re.findall(r"[a-z0-9]{3,}", text.lower()) if x not in STOP}
def similarity(a,b):
    a,b=tokens(a),tokens(b)
    return len(a&b)/len(a|b) if a and b else 0.0

def recheck(path, threshold=.18):
    ledger=Ledger(path); ledger.initialize(); now=dt.datetime.now(dt.timezone.utc).isoformat(); created=0
    hunches=ledger.db.execute("SELECT id,collection,gut_statement FROM hunches WHERE hunch_status IN ('OPEN','PARKED') AND lifecycle != 'REJECTED'").fetchall()
    records=[]
    for table,column in (("statements","statement_text"),("claims","claim_text"),("evidence","description")):
        records += [(r[0],r[1]) for r in ledger.db.execute(f"SELECT id,{column} FROM {table} WHERE lifecycle='ACCEPTED' AND {column} IS NOT NULL")]
    for h in hunches:
        for record_id,text in records:
            score=similarity(h[2],text)
            if score < threshold: continue
            signal_id=ledger.next_id("SIG",h[1])
            with ledger.db:
                exists=ledger.db.execute("SELECT 1 FROM hunch_matches WHERE hunch_id=? AND record_id=? AND method='token-jaccard-v1'",(h[0],record_id)).fetchone()
                if exists: continue
                ledger.db.execute("INSERT INTO signals(id,collection,signal_kind,description,score,source_record_id,created_at) VALUES(?,?,'SIG',?,?,?,?)",(signal_id,h[1],f"New ledger material touches hunch {h[0]}",score,record_id,now))
                ledger.db.execute("INSERT INTO hunch_matches VALUES(?,?,?, ?,?,?)",(h[0],record_id,"token-jaccard-v1",score,now,signal_id))
                ledger.db.execute("INSERT OR IGNORE INTO links(from_id,to_id,link_type,source,created_at) VALUES(?,?,'PROMOTED_FROM','hunch-recheck',?)",(signal_id,h[0],now))
            created+=1
    ledger.close(); return created

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('ledger'); p.add_argument('--threshold',type=float,default=.18); a=p.parse_args(); print(f"Created {recheck(a.ledger,a.threshold)} candidate signals")
