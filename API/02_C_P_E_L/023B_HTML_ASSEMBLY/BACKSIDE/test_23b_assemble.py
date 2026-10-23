"""Tests for 23B_HTML_ASSEMBLY: atom JSON/YAML -> standalone HTML pages."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

BACKSIDE = Path(__file__).resolve().parent
FRONT = BACKSIDE.parent


@pytest.fixture
def sample_atom(tmp_path: Path) -> Path:
    atom = {
        "protocol_version": "ATLAS-ATOM-1.2",
        "atom": {
            "type": "claim",
            "status": "leanProven",
            "id": "TEST-001",
            "role": "Test Claim",
            "title": "Test Atom for HTML Assembly",
            "claim": "A test claim used by the HTML assembly test suite.",
            "commitment": "Canon"
        },
        "identity": {
            "uuid": "00000000-0000-0000-0000-000000000001",
            "semantic_code": "ATOM.TEST.L1.C1",
            "human_label": "Test Atom",
            "publication_state": "canon",
            "version": "1.0",
            "source_hash": "sha256:test",
            "last_computed": "2026-10-17T00:00:00Z"
        },
        "lens": {
            "m05": "Test rests on",
            "m06": "Test weakest link",
            "m07": "Test kill condition",
            "m08": "Test support"
        },
        "computed": {
            "blast_radius": 1,
            "articulation_point": False,
            "dependency_depth": 1,
            "reachability_up": 0,
            "reachability_down": 0
        }
    }
    p = tmp_path / "test-atom.json"
    p.write_text(json.dumps(atom, indent=2), encoding="utf-8")
    return p


def test_backside_has_required_files() -> None:
    for required in ("23b_assemble.py", "FOCUS.md", "PROMPT.md", "station.json", "README.md"):
        assert (BACKSIDE / required).exists(), f"BACKSIDE lacks {required}"


def test_front_folder_has_only_launchers_inbox_outbox_backside() -> None:
    allowed = {"INBOX", "OUTBOX", "BACKSIDE"}
    extras = [p.name for p in FRONT.iterdir() if p.is_dir() and p.name not in allowed]
    assert not extras, f"Unexpected folders in front: {extras}"
    bats = list(FRONT.glob("*.bat"))
    assert 1 <= len(bats) <= 4, f"Expected 1-4 .bat launchers, found {len(bats)}"


def test_assembly_produces_self_contained_html(sample_atom: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(BACKSIDE / "23b_assemble.py"), str(sample_atom), "--outbox", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"Script failed: {result.stdout}\n{result.stderr}"

    html_path = out / "test-atom.html"
    receipt_path = out / "test-atom.receipt.json"
    assert html_path.exists(), "Expected output HTML file"
    assert receipt_path.exists(), "Expected receipt JSON file"

    html = html_path.read_text(encoding="utf-8")
    assert '<script type="application/json" id="atom-data">' in html
    assert "Test Atom for HTML Assembly" in html
    assert "ATLAS-ATOM-1.2" in html
    assert "<style>" in html and "</style>" in html
    assert "let GRAMMAR = { ...DEFAULT_GRAMMAR" in html

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["station"] == "23B_HTML_ASSEMBLY"
    assert receipt["page"] == "test-atom.html"
    assert receipt["type"] == "claim"


def test_index_html_lists_built_pages(sample_atom: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    subprocess.run(
        [sys.executable, str(BACKSIDE / "23b_assemble.py"), str(sample_atom), "--outbox", str(out)],
        check=True,
    )
    index = out / "index.html"
    assert index.exists()
    text = index.read_text(encoding="utf-8")
    assert "test-atom.html" in text
    assert "claim" in text
