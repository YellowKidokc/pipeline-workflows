"""station_runner.py — Execute ONE station with I/O contract validation.

Flow: validate input types -> call RUN.bat (local stations) or send the
station prompt to Ollama (prompt-based stations) -> validate output types
-> return a result record.

This is wiring only. It never writes into the station folder, never moves
originals, and only produces files inside the packet's OUTPUT/.

Usage:
    python scripts/station_runner.py claim-extractor path/to/packet
    python scripts/station_runner.py summarizer path/to/packet --timeout 600
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "stations" / "STATION_REGISTRY.json"
CONFIG_PATH = REPO_ROOT / "pipeline.config.json"
BRAIN_UNC = os.environ.get("FORGE_BRAIN_ROOT", r"\\dlowenas\brain")

RUN_CANDIDATES = ("RUN.bat", "START_BIL.bat", "RUN_PIPELINE.bat", "run.bat")
PROMPT_CANDIDATES = ("prompt.md", "PROMPT.md")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def resolve(path_str: str) -> Path:
    path = Path(path_str)
    if path.exists():
        return path
    if path_str[:2].upper() == "X:":
        fallback = Path(BRAIN_UNC + path_str[2:])
        if fallback.exists():
            return fallback
    return path


def find_station_config(name: str) -> dict:
    for config_file in (REPO_ROOT / "stations").glob("*/*.json"):
        if config_file.stem == name:
            return load_json(config_file)
    registry = load_json(REGISTRY_PATH).get("stations", {})
    if name in registry:
        return {"name": name, **registry[name]}
    raise SystemExit(f"station {name!r} not found in stations/ configs or STATION_REGISTRY.json")


def validate_inputs(config: dict, input_dir: Path) -> tuple[list[Path], list[Path]]:
    accepts = [a.lower().lstrip(".") for a in config.get("input", {}).get("accepts", [])]
    files = sorted(p for p in input_dir.rglob("*") if p.is_file())
    if not accepts or "*" in accepts:
        return files, []
    accepted = [f for f in files if f.suffix.lower().lstrip(".") in accepts]
    rejected = [f for f in files if f not in accepted]
    return accepted, rejected


def validate_outputs(config: dict, output_dir: Path, before: set[str]) -> dict:
    produces = [p.lower().lstrip(".") for p in config.get("output", {}).get("produces", [])]
    after = {str(p) for p in output_dir.rglob("*") if p.is_file()}
    new_files = sorted(after - before)
    matching = [
        f for f in new_files
        if not produces or "*" in produces or Path(f).suffix.lower().lstrip(".") in produces
    ]
    return {"new_files": len(new_files), "matching_declared_types": len(matching), "files": new_files[:50]}


def run_bat(config: dict, station_path: Path, packet: Path, timeout: int) -> dict:
    bat = next((station_path / b for b in RUN_CANDIDATES if (station_path / b).is_file()), None)
    if bat is None:
        return {"result": "fail", "notes": f"no RUN.bat found in {station_path}"}
    env = dict(os.environ)
    env["FORGE_INPUT"] = str(packet / "INPUT")
    env["FORGE_OUTPUT"] = str(packet / "OUTPUT")
    env["FORGE_PACKET"] = str(packet)
    try:
        proc = subprocess.run(
            ["cmd", "/c", str(bat)],
            cwd=str(station_path),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"result": "fail", "notes": f"RUN.bat timed out after {timeout}s"}
    log_dir = packet / "LOGS"
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"{config['name']}.run.log").write_text(
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n", encoding="utf-8"
    )
    if proc.returncode != 0:
        return {"result": "fail", "notes": f"RUN.bat exited {proc.returncode}; see LOGS/{config['name']}.run.log"}
    return {"result": "pass", "notes": "RUN.bat exited 0"}


def run_prompt(config: dict, station_path: Path, packet: Path, services: dict, timeout: int) -> dict:
    prompt_file = next((station_path / p for p in PROMPT_CANDIDATES if (station_path / p).is_file()), None)
    if prompt_file is None:
        station_json = station_path / "station.json"
        if station_json.is_file():
            prompt_text = load_json(station_json).get("prompt", "")
        else:
            return {"result": "fail", "notes": f"no prompt.md or station.json in {station_path}"}
    else:
        prompt_text = prompt_file.read_text(encoding="utf-8-sig")
    if not prompt_text.strip():
        return {"result": "fail", "notes": "station prompt is empty"}

    ollama_url = services.get("ollama", "http://localhost:11434").rstrip("/")
    model = services.get("ollama_model", "phi4")
    output_dir = packet / "OUTPUT"
    output_dir.mkdir(parents=True, exist_ok=True)
    processed, failures = 0, []
    accepted, _ = validate_inputs(config, packet / "INPUT")
    for file_path in accepted:
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            failures.append(f"{file_path.name}: unreadable ({exc})")
            continue
        full_prompt = f"{prompt_text}\n\n---\n\nFILE: {file_path.name}\n\n{content[:24000]}"
        request = urllib.request.Request(
            f"{ollama_url}/api/generate",
            data=json.dumps({"model": model, "prompt": full_prompt, "stream": False}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                text = json.loads(response.read().decode("utf-8")).get("response", "")
        except Exception as exc:
            failures.append(f"{file_path.name}: Ollama call failed ({exc})")
            continue
        out_path = output_dir / f"{file_path.stem}.{config['name']}.md"
        out_path.write_text(text, encoding="utf-8")
        processed += 1
    if failures and not processed:
        return {"result": "fail", "notes": "; ".join(failures)[:500]}
    notes = f"{processed} file(s) through {model}"
    if failures:
        notes += f"; {len(failures)} failure(s): " + "; ".join(failures)[:300]
    return {"result": "pass" if not failures else "review", "notes": notes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute one station against a packet with I/O validation.")
    parser.add_argument("station", help="Station name from STATION_REGISTRY.json")
    parser.add_argument("packet", help="Packet folder containing INPUT/ and OUTPUT/")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args(argv)

    config = find_station_config(args.station)
    packet = Path(args.packet)
    (packet / "OUTPUT").mkdir(parents=True, exist_ok=True)
    station_path = resolve(config.get("path", ""))
    services = load_json(CONFIG_PATH).get("services", {}) if CONFIG_PATH.exists() else {}

    record = {"station": args.station, "packet": str(packet), "started_at": utcnow()}

    if not station_path.exists():
        record.update({"result": "fail", "notes": f"station path missing: {config.get('path')}"})
    else:
        accepted, rejected = validate_inputs(config, packet / "INPUT")
        record["input_validation"] = {"accepted": len(accepted), "rejected": [str(r) for r in rejected[:20]]}
        if not accepted:
            record.update({"result": "skip", "notes": "no inputs match the station's accepted types"})
        else:
            before = {str(p) for p in (packet / "OUTPUT").rglob("*") if p.is_file()}
            has_bat = any((station_path / b).is_file() for b in RUN_CANDIDATES)
            if has_bat:
                record.update(run_bat(config, station_path, packet, args.timeout))
            else:
                record.update(run_prompt(config, station_path, packet, services, args.timeout))
            record["output_validation"] = validate_outputs(config, packet / "OUTPUT", before)

    record["finished_at"] = utcnow()
    print(json.dumps(record, indent=2))
    return 0 if record.get("result") in {"pass", "skip", "review"} else 1


if __name__ == "__main__":
    sys.exit(main())
