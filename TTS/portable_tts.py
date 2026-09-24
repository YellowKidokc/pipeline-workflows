"""Small, location-independent Markdown/text to MP3 converter."""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path


SUPPORTED = {".md", ".txt"}
LANES = ("PRIORITY", "SERIES", "GENERAL")


def clean_for_speech(text: str) -> str:
    """Remove noisy Markdown while preserving the readable words."""
    text = text.lstrip("\ufeff")
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"!?\[\[([^]|]+)(?:\|([^]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"(?m)^\s*#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*>\s?", "", text)
    text = re.sub(r"[*_~`]", "", text)
    text = re.sub(r"(?m)^\s*[-+*]\s+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def unique_output(path: Path) -> Path:
    if not path.exists():
        return path
    number = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{number}{path.suffix}")
        if not candidate.exists():
            return candidate
        number += 1


async def convert(source: Path, destination: Path, voice: str, rate: str) -> bool:
    try:
        import edge_tts
    except ImportError:
        print("[ERROR] edge-tts is not installed. Double-click SETUP_OR_FIX.bat.")
        return False

    try:
        raw = source.read_text(encoding="utf-8", errors="replace")
        spoken = clean_for_speech(raw)
        if not spoken:
            print(f"[SKIP] No readable text: {source}")
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        await edge_tts.Communicate(spoken, voice, rate=rate).save(str(destination))
        print(f"[OK] {source.name} -> {destination}")
        return True
    except Exception as exc:
        print(f"[ERROR] {source}: {exc}")
        return False


async def main() -> int:
    parser = argparse.ArgumentParser(description="Portable text/Markdown to MP3")
    parser.add_argument("source", nargs="?", help="Optional .txt/.md file or folder")
    parser.add_argument("--voice", default="en-US-BrianMultilingualNeural")
    parser.add_argument("--rate", default="+6%")
    parser.add_argument("--workers", type=int, default=2, choices=range(1, 6), metavar="1-5")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    inbox = root / "INBOX"
    outbox = root / "OUTBOX"
    inbox.mkdir(exist_ok=True)
    outbox.mkdir(exist_ok=True)
    for lane in LANES:
        (inbox / lane).mkdir(exist_ok=True)

    if args.source:
        selected = Path(args.source).resolve()
        if selected.is_file():
            sources = [selected] if selected.suffix.lower() in SUPPORTED else []
            base = selected.parent
        elif selected.is_dir():
            sources = sorted(p for p in selected.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
            base = selected
        else:
            print(f"[ERROR] Not found: {selected}")
            return 1
    else:
        # The root of INBOX is accepted as GENERAL for easy backward compatibility.
        sources = []
        for lane in LANES:
            sources.extend(sorted(p for p in (inbox / lane).rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED))
        sources.extend(sorted(p for p in inbox.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED))
        base = inbox

    if not sources:
        print(f"[INFO] No .txt or .md files found. Put files in: {inbox}")
        return 0

    print(f"[INFO] Running up to {args.workers} conversions at once.")
    failures = 0
    semaphore = asyncio.Semaphore(args.workers)

    async def run_one(source: Path, output: Path) -> bool:
        async with semaphore:
            return await convert(source, output, args.voice, args.rate)

    # Finish each lane before beginning the next lane. Jobs inside a lane run in parallel.
    if args.source:
        groups = [("SELECTED", sources)]
    else:
        groups = []
        for lane in LANES:
            lane_root = inbox / lane
            groups.append((lane, [p for p in sources if p.is_relative_to(lane_root)]))
        groups.append(("GENERAL (INBOX root)", [p for p in sources if p.parent == inbox]))

    reserved: set[Path] = set()
    for lane_name, lane_sources in groups:
        if not lane_sources:
            continue
        print(f"\n[{lane_name}] {len(lane_sources)} file(s)")
        jobs = []
        for source in lane_sources:
            relative = source.relative_to(base) if source.is_relative_to(base) else Path(source.name)
            candidate = (outbox / relative).with_suffix(".mp3")
            while candidate.exists() or candidate in reserved:
                candidate = unique_output(candidate)
                if candidate in reserved:
                    candidate = candidate.with_name(f"{candidate.stem}_copy{candidate.suffix}")
            reserved.add(candidate)
            jobs.append(run_one(source, candidate))
        results = await asyncio.gather(*jobs)
        failures += sum(not result for result in results)

    print(f"\nFinished: {len(sources) - failures} succeeded, {failures} failed.")
    print(f"Original files were left untouched. MP3 files are in: {outbox}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
