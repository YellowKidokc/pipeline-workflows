import json
from pathlib import Path
import pytest
from scripts.unified import run_workflow, watch_once
from scripts.orchestrator import Orchestrator
from engines.pipeline import pof_bridge


def test_preview_does_not_create_packet(tmp_path):
    packet = tmp_path / 'packet'
    result = run_workflow('review-document', packet)
    assert result['status'] == 'preview'
    assert not packet.exists()


def test_pof_station_full_source_stops_at_review(tmp_path, monkeypatch):
    packet = tmp_path / 'packet'; (packet / 'INPUT').mkdir(parents=True)
    text = 'text ' * 6000 + 'IMPORTANT FINAL BOUNDARY'
    (packet / 'INPUT' / 'paper.md').write_text(text, encoding='utf-8')
    calls = []
    def fake(request, **kwargs):
        calls.append(request)
        return {'status': 'completed', 'text': 'candidate analysis', 'receipt': 'fixture'}
    monkeypatch.setattr(pof_bridge, 'call_pof', fake)
    status = run_workflow('review-document', packet, execute=True)
    assert status['status'] == 'review'
    assert text in calls[0]['text']
    assert (packet / 'INPUT' / 'paper.md').read_text(encoding='utf-8') == text
    outputs = list((packet / 'OUTPUT' / 'pof-source-review').glob('*.json'))
    assert json.loads(outputs[0].read_text())['canon_status'] == 'CANDIDATE_DRAFT'
    with pytest.raises(ValueError, match='requires review'):
        run_workflow('review-document', packet, execute=True)
    assert len(calls) == 1


def test_watcher_settles_and_does_not_repeat_review(tmp_path):
    source = tmp_path / 'in'; source.mkdir()
    (source / 'a.md').write_text('original')
    registry = tmp_path / 'watch.json'
    registry.write_text(json.dumps({'state_root': str(tmp_path / 'state'), 'watches': [
        {'enabled': True, 'folder': str(source), 'workflow': 'review-document', 'settle_seconds': 2}]}))
    calls = []
    def fake(name, packet, **kwargs):
        calls.append(packet)
        assert (packet / 'INPUT' / 'a.md').read_text() == 'original'
        return {'status': 'review'}
    watch_once(registry, execute=False, runner=fake)
    assert not (tmp_path / 'state').exists()
    watch_once(registry, True, fake, now=1)
    assert not calls
    watch_once(registry, True, fake, now=4)
    watch_once(registry, True, fake, now=8)
    assert len(calls) == 1
    assert (source / 'a.md').read_text() == 'original'


def test_preview_history_cannot_skip_real_execution(tmp_path):
    packet = tmp_path / 'packet'; (packet / 'INPUT').mkdir(parents=True)
    (packet / 'INPUT' / 'a.md').write_text('source')
    root = Path(__file__).resolve().parents[1]
    preview = Orchestrator(dry_run=True, manifest_path=tmp_path / 'manifest.json')
    preview.run(root / 'workflows/review-document.json', packet)
    with pytest.raises(ValueError, match='Preview and execution'):
        run_workflow('review-document', packet, execute=True)
