"""Schema dataclasses for the Phase 1 CocoIndex knowledge-graph bridge."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PaperNode:
    id: str
    title: str
    source_sha256: str
    chapter: str
    series: str
    domain: str
    content_type: str
    paper_rating: float | None
    governing_question: str
    one_sentence_finding: str
    evd_support: int | None
    evd_counter: int | None
    evd_balance: float | None
    truth_predicates_count: int | None
    semantic_provider: str
    semantic_model: str
    processed_date: str

    def to_dict(self) -> dict[str, Any]:
        d = {
            "id": self.id,
            "type": "Paper",
            "title": self.title,
            "source_sha256": self.source_sha256,
            "chapter": self.chapter,
            "series": self.series,
            "domain": self.domain,
            "content_type": self.content_type,
            "paper_rating": self.paper_rating,
            "governing_question": self.governing_question,
            "one_sentence_finding": self.one_sentence_finding,
            "evd_support": self.evd_support,
            "evd_counter": self.evd_counter,
            "evd_balance": self.evd_balance,
            "truth_predicates_count": self.truth_predicates_count,
            "semantic_provider": self.semantic_provider,
            "semantic_model": self.semantic_model,
            "processed_date": self.processed_date,
        }
        return d


@dataclass
class TruthPredicateNode:
    id: str
    paper_id: str
    predicate_num: str
    predicate_text: str
    modality: str
    warrant: str
    formal_notation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": "TruthPredicate",
            "paper_id": self.paper_id,
            "predicate_num": self.predicate_num,
            "predicate_text": self.predicate_text,
            "modality": self.modality,
            "warrant": self.warrant,
            "formal_notation": self.formal_notation,
        }


@dataclass
class AxiomNode:
    id: str
    canonical_id: str
    uuid: str
    domain: str
    status: str
    formal_definition: str
    common_sense_meaning: str
    governing_questions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": "Axiom",
            "canonical_id": self.canonical_id,
            "uuid": self.uuid,
            "domain": self.domain,
            "status": self.status,
            "formal_definition": self.formal_definition,
            "common_sense_meaning": self.common_sense_meaning,
            "governing_questions": self.governing_questions,
        }


@dataclass
class EntityNode:
    id: str
    display_name: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": "Entity",
            "display_name": self.display_name,
        }


@dataclass
class Edge:
    from_id: str
    to_id: str
    rel_type: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "from_id": self.from_id,
            "to_id": self.to_id,
            "rel_type": self.rel_type,
            "properties": self.properties,
        }
