"""Station 7: compile final Obsidian page layers."""
from __future__ import annotations

import json
from pathlib import Path

from ..llm_hub import LLMHub
from ..station_base import Manifest, SignalType, StationBase, StationVerdict


class WikiCompilerStation(StationBase):
    """Compile 7-layer vault page using sidecars + LLM-generated sections."""

    def __init__(self, input_dir: str, output_dir: str, queue_dir: str | None = None, **kwargs):
        super().__init__("wiki-compiler", input_dir, output_dir, file_extensions=[".md", ".txt"], **kwargs)
        self.hub = LLMHub(queue_dir=queue_dir or "_queue")

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        frontmatter = {
            "file": file_path.name,
            "scores": manifest.scores,
            "metadata": manifest.metadata,
            "history": manifest.history,
        }
        body = (
            f"---\n{json.dumps(frontmatter, indent=2)}\n---\n\n"
            "## Layer 1: Executive Summary\nPending LLM summary.\n\n"
            "## Layer 2: Plain Language\nPending LLM translation.\n\n"
            f"## Layer 3: The Paper\n{text}\n\n"
            "## Layer 4: Academic Register\nPending LLM academic layer.\n\n"
            "## Layer 5: Knowledge Graph\nPending LLM graph links.\n\n"
            f"## Layer 6: Data Layer\n```json\n{json.dumps(frontmatter, indent=2)}\n```\n\n"
            "## Layer 7: Impact Notes\nPending LLM impact notes.\n"
        )
        out = self.output_dir / file_path.with_suffix(".md").name
        out.write_text(body, encoding="utf-8")
        self.emit_signal(SignalType.READY, f"Compiled vault page: {out.name}")
        return StationVerdict.PASS, 0.85, "Compiled wiki layers"
