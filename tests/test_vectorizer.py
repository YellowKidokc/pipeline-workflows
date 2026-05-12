from engines.pipeline.stations.vectorizer import VectorizerStation
from engines.pipeline.station_base import Manifest

def test_vectorizer(tmp_path):
    src = tmp_path / "v.md"; src.write_text("a\n\n b")
    out = tmp_path / "out"
    m = Manifest(file_path=str(src), file_hash="h", pipeline_name="p", current_station="s")
    st = VectorizerStation(str(tmp_path), str(out))
    verdict, score, _ = st.process(src, m)
    assert (src.with_suffix('.md.vectors.json')).exists()
