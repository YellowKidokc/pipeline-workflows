"""ClipSyncExport runner — captures clipboard-style snippets into vault drops.

Treats every file in INPUT as a clipped fragment, classifies it via the
ClassifierStation, then writes a vault-ready markdown drop with frontmatter
and a manifest entry per clip.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, UTC
from pathlib import Path

from engines.pipeline.station_base import Manifest
from engines.pipeline.stations.classifier import ClassifierStation
from engines.pipeline.stations.lossless_formatter import LosslessFormatterStation


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED = {".md", ".txt", ".html", ".htm"}


def ensure_dirs() -> None:
    for name in ["INPUT", "OUTPUT", "REVIEW", "ARCHIVE", "ERROR", "CONFIG", "PROMPTS", "SCRIPTS", "LOGS"]:
        (ROOT / name).mkdir(exist_ok=True)


def run(mode: str = "stage") -> list[dict]:
    ensure_dirs()
    inputs = [p for p in (ROOT / "INPUT").iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED]
    out = ROOT / "OUTPUT"
    vault_drop = out / "vault_drop"
    vault_drop.mkdir(parents=True, exist_ok=True)

    classifier = ClassifierStation(str(ROOT / "INPUT"), str(out / "classified"))
    lossless = LosslessFormatterStation(str(ROOT / "INPUT"), str(out / "cleaned"))

    manifest_rows: list[dict] = []
    for fp in inputs:
        manifest = Manifest(
            file_path=str(fp),
            file_hash=Manifest.compute_hash(str(fp)),
            pipeline_name="clip-sync",
            current_station="classifier",
        )
        v_cls = classifier.process(fp, manifest)
        manifest.record_station(classifier.name, v_cls[0], v_cls[1], v_cls[2])

        v_loss = lossless.process(fp, manifest)
        manifest.record_station(lossless.name, v_loss[0], v_loss[1], v_loss[2])

        cleaned = lossless.output_dir / f"{fp.stem}.md"
        body = cleaned.read_text(encoding="utf-8") if cleaned.exists() else fp.read_text(encoding="utf-8", errors="replace")
        timestamp = datetime.now(UTC).isoformat()
        drop_name = f"{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{fp.stem}.md"
        drop_path = vault_drop / drop_name
        frontmatter = (
            "---\n"
            f"clip_source: {fp.name}\n"
            f"captured_at: {timestamp}\n"
            f"classification_score: {v_cls[1]}\n"
            f"laws: {manifest.metadata.get('laws', [])}\n"
            "---\n\n"
        )
        drop_path.write_text(frontmatter + body, encoding="utf-8")

        manifest_rows.append(
            {
                "source": fp.name,
                "drop": str(drop_path),
                "classifier_score": v_cls[1],
                "lossless_score": v_loss[1],
                "laws": manifest.metadata.get("laws", []),
                "doc_type": manifest.metadata.get("doc_type", "unknown"),
            }
        )

    logs = ROOT / "LOGS"
    (logs / "last_run.log").write_text(
        f"mode={mode}\ninputs={len(inputs)}\nprocessed={len(manifest_rows)}\n",
        encoding="utf-8",
    )
    (logs / "manifest.json").write_text(json.dumps(manifest_rows, indent=2), encoding="utf-8")
    print(f"ClipSyncExport: {mode} run complete. {len(manifest_rows)} clip(s) processed.")
    return manifest_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pipeline", "stage"], default="stage")
    args = parser.parse_args()
    run(args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
