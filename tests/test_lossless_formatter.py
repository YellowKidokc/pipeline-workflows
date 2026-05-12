from engines.pipeline.stations.lossless_formatter import LosslessFormatterStation
from engines.pipeline.station_base import Manifest

def test_lossless(tmp_path):
    src = tmp_path / "n.txt"; src.write_text("um this this is text")
    m = Manifest(file_path=str(src), file_hash="h", pipeline_name="p", current_station="s")
    st = LosslessFormatterStation(str(tmp_path), str(tmp_path / "out"))
    verdict, score, _ = st.process(src, m)
    assert score > 0
