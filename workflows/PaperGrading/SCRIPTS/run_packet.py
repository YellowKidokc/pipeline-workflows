"""PaperGrading packet runner — classify → framework-tag → grade → rubric."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engines.pipeline.rubric_exporter import RubricExporter
from engines.pipeline.station_base import Manifest
from engines.pipeline.stations.classifier import ClassifierStation
from engines.pipeline.stations.framework_classifier import FrameworkClassifierStation
from engines.pipeline.stations.paper_grader import PaperGraderStation


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED = {".md", ".txt"}


def ensure_dirs() -> None:
    for name in ["INPUT", "OUTPUT", "REVIEW", "ARCHIVE", "ERROR", "CONFIG", "PROMPTS", "SCRIPTS", "LOGS"]:
        (ROOT / name).mkdir(exist_ok=True)


def run(mode: str = "stage") -> list[dict]:
    ensure_dirs()
    inputs = [p for p in (ROOT / "INPUT").iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED]
    out = ROOT / "OUTPUT"
    logs = ROOT / "LOGS"

    classifier = ClassifierStation(str(ROOT / "INPUT"), str(out / "classified"))
    framework = FrameworkClassifierStation(str(out / "classified"), str(out / "framework"))
    grader = PaperGraderStation(str(out / "framework"), str(out / "graded"), queue_dir=str(ROOT / "_queue"))
    exporter = RubricExporter(out / "rubric")

    results: list[dict] = []
    for fp in inputs:
        manifest = Manifest(
            file_path=str(fp),
            file_hash=Manifest.compute_hash(str(fp)),
            pipeline_name="paper-grading",
            current_station="classifier",
        )
        v_cls = classifier.process(fp, manifest)
        manifest.record_station(classifier.name, v_cls[0], v_cls[1], v_cls[2])

        record: dict = {"file": fp.name, "classifier": v_cls[1]}

        if mode == "pipeline":
            v_fw = framework.process(fp, manifest)
            manifest.record_station(framework.name, v_fw[0], v_fw[1], v_fw[2])
            record["framework"] = v_fw[1]

            v_grade = grader.process(fp, manifest)
            manifest.record_station(grader.name, v_grade[0], v_grade[1], v_grade[2])
            record["grade_status"] = v_grade[0].value
            record["grade_score"] = v_grade[1]

            excel_path, html_path = exporter.export(fp.parent, fp.stem)
            record["rubric_excel"] = str(excel_path)
            record["rubric_html"] = str(html_path)

        results.append(record)

    (logs / "last_run.log").write_text(
        f"mode={mode}\ninputs={len(inputs)}\nprocessed={len(results)}\n",
        encoding="utf-8",
    )
    (logs / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"PaperGrading: {mode} run complete. {len(results)} file(s) processed.")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pipeline", "stage"], default="stage")
    args = parser.parse_args()
    run(args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
