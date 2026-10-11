#!/usr/bin/env python3
"""Shared DeepSeek caller for candidate Axiom and Master Equation mappings."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from html.parser import HTMLParser
from pathlib import Path


class TextExtractor(HTMLParser):
    BLOCKS = {"p", "li", "blockquote", "figcaption", "td", "th", "h1", "h2", "h3", "h4"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self.skip += 1
        elif not self.skip and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1
        elif not self.skip and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="strict")
    if path.suffix.lower() in {".html", ".htm"}:
        parser = TextExtractor()
        parser.feed(raw)
        raw = "\n".join(x.strip() for x in "".join(parser.parts).splitlines() if x.strip())
    return raw


def reference_context(station_dir: Path, station: str) -> str:
    refs = station_dir / "REFERENCES"
    if station == "axiom_nodes":
        names = ["README.md", "reference_manifest.json", "AXIOM_CHAIN_MASTER_v2.3_CANONICAL_SEALED.md"]
    else:
        names = [
            "README.md",
            "reference_manifest.json",
            "CANONICAL_DEFINITIONS_20260922.json",
            "MASTER_EQUATION_CANONICAL_LOCK_v4.md",
            "THE_MASTER_EQUATION_CANONICAL_DOCUMENT_20260809.md",
        ]
    chunks = []
    for name in names:
        path = refs / name
        if not path.exists():
            raise FileNotFoundError(f"Required governed reference is missing: {path}")
        chunks.append(f"\n===== {name} =====\n{path.read_text(encoding='utf-8', errors='strict')}")
    return "".join(chunks)


def call_deepseek(system: str, user: str, model: str, max_tokens: int, timeout: int) -> tuple[dict, dict]:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set")
    body = {
        "model": model,
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            envelope = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"DeepSeek HTTP {exc.code}; response body withheld") from exc
    choice = envelope["choices"][0]
    if choice.get("finish_reason") == "length":
        raise RuntimeError("DeepSeek response was truncated")
    result = json.loads(choice["message"]["content"])
    provider = {
        "provider": "deepseek",
        "model": envelope.get("model", model),
        "finish_reason": choice.get("finish_reason"),
        "usage": envelope.get("usage"),
    }
    return result, provider


def validate_result(data: dict, station: str) -> None:
    required = {
        "axiom_nodes": ["schema_version", "station", "paper", "mappings", "unmapped_claims", "conflicts", "summary"],
        "master_equation": ["schema_version", "station", "paper", "equation_assessment", "coordinate_mappings", "covariance_analysis", "conflicts", "summary"],
    }[station]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Invalid {station} JSON; missing: {', '.join(missing)}")
    if data.get("station") != station:
        raise ValueError(f"Invalid station identity: {data.get('station')!r}")
    rows = data["mappings"] if station == "axiom_nodes" else data["coordinate_mappings"]
    if not isinstance(rows, list):
        raise ValueError("Mapping collection must be an array")
    for index, row in enumerate(rows, 1):
        quote = str(row.get("paper_quote", "")).strip()
        if not quote:
            raise ValueError(f"Mapping {index} has no exact paper_quote")
        confidence = row.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            raise ValueError(f"Mapping {index} has invalid confidence")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("station", choices=["axiom_nodes", "master_equation"])
    parser.add_argument("source", type=Path)
    parser.add_argument("--station-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"))
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--max-source-chars", type=int, default=180000)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = args.source.resolve()
    source_bytes = source.read_bytes()
    paper = source_text(source)
    if len(paper) > args.max_source_chars:
        raise SystemExit(f"Source has {len(paper)} characters; chunking is required before this pilot call")
    prompt = (args.station_dir / "PROMPTS" / "evaluate.txt").read_text(encoding="utf-8")
    context = reference_context(args.station_dir, args.station)
    paper_id = re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-")
    run_id = str(uuid.uuid4())
    user = (
        f"GOVERNED REFERENCE PACKAGE:\n{context}\n\n"
        f"PAPER_ID: {paper_id}\nSOURCE_SHA256: {hashlib.sha256(source_bytes).hexdigest()}\n"
        f"PAPER TEXT:\n{paper}\n"
    )
    result, provider = call_deepseek(prompt, user, args.model, args.max_tokens, args.timeout)
    result["paper"] = {
        **(result.get("paper") if isinstance(result.get("paper"), dict) else {}),
        "paper_id": paper_id,
        "source_filename": source.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
    }
    validate_result(result, args.station)
    output = args.output or source.with_name(f"{source.stem}.{args.station}.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    receipt = {
        "status": "SUCCEEDED",
        "run_id": run_id,
        "station": args.station,
        "paper_id": paper_id,
        "source": str(source),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "output": str(output.resolve()),
        "completed_at": utc_now(),
        "provider": provider,
        "result_status": "CANDIDATE_REVIEW_REQUIRED",
    }
    output.with_suffix(".run.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
