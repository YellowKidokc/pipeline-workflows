"""Station 6: claim extraction and axiom mapping via LLMHub."""
from __future__ import annotations

import json
from pathlib import Path

from ..llm_hub import LLMHub
from ..station_base import Manifest, SignalType, StationBase, StationVerdict


class AxiomMapperStation(StationBase):
    """Map extracted claims to axiom references and detect gaps."""

    def __init__(self, input_dir: str, output_dir: str, queue_dir: str | None = None, **kwargs):
        super().__init__("axiom-mapper", input_dir, output_dir, file_extensions=[".md", ".txt"], **kwargs)
        self.hub = LLMHub(queue_dir=queue_dir or "_queue")

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        side = file_path.with_suffix(file_path.suffix + ".axioms.json")
        if not side.exists():
            job_id = self.hub.submit("axiom-mapper", str(file_path), "extract_claims", backend="claude_api", priority="batch", input_text=file_path.read_text(encoding="utf-8")[:6000])
            side.write_text(json.dumps({"job_id": job_id}, indent=2), encoding="utf-8")
            return StationVerdict.HOLD, 0.0, f"Submitted mapping job {job_id}"

        meta = json.loads(side.read_text(encoding="utf-8"))
        completed = Path(self.hub.queue_dir) / "completed" / f"{meta.get('job_id')}.json"
        if not completed.exists():
            return StationVerdict.HOLD, 0.0, "Awaiting axiom extraction"
        result = json.loads(completed.read_text(encoding="utf-8"))
        result_json = result.get("result_json") or {}
        claims = result_json.get("claims", [])
        mappings = result_json.get("mappings", [])
        gaps = result_json.get("gaps", [])
        contradictions = result_json.get("contradictions", [])
        for gap in gaps:
            self.emit_signal(SignalType.GAP, f"Uncovered axiom: {gap}")
        for contradiction in contradictions:
            self.emit_signal(SignalType.QUALITY, f"Axiom contradiction: {contradiction}")
        side.write_text(json.dumps({"claims": claims, "mappings": mappings, "gaps": gaps, "contradictions": contradictions}, indent=2), encoding="utf-8")
        score = float(result_json.get("confidence", 0.6))
        return (StationVerdict.PASS if score >= self.threshold_pass else StationVerdict.REVIEW, score, "Mapped claims to axioms")
