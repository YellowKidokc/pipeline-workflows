from engines.pipeline.stations.axiom_mapper import AxiomMapperStation
from engines.pipeline.station_base import Manifest, StationVerdict

def test_axiom_submit_mode(tmp_path):
    src = tmp_path / "a.md"; src.write_text("claim")
    m = Manifest(file_path=str(src), file_hash="h", pipeline_name="p", current_station="s")
    st = AxiomMapperStation(str(tmp_path), str(tmp_path / "out"), queue_dir=str(tmp_path / "q"))
    verdict, _, _ = st.process(src, m)
    assert verdict == StationVerdict.HOLD
