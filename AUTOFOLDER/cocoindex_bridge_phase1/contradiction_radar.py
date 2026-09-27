"""Standalone contradiction-radar over the Phase 1 knowledge graph output."""
from __future__ import annotations

import json
import os
import pathlib
import re
from collections import defaultdict
from itertools import combinations
from typing import Any

# Force UTF-8 mode for all file I/O and stdout on Windows.
os.environ.setdefault("PYTHONUTF8", "1")

DEFAULT_OUTPUT_DIR = "D:/GitHub/Canonizationv1/bridge/cocoindex-pipeline/output"


def _is_negative_modality(modality: str) -> bool:
    if not modality:
        return False
    if modality.startswith(r"$\neg"):
        return True
    lowered = modality.lower()
    if re.search(r"\bnot\b", lowered) or re.search(r"\bno\s", lowered):
        return True
    return False


def _polarity(modality: str) -> str:
    return "negative" if _is_negative_modality(modality) else "positive"


def main() -> None:
    output_dir = pathlib.Path(
        os.environ.get("OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    )
    nodes_path = output_dir / "nodes.json"
    edges_path = output_dir / "edges.json"

    with open(nodes_path, encoding="utf-8") as f:
        nodes: list[dict[str, Any]] = json.load(f)
    with open(edges_path, encoding="utf-8") as f:
        edges: list[dict[str, Any]] = json.load(f)

    node_by_id: dict[str, dict[str, Any]] = {n["id"]: n for n in nodes}

    # Map entity id -> list of predicate ids that mention it.
    entity_to_predicates: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge["rel_type"] != "MENTIONS":
            continue
        from_node = node_by_id.get(edge["from_id"], {})
        to_node = node_by_id.get(edge["to_id"], {})
        if from_node.get("type") == "TruthPredicate" and to_node.get("type") == "Entity":
            entity_to_predicates[edge["to_id"]].append(edge["from_id"])

    contradictions: list[dict[str, Any]] = []
    # entity_id -> {"display": str, "mentions": int, "count": int, "example_pair": tuple[str, str]}
    entity_summary: dict[str, dict[str, Any]] = {}

    for entity_id, predicate_ids in sorted(entity_to_predicates.items()):
        # Deduplicate while preserving order.
        seen: set[str] = set()
        unique_ids: list[str] = []
        for pid in predicate_ids:
            if pid not in seen:
                seen.add(pid)
                unique_ids.append(pid)

        if len(unique_ids) < 2:
            continue

        polarities = {
            pid: _polarity(node_by_id.get(pid, {}).get("modality", ""))
            for pid in unique_ids
        }

        entity_display = node_by_id.get(entity_id, {}).get("display_name", entity_id)
        entity_summary[entity_id] = {
            "display": entity_display,
            "mentions": len(unique_ids),
            "count": 0,
            "example_pair": ("", ""),
        }

        for a, b in combinations(unique_ids, 2):
            pol_a = polarities[a]
            pol_b = polarities[b]
            if pol_a == pol_b:
                continue

            text_a = node_by_id.get(a, {}).get("predicate_text", "")
            text_b = node_by_id.get(b, {}).get("predicate_text", "")

            contradictions.append(
                {
                    "entity": entity_id,
                    "entity_display": entity_display,
                    "predicate_ids": [a, b],
                    "polarities": [pol_a, pol_b],
                    "texts": [text_a, text_b],
                }
            )
            entity_summary[entity_id]["count"] += 1
            if not entity_summary[entity_id]["example_pair"][0]:
                entity_summary[entity_id]["example_pair"] = (text_a, text_b)

    contradictions_path = output_dir / "contradictions.json"
    with open(contradictions_path, "w", encoding="utf-8") as f:
        json.dump(contradictions, f, ensure_ascii=False, indent=2)

    print(f"Loaded {len(nodes):,} nodes and {len(edges):,} edges.")
    print(
        f"Found {len(contradictions):,} contradiction candidate(s) across "
        f"{len(entity_to_predicates):,} mentioned entity(ies)."
    )
    print(f"Wrote {contradictions_path}\n")

    print("Top 20 entities by number of opposite-polarity predicate pairs:")
    print("-" * 80)
    sorted_entities = sorted(
        entity_summary.values(),
        key=lambda row: row["count"],
        reverse=True,
    )[:20]
    for i, row in enumerate(sorted_entities, start=1):
        print(
            f"{i:2}. {row['display']:<30} "
            f"pairs={row['count']:<4} mentions={row['mentions']}"
        )
        a, b = row["example_pair"]
        if a and b:
            print(f"    + {a[:80]}{'...' if len(a) > 80 else ''}")
            print(f"    - {b[:80]}{'...' if len(b) > 80 else ''}")


if __name__ == "__main__":
    main()
