from engines.pipeline.stations.paper_grader import PaperGraderStation
from engines.pipeline.station_base import Manifest, StationVerdict

def test_submit_mode(tmp_path):
    src = tmp_path / "g.md"; src.write_text("hello")
    m = Manifest(file_path=str(src), file_hash="h", pipeline_name="p", current_station="s")
    st = PaperGraderStation(str(tmp_path), str(tmp_path / "out"), queue_dir=str(tmp_path / "q"))
    verdict, _, _ = st.process(src, m)
    assert verdict == StationVerdict.HOLD
