import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

from openintel.ledger import Ledger

SCRIPTS = Path("workflows/YouTubeChannelRefinery/SCRIPTS").resolve()
sys.path.insert(0, str(SCRIPTS))
import job_queue
import scheduler
import station_common
import station_impl


def seed_video(tmp_path, profile="general"):
    ledger_path = tmp_path / "ledger.sqlite"
    ledger = Ledger(ledger_path); ledger.initialize()
    source = ledger.add_source("HAB", title="Resurrection Evidence", url="https://youtu.be/demo")
    with ledger.db:
        ledger.db.execute(
            "INSERT INTO videos(id,source_id,collection,channel,chapter,title,url,profile,raw_transcript) VALUES(?,?,?,?,?,?,?,?,?)",
            ("VID-HAB-demo", source, "HAB", "Gary Habermas", 1, "Resurrection Evidence", "https://youtu.be/demo", profile,
             "Gary Habermas says Romans 10:9 shows the resurrection was believed in 1975. The historical argument has several facts."),
        )
    ledger.close()
    return ledger_path


def test_every_station_runs_alone_and_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENINTEL_VAULT_ROOT", str(tmp_path / "vault"))
    ledger_path = seed_video(tmp_path)
    monkeypatch.setattr(station_impl, "_nas", lambda *args: {"entities": [], "labels": [], "scores": []})
    monkeypatch.setattr(station_impl, "_llm", lambda *args: {})
    for name in station_common.STATIONS:
        assert station_common.run_station(ledger_path, "VID-HAB-demo", name) == "done"
        assert station_common.run_station(ledger_path, "VID-HAB-demo", name) == "already_done"
    db = sqlite3.connect(ledger_path)
    assert db.execute("SELECT count(*) FROM station_runs WHERE status='DONE'").fetchone()[0] == 11


def test_ckg_has_five_sections_and_profile_lens(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENINTEL_VAULT_ROOT", str(tmp_path / "vault"))
    monkeypatch.setattr(station_impl, "_nas", lambda *args: {"entities": [], "labels": [], "scores": []})
    monkeypatch.setattr(station_impl, "_llm", lambda *args: {})
    monkeypatch.setattr(station_impl, "_prefs", lambda ctx: {"paragraph_words": 200, "theme_threshold": .35})
    for profile in ("general", "christian"):
        root = tmp_path / profile; root.mkdir()
        ledger_path = seed_video(root, profile)
        for name in station_common.STATIONS:
            station_common.run_station(ledger_path, "VID-HAB-demo", name)
        card = next((tmp_path / "vault/YouTube/Gary Habermas").glob("*Chapter*— CKG.md"))
        text = card.read_text()
        for heading in ("What this is", "What it means", "How it connects", "Mini graph", "Open threads"):
            assert f"## {heading}" in text
        assert ("## Christian lens" in text) is (profile == "christian")
        card.unlink()


def test_queue_idle_pause_and_resume_without_duplicates(tmp_path):
    queue = tmp_path / "queue.json"
    job = job_queue.enqueue("channel.md", "general", "idle", "Channel", path=queue)
    data = job_queue.load(queue); data["jobs"][0]["videos"] = ["v1", "v2"]; job_queue.save(data, queue)
    calls = []
    idle_values = iter([9999, 0, 9999, 9999])
    idle = lambda: next(idle_values)
    run = lambda job, video: (lambda: calls.append(video))
    first = scheduler.process_once(queue, {"idle_minutes": 1, "max_desktop_cpu": 30}, idle_fn=idle, cpu_fn=lambda: 0, fullscreen_fn=lambda: False, runner=run)
    assert first["status"] == "PAUSED" and calls == ["v1"]
    second = scheduler.process_once(queue, {"idle_minutes": 1, "max_desktop_cpu": 30}, idle_fn=idle, cpu_fn=lambda: 0, fullscreen_fn=lambda: False, runner=run)
    assert second["status"] == "DONE" and calls == ["v1", "v2"]


def test_watcher_stable_file_spawns_prompt_but_does_not_run(tmp_path):
    watcher_path = SCRIPTS / "watcher.py"
    spec = importlib.util.spec_from_file_location("refinery_watcher", watcher_path)
    watcher = importlib.util.module_from_spec(spec); spec.loader.exec_module(watcher)
    inbox = tmp_path / "input"; inbox.mkdir(); source = inbox / "channel.md"
    source.write_text("# Example - Videos\n\n## 1. First\n")
    commands = []
    found = watcher.scan_once(inbox, tmp_path / "seen.json", sleep=lambda _: None, spawn=lambda command: commands.append(command))
    assert found == [source] and "prompt.py" in commands[0][1]
    assert not (tmp_path / "queue.json").exists()
