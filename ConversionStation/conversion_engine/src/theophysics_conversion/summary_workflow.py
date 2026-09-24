from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_INPUT_ROOT = Path("Workspace/CONVERTED")
DEFAULT_SUMMARY_ROOT = DEFAULT_INPUT_ROOT / "_summaries"


@dataclass(frozen=True)
class Stage:
    number: int
    name: str
    folder: str
    description: str
    optional: bool = False


STAGES = [
    Stage(0, "workflow-control-ledger", "00-workflow-control-ledger", "Identify the workflow, create a run ID, and hold every step accountable."),
    Stage(1, "conversion-layer", "01-conversion-layer", "Optional station conversion from source formats into Markdown.", True),
    Stage(2, "clean-markdown-layer", "02-clean-markdown-layer", "Clean converted Markdown while preserving Markdown structure."),
    Stage(3, "source-inventory", "03-source-inventory", "Index clean Markdown files by series and source path."),
    Stage(4, "series-vectorization", "04-series-vectorization", "Build or refresh per-series vector/search index from clean Markdown."),
    Stage(5, "summary-drafts", "05-summary-drafts", "Draft summaries from clean Markdown and retrieved series context."),
    Stage(6, "definition-and-claim-drafts", "06-definition-and-claim-drafts", "Draft definitions, key claims, and claim-control notes."),
    Stage(7, "summaries-done", "07-summaries-done", "Summaries are drafted, routed, indexed, and ready for checker review."),
    Stage(8, "ollama-checker", "08-ollama-checker", "Optional local Ollama QA/checker pass.", True),
    Stage(9, "canonical-publish", "09-canonical-publish", "Human-reviewed canonical summaries and definitions.", True),
]


def slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    return "-".join(part for part in cleaned.split("-") if part) or "all-series"


def discover_markdown(input_root: Path, summary_root: Path, series: str | None) -> list[Path]:
    files = []
    for path in input_root.rglob("*.md"):
        if summary_root in path.parents:
            continue
        if series:
            try:
                rel = path.relative_to(input_root)
            except ValueError:
                continue
            if not rel.parts or rel.parts[0].lower() != series.lower():
                continue
        files.append(path)
    return sorted(files)


def source_series(input_root: Path, path: Path) -> str:
    try:
        rel = path.relative_to(input_root)
    except ValueError:
        return "unknown"
    return rel.parts[0] if len(rel.parts) > 1 else "_root"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_scaffold(summary_root: Path) -> None:
    for folder in [
        "by-source",
        "clean-markdown",
        "definitions",
        "index",
        "qa",
        "vectors",
        "workflow-runs",
        "_prompts",
    ]:
        (summary_root / folder).mkdir(parents=True, exist_ok=True)
    for stage in STAGES:
        (summary_root / "workflow-runs" / stage.folder).mkdir(parents=True, exist_ok=True)


def write_inventory(input_root: Path, summary_root: Path, files: list[Path], run_id: str) -> Path:
    index_dir = summary_root / "index"
    index_dir.mkdir(parents=True, exist_ok=True)
    inventory_path = index_dir / f"source-inventory-{run_id}.csv"
    latest_path = index_dir / "source-inventory.latest.csv"
    rows = []
    for path in files:
        rel = path.relative_to(input_root)
        series = source_series(input_root, path)
        summary_path = summary_root / "by-source" / rel.with_suffix(".summary.md")
        rows.append(
            {
                "source_series": series,
                "source_path": str(path),
                "relative_path": str(rel),
                "bytes": path.stat().st_size,
                "sha256": file_sha256(path),
                "summary_path": str(summary_path),
                "status": "inventory_only",
            }
        )
    for target in [inventory_path, latest_path]:
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["source_series", "source_path", "relative_path", "bytes", "sha256", "summary_path", "status"],
            )
            writer.writeheader()
            writer.writerows(rows)
    return inventory_path


def write_stage_ledger(summary_root: Path, run_id: str, selected_stages: list[Stage], dry_run: bool) -> tuple[Path, Path]:
    ledger_dir = summary_root / "workflow-runs"
    csv_path = ledger_dir / f"{run_id}.stage-ledger.csv"
    jsonl_path = ledger_dir / f"{run_id}.events.jsonl"
    now = datetime.now().isoformat(timespec="seconds")
    rows = []
    for stage in selected_stages:
        rows.append(
            {
                "run_id": run_id,
                "stage_number": stage.number,
                "stage_name": stage.name,
                "status": "planned" if dry_run else "pending",
                "started_at": "",
                "finished_at": "",
                "input_count": "",
                "output_count": "",
                "error_count": 0,
                "notes": stage.description,
            }
        )
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "run_id",
                "stage_number",
                "stage_name",
                "status",
                "started_at",
                "finished_at",
                "input_count",
                "output_count",
                "error_count",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    events = [
        {
            "run_id": run_id,
            "timestamp": now,
            "event": "workflow_run_created",
            "dry_run": dry_run,
            "stage_count": len(selected_stages),
        }
    ]
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=True) + "\n")
    return csv_path, jsonl_path


def write_run_manifest(
    summary_root: Path,
    run_id: str,
    args: argparse.Namespace,
    files: list[Path],
    selected_stages: list[Stage],
) -> Path:
    manifest = {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "workflow_name": "HTML to Markdown Summary Workflow",
        "workflow_version": "0.2-layer-0-ledger",
        "input_root": str(args.input_root),
        "summary_root": str(args.summary_root),
        "series": args.series or "all",
        "run_station": args.run_station,
        "dry_run": args.dry_run,
        "file_count": len(files),
        "selected_stages": [asdict(stage) for stage in selected_stages],
    }
    path = summary_root / "workflow-runs" / f"{run_id}.manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Dummy-wired Theophysics summary workflow runner.")
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT_ROOT)
    parser.add_argument("--summary-root", type=Path, default=DEFAULT_SUMMARY_ROOT)
    parser.add_argument("--series", help="Process only one top-level series folder, e.g. genesis-to-quantum.")
    parser.add_argument("--from-stage", type=int, default=0)
    parser.add_argument("--to-stage", type=int, default=7)
    parser.add_argument("--run-station", action="store_true", help="Reserved for running HTML station before summaries.")
    parser.add_argument("--dry-run", action="store_true", help="Print plan and write manifests only.")
    args = parser.parse_args()

    args.input_root = args.input_root.resolve()
    args.summary_root = args.summary_root.resolve()
    ensure_scaffold(args.summary_root)

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    selected = [stage for stage in STAGES if args.from_stage <= stage.number <= args.to_stage]
    files = discover_markdown(args.input_root, args.summary_root, args.series)
    inventory = write_inventory(args.input_root, args.summary_root, files, run_id)
    stage_ledger, event_log = write_stage_ledger(args.summary_root, run_id, selected, args.dry_run)
    manifest = write_run_manifest(args.summary_root, run_id, args, files, selected)

    print(f"run_id={run_id}")
    print(f"input_root={args.input_root}")
    print(f"summary_root={args.summary_root}")
    print(f"series={args.series or 'all'}")
    print(f"markdown_files={len(files)}")
    print(f"inventory={inventory}")
    print(f"manifest={manifest}")
    print(f"stage_ledger={stage_ledger}")
    print(f"event_log={event_log}")
    print("stages:")
    for stage in selected:
        marker = "optional" if stage.optional else "required"
        print(f"  {stage.number}: {stage.name} ({marker}) - {stage.description}")
    if not args.run_station:
        print("station=skipped")
    if args.to_stage >= 7:
        print("process_7=summaries-done target stage selected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
