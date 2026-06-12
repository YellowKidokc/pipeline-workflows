import json
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_model_registry_documents_all_model_slots():
    registry = load("models/MODEL_REGISTRY.json")
    slots = registry["slots"]

    expected_m_slots = {f"M{i:02d}" for i in range(1, 13)}
    expected_p_slots = {f"P{i:02d}" for i in range(1, 8)}
    actual_prefixes = {key.split("_", 1)[0] for key in slots}

    assert len(slots) == 19
    assert expected_m_slots <= actual_prefixes
    assert expected_p_slots <= actual_prefixes
    assert registry["_meta"]["source_of_truth"].startswith("models/MODEL_REGISTRY.json")


def test_model_health_and_fallbacks_make_degraded_empty_slots_visible():
    registry = load("models/MODEL_REGISTRY.json")
    health = load("models/MODEL_HEALTH.json")
    fallbacks = load("models/MODEL_FALLBACKS.json")

    assert health["_meta"]["canonical_registry"] == "models/MODEL_REGISTRY.json"
    assert fallbacks["_meta"]["canonical_registry"] == "models/MODEL_REGISTRY.json"

    degraded_slots = set(health["summary"]["degraded"])
    empty_slots = set(health["summary"]["empty"])

    assert degraded_slots == {"M02_embedder", "M03_contradiction"}
    assert empty_slots == {"M11_math_verify", "M12_paper_review", "P04_paper_recommender"}

    for slot_key in degraded_slots | empty_slots:
        assert slot_key in registry["slots"]
        assert slot_key in health["slots"]

    for fallback in fallbacks["fallbacks"].values():
        assert fallback["for_slot"] in degraded_slots
        assert fallback["path"].startswith("X:\\Backside\\_models\\_Models")


def test_nested_model_configs_point_back_to_registry():
    registry = load("models/MODEL_REGISTRY.json")
    registry_slots = set(registry["slots"])

    nlp = load("models/nlp/nlp-pipeline.json")
    assert nlp["_meta"]["canonical_registry"] == "../MODEL_REGISTRY.json"
    assert {item["slot_key"] for item in nlp["slots"]} <= registry_slots

    preference_files = sorted(Path("models/preference").glob("*.json"))
    assert len(preference_files) == 7
    for path in preference_files:
        data = load(str(path))
        assert data["_meta"]["canonical_registry"] == "../MODEL_REGISTRY.json"
        assert data["_meta"]["slot_key"] in registry_slots
