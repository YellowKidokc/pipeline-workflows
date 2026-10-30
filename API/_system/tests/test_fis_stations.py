"""10_FIS stations against the real David-OSv3 engine (set ONE_MENU_DAVID_OSV3, or david_osv3 in paths.json).

Skipped when no FIS engine is reachable: these stations are wrappers and must not be tested against a fake engine.
"""
import hashlib
import http.server
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

HOME = Path(__file__).resolve().parents[1]
MAIN = HOME.parent
sys.path.insert(0, str(HOME))
STATIONS = {n: MAIN / "10_FIS" / f"{n}_{name}" / "BACKSIDE" / f"{n}_{name.lower()}.py"
            for n, name in (("101", "FIS_INVENTORY"), ("102", "FIS_EXACT_COPIES"), ("103", "FIS_CLASSIFY"))}
SECRET = "CONTENT-MUST-NOT-LEAVE-THE-MACHINE"


def engine_home():
    try:
        from engine import fis
        return fis.osv3()
    except Exception:
        return None


def tree_hashes(root: Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink():
            out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


@unittest.skipUnless(engine_home(), "David-OSv3 FIS engine not reachable (set ONE_MENU_DAVID_OSV3)")
class FisStations(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.a, self.b = self.tmp / "root_a", self.tmp / "root_b"
        (self.a / "notes").mkdir(parents=True)
        (self.b / "copies").mkdir(parents=True)
        text = f"# Paper\n\nThe resurrection argument, version one. {SECRET}\n" * 20
        (self.a / "notes" / "paper.md").write_text(text)
        (self.b / "copies" / "renamed copy.md").write_text(text)                       # identical, different name
        (self.b / "copies" / "paper revised.md").write_text(text.replace("version one", "version two"))  # same size, revised
        for i in range(19):                    # 11 documents of 20 files: "mixed" at 0.55, below 0.6, so the rules ask
            (self.a / "notes" / f"misc_{i}.{'txt' if i < 10 else 'png'}").write_text(f"x{i}" * (i + 1))
        os.symlink(self.tmp / "nowhere", self.a / "notes" / "broken link.md")         # unreadable: stat fails
        self.db = self.tmp / "out" / "fis.sqlite"
        self.out = self.tmp / "out"
        self.env = dict(os.environ, ONE_MENU_DAVID_OSV3=str(engine_home()))

    def run_station(self, n, *args):
        r = subprocess.run([sys.executable, str(STATIONS[n]), *args, "--db", str(self.db), "--outbox", str(self.out / n)],
                           env=self.env, capture_output=True, text=True, timeout=300)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        return r.stdout

    def inventory(self):
        self.run_station("101", str(self.a), str(self.b), "--apply")
        return sqlite3.connect(self.db)

    def test_dry_run_scans_nothing(self):
        self.run_station("101", str(self.a), str(self.b))
        self.assertFalse(self.db.exists())
        self.assertTrue(any("PLAN" in p.name for p in (self.out / "101").iterdir()))

    def test_identical_files_with_different_names_are_one_copy_group(self):
        con = self.inventory()
        self.run_station("102", "--apply")
        groups = [json.loads(p) for (p,) in con.execute("SELECT paths FROM dup_groups")]
        names = [sorted(Path(x).name for x in g) for g in groups]
        self.assertIn(["paper.md", "renamed copy.md"], names)

    def test_revised_document_stays_distinct(self):
        con = self.inventory()
        self.run_station("102", "--apply")
        for (p,) in con.execute("SELECT paths FROM dup_groups"):
            self.assertNotIn("paper revised.md", [Path(x).name for x in json.loads(p)])

    def test_unreadable_files_are_reported(self):
        con = self.inventory()
        reasons = dict(con.execute("SELECT path, reason FROM skipped"))
        self.assertTrue(any(k.endswith("broken link.md") and v.startswith("unreadable") for k, v in reasons.items()), reasons)
        (self.b / "copies" / "renamed copy.md").unlink()                 # gone before hashing: must be reported, not dropped
        self.run_station("102", "--apply")
        reasons = dict(con.execute("SELECT path, reason FROM skipped"))
        self.assertTrue(any(k.endswith("renamed copy.md") and v == "unreadable while hashing" for k, v in reasons.items()))
        report = next((self.out / "102").glob("FIS EXACT COPIES · scan *.md")).read_text()
        self.assertIn("renamed copy.md", report)

    def test_authority_left_unresolved_without_approval_evidence(self):
        (self.a / "notes" / "paper FINAL CANON.md").write_text("final " * 50)
        con = self.inventory()
        self.run_station("103")
        facets = {f for (f,) in con.execute("SELECT DISTINCT facet FROM inferences")}
        self.assertFalse(facets & {"authority", "canon", "canonical"}, facets)
        self.assertEqual({"shadow"}, {s for (s,) in con.execute("SELECT DISTINCT status FROM inferences")})

    def test_no_source_file_changes_and_no_output_inside_a_root(self):
        before = tree_hashes(self.a) | tree_hashes(self.b)
        self.inventory()
        self.run_station("102", "--apply")
        self.run_station("103")
        self.assertEqual(before, tree_hashes(self.a) | tree_hashes(self.b))
        r = subprocess.run([sys.executable, str(STATIONS["101"]), str(self.a), "--apply", "--db", str(self.a / "fis.sqlite"),
                            "--outbox", str(self.out / "x")], env=self.env, capture_output=True, text=True, timeout=120)
        self.assertNotEqual(0, r.returncode)
        self.assertIn("protected root", r.stderr)
        self.assertFalse((self.a / "fis.sqlite").exists())

    def test_classify_sends_names_only_through_forge(self):
        seen = []

        class Forge(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers["Content-Length"])).decode()
                seen.append((self.path, body))
                reply = {"choices": [{"message": {"content": '{"kind": "mixed", "domain": "test", "purpose": "t", "confidence": 0.4}'}}]}
                data = json.dumps(reply).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *a):
                pass

        srv = http.server.HTTPServer(("127.0.0.1", 0), Forge)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            con = self.inventory()
            open_q = con.execute("SELECT COUNT(*) FROM questions WHERE status='open'").fetchone()[0]
            self.env["FORGE_URL"] = f"http://127.0.0.1:{srv.server_port}"
            self.run_station("103", "--apply")
        finally:
            srv.shutdown()
            srv.server_close()
        self.assertGreater(open_q, 0, "the fixture should leave at least one folder unresolved")
        self.assertEqual(open_q, len(seen))
        for path, body in seen:
            self.assertEqual("/v1/chat/completions", path)
            self.assertNotIn(SECRET, body)
        if seen:
            self.assertTrue(con.execute("SELECT COUNT(*) FROM inferences WHERE source LIKE 'llm:forge:%'").fetchone()[0])


if __name__ == "__main__":
    unittest.main()
