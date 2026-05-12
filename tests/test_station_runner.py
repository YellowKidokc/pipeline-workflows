from pathlib import Path
from engines.pipeline.station_runner import StationRunner
from engines.pipeline.station_base import StationBase, Manifest, StationVerdict

class Dummy(StationBase):
    def __init__(self, d):
        super().__init__("dummy", d, d)
    def process(self, file_path, manifest):
        return StationVerdict.PASS, 0.9, "ok"

def test_runner_logs(tmp_path):
    fp = tmp_path / "a.txt"; fp.write_text("x")
    m = Manifest(file_path=str(fp), file_hash="h", pipeline_name="p", current_station="dummy")
    r = StationRunner(workflow_name="PaperGrading", log_dir=str(tmp_path))
    verdict, *_ = r.run(Dummy(str(tmp_path)), fp, m)
    assert verdict == StationVerdict.PASS
