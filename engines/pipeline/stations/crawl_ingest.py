"""Station: normalize web crawler JSON dumps into markdown for the pipeline."""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..station_base import Manifest, SignalType, StationBase, StationVerdict


class CrawlIngestStation(StationBase):
    """Turn one .json crawl dump (list or dict) into a per-row markdown file."""

    def __init__(self, input_dir: str, output_dir: str, **kwargs):
        super().__init__("crawl-ingest", input_dir, output_dir, file_extensions=[".json"], **kwargs)

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.emit_signal(SignalType.ERROR, f"crawl JSON invalid: {exc}", {"file": file_path.name})
            return StationVerdict.FAIL, 0.0, f"invalid json: {exc}"

        rows = payload if isinstance(payload, list) else [payload]
        sections: list[str] = []
        url_count = 0
        seen_urls: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                continue
            title = str(row.get("title", "untitled")).strip() or "untitled"
            url = str(row.get("url", "")).strip()
            content = str(row.get("content") or row.get("text") or "").strip()
            authority = row.get("authority_score")
            if url:
                if url in seen_urls:
                    self.emit_signal(SignalType.DUPLICATE, f"duplicate url in crawl: {url}", {"url": url})
                    continue
                seen_urls.add(url)
                url_count += 1
            content = self._strip_html(content)
            header = f"# {title}\n"
            if url:
                header += f"\nSource: {url}\n"
            if authority is not None:
                header += f"\nAuthority: {authority}\n"
            sections.append(f"{header}\n{content}\n")

        if not sections:
            return StationVerdict.FAIL, 0.0, "no usable rows in crawl payload"

        out_md = self.output_dir / f"{file_path.stem}.md"
        out_md.write_text("\n\n---\n\n".join(sections), encoding="utf-8")

        manifest.metadata["crawl_rows"] = len(sections)
        manifest.metadata["crawl_unique_urls"] = url_count
        score = min(1.0, 0.4 + min(0.5, len(sections) * 0.1))
        return StationVerdict.PASS, score, f"normalized {len(sections)} crawl row(s)"

    def _strip_html(self, raw: str) -> str:
        cleaned = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
        cleaned = re.sub(r"(?s)<[^>]+>", " ", cleaned)
        return re.sub(r"[ \t]+", " ", cleaned).strip()
