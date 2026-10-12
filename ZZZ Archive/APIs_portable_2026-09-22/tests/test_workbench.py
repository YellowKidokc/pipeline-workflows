import json, shutil, subprocess, sys
from pathlib import Path
import pytest

API=Path(__file__).parents[1]
sys.path.insert(0,str(API))
from workbench.cli import create
from workbench.coordinator import aggregate, discover
from workbench.export import clean_export
from workbench.providers import Provider, ProviderError, ProviderResult
from workbench.station import Runner, StationLock

TEMPLATE=API/"templates"/"MY_STATION"

class CountingProvider:
    name="mock"; model="counting"
    def __init__(self, fail_at=None): self.calls=[]; self.fail_at=fail_at
    def complete(self,prompt,max_tokens,call_id):
        self.calls.append(call_id)
        if self.fail_at and len(self.calls)==self.fail_at: raise ProviderError("planned","network",True)
        return ProviderResult("ok:"+prompt[-20:],{"input_tokens":7,"output_tokens":2})

def station(tmp_path,name="Station With Spaces"):
    root=tmp_path/name; create(TEMPLATE,root)
    config=json.loads((root/"CONFIG/station.json").read_text()); config["queue"]["settle_seconds"]=0
    (root/"CONFIG/station.json").write_text(json.dumps(config))
    return root

def test_blank_clone_unique_and_relocation_preserves_identity(tmp_path):
    one=station(tmp_path,"one"); two=station(tmp_path,"two")
    first=json.loads((one/"STATE/identity.json").read_text())["station_id"]
    assert first != json.loads((two/"STATE/identity.json").read_text())["station_id"]
    moved=tmp_path/"renamed outside repository"; one.rename(moved)
    assert json.loads((moved/"STATE/identity.json").read_text())["station_id"]==first
    assert not list((two/"LOGS").glob("*.jsonl"))

def test_bundled_station_runs_outside_repository(tmp_path):
    root=station(tmp_path,"portable renamed"); (root/"INBOX/story.txt").write_text("Once upon a time")
    result=subprocess.run([sys.executable,str(root/"SCRIPTS/workbench_cli.py"),"run-once","--root",str(root)],cwd=tmp_path,text=True,capture_output=True)
    assert result.returncode==0, result.stderr
    assert (root/"OUTBOX/story__receipt.json").exists()

def test_nested_series_priority_and_complete_coverage(tmp_path):
    root=station(tmp_path); (root/"INBOX/SERIES/b").mkdir(); (root/"INBOX/SERIES/b/002.txt").write_text("B"*25000)
    (root/"INBOX/001.txt").write_text("ordinary"); (root/"INBOX/_PRIORITY/z.txt").write_text("priority")
    assert "_PRIORITY" in Runner(root,CountingProvider()).candidates()[0].parts
    rows=Runner(root,CountingProvider()).run_once(); assert len(rows)==3 and all(r["status"]=="completed" for r in rows)
    receipt=json.loads(next((root/"OUTBOX").glob("002__receipt.json")).read_text())
    coverage=[x for x in receipt["coverage"] if x["step"]=="response"]
    assert coverage[0]["start"]==0 and coverage[-1]["end"]==25000 and len(coverage)==2

def test_resume_does_not_repeat_completed_api_step(tmp_path):
    root=station(tmp_path); (root/"INBOX/a.txt").write_text("source")
    config=json.loads((root/"CONFIG/station.json").read_text()); config["steps"].append({"name":"second","type":"api","prompt":"01_PROCESS_DOCUMENT.md"}); (root/"CONFIG/station.json").write_text(json.dumps(config))
    flaky=CountingProvider(fail_at=2); assert Runner(root,flaky).run_once()[0]["status"]=="failed"
    resumed=CountingProvider(); assert Runner(root,resumed).run_once()[0]["status"]=="completed"
    assert len(resumed.calls)==1

def test_duplicate_launch_lock(tmp_path):
    root=station(tmp_path)
    with StationLock(root):
        with pytest.raises(RuntimeError,match="already running"): StationLock(root).__enter__()

def test_rate_limit_retry_after_and_no_model_fallback():
    calls=[]; sleeps=[]
    def transport(url,headers,payload,timeout):
        calls.append((url,payload["model"],headers)); return ((429,{"Retry-After":"0"},{"error":{"message":"slow"}}) if len(calls)==1 else (200,{}, {"id":"r","choices":[{"message":{"content":"done"}}]}))
    p=Provider("deepseek","explicit-model","secret",retries=1,transport=transport,sleep=sleeps.append)
    assert p.complete("hi",10,"call").text=="done" and [c[1] for c in calls]==["explicit-model"]*2 and sleeps==[0]

@pytest.mark.parametrize("name,response",[
    ("openai",{"id":"o","output":[{"content":[{"type":"output_text","text":"ok"}]}]}),
    ("anthropic",{"id":"a","content":[{"type":"text","text":"ok"}]}),
    ("deepseek",{"id":"d","choices":[{"message":{"content":"ok"}}]}),
    ("openrouter",{"id":"r","choices":[{"message":{"content":"ok"}}]}),
])
def test_official_provider_wire_shapes_are_mocked(name,response):
    seen={}
    def transport(url,headers,payload,timeout): seen.update(url=url,headers=headers,payload=payload); return 200,{},response
    assert Provider(name,"chosen-model","not-a-real-key",transport=transport).complete("input",20,"call-id").text=="ok"
    assert seen["payload"]["model"]=="chosen-model" and "not-a-real-key" in str(seen["headers"])
    assert "input" in str(seen["payload"])

def test_bad_provider_response_is_failure(tmp_path):
    def transport(*args): return 200,{}, {"choices":[]}
    p=Provider("openrouter","m","secret",transport=transport)
    with pytest.raises(ProviderError) as error: p.complete("x",1,"c")
    assert error.value.category=="corrupt_response"

def test_corrupted_output_is_regenerated(tmp_path):
    root=station(tmp_path); (root/"INBOX/a.txt").write_text("source")
    first=CountingProvider(); assert Runner(root,first).run_once()[0]["status"]=="completed"
    (root/"OUTBOX/a__02_response.md").write_text("tampered")
    second=CountingProvider(); assert Runner(root,second).run_once()[0]["status"]=="completed"
    assert len(second.calls)==1 and "tampered" not in (root/"OUTBOX/a__02_response.md").read_text()

def test_duplicate_identity_offline_aggregation_and_stale_root(tmp_path):
    one=station(tmp_path,"one"); two=station(tmp_path,"two")
    shutil.copy2(one/"STATE/identity.json",two/"STATE/identity.json")
    inv=discover([tmp_path,tmp_path/"unavailable"])
    assert sum(s["status"]=="duplicate_identity" for s in inv["stations"])==2
    assert any(s["status"]=="stale_path" for s in inv["stations"])
    assert aggregate(inv,tmp_path/"central/activity.csv")==0

def test_clean_export_has_no_secret_or_history(tmp_path):
    source=station(tmp_path,"source"); (source/"CONFIG/private.local.json").write_text('{"api_key":"SECRET"}')
    (source/"INBOX/paper.txt").write_text("private"); (source/"LOGS/events.jsonl").write_text("history")
    destination=tmp_path/"export"; clean_export(source,destination)
    all_text="".join(p.read_text(errors="ignore") for p in destination.rglob("*") if p.is_file())
    assert "SECRET" not in all_text
    assert not (destination/"CONFIG/private.local.json").exists() and not (destination/"INBOX/paper.txt").exists() and not (destination/"LOGS/events.jsonl").exists()
    assert (destination/"STATE/identity.json").exists()
