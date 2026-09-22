import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
import shutil
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "SCRIPTS"))
sys.path.insert(0, str(ROOT / "EVIDENCE/SCRIPTS"))
import api_workbench as app
import article_stack
from export_portable import export
from portable_session import Session


class PortableTests(unittest.TestCase):
    def test_relocation_and_launcher_arguments(self):
        with tempfile.TemporaryDirectory(prefix="API relocated space ") as d:
            root = Path(d)
            app.initialize(root)
            env = app.environment(root)
            self.assertEqual(env["LEAN4_ROOT"], str(root / "LEAN4"))
            self.assertTrue(env["LEAN4_READING_LIBRARY"].startswith(str(root)))
            cmd = app.command("LEAN4", root=root)
            self.assertIn("--count-only", cmd)
            self.assertEqual(cmd[cmd.index("--workers") + 1], "12")
            self.assertIn("--auto", app.command("LEAN4", "watch", root))

    def test_snapshot_nested_inputs_ignores_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); app.initialize(root)
            p = root / "LEAN4/INBOX/Some Project"
            p.mkdir(); (p / "A.lean").write_text("example : True := by trivial")
            (p / ".lake").mkdir(); (p / ".lake/Ignore.lean").write_text("ignore")
            self.assertEqual(len(app.snapshot("LEAN4", root)), 1)

    def test_original_bytes_and_corrupt_stack(self):
        original = b"\xef\xbb\xbfOriginal\r\nwith mixed\nlines\r\n"
        stacked = article_stack.stack("Review", original)
        self.assertEqual(article_stack.original_of(stacked), original)
        with self.assertRaises(ValueError):
            article_stack.original_of(stacked + b"changed")

    def test_session_survives_source_move(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); p = root / "a.md"; p.write_text("original")
            session = Session(root, "deepseek", "test", 12)
            session.select([(p, False, None)])
            p.rename(root / "moved.md")
            session.mark(p, "SUCCESS")
            self.assertIn("SUCCESS", session.path.read_text(encoding="utf-8-sig"))
            self.assertIn("a.md", session.path.read_text(encoding="utf-8-sig"))

    def test_export_excludes_private_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "source"; root.mkdir()
            (root / "safe.py").write_text("print('safe')")
            (root / "keys.local.json").write_text('{"key":"private-test-only"}')
            (root / "paper.md").write_text("private paper")
            (root / "PACKAGE_FILES.json").write_text(json.dumps({"files": ["safe.py", "PACKAGE_FILES.json"]}))
            target = export(Path(d) / "portable.zip", root)
            with zipfile.ZipFile(target) as z:
                self.assertNotIn("APIs/keys.local.json", z.namelist())
                self.assertNotIn("APIs/paper.md", z.namelist())

    def test_second_launcher_cannot_lock_same_lane(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); app.initialize(root)
            with app.lane_lock("LEAN4", root):
                code = "import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); import api_workbench as a; c=a.lane_lock('LEAN4',Path(sys.argv[2])); c.__enter__()"
                res = subprocess.run([sys.executable, "-c", code, str(ROOT / "SCRIPTS"), str(root)], capture_output=True)
                self.assertNotEqual(res.returncode, 0)

    def test_relocated_evidence_mock_success_failure_and_original(self):
        with tempfile.TemporaryDirectory(prefix="Portable Evidence ") as d:
            root = Path(d)
            scripts = root / "EVIDENCE/SCRIPTS"
            shutil.copytree(ROOT / "EVIDENCE/SCRIPTS", scripts, ignore=shutil.ignore_patterns("__pycache__"))
            inbox = root / "EVIDENCE/INBOX/Series folder/deeper"
            inbox.mkdir(parents=True)
            original = b"\xef\xbb\xbf# Original\r\nPreserve all bytes.\r\n"
            (inbox / "good.md").write_bytes(original)
            (inbox / "bad.md").write_text("test failure")
            code = '''
import sys
sys.path.insert(0, sys.argv[1])
import turbo_pipeline_runner as p
def fake(*args, **kwargs):
    return 'clean_title: Good\ndomain_primary: theology\npaper_rating: 7\none_sentence_finding: Mock only\n\n# Mock companion\n', {}
p.call_deepseek_raw = fake
real = p.PaperProcessor.process_single_paper
def process(self, path, *args, **kwargs):
    if path.name == 'bad.md': raise RuntimeError('Expected fixture failure')
    return real(self, path, *args, **kwargs)
p.PaperProcessor.process_single_paper = process
sys.argv = ['test', '--single-batch', '--provider', 'deepseek', '--model', 'mock-only']
raise SystemExit(p.main())
'''
            # Escape newlines in the fixture response inside the subprocess source.
            code = code.replace("return 'clean_title: Good\ndomain_primary: theology\npaper_rating: 7\none_sentence_finding: Mock only\n\n# Mock companion\n', {}",
                                "return 'clean_title: Good\\ndomain_primary: theology\\npaper_rating: 7\\none_sentence_finding: Mock only\\n\\n# Mock companion\\n', {}")
            result = subprocess.run([sys.executable, "-X", "utf8", "-c", code, str(scripts)], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            reports = list((root / "EVIDENCE/OUTBOX/FOR_SUBSTACK").glob("*.md"))
            self.assertEqual(len(reports), 1, result.stdout + result.stderr)
            self.assertEqual(article_stack.original_of(reports[0].read_bytes()), original)
            sessions = list((root / "EVIDENCE/OUTBOX/RUNS").glob("*/PAPERS.csv"))
            self.assertEqual(len(sessions), 1)
            ledger = sessions[0].read_text(encoding="utf-8-sig")
            self.assertIn("SUCCESS", ledger); self.assertIn("FAILED", ledger)
            self.assertTrue(any(p.read_bytes() == original for p in (root / "EVIDENCE/PROCESSED_ORIGINALS").iterdir()))

    def test_watch_waits_for_settling_and_does_not_repeat_unchanged_input(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); app.initialize(root)
            (root / "LEAN4/INBOX/a.lean").write_text("example : True := by trivial")
            values = dict(app.DEFAULTS, watch_lanes=["LEAN4"], settle_seconds=5)
            child = mock.Mock(returncode=0)
            child.poll.return_value = 0
            with mock.patch.object(app, "config", return_value=values), \
                 mock.patch.object(app, "environment", return_value={"DEEPSEEK_API_KEY": "mock-only"}), \
                 mock.patch.object(app.time, "monotonic", side_effect=[0, 2, 6, 8]), \
                 mock.patch.object(app.time, "sleep", side_effect=[None, None, None, KeyboardInterrupt]), \
                 mock.patch.object(app.subprocess, "Popen", return_value=child) as start:
                self.assertEqual(app.watch(root), 0)
                self.assertEqual(start.call_count, 1)

    def test_lean_reader_retains_per_session_csv(self):
        with tempfile.TemporaryDirectory(prefix="Lean portable ") as d:
            root = Path(d)
            scripts = root / "LEAN4/SCRIPTS"
            shutil.copytree(ROOT / "LEAN4/SCRIPTS", scripts, ignore=shutil.ignore_patterns("__pycache__"))
            p = root / "LEAN4/INBOX/a.lean"; p.parent.mkdir(parents=True)
            p.write_text("example : True := by trivial")
            code = '''
import os,sys
from pathlib import Path
root=Path(sys.argv[1])
os.environ['LEAN4_ROOT']=str(root/'LEAN4')
os.environ['LEAN4_READING_LIBRARY']=str(root/'LEAN4/OUTBOX/READING_LIBRARY')
sys.path.insert(0,str(root/'LEAN4/SCRIPTS'))
import pipeline as p
class Client:
    def __init__(self,provider,model): self.provider,self.model=provider,model
p.Client=Client
p.analyze_reader=lambda *args: '# Mock source explanation'
sys.argv=['test','deepseek','--auto','--reader-papers','--model','mock-only']
raise SystemExit(p.main())
'''
            res = subprocess.run([sys.executable, "-X", "utf8", "-c", code, str(root)], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            ledgers = list((root / "LEAN4/OUTBOX/RUNS").glob("*/PAPERS.csv"))
            self.assertEqual(len(ledgers), 1)
            self.assertIn("REVIEW_COMPLETE", ledgers[0].read_text(encoding="utf-8-sig"))
            self.assertEqual(p.read_text(), "example : True := by trivial")


if __name__ == "__main__":
    unittest.main()
