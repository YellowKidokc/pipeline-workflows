"""CocoIndex v1 Phase 1 bridge for the Faith Through Physics canonization project."""
from __future__ import annotations

import json
import os
import pathlib
import re
import sqlite3
from collections.abc import Iterator
from typing import Any

# Force UTF-8 mode for all file I/O and stdout on Windows.
os.environ.setdefault("PYTHONUTF8", "1")

import cocoindex as coco
from cocoindex.connectors import localfs

from schema import AxiomNode, Edge, EntityNode, PaperNode, TruthPredicateNode

DEFAULT_DB = "D:/GitHub/Canonizationv1/theophysics_pipeline.db"
DEFAULT_AXIOM_JS = (
    "D:/GitHub/Canonizationv1/Canonization-integration-20260904/workbench/axiom-all-nodes.js"
)
DEFAULT_OUTPUT_DIR = "D:/GitHub/Canonizationv1/bridge/cocoindex-pipeline/output"

STOP_WORDS = {
    # Recommended base list.
    "the",
    "and",
    "or",
    "of",
    "in",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "to",
    "for",
    "from",
    "by",
    "with",
    "as",
    "on",
    "at",
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    # Extra pronouns / sentence-starter function words that are not entities.
    "i",
    "you",
    "we",
    "he",
    "she",
    "they",
    "there",
    "here",
    "if",
    "not",
    "no",
    "but",
    "so",
    "then",
    "when",
    "where",
    "what",
    "who",
    "why",
    "how",
    "all",
    "each",
    "every",
    "some",
    "any",
    "do",
    "does",
    "did",
    "can",
    "could",
    "will",
    "would",
    "shall",
    "should",
    "may",
    "might",
    "must",
    "have",
    "has",
    "had",
}

_PUNCT_STRIP = """.,;:!?()[]{}"'’-–—"""


def _strip_punct(word: str) -> str:
    return word.strip(_PUNCT_STRIP)


@coco.fn(memo=True, version=1)
def extract_entities(text: str) -> list[tuple[str, str]]:
    """Deterministically extract capitalized 1-3 word phrases from *text*."""
    if not text:
        return []

    raw_words = text.split()
    results: list[tuple[str, str]] = []
    i = 0
    while i < len(raw_words):
        word = _strip_punct(raw_words[i])
        if word and word[0].isupper():
            run: list[str] = []
            j = i
            while j < len(raw_words) and len(run) < 3:
                candidate = _strip_punct(raw_words[j])
                if not candidate or not candidate[0].isupper():
                    break
                run.append(candidate)
                j += 1

            for length in range(1, len(run) + 1):
                phrase = run[:length]
                if all(p.lower() in STOP_WORDS for p in phrase):
                    continue
                display = " ".join(phrase)
                entity_id = display.lower()
                results.append((entity_id, display))

            # Move to the end of this capitalized run to avoid redundant overlap.
            i = j
        else:
            i += 1

    return results


@coco.fn(memo=True)
def load_papers(db_path: str) -> list[PaperNode]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            paper_id, source_sha256, clean_title, chapter, series, domain,
            content_type, paper_rating, governing_question, one_sentence_finding,
            evd_support, evd_counter, evd_balance, truth_predicates_count,
            semantic_provider, semantic_model, processed_date
        FROM papers
        ORDER BY paper_id
        """
    )
    papers: list[PaperNode] = []
    for row in cur.fetchall():
        papers.append(
            PaperNode(
                id=row["paper_id"],
                title=row["clean_title"] or "",
                source_sha256=row["source_sha256"] or "",
                chapter=row["chapter"] or "",
                series=row["series"] or "",
                domain=row["domain"] or "",
                content_type=row["content_type"] or "",
                paper_rating=row["paper_rating"],
                governing_question=row["governing_question"] or "",
                one_sentence_finding=row["one_sentence_finding"] or "",
                evd_support=row["evd_support"],
                evd_counter=row["evd_counter"],
                evd_balance=row["evd_balance"],
                truth_predicates_count=row["truth_predicates_count"],
                semantic_provider=row["semantic_provider"] or "",
                semantic_model=row["semantic_model"] or "",
                processed_date=row["processed_date"] or "",
            )
        )
    conn.close()
    return papers


@coco.fn(memo=True)
def load_truth_predicates(db_path: str) -> list[TruthPredicateNode]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id, paper_id, predicate_num, predicate_text, modality, warrant, formal_notation
        FROM truth_predicates
        ORDER BY paper_id, predicate_num
        """
    )
    predicates: list[TruthPredicateNode] = []
    for row in cur.fetchall():
        predicates.append(
            TruthPredicateNode(
                id=f"{row['paper_id']}/{row['predicate_num']}",
                paper_id=row["paper_id"],
                predicate_num=row["predicate_num"],
                predicate_text=row["predicate_text"] or "",
                modality=row["modality"] if row["modality"] is not None else "",
                warrant=row["warrant"] if row["warrant"] is not None else "",
                formal_notation=row["formal_notation"] if row["formal_notation"] is not None else "",
            )
        )
    conn.close()
    return predicates


@coco.fn(memo=True)
def load_axiom_nodes(js_path: str) -> list[AxiomNode]:
    with open(js_path, encoding="utf-8") as f:
        text = f.read()
    match = re.search(
        r"window\.ALL_CANONICAL_AXIOM_NODES\s*=\s*(\[.*?\]);",
        text,
        re.DOTALL,
    )
    if not match:
        raise ValueError(f"Could not find ALL_CANONICAL_AXIOM_NODES array in {js_path}")
    raw_nodes = json.loads(match.group(1))
    axioms: list[AxiomNode] = []
    for node in raw_nodes:
        identity = node.get("identity", {})
        meaning = node.get("meaning_block", {})
        axioms.append(
            AxiomNode(
                id=identity.get("canonical_id", ""),
                canonical_id=identity.get("canonical_id", ""),
                uuid=identity.get("uuid", ""),
                domain=identity.get("domain", ""),
                status=identity.get("status", ""),
                formal_definition=meaning.get("formal_definition", ""),
                common_sense_meaning=meaning.get("common_sense_meaning", ""),
                governing_questions=meaning.get("governing_questions", {}) or {},
            )
        )
    return axioms


@coco.fn
def build_graph(
    papers: list[PaperNode],
    predicates: list[TruthPredicateNode],
    axioms: list[AxiomNode],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Assemble nodes and edges from the canonical sources."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    entity_map: dict[str, str] = {}

    for paper in papers:
        nodes.append(paper.to_dict())

    for predicate in predicates:
        nodes.append(predicate.to_dict())
        edges.append(
            Edge(
                from_id=predicate.paper_id,
                to_id=predicate.id,
                rel_type="HAS_PREDICATE",
            ).to_dict()
        )

        for entity_id, display in extract_entities(predicate.predicate_text):
            entity_map.setdefault(entity_id, display)
            edges.append(
                Edge(
                    from_id=predicate.id,
                    to_id=entity_id,
                    rel_type="MENTIONS",
                ).to_dict()
            )

    for axiom in axioms:
        nodes.append(axiom.to_dict())
        source_texts = [
            axiom.formal_definition,
            axiom.common_sense_meaning,
        ]
        for source_text in source_texts:
            for entity_id, display in extract_entities(source_text):
                entity_map.setdefault(entity_id, display)
                edges.append(
                    Edge(
                        from_id=axiom.id,
                        to_id=entity_id,
                        rel_type="MENTIONS",
                    ).to_dict()
                )

    for entity_id, display in sorted(entity_map.items()):
        nodes.append(EntityNode(id=entity_id, display_name=display).to_dict())

    return nodes, edges


@coco.lifespan
def theophysics_lifespan(builder: coco.EnvironmentBuilder) -> Iterator[None]:
    """Keep CocoIndex engine state inside the pipeline directory."""
    builder.settings.db_path = pathlib.Path(__file__).parent / "cocoindex.db"
    yield


@coco.fn
def app_main() -> None:
    db_path = os.environ.get("THEOPHYSICS_DB", DEFAULT_DB)
    axiom_js_path = os.environ.get("AXIOM_NODES_JS", DEFAULT_AXIOM_JS)
    output_dir = pathlib.Path(
        os.environ.get("OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    )

    papers = load_papers(db_path)
    predicates = load_truth_predicates(db_path)
    axioms = load_axiom_nodes(axiom_js_path)

    nodes, edges = build_graph(papers, predicates, axioms)

    output_dir.mkdir(parents=True, exist_ok=True)
    localfs.declare_file(
        output_dir / "nodes.json",
        json.dumps(nodes, ensure_ascii=False, indent=2),
        create_parent_dirs=True,
    )
    localfs.declare_file(
        output_dir / "edges.json",
        json.dumps(edges, ensure_ascii=False, indent=2),
        create_parent_dirs=True,
    )


app = coco.App(
    coco.AppConfig(name="TheophysicsBridgePhase1"),
    app_main,
)


if __name__ == "__main__":
    with coco.runtime():
        app.update_blocking(report_to_stdout=True)
