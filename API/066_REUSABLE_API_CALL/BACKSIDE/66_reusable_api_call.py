"""66_REUSABLE_API_CALL: configuration-driven station for repeatable questions and output contracts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir())
sys.path.insert(0, str(ROOT / "_system"))

from engine.output import markdown_to_html, page
from engine.station import ItemResult, Station

LABEL = "66_REUSABLE_API_CALL"
HERE = Path(__file__).resolve().parent


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("PyYAML is required for the reusable station. Run SETUP.bat or: py -3 -m pip install pyyaml") from exc
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path.name} must contain one YAML object.")
    return value


ACTIVE = load_yaml(HERE / "ACTIVE.yaml")
QUESTIONS_PATH = HERE / str(ACTIVE.get("active_questions", "questions.yaml"))
OUTPUTS_PATH = HERE / str(ACTIVE.get("active_outputs", "outputs.yaml"))
PROMPT_PATH = HERE / str(ACTIVE.get("active_prompt", "PROMPT.md"))
QUESTIONS_DOC = load_yaml(QUESTIONS_PATH)
OUTPUTS_DOC = load_yaml(OUTPUTS_PATH)
QUESTIONS = [q for q in QUESTIONS_DOC.get("questions", []) if isinstance(q, dict) and q.get("enabled", False)]
PROFILE_NAME = str(ACTIVE.get("active_output_profile", "json_and_markdown"))
PROFILE = OUTPUTS_DOC.get("profiles", {}).get(PROFILE_NAME)
if not isinstance(PROFILE, dict):
    raise SystemExit(f"Unknown output profile: {PROFILE_NAME}")
if not PROMPT_PATH.is_file():
    raise SystemExit(f"Prompt not found: {PROMPT_PATH}")
BASE_PROMPT = PROMPT_PATH.read_text(encoding="utf-8-sig").strip()


def stable_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def question_prompt(q: dict[str, Any], document: str) -> str:
    key = str(q.get("output_key") or q.get("id"))
    fields = q.get("required_fields") or []
    field_text = ", ".join(map(str, fields)) if fields else "No fixed field list."
    return f"""{BASE_PROMPT}

## Assigned question
ID: {q.get("id")}
Title: {q.get("title")}
Question: {q.get("question")}

## Output contract
{PROFILE.get("instruction", "")}
Top-level output key: {key}
Expected answer type: {q.get("answer_type", "object")}
Required fields: {field_text}

## Frozen source document
{document}
"""


def bundle_prompt(chunk: list[dict[str, Any]], document: str) -> str:
    blocks = []
    keys = []
    for q in chunk:
        key = str(q.get("output_key") or q.get("id"))
        keys.append(key)
        blocks.append(
            f"### {q.get('id')} — {q.get('title')}\n"
            f"OUTPUT KEY: {key}\n"
            f"ANSWER TYPE: {q.get('answer_type', 'object')}\n"
            f"REQUIRED FIELDS: {', '.join(map(str, q.get('required_fields') or []))}\n"
            f"QUESTION: {q.get('question')}"
        )
    return f"""{BASE_PROMPT}

Answer all questions below independently over the same document.
Return one valid JSON object whose keys are exactly: {", ".join(keys)}.
Do not merge questions or omit a key. Use null or an empty list when the document cannot answer.

{chr(10).join(chr(10) + block for block in blocks)}

## Frozen source document
{document}
"""


def chunks(values: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    size = max(1, size)
    return [values[i:i + size] for i in range(0, len(values), size)]


def check_fields(q: dict[str, Any], value: Any, warnings: list[str]) -> None:
    required = list(q.get("required_fields") or [])
    if not required:
        return
    records = value if isinstance(value, list) else [value]
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            warnings.append(f"{q.get('id')}[{index}]: expected an object with fields {required}")
            continue
        missing = [field for field in required if field not in record]
        if missing:
            warnings.append(f"{q.get('id')}[{index}]: missing fields: {', '.join(missing)}")


def markdown_report(title: str, results: dict[str, Any]) -> str:
    lines = [f"# {title}", "", f"Output profile: {PROFILE_NAME}", f"Questions answered: {len(results)}", ""]
    for q in QUESTIONS:
        key = str(q.get("output_key") or q.get("id"))
        if key not in results:
            continue
        value = results[key]
        lines += [f"## {q.get('title', key)}", ""]
        if isinstance(value, str):
            lines += [value, ""]
        else:
            lines += ["```json", json.dumps(value, indent=2, ensure_ascii=False), "```", ""]
    return "\n".join(lines)


def process(ctx):
    if not QUESTIONS:
        ctx.errors.append("No questions are enabled in questions.yaml")
        return None
    mode = str(ACTIVE.get("execution", {}).get("mode", "separate")).lower()
    results: dict[str, Any] = {}

    if mode == "bundle":
        maximum = int(ACTIVE.get("execution", {}).get("max_questions_per_bundle", 6))
        for number, chunk in enumerate(chunks(QUESTIONS, maximum), 1):
            extra = stable_hash({"questions": chunk, "profile": PROFILE})
            data = ctx.cached(
                f"bundle-{number}",
                lambda part=chunk: ctx.call_json(f"bundle_{number}", bundle_prompt(part, ctx.text)),
                extra=extra,
            )
            if isinstance(data, dict):
                for q in chunk:
                    key = str(q.get("output_key") or q.get("id"))
                    if key in data:
                        results[key] = data[key]
                    else:
                        ctx.warnings.append(f"{q.get('id')}: output key {key} was missing")
            elif data is not None:
                ctx.errors.append(f"bundle {number}: expected a JSON object")
    else:
        for q in QUESTIONS:
            qid = str(q.get("id"))
            key = str(q.get("output_key") or qid)
            fmt = str(PROFILE.get("format", "json")).lower()
            extra = stable_hash({"question": q, "profile": PROFILE})
            if fmt in ("markdown", "text", "raw"):
                value = ctx.cached(
                    qid,
                    lambda spec=q: ctx.call_text(qid, question_prompt(spec, ctx.text)),
                    extra=extra,
                )
                if value is not None:
                    results[key] = value
            else:
                data = ctx.cached(
                    qid,
                    lambda spec=q: ctx.call_json(qid, question_prompt(spec, ctx.text)),
                    extra=extra,
                )
                if isinstance(data, dict) and key in data:
                    value = data[key]
                else:
                    value = data
                if value is not None:
                    results[key] = value
                    check_fields(q, value, ctx.warnings)

    if not results:
        return None
    report = markdown_report(f"Configured API call — {ctx.item.title}", results)
    data = {
        "station": LABEL,
        "question_set": QUESTIONS_DOC.get("question_set"),
        "output_profile": PROFILE_NAME,
        "execution_mode": mode,
        "source_id": ctx.item.id,
        "source_sha256": ctx.item.source_hash,
        "enabled_questions": [q.get("id") for q in QUESTIONS],
        "results": results,
        "warnings": ctx.warnings,
    }
    headline = {"questions_answered": len(results), "warnings": len(ctx.warnings)}
    return ItemResult(data, page(f"Configured API call: {ctx.item.title}", markdown_to_html(report)),
                      {"questions": [{"id": q.get("id"), "title": q.get("title"),
                                      "answered": str(q.get("output_key") or q.get("id")) in results}
                                     for q in QUESTIONS]},
                      report, headline)


def main() -> int:
    prompt_files = [
        PROMPT_PATH.name,
        QUESTIONS_PATH.name,
        OUTPUTS_PATH.name,
        "ACTIVE.yaml",
    ]
    station = Station(LABEL, prompt_files=prompt_files)
    print(f"Configuration: {len(QUESTIONS)} enabled question(s) · {PROFILE_NAME} · "
          f"{ACTIVE.get('execution', {}).get('mode', 'separate')} mode")
    return station.run(process)


if __name__ == "__main__":
    raise SystemExit(main())
