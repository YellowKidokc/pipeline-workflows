#!/usr/bin/env python3
"""
HEDGE / SPECULATION DENSITY DETECTOR
======================================
Measures what fraction of sentences contain hedging language
("may," "suggests," "potentially," "it is possible") vs. asserted as fact.

High hedge ratio = tentative/speculative paper.
Low hedge ratio = confident assertions (could be good or overconfident).

No external dependencies beyond standard library + optional spaCy.

Usage:
    python hedge_detector.py paper.md
    python hedge_detector.py paper.md --per-paragraph
"""

import re
import json
import sys
import argparse
from pathlib import Path

# Hedge cue words/phrases compiled from CoNLL-2010 shared task,
# BioScope corpus, and Hyland's hedging taxonomy
HEDGE_CUES = [
    # Epistemic modals
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bwould\b",
    # Epistemic verbs
    r"\bsuggest(?:s|ed|ing)?\b", r"\bindicate(?:s|d)?\b",
    r"\bappear(?:s|ed)?\b", r"\bseem(?:s|ed)?\b",
    r"\bimpl(?:y|ies|ied)\b",
    # Hedging adverbs
    r"\bpossibly\b", r"\bpresumably\b", r"\bperhaps\b",
    r"\bapparently\b", r"\bpotentially\b", r"\bprobably\b",
    r"\bargua?bly\b", r"\bostensibly\b", r"\bplausibly\b",
    r"\btentatively\b", r"\bconceivably\b",
    # Hedging adjectives
    r"\bpossible\b", r"\bprobable\b", r"\blikely\b",
    r"\bunclear\b", r"\buncertain\b", r"\bapproximate\b",
    r"\bputative\b", r"\bpreliminary\b", r"\btentative\b",
    # Hedging phrases
    r"\bit is (?:possible|likely|conceivable|plausible)\b",
    r"\bthere (?:is|are) (?:some|limited) evidence\b",
    r"\bto (?:some|a certain) (?:extent|degree)\b",
    r"\bin (?:some|certain) (?:cases|contexts|circumstances)\b",
    r"\bone (?:could|might) argue\b",
    r"\bit (?:remains|is) (?:to be seen|an open question)\b",
    r"\bwe speculate\b", r"\bwe hypothesize\b",
    r"\bwe conjecture\b", r"\bwe propose\b",
    r"\bnot (?:entirely |fully )?clear\b",
    r"\brequires? further\b",
    r"\bmore research (?:is )?needed\b",
]

# Strong assertion markers (confidence boosters)
BOOSTER_CUES = [
    r"\bclearly\b", r"\bobviously\b", r"\bcertainly\b",
    r"\bundoubtedly\b", r"\bdefinitely\b", r"\bunquestionably\b",
    r"\bdemonstrate(?:s|d)?\b", r"\bprove(?:s|d|n)?\b",
    r"\bestablish(?:es|ed)?\b", r"\bconfirm(?:s|ed)?\b",
    r"\bmust\b", r"\bnecessarily\b", r"\binevitably\b",
    r"\bwe show\b", r"\bwe prove\b", r"\bthis proves?\b",
    r"\bwithout (?:a )?doubt\b", r"\bit is (?:certain|evident)\b",
]

HEDGE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in HEDGE_CUES]
BOOSTER_PATTERNS = [re.compile(p, re.IGNORECASE) for p in BOOSTER_CUES]
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text):
    """Simple sentence splitter."""
    raw = SENTENCE_RE.split(text)
    return [s.strip() for s in raw if len(s.strip()) > 10]


def split_paragraphs(text):
    """Split into paragraphs, skip frontmatter."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]

    paragraphs = []
    current = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                para = " ".join(current)
                if len(para.split()) >= 5:
                    paragraphs.append(para)
                current = []
        elif stripped.startswith("#") or stripped.startswith(">") or stripped.startswith("```"):
            if current:
                para = " ".join(current)
                if len(para.split()) >= 5:
                    paragraphs.append(para)
                current = []
        else:
            current.append(stripped)
    if current:
        para = " ".join(current)
        if len(para.split()) >= 5:
            paragraphs.append(para)
    return paragraphs


def detect_hedges_in_sentence(sentence):
    """Return list of hedge cues found in a sentence."""
    found = []
    low = sentence.lower()
    for pattern in HEDGE_PATTERNS:
        if pattern.search(low):
            found.append(pattern.pattern.replace(r"\b", "").strip())
    return found


def detect_boosters_in_sentence(sentence):
    """Return list of confidence boosters found in a sentence."""
    found = []
    low = sentence.lower()
    for pattern in BOOSTER_PATTERNS:
        if pattern.search(low):
            found.append(pattern.pattern.replace(r"\b", "").strip())
    return found


def score_hedges(text, per_paragraph=False):
    """Score hedge density for a text."""
    result = {"metric": "hedge_density", "version": "1.0"}

    sentences = split_sentences(text)
    total = len(sentences)
    hedged = 0
    boosted = 0
    hedge_examples = []
    booster_examples = []

    for s in sentences:
        h = detect_hedges_in_sentence(s)
        b = detect_boosters_in_sentence(s)
        if h:
            hedged += 1
            if len(hedge_examples) < 5:
                hedge_examples.append({
                    "sentence": s[:120],
                    "cues": h[:3],
                })
        if b:
            boosted += 1
            if len(booster_examples) < 5:
                booster_examples.append({
                    "sentence": s[:120],
                    "cues": b[:3],
                })

    hedge_ratio = hedged / total if total > 0 else 0
    booster_ratio = boosted / total if total > 0 else 0
    certainty_balance = booster_ratio - hedge_ratio

    result["document"] = {
        "total_sentences": total,
        "hedged_sentences": hedged,
        "boosted_sentences": boosted,
        "hedge_ratio": round(hedge_ratio, 4),
        "booster_ratio": round(booster_ratio, 4),
        "certainty_balance": round(certainty_balance, 4),
    }

    # Classification
    if hedge_ratio > 0.40:
        result["document"]["classification"] = "HIGHLY_HEDGED"
    elif hedge_ratio > 0.25:
        result["document"]["classification"] = "MODERATELY_HEDGED"
    elif hedge_ratio > 0.10:
        result["document"]["classification"] = "LIGHTLY_HEDGED"
    else:
        result["document"]["classification"] = "ASSERTIVE"

    result["hedge_examples"] = hedge_examples
    result["booster_examples"] = booster_examples

    if per_paragraph:
        paragraphs = split_paragraphs(text)
        para_scores = []
        for i, para in enumerate(paragraphs):
            sents = split_sentences(para)
            h_count = sum(1 for s in sents if detect_hedges_in_sentence(s))
            b_count = sum(1 for s in sents if detect_boosters_in_sentence(s))
            ratio = h_count / len(sents) if sents else 0
            para_scores.append({
                "index": i,
                "first_words": " ".join(para.split()[:8]),
                "sentences": len(sents),
                "hedged": h_count,
                "boosted": b_count,
                "hedge_ratio": round(ratio, 4),
            })
        result["paragraphs"] = para_scores

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Hedge Density Detector")
    parser.add_argument("paper", help="Markdown file to score")
    parser.add_argument("--per-paragraph", action="store_true")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")
    result = score_hedges(text, per_paragraph=args.per_paragraph)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[HEDGE] Written to {args.output}")
    else:
        print(output)

    d = result["document"]
    print(f"\n  Hedge Ratio: {d['hedge_ratio']:.2%} ({d['hedged_sentences']}/{d['total_sentences']} sentences)")
    print(f"  Booster Ratio: {d['booster_ratio']:.2%}")
    print(f"  Certainty Balance: {d['certainty_balance']:+.4f}")
    print(f"  Classification: {d['classification']}")


if __name__ == "__main__":
    main()
