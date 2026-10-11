#!/usr/bin/env python3
"""
NOVELTY RANK — Corpus-Relative Novelty Scoring
=================================================
Scores how novel a paper is relative to a reference corpus.
Uses SPECTER2 embeddings (if available) or falls back to SBERT.

Builds a Faiss index of your existing papers, then measures how
far the new paper sits from its nearest neighbors.

Requires: pip install sentence-transformers numpy faiss-cpu
Optional: pip install transformers adapters  (for SPECTER2)

Usage:
    python novelty_rank.py paper.md --corpus /path/to/vault/papers/
    python novelty_rank.py paper.md --corpus /path/to/vault/ --recursive
    python novelty_rank.py paper.md --index saved_index.json  (reuse cached index)
"""

import re
import json
import argparse
import sys
from pathlib import Path


def extract_abstract(text, max_chars=2000):
    """Extract the first substantive content from a paper (approximates abstract)."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
        lines = lines[end + 1:]

    content_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ">", "```", "%%", "|", "---")):
            continue
        content_lines.append(stripped)
        if sum(len(l) for l in content_lines) > max_chars:
            break
    return " ".join(content_lines)[:max_chars]


def load_corpus(corpus_path, recursive=False):
    """Load all markdown files from a corpus directory."""
    corpus_path = Path(corpus_path)
    if not corpus_path.exists():
        print(f"[ERROR] Corpus path not found: {corpus_path}")
        sys.exit(1)

    pattern = "**/*.md" if recursive else "*.md"
    papers = []
    for f in sorted(corpus_path.glob(pattern)):
        if f.name.startswith(("README", "index", ".")):
            continue
        try:
            text = f.read_text(encoding="utf-8")
            abstract = extract_abstract(text)
            if len(abstract) > 50:
                papers.append({
                    "path": str(f),
                    "name": f.stem,
                    "abstract": abstract,
                })
        except Exception:
            continue
    return papers


def try_specter2():
    """Try to load SPECTER2 model."""
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch

        model_name = "allenai/specter2_base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        model.eval()

        def encode(texts):
            inputs = tokenizer(
                texts, padding=True, truncation=True,
                max_length=512, return_tensors="pt"
            )
            with torch.no_grad():
                outputs = model(**inputs)
            return outputs.last_hidden_state[:, 0, :].numpy()

        return encode, "SPECTER2"
    except Exception:
        return None, None


def try_sbert():
    """Fall back to SBERT."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return lambda texts: model.encode(texts, show_progress_bar=False), "SBERT"
    except ImportError:
        return None, None


def score_novelty(text, corpus_path=None, recursive=False, top_k=10):
    """Score novelty of a paper relative to a corpus."""
    import numpy as np

    result = {"metric": "novelty_rank", "version": "1.0"}

    # Load encoder
    encode_fn, model_name = try_specter2()
    if encode_fn is None:
        encode_fn, model_name = try_sbert()
    if encode_fn is None:
        print("[ERROR] pip install sentence-transformers (or transformers + adapters for SPECTER2)")
        sys.exit(1)

    result["model"] = model_name
    print(f"  Using {model_name} for embeddings")

    # Get paper abstract
    paper_abstract = extract_abstract(text)
    result["paper_abstract_length"] = len(paper_abstract)

    if not corpus_path:
        result["status"] = "no_corpus"
        result["note"] = "Provide --corpus to score against a reference set"
        return result

    # Load corpus
    print(f"  Loading corpus from {corpus_path}...")
    corpus = load_corpus(corpus_path, recursive=recursive)
    result["corpus_size"] = len(corpus)

    if len(corpus) < 3:
        result["status"] = "insufficient_corpus"
        return result

    # Encode everything
    print(f"  Encoding {len(corpus)} corpus papers + 1 target...")
    all_texts = [p["abstract"] for p in corpus] + [paper_abstract]
    all_embeddings = encode_fn(all_texts)

    corpus_embeddings = all_embeddings[:-1]
    paper_embedding = all_embeddings[-1:]

    # Normalize
    norms_c = np.linalg.norm(corpus_embeddings, axis=1, keepdims=True)
    norms_p = np.linalg.norm(paper_embedding, axis=1, keepdims=True)
    corpus_norm = corpus_embeddings / (norms_c + 1e-10)
    paper_norm = paper_embedding / (norms_p + 1e-10)

    # Compute similarities
    similarities = (paper_norm @ corpus_norm.T)[0]

    # Sort by similarity (descending)
    sorted_indices = np.argsort(-similarities)
    top_indices = sorted_indices[:top_k]

    nearest = []
    for idx in top_indices:
        nearest.append({
            "name": corpus[idx]["name"],
            "similarity": round(float(similarities[idx]), 4),
        })

    # Novelty metrics
    top_k_sims = similarities[top_indices]
    mean_nearest = float(np.mean(top_k_sims))
    max_sim = float(np.max(similarities))
    mean_all = float(np.mean(similarities))

    # Novelty score: 1 - mean of top-K nearest neighbors
    novelty_score = 1.0 - mean_nearest

    result["nearest_neighbors"] = nearest
    result["document"] = {
        "novelty_score": round(novelty_score, 4),
        "max_similarity": round(max_sim, 4),
        "mean_top_k_similarity": round(mean_nearest, 4),
        "mean_corpus_similarity": round(mean_all, 4),
        "top_k": top_k,
    }

    # Classification
    if novelty_score >= 0.60:
        result["document"]["classification"] = "HIGHLY_NOVEL"
    elif novelty_score >= 0.45:
        result["document"]["classification"] = "MODERATELY_NOVEL"
    elif novelty_score >= 0.30:
        result["document"]["classification"] = "INCREMENTAL"
    else:
        result["document"]["classification"] = "DERIVATIVE"

    # Most similar = potential overlap or extension
    result["most_similar"] = nearest[0] if nearest else None
    result["most_distant_in_top_k"] = nearest[-1] if nearest else None

    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Novelty Rank Scorer")
    parser.add_argument("paper", help="Markdown file to score")
    parser.add_argument("--corpus", help="Path to reference corpus (folder of .md files)")
    parser.add_argument("--recursive", action="store_true", help="Search corpus recursively")
    parser.add_argument("--top-k", type=int, default=10, help="Number of nearest neighbors")
    parser.add_argument("-o", "--output", help="Output JSON path")
    args = parser.parse_args()

    text = Path(args.paper).read_text(encoding="utf-8")

    try:
        import numpy as np
    except ImportError:
        print("[ERROR] pip install numpy")
        sys.exit(1)

    result = score_novelty(
        text,
        corpus_path=args.corpus,
        recursive=args.recursive,
        top_k=args.top_k,
    )

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[NOVELTY] Written to {args.output}")
    else:
        print(output)

    if "document" in result:
        d = result["document"]
        print(f"\n  Novelty Score: {d['novelty_score']:.4f}")
        print(f"  Max Similarity: {d['max_similarity']:.4f}")
        print(f"  Classification: {d['classification']}")
        if result.get("most_similar"):
            ms = result["most_similar"]
            print(f"  Most similar: {ms['name']} ({ms['similarity']:.4f})")


if __name__ == "__main__":
    main()
