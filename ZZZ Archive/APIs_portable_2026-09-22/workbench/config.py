from __future__ import annotations
import json, os
from pathlib import Path
from .providers import MockProvider, Provider

def load_config(root: Path) -> dict:
    path = root / "CONFIG" / "station.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    local = root / "CONFIG" / "private.local.json"
    if local.exists():
        private = json.loads(local.read_text(encoding="utf-8"))
        config = _merge(config, private)
    return config

def _merge(a, b):
    out = dict(a)
    for key, value in b.items(): out[key] = _merge(out[key], value) if isinstance(value, dict) and isinstance(out.get(key), dict) else value
    return out

def make_provider(config: dict):
    p = config["provider"]
    if p["name"] == "mock": return MockProvider()
    env_name = p.get("credential_env") or Provider.SPECS[p["name"]][1]
    key = os.environ.get(env_name) or p.get("api_key")
    if not key: raise RuntimeError(f"credential missing: set {env_name} or CONFIG/private.local.json")
    return Provider(p["name"], p["model"], key, p.get("timeout_seconds", 120), p.get("retry_limit", 3))
