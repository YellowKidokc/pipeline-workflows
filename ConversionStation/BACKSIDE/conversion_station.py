"""Simple, source-preserving front door for ConversionStation.

The operator supplies the station INBOX or any file/folder. Sources are read in
place, copied by content hash into BACKSIDE/PRESERVED_ORIGINALS, converted with
the existing conversion engine, and written additively to OUTBOX. Nothing is
moved, deleted, or overwritten.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


STATION = Path(__file__).resolve().parent.parent
ENGINE_SRC = STATION / "conversion_engine" / "src"
sys.path.insert(0, str(ENGINE_SRC))
READABLE_SRC = STATION / "ReadableProseConverter"
sys.path.insert(0, str(READABLE_SRC))

from theophysics_conversion.convert import convert  # noqa: E402
from theophysics_conversion.detect import Format, detect_format  # noqa: E402
from theophysics_conversion.models import ConversionConfig  # noqa: E402
import readable_prose_converter as readable  # noqa: E402


INBOX = STATION / "INBOX"
OUTBOX = STATION / "OUTBOX"
BACKSIDE = STATION / "BACKSIDE"
PRESERVED = BACKSIDE / "PRESERVED_ORIGINALS"
RECEIPTS = BACKSIDE / "RECEIPTS"
LOGS = BACKSIDE / "LOGS"
REVIEW = OUTBOX / "90_NEEDS_REVIEW"

IGNORED_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "backside",
    "outbox",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip(" .")
    return cleaned or "Untitled"


def files_under(source: Path) -> Iterable[Path]:
    if source.is_file():
        yield source
        return
    for root, dirs, files in os.walk(source):
        dirs[:] = [d for d in dirs if d.lower() not in IGNORED_NAMES and not Path(root, d).is_symlink()]
        for name in sorted(files, key=str.casefold):
            if name == ".gitkeep" or name.startswith("~$"):
                continue
            path = Path(root, name)
            if not path.is_symlink():
                yield path


def relative_source(path: Path, source: Path) -> Path:
    if source.is_file():
        return Path(path.name)
    return path.relative_to(source)


def unique_target(requested: Path, source_hash: str) -> Path:
    requested.parent.mkdir(parents=True, exist_ok=True)
    existing_names = {p.name.casefold() for p in requested.parent.iterdir()}
    if requested.name.casefold() not in existing_names:
        return requested
    base = requested.with_name(f"{requested.stem}__{source_hash[:10]}{requested.suffix}")
    candidate = base
    counter = 2
    while candidate.name.casefold() in existing_names:
        candidate = base.with_name(f"{base.stem}__{counter}{base.suffix}")
        counter += 1
    return candidate


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def preserve_source(path: Path, digest: str) -> Path:
    folder = PRESERVED / digest
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / safe_name(path.name)
    if not target.exists():
        # Copy bytes directly so the source is never moved or modified.
        target.write_bytes(path.read_bytes())
    elif sha256(target) != digest:
        raise RuntimeError(f"Preservation collision: {target}")
    return target


def lane_for(fmt: Format) -> str:
    if fmt in {Format.AUDIO, Format.VIDEO}:
        return "02_TRANSCRIPTS"
    if fmt is Format.HTML:
        return "05_HTML"
    return "01_MARKDOWN"


def convert_readable_transcript(path: Path, relative: Path) -> tuple[str, list[str]]:
    """Use the approved sparse-timestamp prose renderer for one transcript."""
    videos = readable.base.read_videos(str(path))
    if len(videos) != 1:
        raise ValueError(
            f"Combined transcript contains {len(videos)} videos; use the channel converter so each video gets its own note."
        )
    video = videos[0]
    if not video.get("segments"):
        raise ValueError("Transcript contains no dialogue segments.")
    punctuate = importlib.util.find_spec("punctuators") is not None
    blocks, _ = readable.prepare_blocks(
        video["segments"],
        interval_seconds=5 * 60,
        use_model=punctuate,
        target_chars=900,
        max_chars=1400,
    )
    if not any(block["paragraphs"] for block in blocks):
        raise ValueError("Transcript cleaning produced no readable paragraphs.")
    lane_names = {"00_PRIORITY", "01_SERIES", "02_GENERAL"}
    channel = path.parent.name
    if channel in lane_names:
        channel = "Imported Transcript"
    raw_title = video.get("title", "") or path.stem
    publish_date = video.get("publish_date") or video.get("upload_date") or video.get("date") or ""
    canonical = readable.youtube_names.parse(raw_title, channel, str(publish_date))
    note = readable.render_note(video, channel, relative.as_posix(), blocks, 5, canonical.h1)
    warnings = [] if punctuate else ["Local punctuation model unavailable; rule-based cleanup was used."]
    return note, warnings


def output_path(path: Path, relative: Path, fmt: Format, digest: str) -> Path:
    lane = OUTBOX / lane_for(fmt)
    parent = Path(*(safe_name(part) for part in relative.parent.parts))
    requested = lane / parent / f"{safe_name(path.stem)}.md"
    return unique_target(requested, digest)


def review_path(path: Path, digest: str) -> Path:
    return unique_target(REVIEW / f"{safe_name(path.name)}__{digest[:10]}.review.txt", digest)


def process_one(path: Path, source: Path, whisper_available: bool) -> dict[str, Any]:
    digest = sha256(path)
    receipt_path = RECEIPTS / f"{digest}.json"
    if receipt_path.exists():
        prior = json.loads(receipt_path.read_text(encoding="utf-8"))
        prior_output = prior.get("output")
        if prior.get("status") == "converted" and prior_output and Path(prior_output).exists():
            return {"source": str(path), "status": "already_converted", "output": prior_output}

    preserved = preserve_source(path, digest)
    fmt = detect_format(path)
    relative = relative_source(path, source)
    config = ConversionConfig(
        export_root=OUTBOX,
        state_root=BACKSIDE / "STATE",
        markitdown_enabled=True,
        whisper_enabled=whisper_available,
        whisper_model_size="base",
    )
    started = now_iso()
    try:
        if fmt is Format.SUBTITLE:
            markdown, warnings = convert_readable_transcript(path, relative)
        else:
            result = convert(path, config=config)
            markdown, warnings = result.markdown, result.warnings
        if not markdown.strip():
            warning_text = "\n".join(warnings) or "The converter returned no Markdown."
            review = review_path(path, digest)
            review.parent.mkdir(parents=True, exist_ok=True)
            review.write_text(
                f"Source: {path}\nDetected format: {fmt.value}\nPreserved copy: {preserved}\n\n{warning_text}\n",
                encoding="utf-8",
            )
            payload = {
                "version": 1,
                "status": "review_required",
                "source": str(path),
                "source_sha256": digest,
                "preserved_original": str(preserved),
                "detected_format": fmt.value,
                "review": str(review),
                "warnings": warnings,
                "started_at": started,
                "finished_at": now_iso(),
            }
            write_json(receipt_path, payload)
            return payload

        target = output_path(path, relative, fmt, digest)
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(markdown, encoding="utf-8")
        payload = {
            "version": 1,
            "status": "converted",
            "source": str(path),
            "source_sha256": digest,
            "preserved_original": str(preserved),
            "detected_format": fmt.value,
            "output": str(target),
            "output_sha256": sha256(target),
            "warnings": warnings,
            "started_at": started,
            "finished_at": now_iso(),
        }
        write_json(receipt_path, payload)
        return payload
    except Exception as exc:  # The batch must continue and report every failed item.
        review = review_path(path, digest)
        review.parent.mkdir(parents=True, exist_ok=True)
        review.write_text(
            f"Source: {path}\nDetected format: {fmt.value}\nPreserved copy: {preserved}\n\nError: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        payload = {
            "version": 1,
            "status": "failed",
            "source": str(path),
            "source_sha256": digest,
            "preserved_original": str(preserved),
            "detected_format": fmt.value,
            "review": str(review),
            "error": f"{type(exc).__name__}: {exc}",
            "started_at": started,
            "finished_at": now_iso(),
        }
        write_json(receipt_path, payload)
        return payload


def prepare() -> None:
    for path in (
        INBOX / "00_PRIORITY",
        INBOX / "01_SERIES",
        INBOX / "02_GENERAL",
        OUTBOX / "01_MARKDOWN",
        OUTBOX / "02_TRANSCRIPTS",
        OUTBOX / "03_AUDIO",
        OUTBOX / "04_VIDEO",
        OUTBOX / "05_HTML",
        REVIEW,
        PRESERVED,
        RECEIPTS,
        LOGS,
        BACKSIDE / "STATE",
        BACKSIDE / "CONFIG",
        BACKSIDE / "ENGINES",
        BACKSIDE / "SYSTEM",
    ):
        path.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert files additively into the ConversionStation OUTBOX.")
    parser.add_argument("source", nargs="?", default=str(INBOX))
    args = parser.parse_args()
    prepare()

    raw = args.source.strip().strip('"')
    source = Path(raw)
    if not source.is_absolute():
        source = (STATION / source).resolve()
    if not source.exists():
        print(f"Source not found: {source}")
        return 2

    whisper_available = importlib.util.find_spec("whisper") is not None
    candidates = list(files_under(source))
    if not candidates:
        print(f"No files found in: {source}")
        return 0

    print(f"ConversionStation: {len(candidates)} file(s)")
    print(f"Source: {source}")
    print(f"Audio/video transcription: {'ready' if whisper_available else 'not installed; routes to review'}")
    results = []
    for index, path in enumerate(candidates, 1):
        result = process_one(path, source, whisper_available)
        results.append(result)
        print(f"[{index}/{len(candidates)}] {path.name} -> {result['status']}")

    counts: dict[str, int] = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    run_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_receipt = LOGS / f"run-{run_stamp}.json"
    write_json(
        run_receipt,
        {
            "version": 1,
            "source": str(source),
            "counts": counts,
            "whisper_available": whisper_available,
            "results": results,
            "finished_at": now_iso(),
        },
    )
    print(f"Receipt: {run_receipt}")
    print(f"Summary: {json.dumps(counts, sort_keys=True)}")
    return 1 if counts.get("failed") or counts.get("review_required") else 0


if __name__ == "__main__":
    raise SystemExit(main())
