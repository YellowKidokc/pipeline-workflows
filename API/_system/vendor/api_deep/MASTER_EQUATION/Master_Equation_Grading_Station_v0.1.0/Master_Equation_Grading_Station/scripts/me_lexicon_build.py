"""me_lexicon_build.py -- Stage 0 of the Master Equation grading pipeline.

Builds ME_LEXICON_V1.xlsx (the single lexicon workbook the ME lexicon pass
reads) from three sources. No API calls.

Sources:
  * ME pill atoms (JSON-LD) -- the ten slot definitions G, M, E, S_eff, T, K,
    R, Q, F, C (ME-01-020..029). Located via the "me_pills" key in
    _system/config/paths.json (found by walking up from this script).
  * Drift rules -- protected markers and context cues from
    master-equation.rules.json, located via the "me_drift_rules" key.
  * Generic epistemic lists (claim strength, hedges, absolutes, grounding,
    contradiction, jargon, propaganda) -- carried over from the sibling FRUITS
    station workbooks when present (in-repo relative lookup), otherwise from
    the baked-in fallback lists below.

Output:
  <STATION_DIR.parents[1]>/ME_LEXICON_V1.xlsx  (the MASTER_EQUATION folder,
  one level above the versioned station folder -- the same relative spot the
  fruits workbooks occupy for the fruits station).

Workbook shape (mirrors what the adapted lexicon_pass.py parses):
  Slot_G .. Slot_C, Product_Test, Fit_Language, Canon_Status, Drift_Marker,
  Grounding, Contradiction, Jargon, Propaganda
      header row: Term | Subcategory | Active   (Active = "Y")
  Weights           header row: Category | Weight
  SEMANTIC_BUCKETS  header row: term | bucket | subbucket  (CLAIM_STRENGTH rows)
  HEDGE_TERMS       header row: term
  ABSOLUTE_TERMS    header row: term
  _Provenance       build record: sources, counts, timestamp

Note on symbols: single-letter slot symbols (G, M, E, T, K, R, Q, F, C) are
included as terms. Matching is case-insensitive with word boundaries, so they
only hit standalone letters -- genuine slot usage in the equation lines, with
a small false-positive risk in prose. S_eff is multi-character and safe.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

STATION_DIR = Path(__file__).resolve().parent.parent
OUT_XLSX = STATION_DIR.parents[1] / "ME_LEXICON_V1.xlsx"  # MASTER_EQUATION folder
WEIGHTS_PATH = Path(__file__).resolve().parent / "weights.json"

# In-repo sibling: the FRUITS station workbooks, source of the generic lists.
# parents: [0] scripts -> [1] station -> [2] v0.1.0 -> [3] MASTER_EQUATION
#          -> [4] api_deep
API_DEEP_DIR = Path(__file__).resolve().parents[4]
FRUITS_TEMPLATE = API_DEEP_DIR / "FRUITS" / "Fruits Template (4).xlsx"
FRUITS_V2 = API_DEEP_DIR / "FRUITS" / "LEXICON_V2.xlsx"

SLOT_AXES = ["g", "m", "e", "s_eff", "t", "k", "r", "q", "f", "c"]

# Curated per-slot vocabulary, seeded from the slot table in
# 08_API_DEEP/057_API_DEEP/BACKSIDE/prompts/MASTER_EQUATION_V2.md and the
# pill definitions (ME-01-020..029). The builder also adds each pill's
# masterEquationFactor name and symbol automatically.
CURATED_SLOT_TERMS = {
    "g": ["negentropy influx", "negentropy", "outside influx", "external influx",
          "influx of coherence", "outside source", "external source of coherence",
          "grace"],
    "m": ["alignment cosine", "alignment", "aligned with its reference",
          "reference vector", "coupling", "misalignment"],
    "e": ["signal propagation fidelity", "signal fidelity", "propagation fidelity",
          "fidelity", "transmission", "channel capacity",
          "truth survives transmission", "signal survives", "noise"],
    "s_eff": ["s_eff", "effective entropy", "entropy production", "s_prod",
              "raw entropy", "entropy enters", "lowers coherence",
              "reduces coherence"],
    "t": ["temporal integration", "time integration", "accumulated consequence",
          "possibility into", "over time", "duration"],
    "k": ["information compression ratio", "compression ratio", "compression",
          "kolmogorov", "compressibility", "ordered meaning compresses",
          "noise does not compress"],
    "r": ["phase transition indicator", "phase transition", "phase transitions",
          "irreversible state change", "state change", "threshold change",
          "change state"],
    "q": ["superposition measure", "superposition", "unresolved state",
          "open possibility", "stays unresolved", "actualized", "actualization",
          "until actualized"],
    "f": ["non-local correlation strength", "non-local correlation",
          "nonlocal correlation", "non-local", "entanglement", "relational bond",
          "no longer independent"],
    "c": ["total integration measure", "local integrator", "integration measure",
          "global-coherence measure", "inside the product", "local global-coherence"],
}

PRODUCT_TEST_TERMS = [
    # (term, subcategory)
    ("product test", "general"),
    ("whole product", "general"),
    ("multiplicative", "multiplicative"),
    ("multiplies", "multiplicative"),
    ("multiplies rather than adds", "multiplicative"),
    ("additive", "additive"),
    ("threshold", "threshold"),
    ("thresholds", "threshold"),
    ("zero-collapse", "zero_collapse"),
    ("zero collapse", "zero_collapse"),
    ("collapses the whole product", "zero_collapse"),
    ("collapses", "zero_collapse"),
    ("any single zero", "zero_collapse"),
    ("any factor is zero", "zero_collapse"),
    ("if any factor is zero", "zero_collapse"),
    ("if one ingredient", "zero_collapse"),
    ("veto property", "zero_collapse"),
    ("veto", "zero_collapse"),
]

FIT_LANGUAGE_TERMS = [
    ("direct", "direct"),
    ("analogous", "analogous"),
    ("stretched", "stretched"),
    ("absent", "absent"),
    ("direct fit", "direct"),
    ("analogous fit", "analogous"),
    ("analogy", "general"),
    ("analog", "general"),
]

CANON_STATUS_TERMS = [
    "LOCKED", "DERIVED", "CANDIDATE",
    "IC-0", "IC-1", "IC-2", "IC-3", "IC-4", "IC-5",
    "INTAKE", "OPENING", "REVIEW", "FROZEN", "ADMITTED", "FLOOR",
    "VERIFIED", "DRAFT", "PROSE",
]

# Baked-in fallbacks for the generic lists (used only when the sibling FRUITS
# workbooks are not found). The primary source is the FRUITS station workbooks.
FALLBACK_CLAIM_STRENGTH = {
    "weak_inference": ["suggests", "may indicate", "is consistent with",
                       "points toward", "raises the possibility",
                       "appears to support", "is compatible with", "could imply"],
    "moderate_claim": ["supports", "explains", "accounts for", "constrains",
                       "predicts", "models", "indicates", "is evidence for",
                       "fits", "tracks"],
    "strong_claim": ["demonstrates", "establishes", "verifies", "proves",
                     "entails", "necessitates", "shows conclusively",
                     "logically implies"],
    "forbidden_unless_formal": ["derives", "proves all", "logically entails",
                                "exact", "universal", "unavoidable",
                                "impossible otherwise",
                                "exact algebraic derivation", "final theory",
                                "underlying math of every field"],
}
FALLBACK_HEDGES = ["probably", "seems", "maybe", "might", "likely", "roughly",
                   "perhaps", "could", "appears", "sort of", "kind of",
                   "possibly"]
FALLBACK_ABSOLUTES = ["proves", "always", "never", "certainly", "obviously",
                      "undeniable", "impossible"]
FALLBACK_TEMPLATE_TERMS = {
    "grounding": ["evidence", "proof", "data", "study", "research",
                  "experiment", "observation", "measurement", "tested",
                  "demonstrated"],
    "contradiction": ["however", "but", "although", "though", "yet",
                      "nevertheless", "nonetheless", "despite", "in spite of",
                      "on the contrary"],
    "jargon": ["operationalize", "problematize", "theorize", "conceptualize",
               "contextualize", "utilize", "leverage", "facilitate",
               "implement", "optimize"],
    "propaganda": ["they don't want you to know", "they're coming for",
                   "they want to control", "the elites", "the powers that be",
                   "the establishment", "the system", "right now",
                   "before it's too late", "this is the moment"],
}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clean(v):
    return str(v).strip() if v is not None else ""


def find_system_config():
    """Walk up from this script to find _system/config/paths.json."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "_system" / "config" / "paths.json"
        if candidate.exists():
            return candidate
    sys.exit("ERROR: could not find _system/config/paths.json by walking up "
             f"from {Path(__file__).resolve()}")


def load_paths():
    cfg_path = find_system_config()
    with open(cfg_path, encoding="utf-8") as f:
        return cfg_path, json.load(f)


def require_path(paths, key):
    raw = clean(paths.get(key))
    if not raw:
        sys.exit(f"ERROR: paths.json key '{key}' is empty. Set it in "
                 "_system/config/paths.json (machine-specific path).")
    p = Path(raw)
    if not p.exists():
        sys.exit(f"ERROR: paths.json key '{key}' points at a missing path: {p}")
    return p


# ---------------------------------------------------------------------------
# Source readers
# ---------------------------------------------------------------------------

def read_slot_pills(pills_dir):
    """Return {slot_axis: {"pill": file, "name": str, "symbol": str,
    "definition": str, "terms": [(term, subcategory), ...]}}."""
    slots = {}
    for pill in sorted(pills_dir.glob("*.jsonld")):
        try:
            with open(pill, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        fac = data.get("masterEquationFactor")
        if not fac:
            continue
        symbol = clean(fac.get("symbol"))
        if not symbol:
            continue
        axis = symbol.lower()
        terms = []
        name = clean(fac.get("name")) or clean(data.get("name"))
        if name:
            terms.append((name, "pill-name"))
        if symbol:
            terms.append((symbol, "pill-symbol"))
        for term in CURATED_SLOT_TERMS.get(axis, []):
            terms.append((term, "curated"))
        slots[axis] = {
            "pill": pill.name,
            "name": name,
            "symbol": symbol,
            "definition": clean(fac.get("definition")),
            "terms": terms,
        }
    return slots


def read_drift_markers(rules_path):
    """Return [(term, subcategory)] from protectedMarkers + contextCues."""
    with open(rules_path, encoding="utf-8") as f:
        rules = json.load(f)
    terms = [(m, "protected") for m in rules.get("protectedMarkers", []) if clean(m)]
    for cls, cues in rules.get("contextCues", {}).items():
        for cue in cues:
            if clean(cue):
                terms.append((clean(cue), f"context-{cls}"))
    return terms


def _find_header(rows, first_cell_names):
    for i, row in enumerate(rows):
        if row and clean(row[0]).lower() in first_cell_names:
            return i, [clean(c).lower() for c in row]
    return None, None


def _template_terms(wb, sheet):
    if sheet not in wb.sheetnames:
        return []
    rows = [tuple(r) for r in wb[sheet].iter_rows(values_only=True)]
    hi, header = _find_header(rows, {"term", "term/phrase"})
    if hi is None:
        return []
    active_col = header.index("active") if "active" in header else None
    terms = []
    for row in rows[hi + 1:]:
        if not row:
            continue
        term = clean(row[0])
        if not term or "#NAME?" in term:
            continue
        if active_col is not None and clean(row[active_col]).upper() != "Y":
            continue
        terms.append(term)
    return terms


def read_fruits_generics():
    """Carry the generic epistemic lists out of the sibling FRUITS workbooks.
    Returns (generic_categories, claim_strength, hedges, absolutes,
    provenance_note)."""
    if not (FRUITS_TEMPLATE.exists() and FRUITS_V2.exists()):
        return (dict(FALLBACK_TEMPLATE_TERMS), dict(FALLBACK_CLAIM_STRENGTH),
                list(FALLBACK_HEDGES), list(FALLBACK_ABSOLUTES),
                "fallback-baked-in (FRUITS workbooks not found)")

    generic = {}
    wb = openpyxl.load_workbook(FRUITS_TEMPLATE, read_only=True, data_only=True)
    try:
        for key, sheet in (("grounding", "Grounding"), ("contradiction", "Contradiction"),
                           ("jargon", "Jargon"), ("propaganda", "Propaganda")):
            terms = _template_terms(wb, sheet)
            generic[key] = terms or list(FALLBACK_TEMPLATE_TERMS[key])
    finally:
        wb.close()

    claim_strength = {k: [] for k in FALLBACK_CLAIM_STRENGTH}
    hedges, absolutes = [], []
    wb = openpyxl.load_workbook(FRUITS_V2, read_only=True, data_only=True)
    try:
        if "SEMANTIC_BUCKETS" in wb.sheetnames:
            rows = [tuple(r) for r in wb["SEMANTIC_BUCKETS"].iter_rows(values_only=True)]
            header = [clean(c).lower() for c in rows[0]]
            ti, bi, si = header.index("term"), header.index("bucket"), header.index("subbucket")
            for row in rows[1:]:
                if not row:
                    continue
                term, bucket, sub = clean(row[ti]), clean(row[bi]), clean(row[si])
                if bucket == "CLAIM_STRENGTH" and sub in claim_strength and term:
                    claim_strength[sub].append(term)
        for sheet, target in (("HEDGE_TERMS", hedges), ("ABSOLUTE_TERMS", absolutes)):
            if sheet not in wb.sheetnames:
                continue
            rows = [tuple(r) for r in wb[sheet].iter_rows(values_only=True)]
            header = [clean(c).lower() for c in rows[0]]
            tcol = header.index("term") if "term" in header else 3
            for row in rows[1:]:
                if row and tcol < len(row):
                    term = clean(row[tcol])
                    if term and "#NAME?" not in term:
                        target.append(term)
    finally:
        wb.close()

    claim_strength = {k: sorted(set(v)) or list(FALLBACK_CLAIM_STRENGTH[k])
                      for k, v in claim_strength.items()}
    hedges = sorted(set(hedges)) or list(FALLBACK_HEDGES)
    absolutes = sorted(set(absolutes)) or list(FALLBACK_ABSOLUTES)
    return (generic, claim_strength, hedges, absolutes,
            f"carried from {FRUITS_TEMPLATE.name} + {FRUITS_V2.name} (sibling FRUITS folder)")


# ---------------------------------------------------------------------------
# Workbook writer
# ---------------------------------------------------------------------------

def dedupe(terms):
    seen, out = set(), []
    for term, sub in terms:
        key = term.lower()
        if term and key not in seen:
            seen.add(key)
            out.append((term, sub))
    return out


def add_term_sheet(wb, title, terms):
    ws = wb.create_sheet(title)
    ws.append(["Term", "Subcategory", "Active"])
    for term, sub in dedupe(terms):
        ws.append([term, sub, "Y"])
    return ws.max_row - 1


def main():
    cfg_path, paths = load_paths()
    pills_dir = require_path(paths, "me_pills")
    rules_path = require_path(paths, "me_drift_rules")

    with open(WEIGHTS_PATH, encoding="utf-8") as f:
        weights = json.load(f)["category_weights"]

    slots = read_slot_pills(pills_dir)
    missing = [a for a in SLOT_AXES if a not in slots]
    if missing:
        sys.exit(f"ERROR: no pill found for slot(s) {missing} in {pills_dir}")

    drift_terms = read_drift_markers(rules_path)
    generic, claim_strength, hedges, absolutes, generics_src = read_fruits_generics()

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    counts = {}

    for axis in SLOT_AXES:
        counts[f"slot_{axis}"] = add_term_sheet(
            wb, f"Slot_{axis.upper() if axis != 's_eff' else 'S_eff'}",
            slots[axis]["terms"])
    counts["product_test"] = add_term_sheet(wb, "Product_Test", PRODUCT_TEST_TERMS)
    counts["fit_language"] = add_term_sheet(wb, "Fit_Language", FIT_LANGUAGE_TERMS)
    counts["canon_status"] = add_term_sheet(
        wb, "Canon_Status", [(t, t) for t in CANON_STATUS_TERMS])
    counts["drift_marker"] = add_term_sheet(wb, "Drift_Marker", drift_terms)
    for key in ("grounding", "contradiction", "jargon", "propaganda"):
        counts[key] = add_term_sheet(
            wb, key.capitalize(), [(t, "generic") for t in generic[key]])

    ws = wb.create_sheet("Weights")
    ws.append(["Category", "Weight"])
    for cat in counts:
        ws.append([cat, weights.get(cat, 0.0)])

    ws = wb.create_sheet("SEMANTIC_BUCKETS")
    ws.append(["term", "bucket", "subbucket"])
    for sub, terms in claim_strength.items():
        for term in terms:
            ws.append([term, "CLAIM_STRENGTH", sub])

    for sheet, terms in (("HEDGE_TERMS", hedges), ("ABSOLUTE_TERMS", absolutes)):
        ws = wb.create_sheet(sheet)
        ws.append(["term"])
        for term in terms:
            ws.append([term])

    ws = wb.create_sheet("_Provenance")
    ws.append(["key", "value"])
    ws.append(["built_at", now_iso()])
    ws.append(["builder", str(Path(__file__).resolve())])
    ws.append(["paths_json", str(cfg_path)])
    ws.append(["me_pills", str(pills_dir)])
    ws.append(["pill_files", "; ".join(slots[a]["pill"] for a in SLOT_AXES)])
    ws.append(["me_drift_rules", str(rules_path)])
    ws.append(["generic_lists_source", generics_src])
    ws.append(["claim_strength_terms", sum(len(v) for v in claim_strength.values())])
    ws.append(["hedge_terms", len(hedges)])
    ws.append(["absolute_terms", len(absolutes)])

    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_XLSX)

    print(f"[me-lexicon-build] wrote {OUT_XLSX}")
    print(f"[me-lexicon-build] generics: {generics_src}")
    for axis in SLOT_AXES:
        print(f"[me-lexicon-build]   slot_{axis}: {counts[f'slot_{axis}']} terms "
              f"(pill: {slots[axis]['pill']})")
    for cat in ("product_test", "fit_language", "canon_status", "drift_marker",
                "grounding", "contradiction", "jargon", "propaganda"):
        print(f"[me-lexicon-build]   {cat}: {counts[cat]} terms")
    print(f"[me-lexicon-build]   claim_strength: "
          f"{sum(len(v) for v in claim_strength.values())} terms, "
          f"hedges: {len(hedges)}, absolutes: {len(absolutes)}")


if __name__ == "__main__":
    main()
