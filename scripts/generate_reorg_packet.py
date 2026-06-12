"""Generate a repo reorganization approval packet.

This script inventories the repo and writes proposed moves/flags. It does not
move files. The output is meant for David and GitHub/Codex review first.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "docs" / "reorg"
JSON_OUT = OUT_DIR / "reorg-packet.json"
MD_OUT = OUT_DIR / "REORG_PACKET.md"

CANONICAL_TOP_LEVEL = {
    ".github",
    "contracts",
    "docs",
    "engines",
    "exports",
    "models",
    "preferences",
    "prompts",
    "queue",
    "reality",
    "schemas",
    "scripts",
    "signals",
    "stations",
    "templates",
    "tests",
    "workflows",
}

RUNTIME_DIR_NAMES = {
    "INPUT",
    "OUTPUT",
    "ARCHIVE",
    "ERROR",
    "LOGS",
    "REVIEW",
    "EXPORTS",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}

HEAVY_SUFFIXES = {
    ".safetensors",
    ".onnx",
    ".bin",
    ".pt",
    ".pkl",
    ".pickle",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".zip",
    ".7z",
    ".rar",
}


@dataclass
class Finding:
    kind: str
    path: str
    recommendation: str
    target: str = ""
    reason: str = ""


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    return ".git" in parts or "__pycache__" in parts


def classify_root_items() -> list[Finding]:
    findings: list[Finding] = []
    for item in sorted(REPO_ROOT.iterdir(), key=lambda p: p.name.lower()):
        if item.name.startswith(".") and item.name not in {".github"}:
            continue
        if item.name in {
            "README.md",
            "AGENTS.md",
            "CODEX_BUILD_PROMPT.md",
            "MYTHOS_INTEGRATION_PROMPT.md",
            "pipeline.config.example.json",
            ".gitignore",
        }:
            continue
        if item.is_dir() and item.name not in CANONICAL_TOP_LEVEL:
            findings.append(
                Finding(
                    kind="noncanonical_root",
                    path=rel(item),
                    recommendation="move_or_explain",
                    target="david/DOES_NOT_FIT.md",
                    reason="Top-level folder is outside the current architecture.",
                )
            )
    return findings


def classify_files() -> list[Finding]:
    findings: list[Finding] = []
    for path in REPO_ROOT.rglob("*"):
        if is_ignored(path) or not path.is_file():
            continue
        if path.name == ".gitkeep":
            continue
        parts = path.relative_to(REPO_ROOT).parts
        if any(part in RUNTIME_DIR_NAMES for part in parts):
            findings.append(
                Finding(
                    kind="runtime_artifact",
                    path=rel(path),
                    recommendation="ignore_or_quarantine",
                    target="david/quarantine/",
                    reason="Runtime/build folder content should not become source truth.",
                )
            )
        if path.suffix.lower() in HEAVY_SUFFIXES:
            findings.append(
                Finding(
                    kind="heavy_artifact",
                    path=rel(path),
                    recommendation="remove_from_repo_keep_on_nas",
                    target="NAS/runtime",
                    reason="Heavy/model/database/archive artifact.",
                )
            )
        if "models" in parts[1:] and parts[0] != "models":
            findings.append(
                Finding(
                    kind="nested_model_reference",
                    path=rel(path),
                    recommendation="promote_model_contract_or_reference",
                    target="models/",
                    reason="Model config/reference should be discoverable from top-level models/.",
                )
            )
    return findings


def suggested_moves() -> list[dict]:
    """Seed high-value move candidates. Human/GitHub review must approve."""
    return [
        {
            "from": "schemas/model.schema.json",
            "to": "contracts/model.schema.json",
            "reason": "Schemas are contracts. Keep compatibility alias if code imports old path.",
            "status": "needs_review",
        },
        {
            "from": "schemas/workflow.schema.json",
            "to": "contracts/workflow.schema.json",
            "reason": "Workflow schema belongs with contracts.",
            "status": "needs_review",
        },
        {
            "from": "schemas/station.schema.json",
            "to": "contracts/station.schema.json",
            "reason": "Station schema belongs with contracts.",
            "status": "needs_review",
        },
        {
            "from": "models/preference/*.json",
            "to": "preferences/engines/",
            "reason": "Preference engine configs should live with preferences; model registry stays in models/.",
            "status": "needs_review",
        },
    ]


def write_markdown(findings: list[Finding], moves: list[dict]) -> None:
    lines = [
        "# Reorganization Packet",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Findings: {len(findings)}",
        f"- Suggested moves: {len(moves)}",
        "",
        "## Doctrine",
        "",
        "- GitHub is the governor/spec layer.",
        "- NAS is the runtime/body layer.",
        "- Models are top-level contracts under `models/`; weights stay on NAS.",
        "- Station bodies may be mirrored under `stations/source/`, but live paths stay in `stations/STATION_REGISTRY.json`.",
        "- No move executes until the approval file is edited.",
        "",
        "## Suggested Moves",
        "",
        "| Status | From | To | Reason |",
        "|---|---|---|---|",
    ]
    for move in moves:
        lines.append(f"| {move['status']} | `{move['from']}` | `{move['to']}` | {move['reason']} |")
    lines.extend(["", "## Findings", "", "| Kind | Path | Recommendation | Target | Reason |", "|---|---|---|---|---|"])
    for item in findings:
        lines.append(
            f"| {item.kind} | `{item.path}` | {item.recommendation} | `{item.target}` | {item.reason} |"
        )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    findings = classify_root_items() + classify_files()
    moves = suggested_moves()
    JSON_OUT.write_text(
        json.dumps(
            {
                "generated": datetime.now(timezone.utc).isoformat(),
                "findings": [asdict(item) for item in findings],
                "suggested_moves": moves,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(findings, moves)
    print(f"wrote {JSON_OUT}")
    print(f"wrote {MD_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
