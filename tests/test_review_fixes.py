import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from engines.pipeline.llm_hub import LLMHub
from engines.pipeline.station_base import Manifest, StationVerdict
from engines.pipeline.stations.paper_grader import PaperGraderStation
from workflows.CorpusTriage.SCRIPTS.triage_folder import triage

ROOT = Path(__file__).resolve().parents[1]


def test_whole_document_reaches_backend(tmp_path, monkeypatch):
    text = 'begin ' + 'middle ' * 4000 + 'TAIL_SOURCE_Ω'
    hub = LLMHub(str(tmp_path / 'q'), log_dir=str(tmp_path / 'logs'))
    st = PaperGraderStation(str(tmp_path), str(tmp_path / 'out'), queue_dir=str(tmp_path / 'q'))
    st.hub = hub
    src = tmp_path / 'paper.md'
    src.write_text(text, encoding='utf-8')
    manifest = Manifest(file_path=str(src), file_hash='h', pipeline_name='p', current_station='paper-grader')
    assert st.process(src, manifest)[0] == StationVerdict.HOLD
    state = json.loads(src.with_suffix('.md.grade.json').read_text())
    job = hub.get_job(state['job_id'])
    assert job.input_text == text
    captured = []
    monkeypatch.setattr(hub, '_call_ollama', lambda prompt, config: captured.append(prompt) or {'status': 'completed'})
    hub._dispatch(job.to_dict())
    assert text in captured[0]
    assert 'one admitted root axiom' in captured[0]
    failed = tmp_path / 'q' / 'failed' / f'{job.job_id}.json'
    failed.write_text(json.dumps({'error': 'context exceeded'}))
    assert st.process(src, manifest)[0] == StationVerdict.REVIEW


def test_triage_uses_content_and_preserves_source(tmp_path):
    src = tmp_path / 'src'
    src.mkdir()
    content = 'Abstract introduction grace L1 theorem conclusion ' * 220
    (src / 'a.md').write_text(content)
    (src / ('long_name_' * 12 + '.md')).write_text(content)
    before = {f.name: f.read_bytes() for f in src.iterdir()}
    out = tmp_path / 'out'
    triage(src, out)
    rows = json.loads((out / 'triage_manifest.json').read_text())
    assert len(rows) == 2
    assert rows[0]['quality'] == rows[1]['quality']
    assert all(r['duplicate'] for r in rows)
    assert {f.name: f.read_bytes() for f in src.iterdir()} == before
    result = subprocess.run([sys.executable, str(ROOT / 'workflows/CorpusTriage/SCRIPTS/run_packet.py'), '--input', str(src), '--output', str(out)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_adversarial_review_sees_source_tail(monkeypatch):
    folder = ROOT / 'workflows/EvidenceChainIntake/SCRIPTS'
    monkeypatch.syspath_prepend(str(folder))
    spec = importlib.util.spec_from_file_location('epistemic_review_test', folder / 'epistemic_intake_v2.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = 'source ' * 5000 + 'FINAL_QUALIFICATION'
    assert source in module.prompt_call_3({}, {}, source)


def test_unwired_packets_do_not_claim_success(tmp_path):
    for name in ['PaperGrading', 'KnowledgeRefineryBackplane']:
        source = ROOT / 'workflows' / name / 'SCRIPTS/run_packet.py'
        target = tmp_path / name / 'SCRIPTS/run_packet.py'
        target.parent.mkdir(parents=True)
        target.write_bytes(source.read_bytes())
        result = subprocess.run([sys.executable, str(target)], capture_output=True, text=True)
        assert result.returncode == 2
        assert 'No files processed' in result.stdout
