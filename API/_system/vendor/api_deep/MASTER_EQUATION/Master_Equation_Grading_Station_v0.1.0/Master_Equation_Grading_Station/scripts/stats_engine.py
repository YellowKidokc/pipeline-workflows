"""stats_engine.py -- Stage 2 of the Master Equation grading pipeline.

Reads grading_out/<paper>.lexicon.json (Stage 1 output), computes the ME
statistics, and writes grading_out/<paper>.stats.json. No API calls.
Adapted from the Fruits of the Spirit grading station (stats_engine_v1);
same stat-record framework and per-sentence series block.

Each statistic is {key, value, unit, note, in_report}. The in_report
whitelist in weights.json marks the decision-relevant stats, which are
printed to the console as a tidy table.

ME-specific blocks:
  me.score            TRUTH-formula analogue (see weights.json _me_formula_note)
  slot.coverage_*     which of the ten slots (G M E S_eff T K R Q F C) appear
  slot_axis.*         per-slot totals, shares, densities, entropy
  fit.*               fit-vocabulary distribution (direct/analogous/stretched/absent)
  canon_status.*      canon-status term counts
  drift_marker.*      protected-marker / context-cue hits
  drift.*             per-third density drift

Inputs:
  --paper   Path to the original paper (used to locate <paper>.lexicon.json),
            or a path to the .lexicon.json directly.
Output:
  grading_out/<paper>.stats.json
"""

import argparse
import hashlib
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

STATION_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = STATION_DIR / "grading_out"
WEIGHTS_PATH = Path(__file__).resolve().parent / "weights.json"


def load_weights():
    """Load scripts/weights.json (the tuning file). Fail loudly if missing."""
    if not WEIGHTS_PATH.exists():
        sys.exit(f"ERROR: tuning file not found: {WEIGHTS_PATH}\n"
                 "weights.json holds the category weights and tunables; restore it.")
    with open(WEIGHTS_PATH, encoding="utf-8") as f:
        return json.load(f)


SLOT_AXES = ["g", "m", "e", "s_eff", "t", "k", "r", "q", "f", "c"]
SLOT_CATEGORIES = [f"slot_{a}" for a in SLOT_AXES]
CATEGORIES = SLOT_CATEGORIES + [
    "product_test", "fit_language", "canon_status", "drift_marker",
    "grounding", "contradiction", "jargon", "propaganda",
]
CLAIM_KEYS = ["weak", "moderate", "strong", "forbidden"]
FIT_LEVELS = ["direct", "analogous", "stretched", "absent"]
CANON_TERMS = ["locked", "derived", "candidate",
               "ic-0", "ic-1", "ic-2", "ic-3", "ic-4", "ic-5",
               "intake", "opening", "review", "frozen", "admitted", "floor",
               "verified", "draft", "prose"]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def shannon_entropy(counts):
    total = sum(counts)
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return round(h, 4)


def percentile(sorted_vals, pct):
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * pct / 100.0
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return round(sorted_vals[int(k)], 4)
    return round(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f), 4)


def term_sentence_counts(sentences, category):
    """term -> number of sentences whose matched_terms include it."""
    counts = {}
    for s in sentences:
        for term in s["categories"][category]["matched_terms"]:
            counts[term] = counts.get(term, 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser(description="Stage 2: ME statistics engine (no API).")
    ap.add_argument("--paper", required=True,
                    help="Path to the paper, or to its .lexicon.json.")
    args = ap.parse_args()

    p = Path(args.paper)
    lex_path = p if p.suffix == ".json" else OUT_DIR / f"{p.stem}.lexicon.json"
    if not lex_path.exists() and not p.suffix == ".json":
        lex_path = OUT_DIR / f"{p.name}.lexicon.json"
    with open(lex_path, encoding="utf-8") as f:
        lex = json.load(f)

    tuning = load_weights()
    weights = tuning["category_weights"]
    axis_weights = tuning.get("slot_axis_weights", {})
    coverage_weight = float(tuning.get("coverage_bonus_weight", 10.0))
    z_threshold = float(tuning.get("spike_z_threshold", 2.0))
    weights_sha = hashlib.sha256(WEIGHTS_PATH.read_bytes()).hexdigest()

    sentences = lex["sentences"]
    n_sent = len(sentences)
    words_per = [s["word_count"] for s in sentences]
    total_words = sum(words_per) or 1

    stats = []

    def add(key, value, unit, note, in_report=False):
        # in_report flags are assigned from the weights.json whitelist below;
        # the parameter marks intent at the call site.
        stats.append({"key": key, "value": value, "unit": unit,
                      "note": note, "in_report": False})

    # --- volume -----------------------------------------------------------
    add("volume.sentences", n_sent, "count", "Sentence count from Stage 1 splitter", True)
    add("volume.words", sum(words_per), "count", "Total word count", True)
    add("volume.paragraphs", lex.get("paragraph_count", 0), "count", "Blank-line separated blocks")
    add("volume.sentence_len.avg", round(statistics.fmean(words_per), 2) if words_per else 0,
        "words", "Mean sentence length", True)
    add("volume.sentence_len.median", statistics.median(words_per) if words_per else 0, "words", "Median sentence length")
    add("volume.sentence_len.stdev", round(statistics.pstdev(words_per), 2) if len(words_per) > 1 else 0,
        "words", "Population stdev of sentence length")
    add("volume.sentence_len.min", min(words_per) if words_per else 0, "words", "Shortest sentence")
    add("volume.sentence_len.max", max(words_per) if words_per else 0, "words", "Longest sentence")

    # --- per-category volume + density ------------------------------------
    cat_hits = {c: [s["categories"][c]["hits"] for s in sentences] for c in CATEGORIES}
    cat_totals = {c: sum(cat_hits[c]) for c in CATEGORIES}
    cat_uniques = {c: len({t for s in sentences for t in s["categories"][c]["matched_terms"]})
                   for c in CATEGORIES}
    gate_density = {"product_test", "drift_marker", "grounding", "propaganda"}
    for c in CATEGORIES:
        add(f"{c}.hits", cat_totals[c], "count", f"Total {c} lexicon hits")
        add(f"{c}.unique_terms", cat_uniques[c], "count", f"Distinct {c} terms matched")
        add(f"{c}.density_per_100w", round(cat_totals[c] / total_words * 100, 3),
            "hits/100 words", f"{c} density", c in gate_density)
        add(f"{c}.weighted_score", round(cat_totals[c] * weights.get(c, 0.0), 3),
            "weighted", f"{c} hits x weight {weights.get(c, 0.0)}")

    # --- slot coverage -------------------------------------------------------
    axis_totals = {a: sum(s["slot_axes"].get(a, 0) for s in sentences) for a in SLOT_AXES}
    covered = [a for a in SLOT_AXES if axis_totals[a] > 0]
    add("slot.coverage_count", len(covered), "slots",
        "How many of the ten slots appear at all", True)
    add("slot.coverage_list", covered, "list", "Slots with at least one hit", True)
    add("slot.coverage_missing", [a for a in SLOT_AXES if a not in covered], "list",
        "Slots with no hits")

    # --- ME_SCORE (TRUTH-formula analogue) ----------------------------------
    slot_total = sum(cat_totals[c] for c in SLOT_CATEGORIES)
    me_pos = slot_total * weights.get("slot_g", 1.0) + \
        cat_totals["product_test"] * weights.get("product_test", 1.5) + \
        cat_totals["grounding"] * weights.get("grounding", 2.0)
    me_neg = sum(cat_totals[c] * weights.get(c, 0.0)
                 for c in ("contradiction", "jargon", "propaganda"))
    coverage_bonus = len(covered) / len(SLOT_AXES) * coverage_weight
    me_score = me_pos + me_neg + coverage_bonus
    add("me.score", round(me_score, 3), "weighted",
        "ME_SCORE = slot hits x1.0 + product_test x1.5 + grounding x2.0 "
        "+ coverage bonus ((covered/10) x coverage_bonus_weight) "
        "+ contradiction x-0.5 + jargon x-0.3 + propaganda x-2.0 "
        "(see weights.json _me_formula_note)", True)
    add("me.positive_component", round(me_pos, 3), "weighted",
        "slot + product_test + grounding contribution")
    add("me.negative_component", round(me_neg, 3), "weighted",
        "contradiction + jargon + propaganda contribution")
    add("me.coverage_bonus", round(coverage_bonus, 3), "weighted",
        f"(slots covered {len(covered)}/10) x coverage_bonus_weight {coverage_weight}", True)
    add("me.per_100_words", round(me_score / total_words * 100, 3), "weighted/100 words",
        "ME_SCORE normalized by length", True)

    # --- slot axes -------------------------------------------------------------
    axis_sum = sum(axis_totals.values()) or 1
    for a in SLOT_AXES:
        add(f"slot_axis.{a}.total", axis_totals[a], "count", f"Attributed {a} slot hits", True)
    for a in SLOT_AXES:
        add(f"slot_axis.{a}.share", round(axis_totals[a] / axis_sum, 4), "share",
            f"Share of attributed slot hits for {a}")
    for a in SLOT_AXES:
        add(f"slot_axis.{a}.density_per_100sent",
            round(axis_totals[a] / max(n_sent, 1) * 100, 3),
            "hits/100 sentences", f"{a} slot density per 100 sentences")
    ranked = sorted(SLOT_AXES, key=lambda a: axis_totals[a], reverse=True)
    add("slot_axis.strongest", ranked[0], "axis", f"Strongest slot ({axis_totals[ranked[0]]} hits)")
    add("slot_axis.weakest", ranked[-1], "axis", f"Weakest slot ({axis_totals[ranked[-1]]} hits)")
    add("slot_axis.entropy", shannon_entropy(list(axis_totals.values())), "bits",
        "Shannon entropy across the ten slots")
    add("slot_axis.attributed_hits", sum(axis_totals.values()), "count",
        "Slot hits attributable to a canonical slot axis")
    add("slot_axis.weighted_total",
        round(sum(axis_totals[a] * float(axis_weights.get(a, 1.0)) for a in SLOT_AXES), 3),
        "weighted", "Slot-axis totals weighted by weights.json slot_axis_weights")

    # --- fit-vocabulary distribution --------------------------------------------
    fit_counts = term_sentence_counts(sentences, "fit_language")
    fit_level_counts = {lvl: fit_counts.get(lvl, 0) for lvl in FIT_LEVELS}
    fit_sum = sum(fit_level_counts.values()) or 1
    for lvl in FIT_LEVELS:
        add(f"fit.{lvl}.sentences", fit_level_counts[lvl], "sentences",
            f"Sentences containing the fit-level term '{lvl}'")
        add(f"fit.{lvl}.share", round(fit_level_counts[lvl] / fit_sum, 4), "share",
            f"Share of fit-level sentence markers that are '{lvl}'")

    # --- canon-status vocabulary ---------------------------------------------------
    canon_counts = term_sentence_counts(sentences, "canon_status")
    for term in CANON_TERMS:
        add(f"canon_status.term.{term.replace('-', '_')}", canon_counts.get(term, 0),
            "sentences", f"Sentences containing canon-status term '{term}'")
    top_canon = sorted(canon_counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    add("canon_status.top_terms",
        [{"term": t, "sentences": n} for t, n in top_canon], "list",
        "Top canon-status terms by sentence count")

    # --- drift markers ---------------------------------------------------------------
    drift_counts = term_sentence_counts(sentences, "drift_marker")
    top_drift = sorted(drift_counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    add("drift_marker.top_terms",
        [{"term": t, "sentences": n} for t, n in top_drift], "list",
        "Top drift markers (protected markers + context cues) by sentence count")
    protected_hits = sum(n for t, n in drift_counts.items() if "-" in t and "fragment" in t or t == "historical-note")
    add("drift_marker.protected_hits", protected_hits, "sentences",
        "Sentences containing a protected marker (raw-fragment / exact-fragment / historical-note)")

    # --- claim strength ----------------------------------------------------------------
    cs_totals = {k: sum(s["claim_strength"][k] for s in sentences) for k in CLAIM_KEYS}
    cs_sum = sum(cs_totals.values()) or 1
    for k in CLAIM_KEYS:
        add(f"claim_strength.{k}.count", cs_totals[k], "count", f"CLAIM_STRENGTH {k} hits")
        add(f"claim_strength.{k}.share", round(cs_totals[k] / cs_sum, 4), "share",
            f"Share of claim-strength hits that are {k}")
    weak_n, strong_n = cs_totals["weak"], cs_totals["strong"]
    add("claim_strength.strong_to_weak_ratio",
        round(strong_n / weak_n, 4) if weak_n else (None if strong_n == 0 else "inf"),
        "ratio", "strong_claim : weak_inference", True)
    add("claim_strength.forbidden_share", round(cs_totals["forbidden"] / cs_sum, 4), "share",
        "forbidden_unless_formal share of claim-strength hits")

    # --- hedges vs absolutes -------------------------------------------------------------
    hedge_n = sum(s["hedges"] for s in sentences)
    abs_n = sum(s["absolutes"] for s in sentences)
    add("hedge.count", hedge_n, "count", "Hedge term hits")
    add("absolute.count", abs_n, "count", "Absolute term hits")
    add("hedge.density_per_100w", round(hedge_n / total_words * 100, 3), "hits/100 words", "Hedge density")
    add("absolute.density_per_100w", round(abs_n / total_words * 100, 3), "hits/100 words", "Absolute density")
    add("hedge_to_absolute_ratio",
        round(hedge_n / abs_n, 4) if abs_n else (None if hedge_n == 0 else "inf"),
        "ratio", "hedges : absolutes; high = calibrated, low = overclaiming", True)

    # --- grounding to claim -----------------------------------------------------------------
    total_claims = sum(cs_totals.values())
    add("grounding_to_claim_ratio",
        round(cat_totals["grounding"] / total_claims, 4) if total_claims else None,
        "ratio", "grounding hits : claim-strength hits (evidence per claim signal)", True)

    # --- per-third drift -----------------------------------------------------------------------
    slot_hits_per_sent = [sum(s["categories"][c]["hits"] for c in SLOT_CATEGORIES)
                          for s in sentences]
    drift_sources = {
        "slot_all": slot_hits_per_sent,
        "product_test": cat_hits["product_test"],
        "drift_marker": cat_hits["drift_marker"],
    }
    third = max(1, n_sent // 3)
    third_idx = [(0, third), (third, 2 * third), (2 * third, n_sent)]
    for name, xs in drift_sources.items():
        densities = []
        for i, (lo, hi) in enumerate(third_idx):
            w = sum(words_per[lo:hi]) or 1
            h = sum(xs[lo:hi])
            d = round(h / w * 100, 3)
            densities.append(d)
            add(f"drift.{name}.third{i + 1}_density", d, "hits/100 words",
                f"{name} density in document third {i + 1}")
        add(f"drift.{name}.delta_third3_minus_third1", round(densities[2] - densities[0], 3),
            "hits/100 words", f"{name} density drift from first to last third")

    # --- spike detection ----------------------------------------------------------------------------
    for c in CATEGORIES:
        xs = cat_hits[c]
        if len(xs) < 2:
            mean, sd = (xs[0] if xs else 0), 0.0
        else:
            mean, sd = statistics.fmean(xs), statistics.pstdev(xs)
        scored = []
        for s in sentences:
            x = s["categories"][c]["hits"]
            z = (x - mean) / sd if sd > 0 else 0.0
            scored.append((z, s))
        add(f"spikes.{c}.count_z_gt_2", sum(1 for z, _ in scored if z > z_threshold), "count",
            f"Sentences with {c} z-score > {z_threshold} (weights.json spike_z_threshold)")
        top = sorted(scored, key=lambda zs: zs[0], reverse=True)[:5]
        add(f"spikes.{c}.top5",
            [{"sentence_idx": s["idx"], "z": round(z, 3), "hits": s["categories"][c]["hits"],
              "excerpt": s["text"][:90]} for z, s in top if z > 0],
            "list", f"Top 5 {c} spikes by per-sentence z-score",
            c in ("product_test", "drift_marker", "grounding", "propaganda"))

    # --- distribution shape -----------------------------------------------------------------------------
    sent_scores = [round(sum(s["categories"][c]["weighted_score"] for c in CATEGORIES), 4)
                   for s in sentences]
    sorted_scores = sorted(sent_scores)
    sorted_lens = sorted(words_per)
    add("dist.sentence_score.p25", percentile(sorted_scores, 25), "weighted", "25th percentile per-sentence weighted score")
    add("dist.sentence_score.p50", percentile(sorted_scores, 50), "weighted", "Median per-sentence weighted score")
    add("dist.sentence_score.p75", percentile(sorted_scores, 75), "weighted", "75th percentile per-sentence weighted score")
    add("dist.sentence_score.p90", percentile(sorted_scores, 90), "weighted", "90th percentile per-sentence weighted score")
    add("dist.sentence_len.p25", percentile(sorted_lens, 25), "words", "25th percentile sentence length")
    add("dist.sentence_len.p75", percentile(sorted_lens, 75), "words", "75th percentile sentence length")
    add("dist.sentence_len.p90", percentile(sorted_lens, 90), "words", "90th percentile sentence length")
    if len(words_per) > 2 and statistics.pstdev(words_per) > 0:
        m, sd = statistics.fmean(words_per), statistics.pstdev(words_per)
        skew = statistics.fmean([((w - m) / sd) ** 3 for w in words_per])
    else:
        skew = 0.0
    add("dist.sentence_len.skewness", round(skew, 4), "skew", "Fisher moment skewness of sentence lengths")
    add("dist.sentence_score.entropy", shannon_entropy(
        [max(0.0, sc - min(sorted_scores)) + 1e-9 for sc in sent_scores]), "bits",
        "Entropy of per-sentence weighted-score mass (shifted non-negative)")
    add("dist.claim_strength.entropy", shannon_entropy(list(cs_totals.values())), "bits",
        "Entropy across claim-strength classes")

    # --- series block for charting -----------------------------------------------------------------------
    series = {
        "sentence_idx": [s["idx"] for s in sentences],
        "word_count": words_per,
        "weighted_total": sent_scores,
        "slot_count": [len(s["slot_axes"]) for s in sentences],
        "hedges": [s["hedges"] for s in sentences],
        "absolutes": [s["absolutes"] for s in sentences],
        **{f"claim_{k}": [s["claim_strength"][k] for s in sentences] for k in CLAIM_KEYS},
        **{c: cat_hits[c] for c in CATEGORIES},
    }

    # in_report whitelist from weights.json is authoritative
    whitelist = set(tuning.get("in_report_whitelist", []))
    for st in stats:
        st["in_report"] = st["key"] in whitelist

    in_report_n = sum(1 for st in stats if st["in_report"])
    out_path = OUT_DIR / f"{lex['paper_name']}.stats.json"
    payload = {
        "paper": lex["paper"],
        "paper_name": lex["paper_name"],
        "generated_at": now_iso(),
        "stage": "me_stats_engine_v1",
        "source_lexicon_json": str(lex_path),
        "weights_file": str(WEIGHTS_PATH),
        "weights_sha256": weights_sha,
        "stat_count": len(stats),
        "in_report_count": in_report_n,
        "stats": stats,
        "series": series,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    # --- console table of in_report stats -------------------------------------------------------------------
    rows = [st for st in stats if st["in_report"]]
    kw = max(len(st["key"]) for st in rows)
    print(f"\n=== IN-REPORT STATS ({len(rows)} of {len(stats)}) — {lex['paper_name']} ===")
    print(f"{'key'.ljust(kw)}  {'value'.rjust(12)}  unit")
    print("-" * (kw + 28))
    for st in rows:
        v = st["value"]
        if isinstance(v, list):
            v = f"[{len(v)} items]"
        elif v is None:
            v = "n/a"
        print(f"{st['key'].ljust(kw)}  {str(v).rjust(12)}  {st['unit']}")
    print(f"\n[stats] {len(stats)} stats ({in_report_n} in_report) -> {out_path}")


if __name__ == "__main__":
    main()
