"""Timed transcripts -> canonical transcript markdown.

Reads SRT, VTT, SBV, transcript JSON (YouTube json3, Whisper `segments`,
youtube-transcript-api lists) and text copied from YouTube's transcript panel
("1:011 minute, 1 second..."). Writes the layout the YouTube argument pipeline
(yt-transcript-downloader/pipeline-workflows/deepseek-home) reads:

    # Title
    **Video ID:** `abc123`   (when known)
    ---
    ## Transcript
    [mm:ss] text

Rolling auto-caption repeats are removed; the words themselves are not edited.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from ..models import ConvertResult

PANEL_TIME = re.compile(r"^((?:\d+:)?\d{1,2}:\d{2})\d+ (?:hours?|minutes?|seconds?)(?:, \d+ (?:minutes?|seconds?))*")
CUE_TIME = re.compile(r"(\d+:)?(\d{1,2}):(\d{2})[.,](\d{1,3})")
VIDEO_ID = re.compile(r"(?:\[|[-_ ]|^)([A-Za-z0-9_-]{11})(?:\]|$)")


def looks_like_panel(text: str) -> bool:
    """True for text pasted from YouTube's 'Show transcript' panel."""
    lines = [l for l in text.splitlines()[:40] if l.strip()]
    return sum(bool(PANEL_TIME.match(l)) for l in lines) >= 3


def _secs(m: re.Match) -> float:
    h = int(m.group(1)[:-1]) if m.group(1) else 0
    return h * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4).ljust(3, "0")) / 1000


def _clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)            # VTT inline tags <c>, <00:00:01.000>
    text = re.sub(r"\{\\[^}]*\}", "", text)          # SSA-style tags
    return re.sub(r"\s+", " ", text.replace("&nbsp;", " ").replace("&amp;", "&")).strip()


def parse_cues(text: str) -> list[tuple[float, str]]:
    """SRT / VTT / SBV: blocks with a start time and one or more text lines."""
    out = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        lines = [l for l in block.split("\n") if l.strip()]
        for i, line in enumerate(lines):
            if "-->" in line or re.match(r"^\d+:\d{2}:\d{2}\.\d{3},\d+:\d{2}:\d{2}\.\d{3}$", line.strip()):
                m = CUE_TIME.search(line)
                if m:
                    body = _clean(" ".join(lines[i + 1:]))
                    if body:
                        out.append((_secs(m), body))
                break
    return out


def parse_json(text: str) -> list[tuple[float, str]]:
    data = json.loads(text)
    if isinstance(data, dict) and "events" in data:           # YouTube json3
        return [(e.get("tStartMs", 0) / 1000, _clean("".join(s.get("utf8", "") for s in e.get("segs", []))))
                for e in data["events"] if e.get("segs")]
    if isinstance(data, dict) and "segments" in data:         # Whisper
        return [(float(s.get("start", 0)), _clean(s.get("text", ""))) for s in data["segments"]]
    if isinstance(data, list):                                # youtube-transcript-api
        return [(float(s.get("start", s.get("offset", 0))), _clean(s.get("text", ""))) for s in data
                if isinstance(s, dict)]
    raise ValueError("JSON is not a recognized transcript shape (json3, Whisper segments, or a list of {start, text})")


def parse_panel(text: str) -> tuple[list[tuple[float, str]], list[tuple[float, str]]]:
    """Returns (segments, chapters) from the YouTube transcript panel paste.
    A chapter is stamped with the time of the first line after its heading."""
    segs, chapters, pending = [], [], []
    for line in text.splitlines():
        m = PANEL_TIME.match(line)
        if m:
            parts = [int(p) for p in m.group(1).split(":")]
            t = sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
            body = _clean(line[m.end():])
            if body:
                chapters += [(t, c) for c in pending]
                pending = []
                segs.append((t, body))
        elif re.match(r"^Chapter \d+:", line.strip()):
            pending.append(line.strip())
    return segs, chapters


def dedupe(segs: list[tuple[float, str]]) -> list[tuple[float, str]]:
    """Drop rolling-caption repeats: exact repeats and cues that only restate the previous one."""
    out: list[tuple[float, str]] = []
    for t, s in segs:
        if not s or s in ("[Music]", "[Applause]"):
            continue
        if out:
            prev = out[-1][1]
            if s == prev or prev.endswith(s):
                continue
            if s.startswith(prev):                     # cue repeats previous text then adds words
                s = s[len(prev):].strip()
                if not s:
                    continue
        out.append((t, s))
    return out


def stamp(t: float) -> str:
    t = int(t)
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def title_and_id(path: Path, text: str) -> tuple[str, str]:
    stem = re.sub(r"\.(en|en-US|en-orig|[a-z]{2})$", "", path.stem)   # yt-dlp language suffix
    m = VIDEO_ID.search(stem)
    vid = m.group(1) if m and re.search(r"[A-Z0-9_-]", m.group(1)) and not m.group(1).isalpha() else ""
    title = stem.replace(f"[{vid}]", "").strip(" -_") if vid else stem
    head = re.search(r"\*\*Video ID:\*\*\s*`([^`]+)`", text)
    return title or path.stem, (head.group(1) if head else vid)


def convert_transcript(path: Path, kind: str) -> ConvertResult:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    chapters: list[tuple[float, str]] = []
    if kind == "JSON":
        segs = parse_json(raw)
    elif kind == "PANEL":
        segs, chapters = parse_panel(raw)
    else:
        segs = parse_cues(raw)
    segs = dedupe(segs)
    title, vid = title_and_id(path, raw)
    if not segs:
        return ConvertResult(markdown="", metadata={"source_format": kind},
                             warnings=[f"No timed transcript lines found in {path.name}"])

    head = [f"# {title}", ""]
    if vid:
        head += [f"**Video ID:** `{vid}`", f"**URL:** https://www.youtube.com/watch?v={vid}"]
    head += [f"**Retrieved via:** conversion-station ({kind.lower()})",
             f"**Captured:** {datetime.now():%Y-%m-%d %H:%M}", "", "---", "", "## Transcript", ""]
    body, ci = [], 0
    for t, s in segs:
        while ci < len(chapters) and chapters[ci][0] <= t:
            body += ["", f"### {chapters[ci][1]}", ""]
            ci += 1
        body.append(f"[{stamp(t)}] {s}")
    words = sum(len(s.split()) for _, s in segs)
    warnings = [] if vid else ["No YouTube video ID found (name the file 'Title [VIDEOID].srt' to add links)."]
    return ConvertResult(markdown="\n".join(head + body) + "\n",
                         metadata={"source_format": kind, "segments": len(segs), "words": words,
                                   "video_id": vid, "title": title},
                         warnings=warnings)
