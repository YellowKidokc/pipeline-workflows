"""Read-only completeness checks: python -m unittest discover -s API/_system/tests -p test_station_feed.py"""
import hashlib
import json
import sys
import unittest
from pathlib import Path

SYSTEM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SYSTEM))
from engine.console import listing
from engine.paths import MAIN, station_dir, station_rows

class StationFeedTests(unittest.TestCase):
    def test_every_station_on_disk_is_registered_and_visible(self):
        before = (SYSTEM / "config/stations.json").read_bytes()
        feed = listing()
        self.assertEqual(before, (SYSTEM / "config/stations.json").read_bytes())
        self.assertFalse([s for s in feed["stations"] if "error" in s])
        registered = {station_dir(r["label"], repair=False).resolve() for r in station_rows() if not r.get("retired")}
        self.assertEqual([], [str(p) for p in MAIN.rglob("station.json") if p.parent.resolve() not in registered])
        policy = json.loads((SYSTEM / "config/workspace.json").read_text())
        groups = dict(policy["groups"])
        self.assertEqual(groups[""], "Front stations")
        visible = [s for s in feed["stations"] if s["label"] not in policy["EXCLUDED_FROM_PAGE"]]
        self.assertEqual(len(visible), len(feed["stations"]) - len(policy["EXCLUDED_FROM_PAGE"]))
        for station in visible:
            self.assertIn(station.get("family") if station.get("family") in groups else "", groups)
        self.assertIn("41_STORY", [s["label"] for s in visible])
        self.assertIn("042_KAIT_STORIES", [s["label"] for s in visible])

    def test_story_prompts_match_source_bytes(self):
        story = next(s for s in listing()["stations"] if s["label"] == "41_STORY")
        back = station_dir("41_STORY", repair=False)
        self.assertEqual(len(story["prompts"]), 5)
        for prompt in story["prompts"]:
            self.assertEqual(prompt["sha256"], hashlib.sha256((back / prompt["file"]).read_bytes()).hexdigest())

if __name__ == "__main__":
    unittest.main()
