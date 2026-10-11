#!/usr/bin/env python3
"""
TOPIC COHERENCE SCORER (Contextualized)
=========================================
Measures whether each paragraph stays on-topic and whether
transitions between paragraphs are logical.

Uses SBERT embeddings to compute cosine similarity between
consecutive paragraphs. Drops indicate topic jumps.

Requires: pip install sentence-transformers numpy

Usage:
    python topic_coherence.py paper.md
    python topic_coherence.py paper.md --threshold 0.3
"""

import re
import json
import argparse
import sys
from pathlib import Path


def split_paragraphs(text):
    """Split into paragraphs, skip frontmatter and markup."""
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
                if len(para.split()) >= 10:
                    paragraphs.append(para)
                current = []
        elif stripped.startswith(("#", ">", "```", "|", "%%", "---")):
            if current:
                para = " ".join(current)
                if len(para.split()) >= 10:
                    paragraphs.append(para)
                current = []
        else:
            current.append(stripped)
    if current:
        para = " ".join(current)
        if len(para.split()) >= 10:
            paragraphs.append(para)
    return paragraphs


def score_topic_coherence(text, drop_threshold=0.3):
    """Score topic coherence via consecutive paragraph similarity."""
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except ImportError:
        print("[ERROR] pip install sentence-transformers numpy")
        sys.exit(1)

    result = {"metric": "topic_coherence", "version": "1.0"}

    paragraphs = split_paragraphs(text)
    result["paragraph_count"] = len(paragraphs)

    if len(paragraphs) < 3:
        result["status"] = "insufficient_paragraphs"
        return result

    print(f"  Loading SBERT model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"  Encoding {len(paragraphs)} paragraphs...")
    embeddings = model.encode(paragraphs, show_progress_bar=False)

    # Normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / (norms + 1e-10)

    # Consecutive similarities
    transitions = []
    for i in range(len(paragraphs) - 1):
        sim = float(np.dot(normalized[i], normalized[i + 1]))
        transitions.append({
            "from_index": i,
            "to_index": i + 1,
            "from_preview": " ".join(paragraphs[i].split()[:8]),
            "to_preview": " ".join(paragraphs[i + 1].split()[:8]),
            "similarity": round(sim, 4),
        })

    sims = [t["similarity"] for t in transitions]

    # Global coherence: mean of all adjacent paragraph similarities
    mean_coherence = float(np.mean(sims))
    min_coherence = float(np.min(sims))
    std_coherence = float(np.std(sims))

    # Detect drops
    drops = [t for t in transitions if t["similarity"] < drop_threshold]

    # Also compute global pairwise coherence (all paragraphs to all paragraphs)
    full_sim_matrix = normalized @ normalized.T
    upper_triangle = []
    n = len(paragraphs)
    for i in range(n):
        for j in range(i + 1, n):
            upper_triangle.append(full_sim_matrix[i, j])
    global_coherence = float(np.mean(upper_triangle))

    result["document"] = {
        "adjacent_coherence_mean": round(mean_coherence, 4),
        "adjacent_coherence_min": round(min_coherence, 4),
        "adjacent_coherence_std": round(std_coherence, 4),
        "global_coherence": round(global_coherence, 4),
        "topic_drops": len(drops),
        "drop_threshold": drop_threshold,
    }

    # Classification
    if mean_coherence >= 0.60 and len(drops) == 0:
        result["document"]["classification"] = "HIGHLY_COHERENT"
    elif mean_coherence >= 0.45 and len(drops) <= 1:
        result["document"]["classification"] = "COHERENT"
    elif mean_coherence >= 0.35:
        result["document"]["classification"] = "MODERATELY_COHERENT"
    elif mean_coherence >= 0.25:
        result["document"]["classification"] = "LOOSELY_COHERENT"
    else:
        result["document"]["classification"] = "FRAGMENTED"

    result["transitions"] = transitions
    result["topic_drops"] = drops

    # Section-level coherence (group by topic clusters)
    # Find natural break points where similarity drops below threshold
    break_points = [0]
    for i, t in enumerate(transitions):
        if t["similarity"] < drop_threshold:
            break_points.append(i + 1)
    break_points.append(len(paragraphs))

    sections = []
    for i in range(len(break_points) - 1):
        start = break_points[i]
        end = break_points[i + 1]
        if end - start >= 2:
            section_sims = sims[start:end - 1] if start < end - 1 else []
            sections.append({
                "paragraphs": f"{start}-{end - 1}",
                "length": end - start,
                "internal_coherence": round(float(np.mean(section_sims)), 4) if section_sims else None,
                "preview": " ".join(paragraphs[start].split()[:10]),
            })
    result["detected_sections"] = sections

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Topic Coherence Scorer")
    parser.add_argument("paper", help="Markdown file to score")
    parser.add_argument("--threshold", type=float, default=0.3,
                        help="Similarity threshold for topic drop (default: 0.3)")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")
    result = score_topic_coherence(text, drop_threshold=args.threshold)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[COHERENCE] Written to {args.output}")
    else:
        print(output)

    if "document" in result:
        d = result["document"]
        print(f"\n  Adjacent coherence: {d['adjacent_coherence_mean']:.4f}")
        print(f"  Global coherence: {d['global_coherence']:.4f}")
        print(f"  Topic drops: {d['topic_drops']}")
        print(f"  Classification: {d['classification']}")


if __name__ == "__main__":
    main()
