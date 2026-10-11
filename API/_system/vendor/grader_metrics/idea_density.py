#!/usr/bin/env python3
"""
PROPOSITIONAL IDEA DENSITY (P-Density)
=======================================
Measures conceptual throughput per word — how many distinct propositions
are expressed per unit of text. High density = saying things. Low density = filler.

Uses spaCy POS tagging: propositions ≈ verbs + adjectives + adverbs +
prepositions + conjunctions (Brown et al., 2008).

Fallback: regex-based approximation if spaCy unavailable.

Requires (optional): pip install spacy && python -m spacy download en_core_web_sm

Usage:
    python idea_density.py paper.md
    python idea_density.py paper.md --per-paragraph
"""

import sys
import re
import json
import argparse
from pathlib import Path

# POS tags that indicate a proposition (spaCy universal POS)
PROPOSITIONAL_POS = {"VERB", "ADJ", "ADV", "ADP", "SCONJ", "CCONJ"}

# Fallback regex patterns for proposition-bearing words
VERB_RE = re.compile(r"\b(?:is|are|was|were|be|been|being|have|has|had|do|does|did|"
                     r"will|would|shall|should|can|could|may|might|must|"
                     r"\w+(?:ed|ing|ize[sd]?|ate[sd]?|ify|ifies|ified))\b", re.IGNORECASE)
ADJ_RE = re.compile(r"\b\w+(?:ful|less|ous|ive|able|ible|ical|ary|al|ent|ant)\b", re.IGNORECASE)
ADP_RE = re.compile(r"\b(?:in|on|at|to|for|with|from|by|of|about|between|through|"
                    r"during|before|after|above|below|into|upon|within|without|"
                    r"against|among|across|behind|beyond|toward)\b", re.IGNORECASE)
CONJ_RE = re.compile(r"\b(?:and|or|but|because|since|although|while|if|unless|"
                     r"whereas|whether|that|which|when|where|how)\b", re.IGNORECASE)
ADV_RE = re.compile(r"\b(?:not|never|always|often|sometimes|however|therefore|thus|"
                    r"hence|moreover|furthermore|nevertheless|nonetheless|"
                    r"\w+ly)\b", re.IGNORECASE)


_nlp = None

def _get_spacy():
    """Try to load spaCy. Returns nlp or None. Skips if SKIP_SPACY env var set."""
    import os
    if os.environ.get("SKIP_SPACY"):
        return None
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        import spacy
        _nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])
        return _nlp
    except Exception:
        return None


def compute_density_spacy(text):
    """Compute idea density using spaCy POS tags."""
    nlp = _get_spacy()
    if nlp is None:
        return None

    doc = nlp(text[:100000])  # cap at 100k chars
    tokens = [t for t in doc if not t.is_punct and not t.is_space]
    if len(tokens) < 5:
        return None

    propositions = sum(1 for t in tokens if t.pos_ in PROPOSITIONAL_POS)
    return propositions / len(tokens)


def compute_density_regex(text):
    """Fallback: approximate idea density via regex patterns."""
    words = text.split()
    if len(words) < 5:
        return None

    props = 0
    for w in words:
        if VERB_RE.match(w):
            props += 1
        elif ADJ_RE.match(w):
            props += 1
        elif ADP_RE.match(w):
            props += 1
        elif CONJ_RE.match(w):
            props += 1
        elif ADV_RE.match(w):
            props += 1

    return props / len(words)


def compute_density(text, prefer_regex=False):
    """Compute idea density, trying spaCy first then regex fallback."""
    if not prefer_regex:
        result = compute_density_spacy(text)
        if result is not None:
            return result, "spacy"
    return compute_density_regex(text), "regex"


def split_paragraphs(text):
    """Split text into paragraphs, skip frontmatter and blank lines."""
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
        elif stripped.startswith(("#", ">", "```", "|", "%%")):
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


def score_idea_density(text, per_paragraph=False):
    """Score idea density for a text. Returns dict with scores."""
    result = {"metric": "idea_density", "version": "2.0"}

    density, method = compute_density(text)
    result["method"] = method

    if density is None:
        result["document"] = {"idea_density": 0, "classification": "UNKNOWN"}
        return result

    result["document"] = {
        "idea_density": round(density, 4),
        "word_count": len(text.split()),
    }

    if density >= 0.55:
        result["document"]["classification"] = "VERY_DENSE"
    elif density >= 0.50:
        result["document"]["classification"] = "DENSE"
    elif density >= 0.45:
        result["document"]["classification"] = "MODERATE"
    elif density >= 0.40:
        result["document"]["classification"] = "SPARSE"
    else:
        result["document"]["classification"] = "VERY_SPARSE"

    if per_paragraph:
        paragraphs = split_paragraphs(text)
        para_scores = []
        for i, para in enumerate(paragraphs):
            try:
                pd, _ = compute_density(para)
                para_scores.append({
                    "index": i,
                    "first_words": " ".join(para.split()[:8]),
                    "idea_density": round(pd, 4) if pd else None,
                    "word_count": len(para.split()),
                })
            except Exception:
                para_scores.append({
                    "index": i,
                    "first_words": " ".join(para.split()[:8]),
                    "idea_density": None,
                    "error": True,
                })
        result["paragraphs"] = para_scores
        densities = [p["idea_density"] for p in para_scores if p.get("idea_density") is not None]
        if densities:
            result["paragraph_stats"] = {
                "mean": round(sum(densities) / len(densities), 4),
                "min": round(min(densities), 4),
                "max": round(max(densities), 4),
                "count": len(densities),
            }

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Propositional Idea Density Scorer")
    parser.add_argument("paper", help="Markdown file to score")
    parser.add_argument("--per-paragraph", action="store_true", help="Score each paragraph")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")
    result = score_idea_density(text, per_paragraph=args.per_paragraph)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[IDEA DENSITY] Written to {args.output}")
    else:
        print(output)

    d = result["document"]
    print(f"\n  Idea Density: {d['idea_density']:.4f} ({d['classification']})")
    print(f"  Method: {result['method']}")


if __name__ == "__main__":
    main()
