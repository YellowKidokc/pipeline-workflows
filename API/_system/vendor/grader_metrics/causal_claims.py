#!/usr/bin/env python3
"""
CAUSAL CLAIM DENSITY SCORER
==============================
Detects causal assertions in a paper and scores how explicitly
they are warranted vs. merely asserted.

Requires: pip install causalnlp
  (or fallback to regex-based detection if causalnlp unavailable)

Usage:
    python causal_claims.py paper.md
    python causal_claims.py paper.md --per-paragraph
"""

import re
import json
import sys
import argparse
from pathlib import Path
from collections import defaultdict

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

# Explicit causal markers
CAUSAL_EXPLICIT = [
    r"\bcause[sd]?\b", r"\bcausing\b", r"\bcausation\b", r"\bcausal\b",
    r"\bleads? to\b", r"\bled to\b", r"\bresults? in\b", r"\bresulted in\b",
    r"\bproduces?\b", r"\bproduced\b",
    r"\bgenerates?\b", r"\bgenerated\b",
    r"\binduces?\b", r"\binduced\b",
    r"\btriggers?\b", r"\btriggered\b",
    r"\bgives? rise to\b", r"\bgave rise to\b",
    r"\bis (?:due|owing) to\b",
    r"\bbecause\b", r"\bsince\b",
    r"\bthereby\b", r"\bconsequently\b",
    r"\bas a (?:result|consequence)\b",
    r"\bdrives?\b", r"\bdriven by\b",
    r"\bdetermines?\b", r"\bdetermined by\b",
    r"\bnecessitates?\b",
    r"\bif\b.*\bthen\b",
]

# Hedged causal markers
CAUSAL_HEDGED = [
    r"\bmay (?:cause|lead|result|produce)\b",
    r"\bcould (?:cause|lead|result|produce)\b",
    r"\bmight (?:cause|lead|result|produce)\b",
    r"\bsuggests? (?:a |that )?(?:causal|cause)\b",
    r"\bpotentially (?:cause|lead|produce)\b",
    r"\bcorrelat(?:es?|ed|ion)\b",
    r"\bassociat(?:es?|ed|ion)\b",
    r"\blinked? (?:to|with)\b",
    r"\brelated to\b",
    r"\bcontributes? to\b",
    r"\bplays? a role\b",
    r"\binfluen(?:ces?|ced)\b",
    r"\baffects?\b", r"\baffected by\b",
]

# Warranted causal markers (evidence-backed)
CAUSAL_WARRANTED = [
    r"\bdemonstrated? (?:that|to)\b",
    r"\bshown? (?:that|to)\b",
    r"\bproven? (?:that|to)\b",
    r"\bestablished? (?:that|to)\b",
    r"\bconfirmed? (?:that|to)\b",
    r"\beverified? (?:that|to)\b",
    r"\bevidence (?:shows?|indicates?|suggests?|demonstrates?)\b",
    r"\bdata (?:shows?|indicates?|confirms?)\b",
    r"\bexperiment(?:s|ally)?\b.*\b(?:show|confirm|demonstrate)\b",
]

EXPLICIT_RES = [re.compile(p, re.IGNORECASE) for p in CAUSAL_EXPLICIT]
HEDGED_RES = [re.compile(p, re.IGNORECASE) for p in CAUSAL_HEDGED]
WARRANTED_RES = [re.compile(p, re.IGNORECASE) for p in CAUSAL_WARRANTED]


def classify_sentence(sentence):
    """Classify a sentence's causal status."""
    has_explicit = any(p.search(sentence) for p in EXPLICIT_RES)
    has_hedged = any(p.search(sentence) for p in HEDGED_RES)
    has_warrant = any(p.search(sentence) for p in WARRANTED_RES)

    if has_explicit and has_warrant:
        return "WARRANTED_CAUSAL"
    elif has_explicit:
        return "UNWARRANTED_CAUSAL"
    elif has_hedged and has_warrant:
        return "WARRANTED_CORRELATIONAL"
    elif has_hedged:
        return "CORRELATIONAL"
    else:
        return "NON_CAUSAL"


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


def score_causal_claims(text, per_paragraph=False):
    """Score causal claim density and warrant quality."""
    result = {"metric": "causal_claims", "version": "1.0"}

    # Strip frontmatter for sentence extraction
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]
    body = " ".join(l.strip() for l in lines if l.strip() and not l.strip().startswith(("#", ">", "```", "|", "%%")))

    sentences = [s.strip() for s in SENTENCE_RE.split(body) if len(s.split()) >= 5]
    total = len(sentences)

    counts = defaultdict(int)
    examples = defaultdict(list)

    for s in sentences:
        cls = classify_sentence(s)
        counts[cls] += 1
        if len(examples[cls]) < 3:
            examples[cls].append(s[:150])

    causal_total = counts["WARRANTED_CAUSAL"] + counts["UNWARRANTED_CAUSAL"]
    correlational_total = counts["WARRANTED_CORRELATIONAL"] + counts["CORRELATIONAL"]
    warranted_total = counts["WARRANTED_CAUSAL"] + counts["WARRANTED_CORRELATIONAL"]
    all_causal = causal_total + correlational_total

    result["document"] = {
        "total_sentences": total,
        "causal_explicit": causal_total,
        "correlational": correlational_total,
        "warranted": warranted_total,
        "unwarranted": causal_total - counts["WARRANTED_CAUSAL"] + correlational_total - counts["WARRANTED_CORRELATIONAL"],
        "non_causal": counts["NON_CAUSAL"],
        "causal_density": round(all_causal / total, 4) if total > 0 else 0,
        "warrant_ratio": round(warranted_total / all_causal, 4) if all_causal > 0 else 0,
    }

    # Classification
    density = result["document"]["causal_density"]
    warrant = result["document"]["warrant_ratio"]
    if density > 0.30 and warrant > 0.50:
        result["document"]["classification"] = "STRONGLY_CAUSAL_WARRANTED"
    elif density > 0.30:
        result["document"]["classification"] = "STRONGLY_CAUSAL_UNWARRANTED"
    elif density > 0.15 and warrant > 0.50:
        result["document"]["classification"] = "MODERATELY_CAUSAL_WARRANTED"
    elif density > 0.15:
        result["document"]["classification"] = "MODERATELY_CAUSAL_UNWARRANTED"
    elif density > 0.05:
        result["document"]["classification"] = "LIGHTLY_CAUSAL"
    else:
        result["document"]["classification"] = "DESCRIPTIVE"

    result["examples"] = {k: v for k, v in examples.items() if v}

    if per_paragraph:
        paragraphs = split_paragraphs(text)
        para_scores = []
        for i, para in enumerate(paragraphs):
            sents = [s.strip() for s in SENTENCE_RE.split(para) if len(s.split()) >= 5]
            p_counts = defaultdict(int)
            for s in sents:
                p_counts[classify_sentence(s)] += 1
            causal = p_counts["WARRANTED_CAUSAL"] + p_counts["UNWARRANTED_CAUSAL"]
            corr = p_counts["WARRANTED_CORRELATIONAL"] + p_counts["CORRELATIONAL"]
            para_scores.append({
                "index": i,
                "first_words": " ".join(para.split()[:8]),
                "sentences": len(sents),
                "causal": causal,
                "correlational": corr,
                "warranted": p_counts["WARRANTED_CAUSAL"] + p_counts["WARRANTED_CORRELATIONAL"],
                "density": round((causal + corr) / len(sents), 4) if sents else 0,
            })
        result["paragraphs"] = para_scores

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Causal Claim Density Scorer")
    parser.add_argument("paper", help="Markdown file to score")
    parser.add_argument("--per-paragraph", action="store_true")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")
    result = score_causal_claims(text, per_paragraph=args.per_paragraph)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[CAUSAL] Written to {args.output}")
    else:
        print(output)

    d = result["document"]
    print(f"\n  Causal density: {d['causal_density']:.2%}")
    print(f"  Warrant ratio: {d['warrant_ratio']:.2%}")
    print(f"  Classification: {d['classification']}")


if __name__ == "__main__":
    main()
