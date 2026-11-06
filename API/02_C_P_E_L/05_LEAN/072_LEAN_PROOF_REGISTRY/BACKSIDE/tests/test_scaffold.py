from fastapi.testclient import TestClient

from app.main import app


def test_scaffold_does_not_claim_implementation() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["implementation"] == "CODEX_ONLINE_REQUIRED"


def test_governance_separates_interpretation() -> None:
    data = TestClient(app).get("/governance").json()
    assert data["canonical_sources"] == "READ_ONLY"
    assert data["negative_controls_first"] is True
    assert data["interpretation_is_formal_consequence"] is False
    assert data["implementation_status"] == "SCAFFOLD_ONLY"

