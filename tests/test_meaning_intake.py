import hashlib
import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "workflows" / "MeaningIntake" / "SCRIPTS" / "run_packet.py"
SPEC = importlib.util.spec_from_file_location("meaning_intake", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_infer_research_system_source():
    text = """## The evidence\nOriginal paper and negative control.\n## Emerging ladder\nA system model and unresolved question."""
    kind, confidence, signals = MODULE.infer_type(text)
    assert kind in {"research_synthesis", "system"}
    assert confidence >= 0.65
    assert signals


def test_process_preserves_source_and_appends_complete_text(tmp_path, monkeypatch):
    root = tmp_path / "MeaningIntake"
    for name in ("INPUT", "OUTPUT", "REVIEW", "ARCHIVE", "ERROR", "LOGS", "PROMPTS"):
        (root / name).mkdir(parents=True)
    (root / "PROMPTS" / "knowledge_record.md").write_text("{{METADATA}}\n\n{{SOURCE}}", encoding="utf-8")
    source = root / "INPUT" / "watcher.md"
    exact = b"# Watcher\n\n## Evidence\nThe source remains exact.\n"
    source.write_bytes(exact)
    monkeypatch.setattr(MODULE, "ROOT", root)

    result = MODULE.process_file(source, "test-run", MODULE.DEFAULT_CONFIG)

    assert source.read_bytes() == exact
    assert Path(result["preserved_source"]).read_bytes() == exact
    assert result["sha256"] == hashlib.sha256(exact).hexdigest()
    record = Path(result["record"]).read_text(encoding="utf-8")
    assert "CANDIDATE_DRAFT — NOT ADMITTED" in record
    assert "The source remains exact." in record
    receipt = json.loads((root / "OUTPUT" / "watcher.intake.json").read_text(encoding="utf-8"))
    assert receipt["source_sha256"] == result["sha256"]

