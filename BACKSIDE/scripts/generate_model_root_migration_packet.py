"""Generate a non-destructive NAS model-root migration packet.

This script audits GitHub-side references to the current NAS model root and writes
`models/MODEL_ROOT_MIGRATION_PACKET.json`. It does not inspect or mutate NAS
files. GitHub remains the governor/spec layer; NAS remains the runtime/body.
"""
from __future__ import annotations

import json
from pathlib import Path

CURRENT_ROOT = "X:\\Backside\\_models\\_Models"
TARGET_ROOT = "X:\\Models"
PACKET_PATH = Path("models/MODEL_ROOT_MIGRATION_PACKET.json")
REGISTRY_PATH = Path("models/MODEL_REGISTRY.json")
FALLBACKS_PATH = Path("models/MODEL_FALLBACKS.json")
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {
    ".bat",
    ".cfg",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".ps1",
    ".rst",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

KNOWN_NAS_ITEMS = {
    "sbert_minilm": "MOVE_TO_FALLBACKS",
    "deberta_nli": "MOVE_TO_FALLBACKS",
    "huggingface": "MOVE_TO_CACHE",
    "d_brain_huggingface_hub": "MOVE_TO_CACHE",
    ".venv_science_nlp": "MOVE_TO_ENVS",
    "scripts": "MOVE_TO_OPS",
    "health_reports": "MOVE_TO_OPS",
    "loose .bat files": "MOVE_TO_OPS",
    "loose .md files": "MOVE_TO_OPS",
    "loose .py files": "MOVE_TO_OPS",
    "nlp_layer.py": "MOVE_TO_OPS",
    "requirements.txt": "MOVE_TO_OPS",
    "_legacy": "MOVE_TO_LEGACY",
}

TARGET_BUCKETS = {
    "KEEP_AS_MODEL_SLOT": "{root}/{slot_key}/",
    "MOVE_TO_FALLBACKS": "{root}/_fallbacks/{name}/",
    "MOVE_TO_CACHE": "{root}/_cache/{name}/",
    "MOVE_TO_ENVS": "{root}/_envs/science_nlp/",
    "MOVE_TO_OPS": "{root}/_ops/{name}/",
    "MOVE_TO_LEGACY": "{root}/_legacy/{name}/",
    "NEEDS_DAVID_CALL": "No target until David approves the classification.",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_text_path(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {"README", "Makefile"}


def audit_references(root: Path) -> list[dict]:
    references: list[dict] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if not is_text_path(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if CURRENT_ROOT in line or "Backside\\_models\\_Models" in line or "models_root" in line or "MODELS_ROOT" in line:
                references.append(
                    {
                        "path": path.as_posix(),
                        "line": lineno,
                        "text": line.strip(),
                    }
                )
    return references


def packet() -> dict:
    registry = load_json(REGISTRY_PATH)
    fallbacks = load_json(FALLBACKS_PATH)
    slots = registry["slots"]

    dispositions = []
    for slot_key, slot in slots.items():
        dispositions.append(
            {
                "item": slot_key,
                "current_path": slot["path"],
                "target_path": f"{TARGET_ROOT}\\{slot_key}",
                "disposition": "KEEP_AS_MODEL_SLOT",
                "reason": "Canonical M/P model slot from models/MODEL_REGISTRY.json.",
            }
        )

    for name, fallback in fallbacks["fallbacks"].items():
        dispositions.append(
            {
                "item": name,
                "current_path": fallback["path"],
                "target_path": f"{TARGET_ROOT}\\_fallbacks\\{name}",
                "disposition": "MOVE_TO_FALLBACKS",
                "reason": fallback["reason"],
                "for_slot": fallback["for_slot"],
            }
        )

    for name, disposition in KNOWN_NAS_ITEMS.items():
        if disposition == "MOVE_TO_FALLBACKS":
            continue
        if disposition == "MOVE_TO_CACHE":
            target_path = f"{TARGET_ROOT}\\_cache\\{name}"
        elif disposition == "MOVE_TO_ENVS":
            target_path = f"{TARGET_ROOT}\\_envs\\science_nlp"
        elif disposition == "MOVE_TO_OPS":
            target_path = f"{TARGET_ROOT}\\_ops\\{name}"
        elif disposition == "MOVE_TO_LEGACY":
            target_path = f"{TARGET_ROOT}\\_legacy"
        else:
            target_path = None
        dispositions.append(
            {
                "item": name,
                "current_path": f"{CURRENT_ROOT}\\{name}",
                "target_path": target_path,
                "disposition": disposition,
                "reason": "Known NAS root clutter class from operator-provided inventory; verify before moving.",
            }
        )

    dispositions.append(
        {
            "item": "any unclassified loose root file or folder",
            "current_path": f"{CURRENT_ROOT}\\<unknown>",
            "target_path": None,
            "disposition": "NEEDS_DAVID_CALL",
            "reason": "If a file/folder is not explicitly classified in this packet, document it and ask before moving.",
        }
    )

    return {
        "_meta": {
            "description": "Non-destructive migration packet for cleaning the NAS model root. This packet is a plan only; it does not move files.",
            "updated": "2026-06-12",
            "current_models_root": CURRENT_ROOT,
            "target_models_root": TARGET_ROOT,
            "models_root_env": "MODELS_ROOT",
            "doctrine": [
                "GitHub is the governor/spec layer.",
                "NAS is the runtime/body layer.",
                "Do not move or delete model weights without an approval packet.",
                "Prefer MODELS_ROOT indirection over hardcoded paths.",
            ],
        },
        "target_layout": {
            "model_slots": f"{TARGET_ROOT}\\M01-M12 and {TARGET_ROOT}\\P01-P07",
            "fallbacks": f"{TARGET_ROOT}\\_fallbacks",
            "cache": f"{TARGET_ROOT}\\_cache",
            "envs": f"{TARGET_ROOT}\\_envs",
            "ops": f"{TARGET_ROOT}\\_ops",
            "legacy": f"{TARGET_ROOT}\\_legacy",
        },
        "dispositions": dispositions,
        "hardcoded_reference_audit": audit_references(Path(".")),
        "risky_moves_avoided": [
            "No NAS files were moved.",
            "No model weights were uploaded.",
            "No runtime scripts were rewritten in this planning PR.",
            "No station configs were repointed to X:\\Models yet.",
        ],
        "next_pr_plan": [
            "Set/verify MODELS_ROOT on NAS or shell profile.",
            "Create target directories on NAS and perform a dry-run move report.",
            "Update MODEL_REGISTRY and MODEL_FALLBACKS paths from current root to MODELS_ROOT/X:\\Models after the physical move is approved.",
            "Update runtime scripts and station configs in small tested batches.",
        ],
    }


def main() -> int:
    PACKET_PATH.write_text(json.dumps(packet(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {PACKET_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
