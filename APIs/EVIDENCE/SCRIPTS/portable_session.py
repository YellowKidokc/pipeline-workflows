"""One durable CSV per evidence session; not a proof or canon decision."""
import csv
from datetime import datetime, timezone
import hashlib
from pathlib import Path


class Session:
    fields = ["source", "sha256", "status", "error", "selected_utc", "finished_utc", "provider", "model", "workers"]

    def __init__(self, root, provider, model, workers):
        self.root = Path(root)
        self.path = self.root / "OUTBOX/RUNS" / datetime.now().strftime("%Y%m%d-%H%M%S-%f") / "PAPERS.csv"
        self.provider, self.model, self.workers = provider, model, workers
        self.rows = {}

    def select(self, workload):
        for path, _, _ in workload:
            key = str(path.relative_to(self.root))
            self.rows[key] = dict(source=key, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                  status="SELECTED_COMPLETION_UNCONFIRMED", error="",
                                  selected_utc=datetime.now(timezone.utc).isoformat(), finished_utc="",
                                  provider=self.provider, model=self.model, workers=self.workers)
        self.flush()

    def mark(self, path, status, error=""):
        row = self.rows[str(path.relative_to(self.root))]
        row.update(status=status, error=error, finished_utc=datetime.now(timezone.utc).isoformat())
        self.flush()

    def flush(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        with temp.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader(); writer.writerows(self.rows.values())
        temp.replace(self.path)
