"""canary.py — Health check for every station in STATION_REGISTRY.json.

For each station: does the path exist? does RUN.bat exist (when claimed)?
do prompt-based stations have their prompt/station.json? Reports
active / degraded / dead. Read-only — never modifies stations.

Usage:
    python scripts/canary.py                 # table to stdout
    python scripts/canary.py --json          # JSON report to stdout
    python scripts/canary.py --json -o LOGS/canary.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "stations" / "STATION_REGISTRY.json"

# When the X: drive letter is not mounted in this session (services, schtasks),
# fall back to the underlying NAS share.
BRAIN_UNC = os.environ.get("FORGE_BRAIN_ROOT", r"\\dlowenas\brain")

RUN_CANDIDATES = ("RUN.bat", "START_BIL.bat", "RUN_PIPELINE.bat", "run.bat")
PROMPT_CANDIDATES = ("prompt.md", "station.json", "PROMPT.md")


def resolve(path_str: str) -> Path:
    path = Path(path_str)
    if path.exists():
        return path
    if path_str[:2].upper() == "X:":
        fallback = Path(BRAIN_UNC + path_str[2:])
        if fallback.exists():
            return fallback
    return path


def check_station(name: str, entry: dict) -> dict:
    path = resolve(entry.get("path", ""))
    result = {
        "name": name,
        "path": entry.get("path", ""),
        "category": entry.get("category", ""),
        "checks": {},
    }
    checks = result["checks"]
    checks["path_exists"] = path.exists()
    if not checks["path_exists"]:
        result["verdict"] = "dead"
        return result

    has_run_bat_claimed = bool(entry.get("has_run_bat"))
    run_bat_found = any((path / b).is_file() for b in RUN_CANDIDATES) or bool(list(path.glob("*.bat")))
    prompt_found = any((path / p).is_file() for p in PROMPT_CANDIDATES)
    # Separate packages (conversion_station, graphify, ...) expose ps1/pyproject/package entry points.
    package_entry = bool(
        list(path.glob("*.ps1")) or list(path.glob("bin/*.ps1")) or list(path.glob("bin/*.bat"))
        or (path / "pyproject.toml").is_file() or (path / "package.json").is_file()
        or list(path.glob("*.py"))
    )
    checks["run_bat_found"] = run_bat_found
    checks["prompt_found"] = prompt_found
    checks["package_entry"] = package_entry

    try:
        non_empty = any(path.iterdir())
    except OSError:
        non_empty = False
    checks["non_empty"] = non_empty

    if has_run_bat_claimed and not run_bat_found:
        result["verdict"] = "degraded"
        result["reason"] = "registry claims RUN.bat but none found"
    elif not non_empty:
        result["verdict"] = "degraded"
        result["reason"] = "station folder is empty"
    elif not has_run_bat_claimed and not run_bat_found and not prompt_found and not package_entry:
        result["verdict"] = "degraded"
        result["reason"] = "no RUN.bat, prompt, or package entry point — nothing to execute"
    else:
        result["verdict"] = "active"
    return result


def run_canary(registry_path: Path = REGISTRY_PATH) -> dict:
    registry = json.loads(registry_path.read_text(encoding="utf-8-sig"))
    stations = registry.get("stations", {})
    results = [check_station(name, entry) for name, entry in sorted(stations.items())]
    summary = {"active": 0, "degraded": 0, "dead": 0}
    for r in results:
        summary[r["verdict"]] += 1
    return {
        "ran_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "registry": str(registry_path),
        "total": len(results),
        "summary": summary,
        "stations": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ping every station in STATION_REGISTRY.json.")
    parser.add_argument("--registry", default=str(REGISTRY_PATH))
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    parser.add_argument("-o", "--output", default=None, help="Write report to a file")
    args = parser.parse_args(argv)

    report = run_canary(Path(args.registry))

    if args.json or args.output:
        payload = json.dumps(report, indent=2)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(payload + "\n", encoding="utf-8")
        if args.json:
            print(payload)
    if not args.json:
        for r in report["stations"]:
            mark = {"active": "OK  ", "degraded": "WARN", "dead": "DEAD"}[r["verdict"]]
            reason = f"  ({r['reason']})" if r.get("reason") else ""
            print(f"[{mark}] {r['name']:32} {r['verdict']:8}{reason}")
        s = report["summary"]
        print(f"\n{report['total']} stations — active: {s['active']}, degraded: {s['degraded']}, dead: {s['dead']}")
        print("Known-good baseline: at least 23 active.")
    return 0 if report["summary"]["dead"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
