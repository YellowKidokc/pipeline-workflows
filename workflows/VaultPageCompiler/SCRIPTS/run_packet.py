"""VaultPageCompiler runner — drives lossless cleanup, framework tagging, and wiki compile."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engines.pipeline.knowledge_graph import KnowledgeGraph
from engines.pipeline.station_base import Manifest
from engines.pipeline.stations.framework_classifier import FrameworkClassifierStation
from engines.pipeline.stations.lossless_formatter import LosslessFormatterStation
from engines.pipeline.stations.wiki_compiler import WikiCompilerStation


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED = {".md", ".txt"}


def ensure_dirs() -> None:
    for name in ["INPUT", "OUTPUT", "REVIEW", "ARCHIVE", "ERROR", "CONFIG", "PROMPTS", "SCRIPTS", "LOGS"]:
        (ROOT / name).mkdir(exist_ok=True)


def run(mode: str = "stage") -> list[dict]:
    ensure_dirs()
    inputs = [p for p in (ROOT / "INPUT").iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED]
    out = ROOT / "OUTPUT"
    queue = ROOT / "_queue"

    lossless = LosslessFormatterStation(str(ROOT / "INPUT"), str(out / "lossless"))
    framework = FrameworkClassifierStation(str(out / "lossless"), str(out / "framework"))
    wiki = WikiCompilerStation(str(out / "framework"), str(out / "wiki"), queue_dir=str(queue))

    results: list[dict] = []
    for fp in inputs:
        manifest = Manifest(
            file_path=str(fp),
            file_hash=Manifest.compute_hash(str(fp)),
            pipeline_name="vault-page-compiler",
            current_station="lossless",
        )
        v_loss = lossless.process(fp, manifest)
        manifest.record_station(lossless.name, v_loss[0], v_loss[1], v_loss[2])
        cleaned = lossless.output_dir / f"{fp.stem}.md"

        record: dict = {"file": fp.name, "lossless": v_loss[1]}

        if mode == "pipeline" and cleaned.exists():
            v_fw = framework.process(cleaned, manifest)
            manifest.record_station(framework.name, v_fw[0], v_fw[1], v_fw[2])
            record["framework"] = v_fw[1]

            v_wiki = wiki.process(cleaned, manifest)
            manifest.record_station(wiki.name, v_wiki[0], v_wiki[1], v_wiki[2])
            record["wiki_verdict"] = v_wiki[0].value

        results.append(record)

    kg = KnowledgeGraph()
    kg.build_from_sidecars(out)
    kg.export_graph_json(out / "knowledge_graph.json")

    logs = ROOT / "LOGS"
    (logs / "last_run.log").write_text(
        f"mode={mode}\ninputs={len(inputs)}\nprocessed={len(results)}\n",
        encoding="utf-8",
    )
    (logs / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"VaultPageCompiler: {mode} run complete. {len(results)} file(s) processed.")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pipeline", "stage"], default="stage")
    args = parser.parse_args()
    run(args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
