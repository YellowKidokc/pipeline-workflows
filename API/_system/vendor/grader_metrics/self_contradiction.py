#!/usr/bin/env python3
"""
SELF-CONTRADICTION DETECTOR
=============================
Finds internal contradictions within a document by running NLI
(Natural Language Inference) pairwise across claim-bearing sentences.

Uses DeBERTa-v3 NLI model (same as RECON pipeline).

Requires: pip install transformers torch

Usage:
    python self_contradiction.py paper.md
    python self_contradiction.py paper.md --threshold 0.85
    python self_contradiction.py paper.md --max-pairs 500
"""

import re
import json
import argparse
import sys
from pathlib import Path

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

# Patterns that indicate a sentence makes a claim (not just narrative)
CLAIM_PATTERNS = [
    r"\bis\b", r"\bare\b", r"\bwas\b", r"\bwere\b",
    r"\bmust\b", r"\bshould\b", r"\bcannot\b", r"\brequires?\b",
    r"\bimplies?\b", r"\btherefore\b", r"\bthus\b", r"\bhence\b",
    r"\bproves?\b", r"\bdemonstrates?\b", r"\bshows?\b",
    r"\bif\b.*\bthen\b", r"\bonly if\b",
]
CLAIM_RES = [re.compile(p, re.IGNORECASE) for p in CLAIM_PATTERNS]


def extract_claim_sentences(text, min_words=8):
    """Extract sentences that appear to make claims."""
    lines = text.split("\n")
    # Strip frontmatter
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]

    body = " ".join(
        line.strip() for line in lines
        if line.strip()
        and not line.strip().startswith("#")
        and not line.strip().startswith(">")
        and not line.strip().startswith("```")
        and not line.strip().startswith("|")
        and not line.strip().startswith("%%")
    )

    sentences = [s.strip() for s in SENTENCE_RE.split(body) if len(s.split()) >= min_words]

    # Filter to claim-bearing sentences
    claims = []
    for s in sentences:
        if any(p.search(s) for p in CLAIM_RES):
            # Truncate very long sentences
            if len(s) > 300:
                s = s[:300]
            claims.append(s)
    return claims


def load_nli_model():
    """Load DeBERTa NLI model."""
    try:
        from transformers import pipeline
    except ImportError:
        print("[ERROR] pip install transformers torch")
        sys.exit(1)

    print("  Loading DeBERTa-v3-base-mnli-fever-anli...")
    nli = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
        device=-1,  # CPU
    )
    return nli


def check_contradiction_nli(nli, sentence_a, sentence_b):
    """Check if two sentences contradict each other using NLI."""
    result = nli(
        sentence_a,
        candidate_labels=[sentence_b],
        hypothesis_template="{}",
        multi_label=False,
    )
    # This gives us entailment score; for contradiction we need the raw model
    return result


def check_contradictions_direct(claims, threshold=0.80, max_pairs=500):
    """Use NLI model directly for entailment/contradiction/neutral."""
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
    except ImportError:
        print("[ERROR] pip install transformers torch")
        sys.exit(1)

    model_name = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    print(f"  Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

    # Generate pairs (skip adjacent sentences — they're usually consistent)
    pairs = []
    for i in range(len(claims)):
        for j in range(i + 2, min(i + 20, len(claims))):  # window of 20
            pairs.append((i, j))
            if len(pairs) >= max_pairs:
                break
        if len(pairs) >= max_pairs:
            break

    print(f"  Checking {len(pairs)} sentence pairs...")

    contradictions = []
    for idx, (i, j) in enumerate(pairs):
        if idx % 50 == 0 and idx > 0:
            print(f"    ...{idx}/{len(pairs)}")

        inputs = tokenizer(
            claims[i], claims[j],
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)[0]

        # Label order for this model: entailment, neutral, contradiction
        labels = model.config.id2label
        label_map = {}
        for k, v in labels.items():
            label_map[v.lower()] = probs[k].item()

        contradiction_score = label_map.get("contradiction", 0)
        entailment_score = label_map.get("entailment", 0)

        if contradiction_score >= threshold:
            contradictions.append({
                "sentence_a_index": i,
                "sentence_b_index": j,
                "sentence_a": claims[i][:200],
                "sentence_b": claims[j][:200],
                "contradiction_score": round(contradiction_score, 4),
                "entailment_score": round(entailment_score, 4),
            })

    return contradictions, len(pairs)


def score_contradictions(text, threshold=0.80, max_pairs=500):
    """Full contradiction analysis."""
    result = {"metric": "self_contradiction", "version": "1.0"}

    claims = extract_claim_sentences(text)
    result["claim_sentences_found"] = len(claims)

    if len(claims) < 3:
        result["status"] = "insufficient_claims"
        result["contradictions"] = []
        return result

    contradictions, pairs_checked = check_contradictions_direct(
        claims, threshold=threshold, max_pairs=max_pairs
    )

    result["pairs_checked"] = pairs_checked
    result["contradictions_found"] = len(contradictions)
    result["contradiction_rate"] = round(len(contradictions) / pairs_checked, 4) if pairs_checked > 0 else 0
    result["contradictions"] = contradictions
    result["threshold"] = threshold

    # Classification
    rate = result["contradiction_rate"]
    if rate == 0:
        result["classification"] = "INTERNALLY_CONSISTENT"
    elif rate < 0.02:
        result["classification"] = "MINOR_TENSIONS"
    elif rate < 0.05:
        result["classification"] = "MODERATE_CONTRADICTIONS"
    else:
        result["classification"] = "SIGNIFICANT_CONTRADICTIONS"

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Self-Contradiction Detector")
    parser.add_argument("paper", help="Markdown file to scan")
    parser.add_argument("--threshold", type=float, default=0.80,
                        help="Contradiction confidence threshold (default: 0.80)")
    parser.add_argument("--max-pairs", type=int, default=500,
                        help="Max sentence pairs to check (default: 500)")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")
    result = score_contradictions(text, threshold=args.threshold, max_pairs=args.max_pairs)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[CONTRADICTION] Written to {args.output}")
    else:
        print(output)

    print(f"\n  Claims found: {result['claim_sentences_found']}")
    print(f"  Pairs checked: {result.get('pairs_checked', 0)}")
    print(f"  Contradictions: {result['contradictions_found']}")
    print(f"  Classification: {result.get('classification', '?')}")


if __name__ == "__main__":
    main()
