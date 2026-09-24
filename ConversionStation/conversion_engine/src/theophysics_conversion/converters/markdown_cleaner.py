from __future__ import annotations

import argparse
import re
from pathlib import Path


MOJIBAKE_REPLACEMENTS = {
    "\u2014": "-",
    "\u2013": "-",
    "\u2192": "->",
    "\u2194": "<->",
    "\u2209": "not in",
    "\u00b7": "-",
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
    "\u2026": "...",
    "â€”": "-",
    "â€“": "-",
    "â†’": "->",
    "â†”": "<->",
    "âˆ‰": "not in",
    "Â·": "-",
    "Â": "",
    "â€œ": '"',
    "â€": '"',
    "â€˜": "'",
    "â€™": "'",
    "â€¦": "...",
}


def clean_markdown(text: str) -> str:
    """Preserve readable Markdown while removing conversion/export noise."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        text = text.replace(bad, good)

    # Remove YAML front matter if present.
    text = re.sub(r"\A---\n[\s\S]*?\n---\n+", "", text, count=1)

    lines = text.split("\n")
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()

        # Drop common converted website breadcrumb bars.
        if re.fullmatch(r"(\[[^\]]+\]\([^)]+\)\s*(?:->|/|>|/)?\s*){2,}.*", stripped):
            continue

        # Drop empty image placeholders and obvious generated source-map/script residue.
        if stripped.startswith("data:") or stripped.startswith("//# sourceMappingURL="):
            continue
        if re.fullmatch(r"<\/?(script|style|noscript)[^>]*>", stripped, flags=re.I):
            continue

        # Normalize heading/emphasis leakage from HTML class conversion.
        line = re.sub(r"^(#{1,6})\s*__\s*", r"\1 ", line)
        line = re.sub(r"^__\s*", "", line)
        line = re.sub(r"\s+__([A-Z0-9])", r" \1", line)
        line = re.sub(r"__\s*$", "", line)

        # Remove trailing raw HTML anchor/link crumbs but keep readable text.
        line = re.sub(r"\s*\[([^\]]+)\]\((?:\.\./|/)?[^)]*\.html\)\s*$", r" \1", line)

        cleaned.append(line.rstrip())

    text = "\n".join(cleaned)

    # Collapse excessive blank lines and space runs without destroying Markdown blocks.
    text = re.sub(r"[ \t]{3,}", "  ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def clean_file(source: Path, output: Path) -> None:
    raw = source.read_text(encoding="utf-8", errors="replace")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(clean_markdown(raw), encoding="utf-8")


def iter_markdown(input_root: Path) -> list[Path]:
    return sorted(
        path
        for path in input_root.rglob("*.md")
        if "_summaries" not in path.parts and not path.name.endswith(".clean.md")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean converted Markdown while preserving Markdown structure.")
    parser.add_argument("input_root", type=Path)
    parser.add_argument("output_root", type=Path)
    parser.add_argument("--series", help="Only process one top-level series/folder.")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    input_root = args.input_root.resolve()
    output_root = args.output_root.resolve()
    files = iter_markdown(input_root)
    if args.series:
        files = [
            path for path in files
            if path.relative_to(input_root).parts and path.relative_to(input_root).parts[0].lower() == args.series.lower()
        ]
    if args.limit > 0:
        files = files[: args.limit]

    for source in files:
        rel = source.relative_to(input_root)
        output = output_root / rel.with_name(f"{source.stem}.clean.md")
        clean_file(source, output)
        print(f"cleaned={source} -> {output}")

    print(f"cleaned_count={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
