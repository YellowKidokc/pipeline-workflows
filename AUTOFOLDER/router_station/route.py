"""
Portable file router.

Drop this file (plus FolderWatcher.py and route.yaml) into any folder.
It watches configured source folders and routes incoming files according
to ordered rules: copy, move, or run a command.

Usage:
  python route.py                 # watch and route forever
  python route.py --backfill      # route all existing matching files once
  python route.py --dry-run       # log what would be done
  python route.py --once          # one pass, then exit
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time
from typing import Any

from FolderWatcher import FolderWatcher

HERE = pathlib.Path(__file__).resolve().parent
CONFIG = HERE / "route.yaml"
DEFAULT_LOG = HERE / "route.log"
DEFAULT_STATE = HERE / ".route_state.json"


def log(path: pathlib.Path, msg: str) -> None:
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace"), flush=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config(path: pathlib.Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required: pip install pyyaml") from exc
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_state(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {"routed": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(path: pathlib.Path, state: dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    tmp.replace(path)


def expand_placeholders(cmd: str, src: pathlib.Path, dest: pathlib.Path | None) -> str:
    mapping = {
        "{path}": str(src),
        "{name}": src.name,
        "{stem}": src.stem,
        "{ext}": src.suffix,
        "{parent}": str(src.parent),
    }
    if dest:
        mapping["{dest}"] = str(dest)
    for key, val in mapping.items():
        cmd = cmd.replace(key, val)
    return cmd


def _patterns(rule: dict[str, Any]) -> list[str]:
    raw = rule.get("match", "*")
    if isinstance(raw, str):
        return [raw]
    return list(raw)


def matches(rule: dict[str, Any], path: pathlib.Path) -> bool:
    return any(fnmatch.fnmatch(path.name, pat) for pat in _patterns(rule))


def route_file(
    path: pathlib.Path,
    rule: dict[str, Any],
    state: dict[str, Any],
    dry_run: bool,
    log_file: pathlib.Path,
) -> None:
    action = rule.get("action", "copy")
    destinations = rule.get("destinations", [])
    if isinstance(destinations, str):
        destinations = [destinations]

    log(log_file, f"rule '{rule.get('name', 'unnamed')}': {action} {path.name}")

    for dest_str in destinations:
        dest = pathlib.Path(dest_str).expanduser()
        dest.mkdir(parents=True, exist_ok=True)
        target = dest / path.name

        if dry_run:
            log(log_file, f"  would {action} -> {target}")
            continue

        if action == "move":
            shutil.move(str(path), str(target))
            path = target
        elif action == "copy":
            shutil.copy2(str(path), str(target))
        else:
            log(log_file, f"  unknown action: {action}")
            continue

        state["routed"][str(path)] = {
            "time": dt.datetime.now().isoformat(),
            "rule": rule.get("name"),
            "dest": str(target),
        }

    command = rule.get("command")
    if command:
        cmd = expand_placeholders(command, path, None)
        log(log_file, f"  command: {cmd}")
        if not dry_run:
            rc = subprocess.run(cmd, shell=True, check=False).returncode
            if rc != 0:
                log(log_file, f"  warning: command exited {rc}")


def on_change(
    changed: list[tuple[str, pathlib.Path]],
    config: dict[str, Any],
    state: dict[str, Any],
    dry_run: bool,
    log_file: pathlib.Path,
) -> None:
    rules = config.get("routes", [])
    files = {path for event, path in changed if event in ("created", "modified")}

    for path in sorted(files):
        if not path.exists():
            continue
        if str(path) in state.get("routed", {}):
            continue
        for rule in rules:
            if matches(rule, path):
                route_file(path, rule, state, dry_run, log_file)
                break
        else:
            log(log_file, f"no route for {path.name}")


def _resolve_glob_pattern(item: str) -> list[pathlib.Path]:
    """Resolve a path (possibly containing globs) relative to HERE."""
    raw = pathlib.Path(item).expanduser()
    if raw.is_absolute():
        full = raw
    else:
        full = HERE / raw

    # pathlib glob does not handle '..' in patterns, so resolve the base.
    parts = list(full.parts)
    glob_index = next(
        (i for i, part in enumerate(parts) if "*" in str(part) or "?" in str(part)),
        None,
    )
    if glob_index is None:
        return [full.resolve()] if full.exists() else []

    base_parts = parts[:glob_index]
    if not base_parts:
        base = pathlib.Path(".")
    else:
        base = pathlib.Path(*base_parts).resolve()
    if not base.exists():
        return []

    rest = pathlib.Path(*parts[glob_index:])
    return list(base.glob(str(rest)))


def discover_watch_paths(config: dict[str, Any]) -> list[pathlib.Path]:
    watch = config.get("watch", [])
    if not watch:
        return [HERE]

    paths: list[pathlib.Path] = []
    for item in watch if isinstance(watch, list) else [watch]:
        for match in _resolve_glob_pattern(item):
            if match.is_dir():
                paths.append(match.resolve())
            else:
                print(f"warning: watch path is not a directory: {match}", file=sys.stderr)
    return paths


def backfill(
    config: dict[str, Any],
    state: dict[str, Any],
    dry_run: bool,
    log_file: pathlib.Path,
) -> None:
    watch_paths = discover_watch_paths(config)
    rules = config.get("routes", [])
    patterns = set()
    for rule in rules:
        for pat in _patterns(rule):
            patterns.add(pat)

    files: list[pathlib.Path] = []
    for root in watch_paths:
        if not root.exists():
            continue
        for pat in patterns:
            files.extend(root.glob(pat))

    log(log_file, f"backfill: {len(files)} candidate file(s)")
    for path in sorted(set(files)):
        if str(path) in state.get("routed", {}):
            continue
        if not path.is_file():
            continue
        for rule in rules:
            if matches(rule, path):
                route_file(path, rule, state, dry_run, log_file)
                break


def main() -> int:
    ap = argparse.ArgumentParser(description="Portable file router.")
    ap.add_argument("--config", type=pathlib.Path, default=CONFIG, help="path to route.yaml")
    ap.add_argument("--dry-run", action="store_true", help="log actions without executing")
    ap.add_argument("--backfill", action="store_true", help="route existing files once")
    ap.add_argument("--once", action="store_true", help="one pass, then exit")
    ap.add_argument("--debounce", type=float, default=2.0)
    args = ap.parse_args()

    if not args.config.exists():
        print(f"config not found: {args.config}", file=sys.stderr)
        return 1

    config = load_config(args.config)
    log_file = pathlib.Path(config.get("log", DEFAULT_LOG)).expanduser()
    state_file = pathlib.Path(config.get("state", DEFAULT_STATE)).expanduser()
    state = load_state(state_file)

    watch_paths = discover_watch_paths(config)
    if not watch_paths:
        print("no watch paths configured or resolved", file=sys.stderr)
        return 1

    log(log_file, f"router started: {HERE.name}")
    log(log_file, f"watching: {', '.join(str(p) for p in watch_paths)}")

    if args.backfill:
        backfill(config, state, args.dry_run, log_file)
        save_state(state_file, state)
        if args.once:
            return 0

    def callback(changed):
        try:
            on_change(changed, config, state, args.dry_run, log_file)
            save_state(state_file, state)
        except Exception as e:
            log(log_file, f"error in callback: {e}")

    watcher = FolderWatcher(
        path=[str(p) for p in watch_paths],
        callback=callback,
        recursive=False,
        debounce=args.debounce,
        return_mode="files",
    )

    if args.once:
        log(log_file, "--once: nothing to watch; exiting")
        return 0

    try:
        watcher.run_forever()
    except KeyboardInterrupt:
        log(log_file, "stopped by user")
    return 0


if __name__ == "__main__":
    sys.exit(main())
