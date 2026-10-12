"""Parsing and paragraph functions reused from the existing transcript_polish.py.
Unused CLI and duplicate output generators are omitted from this portable package.
"""

import re
import html

GAP_SECONDS = 2.0

MAX_PARA_CHARS = 480

SENTENCE_BREAK_CHARS = 220

TS_SRT = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})")

TS_LINE_MD = re.compile(r"^\[(\d{1,2}):(\d{2})(?::(\d{2}))?\]\s*(.*)$")

MD_SECTION = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.M)

MD_META = re.compile(r"^\*\*(.+?):\*\*\s*(.+?)\s*$", re.M)

def stamp_to_seconds(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms or 0) / 1000.0

def parse_timestamp_line(line):
    """Parse '00:00:00,080 --> 00:00:02,240' -> (start_s, end_s) or None."""
    m = re.match(r"\s*(\S+)\s*-->\s*(\S+)", line)
    if not m:
        return None
    def one(tok):
        t = TS_SRT.fullmatch(tok)
        if t:
            return stamp_to_seconds(*t.groups())
        t = re.fullmatch(r"(\d{1,2}):(\d{2})[,.](\d{3})", tok)
        if t:  # mm:ss,mmm
            m_, s_, ms_ = t.groups()
            return int(m_) * 60 + int(s_) + int(ms_) / 1000.0
        return None
    start, end = one(m.group(1)), one(m.group(2))
    if start is None or end is None:
        return None
    return start, end

def parse_srt(path):
    """SRT/VTT -> list of segments {start, end, text}."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        raw = f.read()
    if raw.strip().startswith("WEBVTT"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else ""
    segments = []
    for block in re.split(r"\n\s*\n", raw):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        ts = None
        text_lines = []
        for index, line in enumerate(lines):
            ts = parse_timestamp_line(line)
            if ts is not None:
                # Everything before the timestamp is a cue ID/header; numeric
                # dialogue after it is real content and must not be discarded.
                text_lines = lines[index+1:]
                break
        if ts is None or not text_lines:
            continue
        text = re.sub(r"\s+", " ", " ".join(text_lines)).strip()
        text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)  # strip <i> etc.
        text = re.sub(r"<\d{1,2}:\d{2}(?::\d{2})?\.\d{3}>", "", text)
        text = html.unescape(text)
        if text:
            segments.append({"start": ts[0], "end": ts[1], "text": text})
    return segments

def parse_md_body(body):
    """Transcript body from a .md -> segments. Timestamped lines become real
    segments; flat text becomes one segment per sentence-ish chunk."""
    segs = []
    for line in body.splitlines():
        m = TS_LINE_MD.match(line.strip())
        if m:
            h, mnt, s, text = m.groups()
            start = (int(h) * 3600 + int(mnt) * 60 + int(s)) if s else (int(h) * 60 + int(mnt))
            if text.strip():
                segs.append({"start": float(start), "end": None, "text": text.strip()})
        elif line.strip():
            # flat prose: split on sentence ends so paragraphing still works
            for chunk in re.split(r"(?<=[.!?])\s+", line.strip()):
                if chunk:
                    segs.append({"start": None, "end": None, "text": chunk})
    return segs

def split_combined_md(raw):
    """Combined channel/playlist .md -> list of {title, meta, body}."""
    parts = MD_SECTION.split(raw)
    # parts: [header, num, title, body, num, title, body, ...]
    videos = []
    for i in range(1, len(parts) - 2, 3):
        num, title, body = parts[i], parts[i + 1], parts[i + 2]
        meta = dict(MD_META.findall(body))
        tmatch = re.search(r"### Transcript\s*\n(.*?)(?:\n---\s*?$|\Z)",
                           body, re.S | re.M)
        videos.append({
            "title": title.strip(),
            "video_id": meta.get("Video ID", "").strip("` "),
            "url": meta.get("URL", ""),
            "language": meta.get("Transcript Language", ""),
            "body": tmatch.group(1).strip() if tmatch else "",
        })
    return videos

def parse_single_md(raw):
    """Single-video .md -> one {title, meta, body}."""
    title_m = re.search(r"^#\s+(.+)$", raw, re.M)
    meta = dict(MD_META.findall(raw))
    tmatch = re.search(r"^### Transcript[^\S\n]*\n(.+?)\s*\Z", raw, re.S | re.M)
    return [{
        "title": title_m.group(1).strip() if title_m else "untitled",
        "video_id": meta.get("Video ID", "").strip("` "),
        "url": meta.get("URL", ""),
        "language": meta.get("Transcript Language", ""),
        "body": tmatch.group(1).strip() if tmatch else "",
    }]

def is_speaker_change(text):
    return text.lstrip().startswith(">>")

def clean_text(text, keep_markers):
    t = re.sub(r"\s+", " ", text).strip()
    if not keep_markers:
        t = re.sub(r"^>>\s*", "", t)
    return t

def build_paragraphs(segments):
    """Merge caption segments into paragraphs.
    Breaks on: speaker change (>>), pause > GAP_SECONDS, sentence end after
    SENTENCE_BREAK_CHARS, or paragraph reaching MAX_PARA_CHARS.
    Returns list of {start, end, text}."""
    paras, cur, cur_start, cur_end = [], [], None, None
    for seg in segments:
        text = seg["text"]
        gap = (seg["start"] - cur_end) if (cur and seg["start"] is not None and cur_end is not None) else 0.0
        hard_break = (
            cur
            and (is_speaker_change(text)
                 or gap > GAP_SECONDS
                 or len(" ".join(cur)) >= MAX_PARA_CHARS
                 or (len(" ".join(cur)) >= SENTENCE_BREAK_CHARS and cur[-1].rstrip().endswith((".", "!", "?"))))
        )
        if hard_break:
            paras.append({"start": cur_start, "end": cur_end,
                          "text": " ".join(cur)})
            cur, cur_start = [], None
        cleaned = clean_text(text, keep_markers=False)
        if cleaned:
            cur.append(cleaned)
            if cur_start is None and seg["start"] is not None:
                cur_start = seg["start"]
            if seg["end"] is not None:
                cur_end = seg["end"]
    if cur:
        paras.append({"start": cur_start, "end": cur_end, "text": " ".join(cur)})
    return paras

def fmt_stamp(seconds):
    if seconds is None:
        return "--:--"
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
