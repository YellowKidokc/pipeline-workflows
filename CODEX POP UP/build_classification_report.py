from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOTS = [
    Path(r"D:\DONT TOUCH BOOT UP\Codex-Powershell_GUI"),
    Path(r"D:\DONT TOUCH BOOT UP\PowerShell-main"),
    Path(r"D:\DONT TOUCH BOOT UP\Python-master"),
]
EXTENSIONS = {".ps1", ".py", ".bat", ".cmd"}
SKIP_PARTS = {".git", "__pycache__", "venv", ".venv", "node_modules", "site-packages"}
OUT_JSON = Path(__file__).resolve().parent / "script_inventory.json"
OUT_MD = Path(__file__).resolve().parent / "SCRIPT_CLASSIFICATION_REPORT.md"


CATEGORY_RULES = [
    ("System", ["cpu", "ram", "drive", "health", "process", "hardware", "bios", "os", "uptime", "battery", "power"]),
    ("Network", ["network", "dns", "vpn", "ping", "wifi", "ip", "port", "subnet", "internet", "http", "url"]),
    ("Files", ["file", "folder", "dir", "zip", "hash", "sha", "md5", "rename", "copy", "move", "search", "scan"]),
    ("Audio", ["audio", "voice", "speak", "tts", "volume", "sound", "mp3"]),
    ("Apps", ["open", "close", "chrome", "firefox", "notepad", "explorer", "task-manager", "calculator"]),
    ("Dev", ["git", "repo", "build", "branch", "commit", "python", "fastapi", "sqlite", "json", "xml"]),
    ("Web", ["scraper", "youtube", "news", "weather", "wiki", "browser", "api"]),
    ("Utilities", ["calendar", "time", "date", "clipboard", "convert", "calculator", "count", "list"]),
]

RISK_RULES = [
    ("destructive", ["delete", "remove", "clear", "wipe", "erase", "reboot", "shutdown", "poweroff", "uninstall", "kill"]),
    ("admin", ["firewall", "registry", "service", "driver", "credential", "admin", "sudo", "elevat"]),
    ("caution", ["install", "move", "rename", "copy", "scaffold", "clone", "pull", "push", "write", "backup", "encrypt"]),
]


def useful_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:8000]
    except OSError:
        return ""


def first_summary(path: Path, text: str) -> str:
    synopsis = re.search(r"\.SYNOPSIS\s+(.+?)(?:\n\s*\.[A-Z]|\Z)", text, flags=re.IGNORECASE | re.DOTALL)
    if synopsis:
        return " ".join(synopsis.group(1).split())[:180]

    docstring = re.search(r'"""(.+?)"""', text, flags=re.DOTALL)
    if docstring:
        return " ".join(docstring.group(1).split())[:180]

    comments = []
    for line in text.splitlines()[:40]:
        clean = line.strip().lstrip("#").strip()
        if clean and len(clean) > 8 and not clean.startswith(("import ", "from ", "@echo")):
            comments.append(clean)
        if len(comments) >= 2:
            break
    if comments:
        return " ".join(comments)[:180]

    return path.stem.replace("-", " ").replace("_", " ").title()


def keywords_for(path: Path, text: str) -> list[str]:
    seed = f"{path.stem} {text[:1200]}".lower()
    words = re.findall(r"[a-z][a-z0-9-]{2,}", seed)
    noise = {
        "the", "and", "for", "with", "this", "that", "from", "script", "powershell",
        "python", "return", "import", "using", "write", "host", "get", "set", "line",
    }
    counts = Counter(word for word in words if word not in noise)
    return [word for word, _ in counts.most_common(8)]


def classify_category(name: str, text: str) -> str:
    haystack = f"{name} {text[:1500]}".lower()
    tokens = set(re.findall(r"[a-z][a-z0-9-]{1,}", haystack))
    scores: dict[str, int] = {}
    for category, terms in CATEGORY_RULES:
        score = 0
        for term in terms:
            if len(term) <= 3:
                score += 1 if term in tokens else 0
            elif term in haystack:
                score += 1
        scores[category] = score
    category, score = max(scores.items(), key=lambda item: item[1])
    return category if score else "Other"


def classify_risk(name: str, text: str) -> str:
    haystack = f"{name} {text[:1800]}".lower()
    tokens = set(re.findall(r"[a-z][a-z0-9-]{1,}", haystack))
    for risk, terms in RISK_RULES:
        for term in terms:
            if len(term) <= 3 and term in tokens:
                return risk
            if len(term) > 3 and term in haystack:
                return risk
    return "safe"


def should_skip(path: Path) -> bool:
    lowered = {part.lower() for part in path.parts}
    return any(part.lower() in lowered for part in SKIP_PARTS)


def scan() -> list[dict[str, object]]:
    rows = []
    for root in ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS or should_skip(path):
                continue
            text = useful_text(path)
            category = classify_category(path.name, text)
            risk = classify_risk(path.name, text)
            rows.append(
                {
                    "title": path.stem.replace("-", " ").replace("_", " ").title(),
                    "category": category,
                    "risk": risk,
                    "kind": path.suffix.lower().lstrip("."),
                    "source": root.name,
                    "path": str(path),
                    "summary": first_summary(path, text),
                    "keywords": keywords_for(path, text),
                }
            )
    return sorted(rows, key=lambda row: (str(row["risk"]), str(row["category"]), str(row["title"])))


def write_report(rows: list[dict[str, object]]) -> None:
    by_category: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_risk: Counter[str] = Counter()
    for row in rows:
        by_category[str(row["category"])].append(row)
        by_risk[str(row["risk"])] += 1

    lines = [
        "# Script Classification Report",
        "",
        f"Scanned roots: {len(ROOTS)}",
        f"Scripts found: {len(rows)}",
        "",
        "## Risk Counts",
        "",
    ]
    for risk, count in sorted(by_risk.items()):
        lines.append(f"- `{risk}`: {count}")

    lines.extend(["", "## Categories", ""])
    for category in sorted(by_category):
        items = by_category[category]
        lines.append(f"### {category} ({len(items)})")
        lines.append("")
        for row in items[:40]:
            keywords = ", ".join(row["keywords"]) if row["keywords"] else "none"
            lines.append(f"- **{row['title']}** [{row['kind']}, {row['risk']}]")
            lines.append(f"  - Source: `{row['source']}`")
            lines.append(f"  - Summary: {row['summary']}")
            lines.append(f"  - Keywords: {keywords}")
            lines.append(f"  - Path: `{row['path']}`")
        if len(items) > 40:
            lines.append(f"- ... {len(items) - 40} more in JSON inventory")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = scan()
    OUT_JSON.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    write_report(rows)
    print(f"Wrote {len(rows)} scripts")
    print(OUT_JSON)
    print(OUT_MD)


if __name__ == "__main__":
    main()
