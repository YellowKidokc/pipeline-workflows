"""Station 3: lossless text cleanup and normalization."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from ..station_base import Manifest, StationBase, StationVerdict


class LosslessFormatterStation(StationBase):
    """Clean STT artifacts and normalize markdown without semantic loss."""

    def __init__(self, input_dir: str, output_dir: str, **kwargs):
        super().__init__("lossless-formatter", input_dir, output_dir, file_extensions=[".md", ".txt"], **kwargs)

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        original = text
        text = text.replace("\r\n", "\n")
        text = re.sub(r"\b(um+|uh+)\b", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(you know|like,? basically|sort of)\b", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"^[ \t]+", "", text, flags=re.MULTILINE)
        title = next((ln.strip("# ") for ln in text.splitlines() if ln.strip()), file_path.stem)
        sidecar = file_path.with_suffix(file_path.suffix + ".fap.json")
        meta = {}
        if sidecar.exists():
            meta = json.loads(sidecar.read_text(encoding="utf-8"))
        frontmatter = (
            f"---\ntitle: \"{title}\"\ndate: {datetime.utcnow().date().isoformat()}\n"
            f"word_count: {len(text.split())}\nsource_file: {file_path.name}\nclassification: {json.dumps(meta)}\n---\n\n"
        )
        cleaned = frontmatter + text.strip() + "\n"
        out_path = self.output_dir / file_path.with_suffix(".md").name
        out_path.write_text(cleaned, encoding="utf-8")
        delta = abs(len(original) - len(text)) / max(len(original), 1)
        score = max(0.2, 1.0 - min(0.7, delta))
        if score >= self.threshold_pass:
            return StationVerdict.PASS, score, "Lossless formatting complete"
        if score <= self.threshold_fail:
            return StationVerdict.REVIEW, score, "Heavy cleanup required"
        return StationVerdict.REVIEW, score, "Moderate cleanup required"
