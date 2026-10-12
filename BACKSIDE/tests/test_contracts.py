import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - CI may not install jsonschema
    Draft202012Validator = None


PRIORITY_CONTRACTS = [
    "workflow",
    "station",
    "model",
    "preference-event",
    "correction",
    "approval",
    "export-manifest",
    "manifest",
]


def load(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(instance, schema):
    if Draft202012Validator is not None:
        Draft202012Validator(schema).validate(instance)


def test_contract_schema_mirrors_preserve_legacy_schema_paths():
    schema_map = load("contracts/schema-map.json")
    assert set(schema_map["mirrors"]) == set(PRIORITY_CONTRACTS)

    for name in PRIORITY_CONTRACTS:
        paths = schema_map["mirrors"][name]
        contract_path = Path(paths["contract"])
        compatibility_path = Path(paths["compatibility"])

        assert contract_path.is_file()
        assert compatibility_path.is_file()
        assert load(contract_path) == load(compatibility_path)


def test_contract_schemas_are_draft_2020_12_json_objects():
    for path in Path("contracts/schemas").glob("*.schema.json"):
        schema = load(path)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema.get("type") == "object"


def test_new_priority_contracts_validate_representative_payloads():
    approval_schema = load("contracts/schemas/approval.schema.json")
    validate({"approved": True, "by": "David", "at": "2026-06-12T00:00:00Z"}, approval_schema)
    validate({"approved": False, "by": "David", "at": "2026-06-12T00:00:00Z", "reason": "wrong route"}, approval_schema)

    preference_schema = load("contracts/schemas/preference-event.schema.json")
    validate(
        {
            "event_type": "preference_event",
            "timestamp": "2026-06-12T00:00:00Z",
            "source": "approval_gate",
            "signal": "manual_approval",
            "weight": 1.0,
            "subject": "packet-001",
        },
        preference_schema,
    )

    export_schema = load("contracts/schemas/export-manifest.schema.json")
    validate(
        {
            "export_id": "export-001",
            "created_at": "2026-06-12T00:00:00Z",
            "source": {"workflow": "sandbox-file-intake", "packet_id": "packet-001"},
            "artifacts": [{"path": "OUTPUT/result.md", "type": "markdown"}],
        },
        export_schema,
    )
