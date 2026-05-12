"""Station 4: chunk and embed text, plus duplicate detection."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

from ..station_base import Manifest, SignalType, StationBase, StationVerdict


class VectorizerStation(StationBase):
    """Build simple paragraph chunks and vectors sidecars."""

    def __init__(self, input_dir: str, output_dir: str, **kwargs):
        super().__init__("vectorizer", input_dir, output_dir, file_extensions=[".md", ".txt"], **kwargs)

    def _embed(self, text: str) -> list[float]:
        # deterministic fallback embedding (no heavyweight deps)
        vals = [0.0] * 8
        for idx, token in enumerate(text.split()[:256]):
            vals[idx % 8] += float((sum(ord(c) for c in token) % 101) / 100.0)
        norm = math.sqrt(sum(v * v for v in vals)) or 1.0
        return [v / norm for v in vals]

    def _cos(self, a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
        vectors = [self._embed(chunk) for chunk in chunks]
        chunk_meta = [{"position": i, "heading_context": ""} for i, _ in enumerate(chunks)]
        sidecar = file_path.with_suffix(file_path.suffix + ".vectors.json")
        sidecar.write_text(json.dumps({"chunks": chunks, "vectors": vectors, "metadata": chunk_meta}, indent=2), encoding="utf-8")

        index_path = self.output_dir / "_index.json"
        index = json.loads(index_path.read_text()) if index_path.exists() else {"documents": []}
        doc_vec = vectors[0] if vectors else [0.0] * 8
        for prior in index.get("documents", []):
            if self._cos(doc_vec, prior.get("embedding", [0.0] * 8)) > 0.92:
                self.emit_signal(SignalType.DUPLICATE, f"Near duplicate of {prior.get('file')}")
        index.setdefault("documents", []).append({"file": file_path.name, "embedding": doc_vec})
        index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
        (self.output_dir / file_path.name).write_text(text, encoding="utf-8")
        score = 0.4 if not chunks else min(1.0, 0.6 + min(0.4, len(chunks) / 12))
        return (StationVerdict.PASS if score >= self.threshold_pass else StationVerdict.REVIEW, score, "Vectorization complete")
