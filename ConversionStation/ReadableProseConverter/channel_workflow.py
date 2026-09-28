#!/usr/bin/env python3
"""Initialize a selection-driven YouTube channel conversion workspace.

This stage is entirely local: it inventories root transcript Markdown files,
creates analysis/prompt/output folders, and writes an Obsidian checkbox sheet.
Only checked records are eligible for later naming, analysis, or conversion.
"""
from __future__ import annotations

import argparse
import csv
import re
from datetime import date
from pathlib import Path


META = re.compile(r"^\*\*(.+?):\*\*\s*`?(.+?)`?\s*$", re.M)
STAMP = re.compile(r"^\[\d{1,2}:\d{2}(?::\d{2})?\]\s*", re.M)
SOURCE_MARKER = re.compile(r"<!--\s*source:\s*(.+?)\s*-->")


def read_record(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    meta = {k.casefold(): v.strip().strip("`") for k, v in META.findall(text[:4000])}
    h1 = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    body = text.split("## Transcript", 1)[-1] if "## Transcript" in text else ""
    placeholder = "no transcript available" in body.casefold() or meta.get("retrieved via", "").casefold() == "failed"
    dialogue = STAMP.sub("", body)
    words = len(re.findall(r"\b[\w’'-]+\b", dialogue, re.UNICODE)) if not placeholder else 0
    return {
        "title": h1.group(1).strip() if h1 else path.stem,
        "video_id": meta.get("video id", ""),
        "url": meta.get("url", ""),
        "source": path.name,
        "status": "unavailable" if placeholder else "ready",
        "words": words,
    }


def initialize(channel_dir: Path) -> None:
    channel_dir = channel_dir.resolve()
    if not channel_dir.is_dir():
        raise SystemExit(f"Channel folder not found: {channel_dir}")

    channel = channel_dir.name
    analysis = channel_dir / "Channel Analysis"
    prompts = channel_dir / "Prompts"
    converted = channel_dir / "Converted to Markdown"
    for folder in (analysis, prompts, converted):
        folder.mkdir(parents=True, exist_ok=True)

    records = [read_record(p) for p in sorted(channel_dir.glob("*.md"), key=lambda p: p.name.casefold())]
    ready = [r for r in records if r["status"] == "ready"]
    unavailable = [r for r in records if r["status"] != "ready"]

    selection = analysis / f"{channel} - 000 Video Selection.md"
    lines = [
        "---",
        "type: youtube_channel_selection",
        f'channel: "{channel}"',
        f"generated: {date.today().isoformat()}",
        f"videos_found: {len(records)}",
        f"ready_transcripts: {len(ready)}",
        f"unavailable_transcripts: {len(unavailable)}",
        "---",
        "",
        f"# {channel} — Video Selection",
        "",
        "Mark a video with `[x]` to authorize its later naming, analysis, and readable-Markdown conversion.",
        "Unchecked videos remain untouched. The hidden source marker is used by the local workflow script.",
        "",
        "## Ready",
        "",
    ]
    for r in ready:
        link = f" — [YouTube]({r['url']})" if r["url"] else ""
        lines.append(f"- [ ] **{r['title']}** — {r['words']:,} words{link} <!-- source: {r['source']} -->")
    if unavailable:
        lines += ["", "## Transcript unavailable", ""]
        for r in unavailable:
            link = f" — [YouTube]({r['url']})" if r["url"] else ""
            lines.append(f"- [ ] **{r['title']}** — unavailable{link} <!-- source: {r['source']} -->")
    selection.write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = analysis / f"{channel} - 000 Channel Summary.md"
    summary.write_text(
        "\n".join([
            f"# {channel} — Channel Summary", "",
            "> Baseline inventory only. Narrative channel analysis has not yet been generated.", "",
            f"- Root video records: {len(records)}",
            f"- Ready transcripts: {len(ready)}",
            f"- Transcript unavailable: {len(unavailable)}",
            f"- Ready transcript words: {sum(int(r['words']) for r in ready):,}",
            f"- Selection control: [[{selection.stem}]]", "",
            "Only videos checked in the selection control proceed to naming, analysis, and conversion.", "",
        ]), encoding="utf-8",
    )

    scorecard = analysis / f"{channel} - 000 Scorecard.csv"
    with scorecard.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["selected", "status", "words", "title", "video_id", "source", "url"])
        writer.writeheader()
        for record in records:
            writer.writerow({"selected": "", **record})

    prompt_readme = prompts / "README.md"
    if not prompt_readme.exists():
        prompt_readme.write_text(
            f"# {channel} — Prompts\n\nReusable channel-summary and selected-transcript analysis prompts belong here.\n"
            "The checkbox sheet in `Channel Analysis` is the authority for which transcripts may proceed.\n",
            encoding="utf-8",
        )

    print(f"Initialized {channel}")
    print(f"  {len(records)} records: {len(ready)} ready, {len(unavailable)} unavailable")
    print(f"  Selection: {selection}")
    print(f"  Summary:   {summary}")
    print(f"  Scorecard: {scorecard}")
    print(f"  Output:    {converted}")


def selected(selection_file: Path) -> None:
    text = selection_file.read_text(encoding="utf-8")
    selected_sources = []
    for line in text.splitlines():
        if not re.match(r"^- \[[xX]\]", line):
            continue
        marker = SOURCE_MARKER.search(line)
        if marker:
            selected_sources.append(marker.group(1).strip())
    for source in selected_sources:
        print(source)
    print(f"Selected: {len(selected_sources)}", file=__import__("sys").stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("initialize")
    init.add_argument("channel_dir", type=Path)
    show = sub.add_parser("selected")
    show.add_argument("selection_file", type=Path)
    args = parser.parse_args()
    if args.command == "initialize":
        initialize(args.channel_dir)
    else:
        selected(args.selection_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
