"""Catalog and command construction shared by the GUI and tests."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys

LAUNCHER_SUFFIXES = {".bat", ".cmd", ".ps1"}


def load_catalog(root: Path, catalog_path: Path) -> list[dict]:
    """Load curated actions and add every otherwise-unlisted Windows launcher."""
    actions = json.loads(catalog_path.read_text(encoding="utf-8"))["actions"]
    known = {
        part.replace("\\", "/").casefold()
        for action in actions
        for part in action["command"]
        if isinstance(part, str) and Path(part).suffix.lower() in LAUNCHER_SUFFIXES
    }
    ignored = {"action_center.bat"}
    for path in sorted(root.rglob("*"), key=lambda item: str(item).casefold()):
        if not path.is_file() or path.suffix.lower() not in LAUNCHER_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        if relative.casefold() in ignored or relative.casefold() in known or ".git" in path.parts:
            continue
        actions.append({
            "name": path.stem.replace("_", " ").title(),
            "category": category_for(relative),
            "description": f"Existing launcher: {relative}. Its own prompts and behavior are unchanged.",
            "command": launcher_command(relative),
            "selection": "none",
            "discovered": True,
        })
    return sorted(actions, key=lambda item: (item["category"].casefold(), item["name"].casefold()))


def category_for(relative: str) -> str:
    lower = relative.casefold()
    if "markdown" in lower or "obsidian" in lower or "document" in lower:
        return "Markdown & documents"
    if "evidence" in lower or "lean" in lower or "grading" in lower:
        return "Evidence & grading"
    if lower.startswith("workflows/"):
        return "Workflow launchers"
    if lower.startswith("apis/") or lower.startswith("api/"):
        return "API tools"
    return "System & utilities"


def launcher_command(relative: str) -> list[str]:
    suffix = Path(relative).suffix.lower()
    if suffix == ".ps1":
        return ["{powershell}", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", relative]
    return ["cmd.exe", "/c", relative]


def build_command(action: dict, root: Path, file_path: str = "", folder_path: str = "") -> list[str]:
    required = action.get("selection", "none")
    if required in {"file", "file_and_folder"} and not file_path:
        raise ValueError("This action requires a file selection.")
    if required in {"folder", "file_and_folder"} and not folder_path:
        raise ValueError("This action requires a folder selection.")
    powershell = "powershell.exe" if os.name == "nt" else "pwsh"
    values = {
        "{python}": sys.executable,
        "{powershell}": powershell,
        "{file}": str(Path(file_path).resolve()) if file_path else "",
        "{folder}": str(Path(folder_path).resolve()) if folder_path else "",
    }
    command = [values.get(part, str(root / part) if _is_repo_path(part, root) else part) for part in action["command"]]
    return command


def _is_repo_path(value: str, root: Path) -> bool:
    return not value.startswith("{") and (root / value).is_file()

