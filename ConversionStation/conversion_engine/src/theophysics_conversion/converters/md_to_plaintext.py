"""
md_to_plaintext.py — Strip Markdown to clean plain text
POF 2828 | Conversion Station

Usage:
  python md_to_plaintext.py                    # process all .md in current folder
  python md_to_plaintext.py path/to/file.md    # single file
  python md_to_plaintext.py path/to/folder/    # all .md in folder

Output: same filename with .txt extension, alongside the source file.
"""

import re
import sys
from pathlib import Path


def strip_markdown(text: str) -> str:
    """Remove all Markdown formatting, leaving clean readable prose."""

    # Remove YAML front matter
    text = re.sub(r"^---[\s\S]*?---\n", "", text, count=1)

    # Headings → text only
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)

    # Bold / italic / strikethrough
    text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}(.+?)_{1,3}", r"\1", text)
    text = re.sub(r"~~(.+?)~~", r"\1", text)

    # Code blocks (fenced)
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)

    # Images → remove entirely
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    # Links → keep label
    text = re.sub(r"\[(.+?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\[(.+?)\]\[.*?\]", r"\1", text)

    # Blockquotes
    text = re.sub(r"^>+\s*", "", text, flags=re.M)

    # Horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.M)

    # Bullet / numbered list markers
    text = re.sub(r"^[\s]*[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.M)

    # HTML tags (if any leaked through)
    text = re.sub(r"<[^>]+>", "", text)

    # HTML entities
    entities = {
        "&amp;": "&", "&lt;": "<", "&gt;": ">",
        "&quot;": '"', "&apos;": "'", "&nbsp;": " ",
    }
    for ent, char in entities.items():
        text = text.replace(ent, char)

    # URLs left bare
    text = re.sub(r"https?://\S+", "", text)

    # Table markers
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"^[-| :]+$", "", text, flags=re.M)

    # Collapse whitespace
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)

    return text.strip()


def process_file(src: Path) -> Path:
    raw = src.read_text(encoding="utf-8", errors="replace")
    clean = strip_markdown(raw)
    out = src.with_suffix(".txt")
    out.write_text(clean, encoding="utf-8")
    kb_in  = len(raw.encode()) // 1024
    kb_out = len(clean.encode()) // 1024
    print(f"  {src.name} → {out.name}  ({kb_in}KB → {kb_out}KB)")
    return out


def main():
    args = sys.argv[1:]

    if not args:
        # No args — process all .md in current directory
        targets = list(Path(".").glob("*.md"))
    else:
        path = Path(args[0])
        if path.is_dir():
            targets = list(path.glob("*.md"))
        elif path.suffix.lower() in (".md", ".markdown"):
            targets = [path]
        else:
            print(f"ERROR: {path} is not a .md file or folder")
            sys.exit(1)

    if not targets:
        print("No .md files found.")
        return

    print(f"Stripping {len(targets)} file(s) to plain text...")
    for f in sorted(targets):
        process_file(f)
    print(f"Done. {len(targets)} .txt file(s) written.")


if __name__ == "__main__":
    main()
