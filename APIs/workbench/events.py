from __future__ import annotations
import csv, json, os, threading
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["time","station_id","run_id","job_id","call_id","workflow","event","status","source","source_hash","step","prompt_version","provider","model","retries","error_category","input_tokens","output_tokens","reported_cost","estimated_cost","output","output_hash"]
_lock = threading.Lock()
def now(): return datetime.now(timezone.utc).isoformat()
def append(path: Path, event: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"time": now(), **event}
    with _lock, path.open("a", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"); fh.flush(); os.fsync(fh.fileno())
    return record
def session_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer=csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore"); writer.writeheader()
        for row in rows: writer.writerow({k: row.get(k, "") for k in FIELDS})
