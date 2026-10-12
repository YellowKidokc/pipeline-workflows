"""Small reusable local NLP capabilities (no model downloads)."""
from __future__ import annotations
import re

def cleanup(text: str, options: dict | None = None) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip() + "\n"
def extract(text: str, options: dict | None = None) -> str:
    return "\n".join(re.findall(r"(?m)^#{1,6}\s+.+$", text)) or "(no headings found)"
def classify(text: str, options: dict | None = None) -> str:
    words = len(text.split()); return f"document_length={'long' if words > 1000 else 'short'}; words={words}"
def chunk(text: str, limit: int, overlap: int = 200):
    if limit <= overlap: raise ValueError("chunk limit must exceed overlap")
    if not text: return [(0, 0, "")]
    result=[]; start=0
    while start < len(text):
        end=min(len(text), start+limit); result.append((start,end,text[start:end]))
        if end == len(text): break
        start=end-overlap
    return result
def index(text: str, options: dict | None = None) -> str:
    terms={w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text)}
    return "\n".join(sorted(terms))

HANDLERS={"cleanup": cleanup, "extract": extract, "classify": classify, "index": index}
