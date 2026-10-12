"""canon_ledger_pass.py -- Stage 4 of the Master Equation grading pipeline.

The canon ledger. The fruits chain has no equivalent: this pass takes the
span judgments, normalizes the claims they carry into atoms, and then checks
each atom against the five canon conditions IN CODE (never the model's call):

  a. address     -- the clerk assigns M### ids in order of first appearance;
                    passes trivially once assigned.
  b. grade       -- passes iff proposed_grade is in the ruled vocabulary
                    (LOCKED | DERIVED | CANDIDATE; lifecycle INTAKE | OPENING |
                    REVIEW | FROZEN | ADMITTED). Anything else is flagged
                    ungraded_vocabulary.
  c. receipt     -- matches against RECORDED Lean receipts only (labels
                    derived from recorded checks, never typed values): the
                    gauntlet receipt, the floor module list, and the atom
                    draft if present. LEAN_PROVEN only when a recorded receipt
                    covers the claim's content tokens; otherwise NOT_ATTEMPTED.
  d. authority   -- passes iff the claim's source sentences cite a ruling
                    (canon_status / drift_marker lexicon hits, or a ruling /
                    ruling-date regex), or the paper header carries a
                    document-level ruling citation.
  e. no_conflict -- conflict_suspect when two claims assign opposed polarities
                    to the same slot, or when a canon-graded claim's sentences
                    carry a protected marker from the drift rules.

Verdicts: CANON-READY (all five pass) / HOLD (receipt NOT_ATTEMPTED or grade
ungraded) / NEEDS-RULING (authority or conflict fail; takes precedence over
HOLD). Missing any condition means not canon.

Inputs:
  --paper <path>   the graded paper (its .spans.json and .lexicon.json must
                   exist in grading_out/; run lexicon_pass.py and
                   span_judge.py first)
  --limit N        process only the first N claims (pilot mode)

Output:
  grading_out/<paper>.canon.json  canonical machine record (manifest + claims)
  grading_out/<paper>.canon.md    human docket for review, ending with the
                                  RETIREMENT WATCH section
  grading_out/<paper>.canoncache.json  memoized LLM normalization responses

Without DEEPSEEK_API_KEY the pass degrades gracefully: claims are collected,
LLM normalization is marked SKIPPED, atoms are built in code from the span
records (proposed_grade None -> grade condition fails -> HOLD), and the
remaining conditions are still evaluated.

API (when enabled): DeepSeek chat completions, model deepseek-chat,
temperature 0.1, JSON mode, one call per chunk of ~10 claims, responses
memoized to the disk cache.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

STATION_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
OUT_DIR = STATION_DIR / "grading_out"
RUBRIC_PATH = SCRIPTS_DIR / "rubric" / "me_rubric_v0.1.0.json"

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"
TEMPERATURE = 0.1
MAX_TOKENS = 4000
TIMEOUT_S = 240
CHUNK_SIZE = 10

CLAIM_ROLES = {"SLOT_CLAIM", "PRODUCT_TEST", "FIT_CLAIM", "DEFINITION", "KILL_CONDITION"}
CLAIM_FITS = {"direct", "analogous"}

GRADES = {"LOCKED", "DERIVED", "CANDIDATE",
          "INTAKE", "OPENING", "REVIEW", "FROZEN", "ADMITTED"}
CLAIM_TYPES = {"definition", "slot_claim", "product_test", "fit_claim",
               "kill_condition", "other"}

RECEIPT_COVERAGE_THRESHOLD = 0.30
RECEIPT_MIN_OVERLAP = 2
RECEIPT_HEURISTIC_NOTE = (
    "Fuzzy term overlap: claim content tokens (words >= 4 chars, stoplist "
    "removed, plus slot-name tokens for the claim's slot refs) are compared "
    "against each recorded receipt source's tokens (receipt text; for floor "
    "modules the file stem camel-split plus theorem/def/axiom/lemma names). "
    "LEAN_PROVEN iff token coverage >= 0.30 of claim tokens with at least 2 "
    "overlapping tokens in the best-matching recorded source; otherwise "
    "NOT_ATTEMPTED. Labels derive from recorded checks only; nothing is "
    "hand-typed."
)

RULING_RE = re.compile(
    r"canonical ruling|ratified|ruling\s*:|admitted to canon|eponym dictionary",
    re.IGNORECASE)
RULING_DATE_RE = re.compile(
    r"(?:january|february|march|april|may|june|july|august|september|october|"
    r"november|december)\s+\d{1,2},?\s+\d{4}", re.IGNORECASE)

_WORD_RE = re.compile(r"[A-Za-z][a-z]+")
_LEAN_DECL_RE = re.compile(r"\b(?:theorem|def|axiom|lemma)\s+([A-Za-z0-9_']+)")
STOPWORDS = {"that", "this", "with", "from", "into", "what", "when", "where",
             "which", "their", "there", "would", "could", "should", "about",
             "paper", "claim", "says", "said", "the", "and", "for"}

SLOT_IDS = [f"slot.{a}" for a in
            ("g", "m", "e", "s_eff", "t", "k", "r", "q", "f", "c")]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def find_system_config():
    """Walk up from this script to find _system/config/paths.json."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "_system" / "config" / "paths.json"
        if candidate.exists():
            return candidate
    return None


def load_paths():
    cfg_path = find_system_config()
    if cfg_path is None:
        return {}, None
    with open(cfg_path, encoding="utf-8") as f:
        return json.load(f), cfg_path


# ---------------------------------------------------------------------------
# Tokenization / receipt corpus
# ---------------------------------------------------------------------------

def content_tokens(text):
    return {t for t in (m.group(0).lower() for m in _WORD_RE.finditer(text or ""))
            if len(t) >= 4 and t not in STOPWORDS}


def camel_split(name):
    return re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z][a-z0-9]*|[a-z0-9]+", name)


def load_receipt_sources(paths):
    """Build the recorded-receipt corpus. Returns a list of
    {kind, path, sha256, tokens}. Reads via the lean_vault paths.json key."""
    sources = []
    vault = str(paths.get("lean_vault", "")).strip()
    if not vault:
        return sources
    vault = Path(vault)

    gauntlet = vault / "THEOPHYSICS_LIBRARY" / "_gauntlet" / "corpus_package" / \
        "RECEIPT_18OF18_2026-10-11.md"
    if gauntlet.exists():
        text = gauntlet.read_text(encoding="utf-8", errors="replace")
        sources.append({"kind": "gauntlet_receipt", "path": str(gauntlet),
                        "sha256": sha256_file(gauntlet),
                        "tokens": sorted(content_tokens(text))})

    floor = vault / "THEOPHYSICS_LIBRARY" / "00_FLOOR"
    if floor.is_dir():
        for lean in sorted(floor.glob("*.lean")):
            text = lean.read_text(encoding="utf-8", errors="replace")
            tokens = set(content_tokens(" ".join(camel_split(lean.stem))))
            tokens |= {t for name in _LEAN_DECL_RE.findall(text)
                       for t in content_tokens(" ".join(camel_split(name)))}
            sources.append({"kind": "floor_module", "path": str(lean),
                            "sha256": sha256_file(lean),
                            "tokens": sorted(tokens)})

    draft = vault / "THEOPHYSICS_LIBRARY" / "_design" / "LATEST_ATOM_DRAFT.json"
    if draft.exists():
        text = draft.read_text(encoding="utf-8", errors="replace")
        sources.append({"kind": "atom_draft", "path": str(draft),
                        "sha256": sha256_file(draft),
                        "tokens": sorted(content_tokens(text))})
    return sources


def load_protected_markers(paths):
    raw = str(paths.get("me_drift_rules", "")).strip()
    if not raw:
        return [], None
    p = Path(raw)
    if not p.exists():
        return [], None
    with open(p, encoding="utf-8") as f:
        rules = json.load(f)
    return [m.lower() for m in rules.get("protectedMarkers", [])], p


# ---------------------------------------------------------------------------
# Claim collection
# ---------------------------------------------------------------------------

def collect_claims(spans_doc):
    """Spans whose judgment role is a claim role, plus any span carrying a
    slot_signal with fit direct or analogous."""
    claims = []
    for sp in spans_doc.get("spans", []):
        if sp.get("status") != "ok":
            continue
        j = sp["judgment"]
        role = j.get("role")
        has_fit_signal = any(s.get("fit") in CLAIM_FITS
                             for s in j.get("slot_signals", []))
        if role not in CLAIM_ROLES and not has_fit_signal:
            continue
        claims.append({
            "span_id": sp["span_id"],
            "role": role,
            "text": sp["text"],
            "sent_idx_start": sp["sent_idx_start"],
            "sent_idx_end": sp["sent_idx_end"],
            "slot_signals": j.get("slot_signals", []),
            "gate_flags": j.get("gate_flags", []),
            "kill_condition": j.get("kill_condition", ""),
        })
    return claims


def degraded_atoms(claims):
    """No-API atoms built in code from the span records. proposed_grade is
    None, so the grade condition fails and the claim lands on HOLD."""
    role_to_type = {"SLOT_CLAIM": "slot_claim", "PRODUCT_TEST": "product_test",
                    "FIT_CLAIM": "fit_claim", "DEFINITION": "definition",
                    "KILL_CONDITION": "kill_condition"}
    atoms = []
    for c in claims:
        atoms.append({
            "statement": " ".join(c["text"].split())[:400],
            "claim_type": role_to_type.get(c["role"], "other"),
            "slot_refs": sorted({s["slot_id"] for s in c["slot_signals"]}),
            "source_spans": [c["span_id"]],
            "source_sentences": list(range(c["sent_idx_start"], c["sent_idx_end"] + 1)),
            "kill_condition": c.get("kill_condition", ""),
            "proposed_grade": None,
        })
    return atoms


# ---------------------------------------------------------------------------
# LLM normalization (memoized)
# ---------------------------------------------------------------------------

NORMALIZE_SYSTEM_PROMPT = """You are the Master Equation canon-ledger normalizer v0.1.0.

You receive a list of claims extracted from a paper (each with its span id,
span role, source text, and slot signals). Normalize each claim into ONE atom.

Reply with STRICT JSON ONLY: {"atoms": [ ... ]}, one atom per input claim, in
the same order, each atom exactly:
{
  "statement": "<the claim as one crisp declarative sentence>",
  "claim_type": "definition|slot_claim|product_test|fit_claim|kill_condition|other",
  "slot_refs": ["slot.g", ...],
  "source_spans": [<span ids from the input>],
  "source_sentences": [<sentence indices from the input>],
  "kill_condition": "<verbatim falsification/kill condition, or empty string>",
  "proposed_grade": "<grade>"
}

proposed_grade MUST be one of the ruled vocabulary and nothing else:
LOCKED | DERIVED | CANDIDATE | INTAKE | OPENING | REVIEW | FROZEN | ADMITTED
Any other label is invalid. If the claim carries no grade vocabulary, use
"INTAKE". Never invent labels. Never add keys. Never merge two claims into
one atom or split one claim into two."""


def extract_json(content):
    content = content.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", content, re.S)
    if m:
        content = m.group(1)
    return json.loads(content)


def call_api(session, api_key, system_prompt, user_payload):
    body = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
        "response_format": {"type": "json_object"},
    }
    r = session.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=TIMEOUT_S,
    )
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"], data.get("usage") or {}


def validate_atom(obj):
    if not isinstance(obj, dict):
        raise ValueError("atom is not a JSON object")
    for key in ("statement", "claim_type", "slot_refs", "source_spans",
                "source_sentences", "kill_condition", "proposed_grade"):
        if key not in obj:
            raise ValueError(f"missing key: {key}")
    if obj["claim_type"] not in CLAIM_TYPES:
        raise ValueError(f"invalid claim_type: {obj['claim_type']!r}")
    obj["slot_refs"] = [s for s in obj["slot_refs"] if s in SLOT_IDS]
    if obj["proposed_grade"] is not None:
        obj["proposed_grade"] = str(obj["proposed_grade"]).strip().upper()
    obj["kill_condition"] = str(obj.get("kill_condition") or "")
    obj["statement"] = str(obj["statement"]).strip()
    if not obj["statement"]:
        raise ValueError("empty statement")
    return obj


def normalize_claims(session, api_key, claims, cache, cache_dirty):
    """One call per chunk of ~10 claims, memoized to the disk cache.
    Returns (atoms, api_calls, token_totals, cache_dirty)."""
    atoms = []
    api_calls = 0
    tokens = {"prompt": 0, "completion": 0, "total": 0}
    for start in range(0, len(claims), CHUNK_SIZE):
        chunk = claims[start:start + CHUNK_SIZE]
        payload_obj = {
            "claims": [{
                "span_id": c["span_id"], "role": c["role"],
                "sent_idx_start": c["sent_idx_start"],
                "sent_idx_end": c["sent_idx_end"],
                "text": c["text"], "slot_signals": c["slot_signals"],
                "kill_condition": c.get("kill_condition", ""),
            } for c in chunk],
        }
        payload = json.dumps(payload_obj, ensure_ascii=False)
        key = sha256_text(NORMALIZE_SYSTEM_PROMPT + "\n" + payload)
        if key in cache:
            raw = cache[key]
        else:
            last_err = None
            raw = None
            for attempt in (1, 2):
                try:
                    raw, usage = call_api(session, api_key, NORMALIZE_SYSTEM_PROMPT, payload)
                    api_calls += 1
                    tokens["prompt"] += usage.get("prompt_tokens") or 0
                    tokens["completion"] += usage.get("completion_tokens") or 0
                    tokens["total"] += usage.get("total_tokens") or 0
                    extract_json(raw)  # probe
                    break
                except Exception as e:  # JSON or request error: one retry
                    last_err = e
                    raw = None
            if raw is None:
                print(f"[canon] chunk at claim {start}: LLM failed ({last_err}); "
                      "falling back to degraded atoms for this chunk")
                atoms.extend(degraded_atoms(chunk))
                continue
            cache[key] = raw
            cache_dirty = True
        try:
            chunk_atoms = extract_json(raw)["atoms"]
        except (json.JSONDecodeError, KeyError, TypeError):
            atoms.extend(degraded_atoms(chunk))
            continue
        by_span = {c["span_id"]: c for c in chunk}
        for obj in chunk_atoms:
            try:
                atoms.append(validate_atom(obj))
            except ValueError as e:
                # keep the raw claim, degraded: invalid atoms never vanish
                fallback = degraded_atoms([by_span.get(obj.get("source_spans", [None])[0],
                                                         chunk[0])])[0]
                fallback["atom_error"] = str(e)
                atoms.append(fallback)
    return atoms, api_calls, tokens, cache_dirty


# ---------------------------------------------------------------------------
# The five conditions (in code; never the model's call)
# ---------------------------------------------------------------------------

def check_grade(proposed_grade):
    """b. grade: passes iff the proposed grade is in the ruled vocabulary."""
    if proposed_grade is None:
        return {"pass": False, "flag": "ungraded_vocabulary",
                "detail": "no proposed grade (normalization skipped or failed)"}
    g = str(proposed_grade).strip().upper()
    if g in GRADES:
        return {"pass": True, "flag": None, "detail": f"grade {g} is in the ruled vocabulary"}
    return {"pass": False, "flag": "ungraded_vocabulary",
            "detail": f"grade {g!r} is outside the ruled vocabulary"}


def check_receipt(atom, receipt_sources, slot_names):
    """c. receipt: LEAN_PROVEN only when a recorded receipt covers the claim's
    content tokens; otherwise NOT_ATTEMPTED."""
    if not receipt_sources:
        return {"pass": False, "status": "NOT_ATTEMPTED", "matched_source": None,
                "score": 0.0, "detail": "no recorded receipt sources available"}
    tokens = set(content_tokens(atom.get("statement", "")))
    for ref in atom.get("slot_refs", []):
        name = slot_names.get(ref, "")
        tokens |= content_tokens(" ".join(camel_split(name)))
    if not tokens:
        return {"pass": False, "status": "NOT_ATTEMPTED", "matched_source": None,
                "score": 0.0, "detail": "claim carries no content tokens"}
    best, best_score, best_overlap = None, 0.0, 0
    for src in receipt_sources:
        inter = tokens & set(src["tokens"])
        score = len(inter) / max(1, len(tokens))
        if score > best_score:
            best, best_score, best_overlap = src, score, len(inter)
    proven = best_score >= RECEIPT_COVERAGE_THRESHOLD and best_overlap >= RECEIPT_MIN_OVERLAP
    return {"pass": proven,
            "status": "LEAN_PROVEN" if proven else "NOT_ATTEMPTED",
            "matched_source": best["path"] if best else None,
            "score": round(best_score, 4),
            "detail": (f"coverage {best_score:.2f} (threshold "
                       f"{RECEIPT_COVERAGE_THRESHOLD}, min overlap "
                       f"{RECEIPT_MIN_OVERLAP})")}


def check_authority(sent_texts, header_text, sent_canon_hits=0, sent_drift_hits=0):
    """d. authority: passes iff the claim's source sentences cite a ruling
    (lexicon canon_status/drift_marker hits or a ruling/ruling-date regex),
    or the paper header carries a document-level ruling citation."""
    joined = " ".join(sent_texts)
    if sent_canon_hits or sent_drift_hits:
        return {"pass": True, "via": "span_lexicon",
                "detail": f"canon_status hits={sent_canon_hits}, drift_marker hits={sent_drift_hits} in claim sentences"}
    if RULING_RE.search(joined) or RULING_DATE_RE.search(joined):
        return {"pass": True, "via": "span_regex",
                "detail": "ruling or ruling-date pattern in claim sentences"}
    if header_text and (RULING_RE.search(header_text) and RULING_DATE_RE.search(header_text)):
        return {"pass": True, "via": "paper_header",
                "detail": "document-level ruling citation in the paper header"}
    return {"pass": False, "via": "none", "detail": "no ruling citation found",
            "flag": "authority_missing"}


def check_no_conflict(atom, atom_polarities, all_polarities, protected_markers, sent_texts):
    """e. no_conflict: conflict_suspect when another claim assigns the opposed
    polarity to the same slot, or when a canon-graded claim's sentences carry
    a protected marker."""
    own_id = atom.get("id")
    for slot_id, pol in atom_polarities.items():
        if pol == 0:
            continue
        for other_id, other_pols in all_polarities.items():
            if other_id == own_id:
                continue
            if other_pols.get(slot_id) == -pol:
                return {"pass": False, "flag": "conflict_suspect",
                        "detail": f"opposed polarity on {slot_id} between {own_id} and {other_id}"}
    grade = (atom.get("proposed_grade") or "").upper()
    if grade in ("LOCKED", "DERIVED", "CANDIDATE"):
        joined = " ".join(sent_texts).lower()
        for marker in protected_markers:
            if marker in joined:
                return {"pass": False, "flag": "conflict_suspect",
                        "detail": f"canon grade {grade} on text carrying protected marker {marker!r}"}
    return {"pass": True, "flag": None, "detail": "no opposed slot assignment, no protected-marker collision"}


def verdict(conditions):
    """CANON-READY (all five pass) / NEEDS-RULING (authority or conflict fail;
    takes precedence) / HOLD (receipt or grade fail)."""
    if not conditions["authority"]["pass"] or not conditions["no_conflict"]["pass"]:
        return "NEEDS-RULING"
    if not conditions["grade"]["pass"] or not conditions["receipt"]["pass"]:
        return "HOLD"
    if not conditions["address"]["pass"]:
        return "HOLD"
    return "CANON-READY"


# ---------------------------------------------------------------------------
# Main pass
# ---------------------------------------------------------------------------

def sentence_evidence(lex, sent_idxs):
    """(texts, canon_status hits, drift_marker hits) for the given sentences."""
    by_idx = {s["idx"]: s for s in lex["sentences"]}
    texts, canon_hits, drift_hits = [], 0, 0
    for i in sent_idxs:
        s = by_idx.get(i)
        if s is None:
            continue
        texts.append(s["text"])
        canon_hits += s["categories"]["canon_status"]["hits"]
        drift_hits += s["categories"]["drift_marker"]["hits"]
    return texts, canon_hits, drift_hits


def main():
    ap = argparse.ArgumentParser(description="Stage 4: ME canon ledger pass.")
    ap.add_argument("--paper", required=True, help="Path to the graded paper.")
    ap.add_argument("--limit", type=int, default=None,
                    help="Process only the first N claims (pilot).")
    args = ap.parse_args()

    paper_path = Path(args.paper)
    spans_path = OUT_DIR / f"{paper_path.stem}.spans.json"
    lex_path = OUT_DIR / f"{paper_path.stem}.lexicon.json"
    for p in (spans_path, lex_path):
        if not p.exists():
            sys.exit(f"ERROR: missing {p} -- run lexicon_pass.py and span_judge.py first.")
    spans_doc = json.loads(spans_path.read_text(encoding="utf-8"))
    lex = json.loads(lex_path.read_text(encoding="utf-8"))
    paper_text = paper_path.read_text(encoding="utf-8")
    header_text = paper_text[:1500]

    with open(RUBRIC_PATH, encoding="utf-8") as f:
        rubric = json.load(f)
    slot_names = {sl["id"]: sl["name"] for sl in rubric["slots"]}

    paths, paths_cfg = load_paths()
    receipt_sources = load_receipt_sources(paths)
    protected_markers, drift_rules_path = load_protected_markers(paths)

    claims = collect_claims(spans_doc)
    total_claims = len(claims)
    if args.limit is not None:
        claims = claims[:args.limit]
    print(f"[canon] {total_claims} claims collected; processing {len(claims)}")

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    cache_path = OUT_DIR / f"{paper_path.stem}.canoncache.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    cache_dirty = False

    if api_key:
        import requests
        session = requests.Session()
        atoms, api_calls, tokens, cache_dirty = normalize_claims(
            session, api_key, claims, cache, cache_dirty)
        normalization = "ok"
    else:
        print("[canon] DEEPSEEK_API_KEY not set -- normalization SKIPPED "
              "(degraded mode: atoms built in code, grade condition fails)")
        atoms, api_calls = degraded_atoms(claims), 0
        tokens = {"prompt": 0, "completion": 0, "total": 0}
        normalization = "skipped_no_api_key"
    if cache_dirty:
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                              encoding="utf-8")

    raw_by_span = {c["span_id"]: c for c in claims}

    # a. address -- the clerk assigns M### ids in order of first appearance.
    for n, atom in enumerate(atoms, start=1):
        atom["id"] = f"M{n:03d}"

    # polarities per atom, from the source spans' verified slot signals.
    atom_polarities = {}
    for atom in atoms:
        pols = {}
        for span_id in atom.get("source_spans", []):
            raw = raw_by_span.get(span_id)
            if raw is None:
                continue
            for sig in raw["slot_signals"]:
                if sig.get("slot_id") in atom.get("slot_refs", []) or not atom.get("slot_refs"):
                    pols[sig["slot_id"]] = sig.get("polarity", 0)
        atom_polarities[atom["id"]] = pols

    # conditions + verdicts
    verdict_counts = {"CANON-READY": 0, "HOLD": 0, "NEEDS-RULING": 0}
    for atom in atoms:
        sent_idxs = atom.get("source_sentences") or []
        texts, canon_hits, drift_hits = sentence_evidence(lex, sent_idxs)
        conditions = {
            "address": {"pass": True, "detail": f"assigned {atom['id']} (first appearance order)"},
            "grade": check_grade(atom.get("proposed_grade")),
            "receipt": check_receipt(atom, receipt_sources, slot_names),
            "authority": check_authority(texts, header_text, canon_hits, drift_hits),
            "no_conflict": check_no_conflict(atom, atom_polarities[atom["id"]],
                                             atom_polarities, protected_markers, texts),
        }
        atom["conditions"] = conditions
        atom["flags"] = sorted({c["flag"] for c in conditions.values() if c.get("flag")})
        atom["verdict"] = verdict(conditions)
        verdict_counts[atom["verdict"]] += 1

    # demotion path: compare receipt source hashes against any previous run.
    previous_path = OUT_DIR / f"{paper_path.stem}.canon.json"
    retirement = []
    previous_hashes = {}
    if previous_path.exists():
        try:
            prev = json.loads(previous_path.read_text(encoding="utf-8"))
            previous_hashes = {s["path"]: s["sha256"]
                               for s in prev.get("manifest", {}).get("receipt_sources", [])}
        except (json.JSONDecodeError, KeyError):
            previous_hashes = {}
    current_hashes = {s["path"]: s["sha256"] for s in receipt_sources}
    for atom in atoms:
        matched = atom["conditions"]["receipt"].get("matched_source")
        if matched and matched in previous_hashes and previous_hashes[matched] != current_hashes.get(matched):
            retirement.append({
                "id": atom["id"], "reason": "receipt_source_changed",
                "detail": f"receipt source {matched} changed since the previous canon.json",
                "statement": atom["statement"]})
        nc = atom["conditions"]["no_conflict"]
        if not nc["pass"] and "protected marker" in nc.get("detail", ""):
            retirement.append({
                "id": atom["id"], "reason": "protected_marker_conflict",
                "detail": nc["detail"], "statement": atom["statement"]})

    manifest = {
        "model": MODEL if api_key else None,
        "base_url": BASE_URL if api_key else None,
        "temperature": TEMPERATURE,
        "normalization": normalization,
        "normalize_prompt_sha256": sha256_text(NORMALIZE_SYSTEM_PROMPT),
        "canon_cache_file": str(cache_path),
        "rubric_file": str(RUBRIC_PATH),
        "rubric_sha256": sha256_file(RUBRIC_PATH),
        "receipt_sources": [{k: s[k] for k in ("kind", "path", "sha256")}
                            for s in receipt_sources],
        "receipt_matching": RECEIPT_HEURISTIC_NOTE,
        "drift_rules_file": str(drift_rules_path) if drift_rules_path else None,
        "drift_rules_sha256": sha256_file(drift_rules_path) if drift_rules_path else None,
        "spans_json": str(spans_path),
        "lexicon_json": str(lex_path),
        "claims_collected": total_claims,
        "claims_processed": len(atoms),
        "api_calls": api_calls,
        "tokens": tokens,
        "verdict_counts": verdict_counts,
        "retirement_watch_count": len(retirement),
        "limit": args.limit,
    }

    payload = {
        "paper": str(paper_path),
        "paper_name": paper_path.stem,
        "generated_at": now_iso(),
        "stage": "me_canon_ledger_v1",
        "manifest": manifest,
        "claims": atoms,
        "retirement_watch": retirement,
    }
    with open(previous_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    md_path = OUT_DIR / f"{paper_path.stem}.canon.md"
    md_path.write_text(render_docket(payload, lex), encoding="utf-8")

    print(f"[canon] verdicts: {verdict_counts} "
          f"({normalization}, api_calls={api_calls})")
    print(f"[canon] wrote {previous_path}")
    print(f"[canon] wrote {md_path}")


def render_docket(payload, lex):
    m = payload["manifest"]
    lines = [
        f"# Canon Docket — {payload['paper_name']}",
        "",
        f"Generated {payload['generated_at']} · stage `{payload['stage']}` · "
        f"normalization `{m['normalization']}`"
        + (f" · model `{m['model']}`" if m.get("model") else ""),
        "",
        f"Claims processed: {m['claims_processed']} of {m['claims_collected']} collected · "
        f"CANON-READY {m['verdict_counts']['CANON-READY']} · "
        f"HOLD {m['verdict_counts']['HOLD']} · "
        f"NEEDS-RULING {m['verdict_counts']['NEEDS-RULING']}",
        "",
        f"Receipt matching: {m['receipt_matching']}",
        "",
    ]
    by_idx = {s["idx"]: s["text"] for s in lex["sentences"]}
    for vclass in ("CANON-READY", "HOLD", "NEEDS-RULING"):
        lines.append(f"## {vclass}")
        lines.append("")
        group = [c for c in payload["claims"] if c["verdict"] == vclass]
        if not group:
            lines.append("_(none)_")
            lines.append("")
            continue
        for c in group:
            cond = c["conditions"]
            lines.append(f"### {c['id']} — {c['claim_type']}")
            lines.append("")
            lines.append(f"**Statement:** {c['statement']}")
            lines.append("")
            lines.append(f"- **Grade proposed:** {c.get('proposed_grade') or '—'}")
            lines.append(f"- **Slots:** {', '.join(c.get('slot_refs') or []) or '—'}")
            lines.append(f"- **Source spans:** {', '.join(str(s) for s in c.get('source_spans', []))}")
            checklist = []
            for key, label in (("address", "address"), ("grade", "grade"),
                               ("receipt", "receipt"), ("authority", "authority"),
                               ("no_conflict", "no_conflict")):
                mark = "x" if cond[key]["pass"] else " "
                extra = cond[key].get("status") or cond[key].get("via") or ""
                checklist.append(f"  - [{mark}] **{label}**"
                                 + (f" ({extra})" if extra else "")
                                 + f" — {cond[key]['detail']}")
            lines.append("- **Five conditions:**")
            lines.extend(checklist)
            if c.get("kill_condition"):
                lines.append(f"- **Kill condition:** {c['kill_condition']}")
            if c.get("flags"):
                lines.append(f"- **Flags:** {', '.join(c['flags'])}")
            quotes = [by_idx[i] for i in (c.get("source_sentences") or [])[:3] if i in by_idx]
            if quotes:
                lines.append("- **Source sentences:**")
                for q in quotes:
                    lines.append(f"  > {q}")
            lines.append("")
    lines.append("## RETIREMENT WATCH")
    lines.append("")
    watch = payload.get("retirement_watch", [])
    if not watch:
        lines.append("_Empty — no receipt source changed since the previous "
                     "canon.json, and no canon-graded claim collides with a "
                     "protected marker. (First run is always empty by "
                     "construction; the mechanism compares against the "
                     "previous run.)_")
    else:
        for w in watch:
            lines.append(f"- **{w['id']}** ({w['reason']}): {w['detail']}")
            lines.append(f"  - {w['statement']}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
