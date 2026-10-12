import json
from pathlib import Path

import pytest

from tools.action_center.action_center_core import build_command, category_for, load_catalog


def test_catalog_discovers_and_sorts_launchers(tmp_path):
    (tmp_path / "workflows" / "Demo").mkdir(parents=True)
    (tmp_path / "workflows" / "Demo" / "RUN_PIPELINE.bat").write_text("@echo off")
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"actions": []}))
    actions = load_catalog(tmp_path, catalog)
    assert actions[0]["name"] == "Run Pipeline"
    assert actions[0]["category"] == "Workflow launchers"
    assert actions[0]["command"][-1] == "workflows/Demo/RUN_PIPELINE.bat"


def test_build_command_requires_and_expands_inputs(tmp_path):
    script = tmp_path / "tool.py"
    script.write_text("")
    action = {"selection": "file_and_folder", "command": ["{python}", "tool.py", "{file}", "{folder}"]}
    with pytest.raises(ValueError, match="file selection"):
        build_command(action, tmp_path)
    command = build_command(action, tmp_path, str(script), str(tmp_path))
    assert command[1] == str(script)
    assert command[2:] == [str(script.resolve()), str(tmp_path.resolve())]


def test_markdown_category_is_readable():
    assert category_for("tools/Combine-Markdown.ps1") == "Markdown & documents"
