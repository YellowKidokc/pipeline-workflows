"""Substack publish station — package paper as faiththruphysics.com HTML + meta."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from ..station_base import Manifest, SignalType, StationBase, StationVerdict


class SubstackPublishStation(StationBase):
    """Render an HTML page with OG metadata, extract laws/axioms badges, and queue for upload."""

    def __init__(self, input_dir: str, output_dir: str, site_url: str = "https://faiththruphysics.com", **kwargs):
        super().__init__("substack-publish", input_dir, output_dir, file_extensions=[".md"], **kwargs)
        self.site_url = site_url.rstrip("/")

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        slug = self._slug(file_path.stem)
        title = self._title(text, file_path.stem)
        summary = self._extract_section(text, "Layer 1: Executive Summary", "Layer 2:") or self._first_paragraph(text)
        body = self._extract_section(text, "Layer 3: The Paper", "Layer 4:") or text
        laws = self._extract_laws(text)
        axioms = self._extract_axioms(text)
        word_count = len(body.split())

        html_doc = self._render_html(slug, title, summary, body, laws, axioms)
        out_path = self.output_dir / f"{slug}.html"
        out_path.write_text(html_doc, encoding="utf-8")

        meta = {
            "slug": slug,
            "title": title,
            "url": f"{self.site_url}/{slug}",
            "summary": summary[:200],
            "laws": laws,
            "axioms": axioms,
            "source": file_path.name,
            "word_count": word_count,
            "r2_queue": True,
        }
        (self.output_dir / f"{slug}.publish.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        if word_count < 200:
            self.emit_signal(SignalType.QUALITY, f"{file_path.name} body under 200 words", {"word_count": word_count})

        score = 0.5 + min(0.3, len(laws) * 0.05) + (0.15 if summary else 0.0) + (0.05 if word_count >= 800 else 0.0)
        verdict = StationVerdict.PASS if score >= self.threshold_pass else StationVerdict.REVIEW
        return verdict, min(score, 1.0), f"substack package: laws={len(laws)} words={word_count}"

    def _slug(self, stem: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
        return slug or "untitled"

    def _title(self, text: str, fallback: str) -> str:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped.lstrip("# ").strip()
        return fallback

    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> str:
        pattern = re.escape(start_marker) + r"\s*\n(.*?)(?=\n##\s*" + re.escape(end_marker) + r"|$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _first_paragraph(self, text: str) -> str:
        for paragraph in re.split(r"\n\s*\n", text):
            stripped = paragraph.strip()
            if stripped and not stripped.startswith(("#", "---", "```")):
                return stripped[:400]
        return ""

    def _extract_laws(self, text: str) -> list[str]:
        found = sorted(set(re.findall(r"\bL(?:10|[1-9])\b", text)))
        return found

    def _extract_axioms(self, text: str) -> list[str]:
        return sorted(set(re.findall(r"\bAS-\d{3}\b", text)))

    def _render_html(self, slug: str, title: str, summary: str, body: str, laws: list[str], axioms: list[str]) -> str:
        safe_title = html.escape(title)
        safe_summary = html.escape(summary[:200])
        law_badges = "".join(
            f"<span class='badge'>{law}</span>" for law in laws
        )
        axiom_badges = "".join(
            f"<span class='badge axiom'>{ax}</span>" for ax in axioms
        )
        body_html = self._markdown_to_html(body)
        return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'>
<title>{safe_title}</title>
<link rel='canonical' href='{self.site_url}/{slug}'>
<meta property='og:title' content='{safe_title}'>
<meta property='og:description' content='{safe_summary}'>
<meta property='og:url' content='{self.site_url}/{slug}'>
<meta property='og:type' content='article'>
<meta property='og:image' content='{self.site_url}/{slug}_thumb.svg'>
<meta name='twitter:card' content='summary_large_image'>
<style>
body{{background:#0d1117;color:#e6d5a8;font-family:Georgia,serif;max-width:760px;margin:0 auto;padding:32px}}
h1{{color:#c9a227}}
.badge{{display:inline-block;border:1px solid #c9a227;padding:2px 8px;margin:2px;border-radius:3px;font-size:.85em}}
.badge.axiom{{border-color:#8ea6c0}}
article{{line-height:1.6;margin-top:24px}}
a{{color:#c9a227}}
</style></head>
<body>
<h1>{safe_title}</h1>
<div class='meta'>{law_badges}{axiom_badges}</div>
<article>{body_html}</article>
</body></html>"""

    def _markdown_to_html(self, text: str) -> str:
        """Tiny markdown→HTML for paragraphs, headings, and emphasis. Good enough for publish-ready pages."""
        lines = text.split("\n")
        out: list[str] = []
        in_para: list[str] = []

        def flush() -> None:
            if in_para:
                out.append("<p>" + " ".join(in_para) + "</p>")
                in_para.clear()

        for raw in lines:
            stripped = raw.strip()
            if not stripped:
                flush()
                continue
            heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
            if heading:
                flush()
                level = len(heading.group(1))
                out.append(f"<h{level}>{html.escape(heading.group(2))}</h{level}>")
                continue
            escaped = html.escape(stripped)
            escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
            escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
            in_para.append(escaped)
        flush()
        return "\n".join(out)
