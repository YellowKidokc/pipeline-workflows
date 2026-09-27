import hashlib
from pathlib import Path
from drop_pipeline.runner import tick,init
from drop_pipeline.routing import validate
import pytest

def test_drop_to_note_and_dedupe(tmp_path):
    init(tmp_path)
    source=tmp_path/'DROP'/'video.md'
    raw='# My video\n\nJesus and grace are discussed in this video. Physics uses measurement and experiment. What evidence supports this claim?'
    source.write_text(raw)
    calls=[]
    def classify(text,name,config):
        calls.append(text)
        return {'route':'youtube','categories':['theology','science'],'reason':'fixture'}
    tick(tmp_path,classify,now=0)
    result=tick(tmp_path,classify,now=4)
    assert result['video.md']['status']=='completed'
    note=(tmp_path/result['video.md']['notes'][0]).read_text(encoding='utf-8')
    assert 'topic/theology' in note and 'topic/science' in note
    assert '## Transcript' in note
    assert source.read_text()==raw
    tick(tmp_path,classify,now=8)
    assert len(calls)==1
    (tmp_path/'DROP'/'duplicate.md').write_text(raw)
    tick(tmp_path,classify,now=9);tick(tmp_path,classify,now=13)
    assert len(calls)==1

def test_no_automatic_paid_retry(tmp_path):
    init(tmp_path);(tmp_path/'DROP'/'x.txt').write_text('Some input')
    calls=[]
    def fail(*args):calls.append(1);raise RuntimeError('network failure')
    tick(tmp_path,fail,now=0);tick(tmp_path,fail,now=4);tick(tmp_path,fail,now=8)
    assert len(calls)==1

def test_router_rejects_paths():
    with pytest.raises(ValueError):validate({'route':'../../escape','categories':[]})
    with pytest.raises(ValueError):validate({'route':'youtube','categories':['made-up']})

def test_subtitles(tmp_path):
    from drop_pipeline.processing import extract
    p=tmp_path/'x.srt';p.write_text('1\n00:00:02,000 --> 00:00:04,000\nA complete sentence.\n')
    video=extract(p)[0]
    assert video['segments'][0]['start']==2
    assert video['text']=='A complete sentence.'

def test_connections_and_portable_workspace(tmp_path):
    import json, shutil
    from drop_pipeline.connections import rebuild
    w=tmp_path/'arbitrary workspace';init(w)
    for name,text in [('video','Scientific evidence includes measurements and experiments. Physics research tests experimental predictions.'),('paper','My physics research examines scientific evidence and experimental measurements. Experiments test predictions.')]:
        (w/'DROP'/(name+'.md')).write_text(text)
    classify=lambda text,name,cfg:{'route':'youtube' if name=='video.md' else 'document','categories':['science']}
    tick(w,classify,now=0);tick(w,classify,now=4)
    links=json.loads((w/'STATE'/'connections.json').read_text())
    assert all(x['related'] for x in links)
    assert 'Scientific evidence' in str(links) or 'scientific evidence' in str(links)
    moved=tmp_path/'different name';shutil.copytree(w,moved)
    assert rebuild(moved)['documents']==2
    state=tick(moved,lambda *args:pytest.fail('Repeated paid routing'),now=8)
    assert all(x['status']=='completed' for x in state.values())

def test_prompt_stage_and_unknown_stage(tmp_path):
    import json
    init(tmp_path)
    (tmp_path/'DROP'/'prompt.txt').write_text('## Instructions\nSummarize the research document {{source}}. Include the scientific evidence and measurements.')
    classify=lambda *args:{'route':'prompt','categories':['science']}
    tick(tmp_path,classify,now=0);state=tick(tmp_path,classify,now=4)
    assert state['prompt.txt']['status']=='completed'
    text=next(p for p in (tmp_path/'OBSIDIAN_READY').glob('*.md') if p.name!='Library Index.md').read_text()
    assert '## Prompt inventory' in text and 'not been executed' in text
    definition=tmp_path/'WORKFLOWS'/'prompt'/'workflow.json'
    data=json.loads(definition.read_text());data['stages'].insert(2,'missing_stage');definition.write_text(json.dumps(data))
    (tmp_path/'DROP'/'new.txt').write_text('Summarize this other research paper and evaluate its scientific evidence.')
    tick(tmp_path,classify,now=8);state=tick(tmp_path,classify,now=12)
    assert state['new.txt']['status']=='failed'

def test_touched_source_does_not_repeat_call(tmp_path):
    import os
    init(tmp_path);p=tmp_path/'DROP'/'a.txt';p.write_text('The scientific measurements support the experimental research hypothesis.')
    calls=[]
    def classify(*args):calls.append(1);return {'route':'document','categories':['science']}
    tick(tmp_path,classify,now=0);tick(tmp_path,classify,now=4)
    st=p.stat();os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns+10000000))
    tick(tmp_path,classify,now=8);tick(tmp_path,classify,now=12)
    assert len(calls)==1

def test_legacy_paths_reprocess_and_integrity(tmp_path):
    import json
    from drop_pipeline.runner import main
    init(tmp_path)
    source=tmp_path/'DROP'/'nested'/'paper.md';source.parent.mkdir()
    source.write_text('Scientific evidence and experimental measurement inform this research paper.',encoding='utf-8')
    classify=lambda *args:{'route':'document','categories':['science']}
    tick(tmp_path,classify,now=0);state=tick(tmp_path,classify,now=4)
    receipt=tmp_path/'STATE'/'jobs.json'
    legacy={k.replace('/',chr(92)):{**v,'packet':v['packet'].replace('/',chr(92)),'notes':[n.replace('/',chr(92)) for n in v['notes']]} for k,v in state.items()}
    receipt.write_text(json.dumps(legacy),encoding='utf-8')
    main(['reprocess','--workspace',str(tmp_path),'--job',r'nested\paper.md','--route','document'])
    state=tick(tmp_path,lambda *a:pytest.fail('Paid routing repeated'),now=8)
    job=state['nested/paper.md']
    assert job['status']=='completed' and '\\' not in job['packet']
    packet=tmp_path/job['packet']
    (packet/'source.md').write_text('Modified packet',encoding='utf-8')
    main(['reprocess','--workspace',str(tmp_path)])
    state=tick(tmp_path,lambda *a:pytest.fail('Paid routing repeated'),now=12)
    assert state['nested/paper.md']['status']=='failed'
    assert 'hash changed' in state['nested/paper.md']['error']
    assert source.read_text(encoding='utf-8').startswith('Scientific evidence')


def test_review_resolution(tmp_path):
    from drop_pipeline.runner import main
    init(tmp_path);(tmp_path/'DROP'/'x.md').write_text('This research document explains scientific evidence and experimental measurements.')
    classify=lambda *args:{'route':'review','categories':['science']}
    tick(tmp_path,classify,now=0);state=tick(tmp_path,classify,now=4)
    assert state['x.md']['status']=='review'
    main(['resolve','--workspace',str(tmp_path),'--job','x.md','--route','document'])
    state=tick(tmp_path,lambda *a:pytest.fail('Resolution rebilled routing'),now=8)
    assert state['x.md']['status']=='completed'
    assert '/document/' in state['x.md']['packet']


def test_portable_paths_reject_escape(tmp_path):
    from drop_pipeline.paths import inside,relative
    assert relative(r'WORKFLOWS\youtube\INPUT\abc')=='WORKFLOWS/youtube/INPUT/abc'
    assert inside(tmp_path,r'WORKFLOWS\youtube')==tmp_path/'WORKFLOWS'/'youtube'
    for bad in ('../escape',r'..\escape','/absolute','C:/absolute'):
        with pytest.raises(ValueError):inside(tmp_path,bad)


def test_routing_covers_every_character(monkeypatch):
    import io,json
    from drop_pipeline.routing import route
    sent=[]
    def response(request,timeout):
        body=json.loads(request.data)
        sent.append(json.loads(body['messages'][1]['content']))
        return io.StringIO(json.dumps({'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'route':'document','categories':['science']})}}]}))
    monkeypatch.setenv('DEEPSEEK_API_KEY','fixture-not-a-real-key')
    monkeypatch.setattr('urllib.request.urlopen',response)
    source=('Scientific measurement α. '*400)
    result=route(source,'paper.md',{'routing_chunk_chars':1000})
    assert ''.join(part['source'] for part in sent)==source
    assert sum(c['chars'] for c in result['chunks'])==len(source)
    assert len(sent)>4


def test_watcher_stop_restart_and_single_owner(tmp_path):
    import json,subprocess,sys,time
    from drop_pipeline.runner import main
    init(tmp_path);(tmp_path/'DROP'/'paper.md').write_text('The experimental research paper describes scientific evidence and physics measurements.')
    tick(tmp_path,lambda *a:{'route':'document','categories':['science']},now=0)
    tick(tmp_path,lambda *a:{'route':'document','categories':['science']},now=4)
    command=[sys.executable,'-m','drop_pipeline.runner','watch','--workspace',str(tmp_path)]
    def until(predicate):
        end=time.monotonic()+20
        while time.monotonic()<end:
            if predicate():return
            time.sleep(.1)
        pytest.fail('Watcher did not reach expected state')
    for iteration in range(2):
        main(['reprocess','--workspace',str(tmp_path)])
        process=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            runtime=tmp_path/'STATE'/'worker.json'
            until(lambda:runtime.exists() and json.loads(runtime.read_text())['pid']==process.pid and json.loads(runtime.read_text())['status']=='watching')
            jobs=json.loads((tmp_path/'STATE'/'jobs.json').read_text())
            assert jobs['paper.md']['status']=='completed'
            if iteration==0:
                duplicate=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
                assert duplicate.returncode!=0
                assert process.poll() is None
            main(['stop','--workspace',str(tmp_path)])
            assert process.wait(timeout=10)==0
            assert json.loads(runtime.read_text())['status']=='stopped'
        finally:
            if process.poll() is None:process.terminate();process.wait(timeout=10)

def test_link_refresh_retries_without_routing(tmp_path,monkeypatch):
    from drop_pipeline import runner
    import json
    init(tmp_path);(tmp_path/'DROP'/'x.md').write_text('Scientific evidence is examined using experimental measurements and research methods.')
    classify=lambda *a:{'route':'document','categories':['science']}
    tick(tmp_path,classify,now=0)
    real_rebuild=runner.rebuild
    def fail(*a):raise OSError('Temporary index write failure')
    monkeypatch.setattr(runner,'rebuild',fail)
    with pytest.raises(OSError):tick(tmp_path,classify,now=4)
    assert json.loads((tmp_path/'STATE'/'link-refresh.json').read_text())['pending']
    monkeypatch.setattr(runner,'rebuild',real_rebuild)
    tick(tmp_path,lambda *a:pytest.fail('Index retry rebilled routing'),now=8)
    assert not json.loads((tmp_path/'STATE'/'link-refresh.json').read_text())['pending']
    assert (tmp_path/'OBSIDIAN_READY'/'Library Index.md').is_file()

def test_multiline_transcript_and_numbered_document(tmp_path):
    from drop_pipeline.processing import extract,readable
    source=tmp_path/'video.md'
    source.write_text('# Video\n### Transcript\nFirst spoken paragraph.\n\nSecond spoken paragraph.\nFinal words here.\n',encoding='utf-8')
    video=extract(source)[0]
    assert 'Final words here.' in video['text']
    assert 'Second spoken paragraph.' in readable(video)
    source.write_text('# Paper\n## 1. Introduction\nA numbered paper section.\n## 2. Conclusion\nFinal argument.',encoding='utf-8')
    assert 'Final argument.' in extract(source)[0]['text']


def test_vtt_cue_identifier_and_numeric_dialogue(tmp_path):
    from drop_pipeline.processing import extract
    p=tmp_path/'video.vtt'
    p.write_text('WEBVTT\n\ncue-one\n00:01.000 --> 00:04.000 align:start\n2024\nScience &amp; faith <00:02.000>are discussed.\n',encoding='utf-8')
    video=extract(p)[0]
    assert video['text']=='2024 Science & faith are discussed.'
    assert video['segments'][0]['start']==1

def test_prompt_markdown_structure_survives(tmp_path):
    init(tmp_path)
    original='# Prompt\n\n## Instructions\n- Read {{source}}.\n- Quote the evidence.\n\n```json\n{"summary": ""}\n```\n'
    (tmp_path/'DROP'/'template.md').write_text(original,encoding='utf-8')
    classify=lambda *a:{'route':'prompt','categories':[]}
    tick(tmp_path,classify,now=0);state=tick(tmp_path,classify,now=4)
    note=(tmp_path/state['template.md']['notes'][0]).read_text(encoding='utf-8')
    assert original in note

def test_status_write_retries_windows_sharing_error(tmp_path,monkeypatch):
    from drop_pipeline import runner
    import json
    target=tmp_path/'worker.json';target.write_text('{"status":"old"}')
    replace=runner.os.replace
    attempts=[]
    def temporarily_locked(source,destination):
        attempts.append(1)
        if len(attempts)<3:raise PermissionError('Windows file sharing conflict')
        return replace(source,destination)
    monkeypatch.setattr(runner.os,'replace',temporarily_locked)
    monkeypatch.setattr(runner.time,'sleep',lambda _:None)
    runner.save(target,{'status':'watching'})
    assert len(attempts)==3
    assert json.loads(target.read_text())['status']=='watching'
    assert not list(tmp_path.glob('*.tmp'))


def test_watcher_survives_status_write_failure(tmp_path,monkeypatch):
    from drop_pipeline import runner
    init(tmp_path)
    original_save=runner.save
    calls=[]
    def denied(path,data):
        if path.name=='worker.json':
            calls.append(data['status'])
            raise PermissionError('Status file remains locked')
        original_save(path,data)
    monkeypatch.setattr(runner,'save',denied)
    def stop_on_sleep(_):(tmp_path/'STATE'/'stop.request').touch()
    monkeypatch.setattr(runner.time,'sleep',stop_on_sleep)
    runner.main(['watch','--workspace',str(tmp_path)])
    assert calls==['working','error','stopped']
