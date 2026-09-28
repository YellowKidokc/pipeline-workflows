"""Portable YouTube transcript naming rules for ReadableProseConverter."""
from __future__ import annotations

import re
from dataclasses import dataclass

LABELS = {
    "chapter": "Ch", "chap": "Ch", "ch": "Ch", "episode": "Ep", "ep": "Ep",
    "part": "Pt", "pt": "Pt", "lecture": "Lec", "lec": "Lec",
    "session": "Session", "lesson": "Lesson", "#": "Ep",
}
NUMBER = re.compile(
    r"(?<![\w])(chapter|chap|ch|episode|ep|part|pt|lecture|lec|session|lesson)\.?\s*#?\s*(\d{1,4})(?!\d)"
    r"|^#\s*(\d{1,4})(?!\d)", re.I,
)
SPLIT = re.compile(r"\s+[-–—|]\s+")
BAD = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


@dataclass
class Name:
    title: str
    label: str = ""
    number: int | None = None
    date: str = ""

    @property
    def lead(self) -> str:
        return f"{self.label} {self.number}" if self.number is not None else self.date

    @property
    def file_stem(self) -> str:
        lead = f"{self.label} {self.number:03d}" if self.number is not None else self.date
        stem = f"{lead} - {self.title}" if lead and self.title else (lead or self.title)
        return safe(stem)

    @property
    def h1(self) -> str:
        return f"{self.lead} · {self.title}" if self.lead and self.title else (self.lead or self.title)


def _plain(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def safe(stem: str, limit: int = 120) -> str:
    stem = BAD.sub(" ", stem)
    stem = re.sub(r"\s+", " ", stem).strip().rstrip(". ")
    return stem[:limit].rstrip(". ") or "untitled"


def parse(raw_title: str, channel: str = "", date: str = "") -> Name:
    title = re.sub(r"\s+", " ", raw_title or "").strip()
    segments = [s.strip() for s in SPLIT.split(title) if s.strip()]
    own = _plain(channel)
    if own:
        kept = [s for s in segments if _plain(s) != own]
        segments = kept or segments
    label, number = "", None
    for i, segment in enumerate(segments):
        match = NUMBER.search(segment)
        if match:
            word = (match.group(1) or "#").lower()
            label, number = LABELS.get(word, "Ep"), int(match.group(2) or match.group(3))
            rest = (segment[:match.start()] + segment[match.end():]).strip(" -–—|:,. ")
            if rest:
                segments[i] = rest
            else:
                segments.pop(i)
            break
    rest = " - ".join(segments).strip(" -–—|:")
    if len(date) == 8 and date.isdigit():
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    return Name(rest or title, label, number, date if number is None else date)
