"""Station 5: async paper grading via LLMHub."""
from __future__ import annotations

import json
from pathlib import Path

from ..llm_hub import LLMHub
from ..station_base import Manifest, StationBase, StationVerdict


class PaperGraderStation(StationBase):
    """Submit grading jobs, then collect completed results."""

    def __init__(self, input_dir: str, output_dir: str, queue_dir: str | None = None, **kwargs):
        super().__init__("paper-grader", input_dir, output_dir, file_extensions=[".md", ".txt"], **kwargs)
        self.hub = LLMHub(queue_dir=queue_dir or "_queue")

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        grade_meta = file_path.with_suffix(file_path.suffix + ".grade.json")
        if not grade_meta.exists():
            text = file_path.read_text(encoding="utf-8", errors="replace")
            job_id = self.hub.submit("paper-grader", str(file_path), "grade_paper", backend="ollama", priority="standard", input_text=text[:4000])
            grade_meta.write_text(json.dumps({"job_id": job_id}, indent=2), encoding="utf-8")
            return StationVerdict.HOLD, 0.0, f"Submitted grading job {job_id}"

        job_id = json.loads(grade_meta.read_text(encoding="utf-8")).get("job_id")
        completed = Path(self.hub.queue_dir) / "completed" / f"{job_id}.json"
        if not completed.exists():
            return StationVerdict.HOLD, 0.0, f"Awaiting completion for {job_id}"
        result = json.loads(completed.read_text(encoding="utf-8"))
        payload = result.get("result_json") or {}
        score = float(payload.get("overall_score", payload.get("score", 0.5)))
        if score >= self.threshold_pass:
            verdict = StationVerdict.PASS
        elif score <= self.threshold_fail:
            verdict = StationVerdict.FAIL
        else:
            verdict = StationVerdict.REVIEW
        return verdict, score, "Collected grader result"
