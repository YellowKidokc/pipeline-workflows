#!/usr/bin/env python3
"""
CONCEPT DRIFT DETECTOR (Intra-Document)
==========================================
Detects when key terms shift meaning across sections of the same paper.
High variance = sloppy or inconsistent definitions.

Uses SBERT contextual embeddings to embed each usage of a key term
in its surrounding context, then measures variance.

Requires: pip install sentence-transformers numpy

Usage:
    python concept_drift.py paper.md
    python concept_drift.py paper.md --terms "coherence,grace,entropy"
    python concept_drift.py paper.md --top-n 15
"""

import re
import json
import argparse
import sys
from pathlib import Path
from collections import defaultdict

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def extract_sections(text):
    """Split text into sections by headings. Returns list of (heading, body) tuples."""
    lines = text.split("\n")
    # Strip frontmatter
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]

    sections = []
    current_heading = "INTRO"
    current_lines = []

    for line in lines:
        if line.strip().startswith("#"):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = line.strip().lstrip("#").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines)))

    return sections


def find_key_terms(text, top_n=15, min_freq=3):
    """Find the most frequent meaningful terms in the text."""
    stopwords = set(
        "the a an and or but if then of to in on for with as by at from is are was were "
        "be being been this that these those it its into over under after before between "
        "through not no yes can cannot must should would could may might we you they he "
        "she i our your their his her them us do does did done have has had also more most "
        "very much such than other each every all any both few many some each will shall "
        "which what when where who whom how about up out just now than so only even still "
        "also already yet here there than because since while during although".split()
    )

    words = re.findall(r"[a-z][a-z\-]+", text.lower())
    freq = defaultdict(int)
    for w in words:
        if len(w) >= 4 and w not in stopwords:
            freq[w] += 1

    # Filter by minimum frequency
    candidates = [(w, c) for w, c in freq.items() if c >= min_freq]
    candidates.sort(key=lambda x: -x[1])
    return [w for w, _ in candidates[:top_n]]


def get_term_contexts(sections, term, context_window=1):
    """For each usage of a term, extract its surrounding sentence context."""
    contexts = []
    for sec_idx, (heading, body) in enumerate(sections):
        sentences = [s.strip() for s in SENTENCE_RE.split(body) if s.strip()]
        for sent_idx, sent in enumerate(sentences):
            if re.search(r"\b" + re.escape(term) + r"\b", sent, re.IGNORECASE):
                # Grab surrounding sentences for context
                start = max(0, sent_idx - context_window)
                end = min(len(sentences), sent_idx + context_window + 1)
                context = " ".join(sentences[start:end])
                contexts.append({
                    "section_index": sec_idx,
                    "section_heading": heading,
                    "context": context[:500],
                })
    return contexts


def compute_drift(contexts, model):
    """Compute embedding variance for a term's contexts."""
    import numpy as np

    if len(contexts) < 2:
        return None

    texts = [c["context"] for c in contexts]
    embeddings = model.encode(texts, show_progress_bar=False)

    # Compute pairwise cosine similarities
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / (norms + 1e-10)
    sim_matrix = normalized @ normalized.T

    # Extract upper triangle (unique pairs)
    n = len(embeddings)
    pair_sims = []
    for i in range(n):
        for j in range(i + 1, n):
            pair_sims.append(sim_matrix[i, j])

    pair_sims = np.array(pair_sims)
    mean_sim = float(np.mean(pair_sims))
    min_sim = float(np.min(pair_sims))
    std_sim = float(np.std(pair_sims))

    # Drift score: 1 - mean_similarity (higher = more drift)
    drift_score = 1.0 - mean_sim

    return {
        "usages": len(contexts),
        "mean_similarity": round(mean_sim, 4),
        "min_similarity": round(min_sim, 4),
        "std_similarity": round(std_sim, 4),
        "drift_score": round(drift_score, 4),
    }


def score_concept_drift(text, terms=None, top_n=15):
    """Full concept drift analysis."""
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except ImportError:
        print("[ERROR] pip install sentence-transformers numpy")
        sys.exit(1)

    result = {"metric": "concept_drift", "version": "1.0"}

    sections = extract_sections(text)
    result["sections_found"] = len(sections)

    if len(sections) < 2:
        result["status"] = "insufficient_sections"
        result["terms"] = []
        return result

    # Get terms
    if terms:
        key_terms = [t.strip().lower() for t in terms.split(",")]
    else:
        key_terms = find_key_terms(text, top_n=top_n)

    result["terms_analyzed"] = key_terms

    print(f"  Loading SBERT model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    term_results = []
    for term in key_terms:
        contexts = get_term_contexts(sections, term)
        if len(contexts) < 2:
            continue

        drift = compute_drift(contexts, model)
        if drift:
            entry = {"term": term, **drift}

            # Flag drifting terms
            if drift["drift_score"] > 0.30:
                entry["status"] = "HIGH_DRIFT"
            elif drift["drift_score"] > 0.20:
                entry["status"] = "MODERATE_DRIFT"
            else:
                entry["status"] = "CONSISTENT"

            # Find the most divergent pair
            if drift["min_similarity"] < 0.7:
                # Find which sections diverge most
                section_headings = [c["section_heading"] for c in contexts]
                entry["note"] = f"Term used across {len(set(section_headings))} sections"

            term_results.append(entry)

    # Sort by drift score descending
    term_results.sort(key=lambda x: -x["drift_score"])
    result["terms"] = term_results

    # Summary stats
    if term_results:
        drift_scores = [t["drift_score"] for t in term_results]
        high_drift = [t for t in term_results if t.get("status") == "HIGH_DRIFT"]
        result["summary"] = {
            "terms_with_drift_data": len(term_results),
            "mean_drift": round(sum(drift_scores) / len(drift_scores), 4),
            "max_drift": round(max(drift_scores), 4),
            "high_drift_terms": len(high_drift),
            "high_drift_list": [t["term"] for t in high_drift],
        }

        if len(high_drift) == 0:
            result["classification"] = "SEMANTICALLY_CONSISTENT"
        elif len(high_drift) <= 2:
            result["classification"] = "MINOR_DRIFT"
        else:
            result["classification"] = "SIGNIFICANT_DRIFT"
    else:
        result["classification"] = "INSUFFICIENT_DATA"

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Concept Drift Detector")
    parser.add_argument("paper", help="Markdown file to scan")
    parser.add_argument("--terms", help="Comma-separated terms to check (default: auto-detect)")
    parser.add_argument("--top-n", type=int, default=15, help="Number of auto-detected terms")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")
    result = score_concept_drift(text, terms=args.terms, top_n=args.top_n)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[DRIFT] Written to {args.output}")
    else:
        print(output)

    if "summary" in result:
        s = result["summary"]
        print(f"\n  Terms analyzed: {s['terms_with_drift_data']}")
        print(f"  Mean drift: {s['mean_drift']:.4f}")
        print(f"  High drift terms: {s['high_drift_list']}")
        print(f"  Classification: {result['classification']}")


if __name__ == "__main__":
    main()
