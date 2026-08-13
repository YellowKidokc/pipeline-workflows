"""TTSRender runner — prepares text for narration and queues TTS jobs.

Cleans inputs via the lossless formatter, splits them into ≤2 500-char chunks
so TTS engines can handle them, then submits one queue job per chunk through
the LLMHub (backend=ollama by default but configurable). Emits a manifest of
chunks and queue job ids that an external TTS worker can pick up.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from engines.pipeline.llm_hub import LLMHub
from engines.pipeline.station_base import Manifest
from engines.pipeline.stations.lossless_formatter import LosslessFormatterStation


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED = {".md", ".txt"}
MAX_CHUNK_CHARS = 2500


def ensure_dirs() -> None:
    for name in ["INPUT", "OUTPUT", "REVIEW", "ARCHIVE", "ERROR", "CONFIG", "PROMPTS", "SCRIPTS", "LOGS"]:
        (ROOT / name).mkdir(exist_ok=True)


def chunk_for_tts(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Break on sentence boundaries, never mid-word, keep chunks ≤ max_chars."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) > max_chars and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current = candidate
    if current:
        chunks.append(current.strip())
    return chunks or [text[:max_chars]]


def run(mode: str = "stage", backend: str = "ollama") -> list[dict]:
    ensure_dirs()
    inputs = [p for p in (ROOT / "INPUT").iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED]
    out = ROOT / "OUTPUT"
    queue = ROOT / "_queue"

    lossless = LosslessFormatterStation(str(ROOT / "INPUT"), str(out / "cleaned"))
    hub = LLMHub(queue_dir=str(queue))

    results: list[dict] = []
    for fp in inputs:
        manifest = Manifest(
            file_path=str(fp),
            file_hash=Manifest.compute_hash(str(fp)),
            pipeline_name="tts-render",
            current_station="lossless",
        )
        v_loss = lossless.process(fp, manifest)
        manifest.record_station(lossless.name, v_loss[0], v_loss[1], v_loss[2])

        cleaned = lossless.output_dir / f"{fp.stem}.md"
        text = cleaned.read_text(encoding="utf-8") if cleaned.exists() else fp.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)

        chunks = chunk_for_tts(text)
        job_ids: list[str] = []
        chunk_dir = out / "chunks" / fp.stem
        chunk_dir.mkdir(parents=True, exist_ok=True)
        for i, chunk in enumerate(chunks):
            chunk_path = chunk_dir / f"chunk_{i:03d}.txt"
            chunk_path.write_text(chunk, encoding="utf-8")
            if mode == "pipeline":
                job_id = hub.submit(
                    station_name="tts-render",
                    file_path=str(chunk_path),
                    prompt_name="tts_synthesize",
                    backend=backend,
                    priority="standard",
                    input_text=chunk,
                )
                job_ids.append(job_id)

        record = {
            "source": fp.name,
            "chunks": len(chunks),
            "chunk_dir": str(chunk_dir),
            "job_ids": job_ids,
            "lossless_score": v_loss[1],
        }
        results.append(record)

    logs = ROOT / "LOGS"
    (logs / "last_run.log").write_text(
        f"mode={mode}\nbackend={backend}\ninputs={len(inputs)}\nprocessed={len(results)}\n",
        encoding="utf-8",
    )
    (logs / "tts_manifest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"TTSRender: {mode} run complete. {len(results)} file(s) chunked.")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pipeline", "stage"], default="stage")
    parser.add_argument("--backend", default="ollama")
    args = parser.parse_args()
    run(args.mode, args.backend)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
