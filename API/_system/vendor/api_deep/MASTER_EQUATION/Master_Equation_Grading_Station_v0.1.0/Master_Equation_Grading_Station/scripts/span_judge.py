"""span_judge.py -- Stage 3 of the Master Equation grading pipeline.

Span-level judgment pass using the DeepSeek chat API. Groups Stage 1 sentences
into spans (~3 sentences each, never crossing a blank-line paragraph break),
sends each span plus its Stage 1 lexicon hits as evidence, and collects a
strict-JSON judgment per span.

Also (re)generates the station's system prompt file
scripts/prompts/me_system_v0.1.0.txt from the rubric
scripts/rubric/me_rubric_v0.1.0.json, quoting the ten slot definitions and
five canon conditions verbatim.

Slot-signal quotes are verified against the source after every call:
exact / whitespace+quote-normalized / corrected (found elsewhere in the
corpus, sentence indices fixed) / dropped (unverifiable -- never presented
as data; recorded under dropped_signals instead).

Inputs:
  --paper <path>   the graded paper (its .lexicon.json must exist in
                   grading_out/; run lexicon_pass.py first)
  --limit N        grade only the first N spans (pilot mode)

Output:
  grading_out/<paper>.spans.json  (per-span judgments + run manifest with
  model, prompt sha256, rubric sha256, lexicon-cache sha256, quote
  verification counts, timestamps)
  grading_out/diagnostics/        raw invalid API responses (never presented
                                  as grades)

API: DeepSeek chat completions, model deepseek-chat, temperature 0.1,
max_tokens 2000, response_format json_object (falls back if unsupported),
concurrency 2, timeout 240s, one retry on invalid JSON.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

STATION_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
OUT_DIR = STATION_DIR / "grading_out"
DIAG_DIR = OUT_DIR / "diagnostics"
RUBRIC_PATH = SCRIPTS_DIR / "rubric" / "me_rubric_v0.1.0.json"
PROMPT_PATH = SCRIPTS_DIR / "prompts" / "me_system_v0.1.0.txt"
LEXICON_CACHE = SCRIPTS_DIR / "lexicon_cache.json"
WEIGHTS_PATH = SCRIPTS_DIR / "weights.json"

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"
TEMPERATURE = 0.1
MAX_TOKENS = 2000
TIMEOUT_S = 240
CONCURRENCY = 2

ROLES = ["SLOT_CLAIM", "PRODUCT_TEST", "FIT_CLAIM", "DEFINITION",
         "KILL_CONDITION", "EVIDENCE", "MECHANISM", "RHETORIC"]

SLOT_IDS = [f"slot.{a}" for a in
            ("g", "m", "e", "s_eff", "t", "k", "r", "q", "f", "c")]
FIT_VOCAB = ["direct", "analogous", "stretched", "absent"]
CANON_FLAGS = ["no_address", "ungraded_vocabulary", "receipt_missing",
               "authority_missing", "conflict_suspect"]

# Categories shown to the model as lexicon evidence.
EVIDENCE_CATEGORIES = [
    "slot_g", "slot_m", "slot_e", "slot_s_eff", "slot_t",
    "slot_k", "slot_r", "slot_q", "slot_f", "slot_c",
    "product_test", "fit_language", "canon_status", "drift_marker",
    "grounding", "contradiction", "jargon", "propaganda",
]

PROMPT_VERSION = "v0.1.0"


def load_weights():
    """Load scripts/weights.json (the tuning file). Fail loudly if missing."""
    if not WEIGHTS_PATH.exists():
        sys.exit(f"ERROR: tuning file not found: {WEIGHTS_PATH}\n"
                 "weights.json holds the category weights and tunables; restore it.")
    with open(WEIGHTS_PATH, encoding="utf-8") as f:
        return json.load(f)


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


# ---------------------------------------------------------------------------
# System prompt (built from the rubric; slot definitions and canon conditions
# quoted verbatim)
# ---------------------------------------------------------------------------

def build_system_prompt(rubric):
    slot_lines = []
    for sl in rubric["slots"]:
        slot_lines.append(
            f'- {sl["id"]} ({sl["symbol"]} — {sl["name"]}): {sl["definition"]}'
        )
    role_lines = "\n".join(
        f'- {r["id"]}: {r["meaning"]}' for r in rubric["span_roles"]
    )
    condition_lines = "\n".join(
        f'- {c["id"]}: {c["meaning"]}' for c in rubric["canon_conditions"]
    )
    return f"""You are the Master Equation span-mode judge {PROMPT_VERSION} (rubric {rubric["rubric_id"]}).

You grade OBSERVABLE TEXT ONLY. Rules you must never break:
- No inference about hidden motives, salvation status, or divine origin.
- Vocabulary is not structure; match slot signals to slot definitions, not vibes.
- Where evidence is missing, say so explicitly. Never invent precision.
- Return STRICT JSON ONLY. No prose, no markdown fences, no commentary.

THE TEN MASTER EQUATION SLOTS (verbatim from the rubric):
{chr(10).join(slot_lines)}

SPAN ROLES (assign exactly one per span):
{role_lines}

THE FIVE CANON CONDITIONS — flag a span when the claim it carries would fail
the condition as stated (verbatim from the rubric):
{condition_lines}

KILL CONDITIONS: {rubric["kill_condition_rule"]}

For each span you receive the span text and a lexicon-evidence block (per-sentence
matched terms per category, claim-strength counts, hedge/absolute counts). Treat the
lexicon hits as evidence pointers, not verdicts; confirm or discount them against the
actual span text.

SLOT SIGNAL RULES (strict):
- A slot_signal maps a span to a slot ONLY when the span engages that slot's
  definition as quoted above. A bare mention of the slot's symbol or vocabulary
  is NOT a signal. If no definition is engaged, omit the signal entirely.
- Each signal carries:
  * "slot_id": exactly one of {", ".join(SLOT_IDS)}.
  * "polarity": +1 if the span says the slot is filled / present / satisfied,
    -1 if it says the slot is empty / failed / violated, 0 if it merely
    discusses the slot without a fill verdict.
  * "fit": one of {", ".join(FIT_VOCAB)} — how the paper's content maps onto the
    slot. "absent" is a normal answer; do not fill slots to look complete.
  * "quote": a VERBATIM substring of the span text carrying the signal.
- Do not force a mapping. If a concept has no clean slot, say so in
  uncertainty_note instead.

Respond with ONE JSON object of exactly this shape:
{{
  "role": one of {", ".join(ROLES)},
  "slot_signals": [{{"slot_id": "slot.<axis>", "polarity": +1 or -1 or 0,
                     "fit": "direct|analogous|stretched|absent",
                     "quote": "<verbatim substring of the span>"}}],
  "gate_flags": ["<canon condition id>", ...],
  "kill_condition": "<verbatim falsification/kill condition, or empty string>",
  "confidence": 0.0-1.0,
  "uncertainty_note": "<what is missing or ambiguous; empty string if nothing>"
}}
Empty arrays are correct when there is no signal. Quotes must be verbatim
substrings of the span text; unverifiable quotes are dropped."""


def ensure_prompt_file(rubric):
    prompt = build_system_prompt(rubric)
    if not PROMPT_PATH.exists() or PROMPT_PATH.read_text(encoding="utf-8") != prompt:
        PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        PROMPT_PATH.write_text(prompt, encoding="utf-8")
        print(f"[span] wrote system prompt: {PROMPT_PATH}")
    return prompt


# ---------------------------------------------------------------------------
# Span construction
# ---------------------------------------------------------------------------

def build_spans(sentences, target):
    """Group consecutive sentences into spans of ~target sentences, never
    crossing a paragraph break."""
    spans = []
    current = []
    for s in sentences:
        if current and (s["paragraph"] != current[-1]["paragraph"] or len(current) >= target):
            spans.append(current)
            current = []
        current.append(s)
    if current:
        spans.append(current)
    return spans


def span_evidence(span_sents):
    per_sent = sentences_compact(span_sents)
    totals = {}
    for cat in EVIDENCE_CATEGORIES:
        terms = sorted({t for s in span_sents for t in s["categories"][cat]["matched_terms"]})
        if terms:
            totals[cat] = {"hits": sum(s["categories"][cat]["hits"] for s in span_sents),
                           "matched_terms": terms}
    cs = {k: sum(s["claim_strength"][k] for s in span_sents)
          for k in ("weak", "moderate", "strong", "forbidden")}
    return {"per_sentence": per_sent, "category_totals": totals,
            "claim_strength": cs,
            "hedges": sum(s["hedges"] for s in span_sents),
            "absolutes": sum(s["absolutes"] for s in span_sents)}


def sentences_compact(span_sents):
    out = []
    for s in span_sents:
        matched = {c: s["categories"][c]["matched_terms"]
                   for c in EVIDENCE_CATEGORIES
                   if s["categories"][c]["matched_terms"]}
        out.append({"idx": s["idx"], "matched": matched,
                    "claim_strength": {k: v for k, v in s["claim_strength"].items() if v},
                    "hedges": s["hedges"], "absolutes": s["absolutes"]})
    return out


# ---------------------------------------------------------------------------
# Quote verification (same discipline as relational_pass:
# exact / normalized / corrected / dropped)
# ---------------------------------------------------------------------------

_WS = re.compile(r"\s+")
_QUOTE_MAP = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "…": "...", "—": "--", "–": "-",
})


def norm_text(s):
    return _WS.sub(" ", str(s).translate(_QUOTE_MAP)).strip().lower()


def verify_signal_quote(quote, span_sents, sent_by_idx):
    """Return (status, corrected_sent_range_or_None).
    status: exact | normalized | corrected | failed.
    exact/normalized: found inside the span. corrected: found elsewhere in the
    paper's sentences. failed: unverifiable."""
    quote = str(quote or "").strip()
    if not quote:
        return "failed", None
    joined = " ".join(s["text"] for s in span_sents)
    if quote in joined:
        return "exact", None
    nq = norm_text(quote)
    if nq and nq in norm_text(joined):
        return "normalized", None
    hits = [i for i, s in sent_by_idx.items() if nq and nq in norm_text(s["text"])]
    if hits:
        return "corrected", [min(hits), max(hits)]
    return "failed", None


def verify_signals(judgment, span_sents, sent_by_idx):
    """Verify every slot_signal quote. Returns
    (verified_signals, dropped_signals, counts). Dropped signals are recorded,
    never presented as data."""
    verified, dropped = [], []
    counts = {"exact": 0, "normalized": 0, "corrected": 0, "dropped": 0}
    for sig in judgment.get("slot_signals", []):
        status, fixed_range = verify_signal_quote(sig.get("quote"), span_sents, sent_by_idx)
        if status == "failed":
            counts["dropped"] += 1
            dropped.append({"signal": sig, "reason": "quote_not_found"})
            continue
        counts[status] += 1
        sig = dict(sig)
        sig["quote_status"] = status
        if fixed_range is not None:
            sig["corrected_sent_range"] = fixed_range
        verified.append(sig)
    return verified, dropped, counts


# ---------------------------------------------------------------------------
# DeepSeek API
# ---------------------------------------------------------------------------

def extract_json(content):
    """Parse a model response as JSON, tolerating markdown fences."""
    content = content.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", content, re.S)
    if m:
        content = m.group(1)
    return json.loads(content)


def call_api(session, api_key, system_prompt, user_payload, use_json_mode=True):
    body = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
    }
    if use_json_mode:
        body["response_format"] = {"type": "json_object"}
    r = session.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=TIMEOUT_S,
    )
    if r.status_code == 400 and use_json_mode:
        # json mode unsupported / rejected: retry the call without it
        return call_api(session, api_key, system_prompt, user_payload, use_json_mode=False)
    r.raise_for_status()
    data = r.json()
    usage = data.get("usage") or {}
    usage = {k: usage.get(k) for k in
             ("prompt_tokens", "completion_tokens", "total_tokens",
              "prompt_cache_hit_tokens", "prompt_cache_miss_tokens")}
    return data["choices"][0]["message"]["content"], use_json_mode, usage


_diag_lock = threading.Lock()


def save_diagnostic(span_id, raw, reason):
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    path = DIAG_DIR / f"span_{span_id:04d}_{reason}.txt"
    with _diag_lock:
        path.write_text(raw if isinstance(raw, str) else json.dumps(raw, ensure_ascii=False, indent=1),
                        encoding="utf-8")
    return str(path)


def _norm_polarity(v):
    """Normalize polarity to +1/-1/0. Raises ValueError on anything else."""
    if v in (1, "+1", "+"):
        return 1
    if v in (-1, "-1", "-"):
        return -1
    if v in (0, "0"):
        return 0
    raise ValueError(f"invalid polarity: {v!r}")


def validate_judgment(obj):
    """Structural validation of one span judgment. Raises ValueError on any
    violation (bad slot_id, bad fit, bad polarity, unknown gate flag)."""
    if not isinstance(obj, dict):
        raise ValueError("judgment is not a JSON object")
    for key in ("role", "slot_signals", "gate_flags", "kill_condition",
                "confidence", "uncertainty_note"):
        if key not in obj:
            raise ValueError(f"missing key: {key}")
    if obj["role"] not in ROLES:
        raise ValueError(f"invalid role: {obj['role']}")
    if not isinstance(obj["slot_signals"], list):
        raise ValueError("slot_signals is not a list")
    for sig in obj["slot_signals"]:
        if not isinstance(sig, dict):
            raise ValueError("slot_signal is not an object")
        slot_id = sig.get("slot_id")
        if slot_id not in SLOT_IDS:
            raise ValueError(f"invalid slot_id: {slot_id!r}")
        sig["polarity"] = _norm_polarity(sig.get("polarity"))
        fit = str(sig.get("fit", "")).strip().lower()
        if fit not in FIT_VOCAB:
            raise ValueError(f"invalid fit: {fit!r}")
        sig["fit"] = fit
        if not str(sig.get("quote", "")).strip():
            raise ValueError("slot_signal quote is empty")
    for flag in obj["gate_flags"]:
        if flag not in CANON_FLAGS:
            raise ValueError(f"invalid gate flag: {flag!r}")
    if not isinstance(obj["kill_condition"], str):
        raise ValueError("kill_condition is not a string")
    try:
        obj["confidence"] = max(0.0, min(1.0, float(obj["confidence"])))
    except (TypeError, ValueError):
        raise ValueError(f"invalid confidence: {obj['confidence']!r}")
    obj["uncertainty_note"] = str(obj.get("uncertainty_note", ""))
    return obj


def grade_span(session, api_key, system_prompt, span_id, span_sents, sent_by_idx):
    text = "\n".join(s["text"] for s in span_sents)
    user_payload = json.dumps({
        "span_id": span_id,
        "span_text": text,
        "lexicon_evidence": span_evidence(span_sents),
    }, ensure_ascii=False)
    record = {
        "span_id": span_id,
        "sent_idx_start": span_sents[0]["idx"],
        "sent_idx_end": span_sents[-1]["idx"],
        "text": text,
    }
    last_raw, last_err = None, None
    for attempt in (1, 2):
        try:
            raw, json_mode, usage = call_api(session, api_key, system_prompt, user_payload)
            last_raw = raw
            judgment = validate_judgment(extract_json(raw))
            verified, dropped, qcounts = verify_signals(judgment, span_sents, sent_by_idx)
            judgment["slot_signals"] = verified
            record.update({"status": "ok", "judgment": judgment,
                           "dropped_signals": dropped,
                           "quote_counts": qcounts,
                           "attempts": attempt, "json_mode": json_mode,
                           "usage": usage})
            return record
        except (json.JSONDecodeError, ValueError) as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt == 1:
                save_diagnostic(span_id, last_raw or "", "invalid_json_attempt1")
                user_payload = json.dumps({
                    "span_id": span_id,
                    "span_text": text,
                    "lexicon_evidence": span_evidence(span_sents),
                    "correction": ("Your previous reply was not valid strict JSON of the "
                                   "required shape. Reply with ONLY the JSON object. "
                                   f"The error was: {last_err}"),
                }, ensure_ascii=False)
        except requests.RequestException as e:
            last_err = f"request error: {e}"
            save_diagnostic(span_id, last_err, "api_error")
            break
    diag = save_diagnostic(span_id, last_raw or last_err or "", "invalid_final")
    record.update({"status": "invalid", "judgment": None,
                   "error": last_err, "diagnostic_file": diag})
    return record


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Stage 3: ME span-level judgment pass (DeepSeek API).")
    ap.add_argument("--paper", required=True, help="Path to the graded paper.")
    ap.add_argument("--limit", type=int, default=None,
                    help="Grade only the first N spans (pilot).")
    args = ap.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        sys.exit("ERROR: DEEPSEEK_API_KEY env var is not set.")

    paper_path = Path(args.paper)
    lex_path = OUT_DIR / f"{paper_path.stem}.lexicon.json"
    if not lex_path.exists():
        sys.exit(f"ERROR: Stage 1 output not found: {lex_path}\nRun lexicon_pass.py first.")
    with open(lex_path, encoding="utf-8") as f:
        lex = json.load(f)

    with open(RUBRIC_PATH, encoding="utf-8") as f:
        rubric = json.load(f)
    rubric_roles = [r["id"] for r in rubric["span_roles"]]
    if rubric_roles != ROLES:
        sys.exit(f"ERROR: rubric span_roles {rubric_roles} do not match the "
                 f"judge's role list {ROLES}")
    tuning = load_weights()
    system_prompt = ensure_prompt_file(rubric)

    spans = build_spans(lex["sentences"], int(tuning.get("span_size", 3)))
    sent_by_idx = {s["idx"]: s for s in lex["sentences"]}
    total_spans = len(spans)
    if args.limit is not None:
        spans = spans[:args.limit]
    print(f"[span] {total_spans} spans total; judging {len(spans)} "
          f"(model={MODEL}, concurrency={CONCURRENCY})")

    manifest = {
        "model": MODEL,
        "base_url": BASE_URL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "prompt_version": PROMPT_VERSION,
        "prompt_file": str(PROMPT_PATH),
        "prompt_sha256": sha256_text(system_prompt),
        "rubric_file": str(RUBRIC_PATH),
        "rubric_sha256": sha256_file(RUBRIC_PATH),
        "weights_file": str(WEIGHTS_PATH),
        "weights_sha256": sha256_file(WEIGHTS_PATH),
        "lexicon_cache_file": str(LEXICON_CACHE),
        "lexicon_cache_sha256": sha256_file(LEXICON_CACHE) if LEXICON_CACHE.exists() else None,
        "lexicon_json": str(lex_path),
        "started_at": now_iso(),
        "limit": args.limit,
        "spans_total": total_spans,
        "spans_graded": len(spans),
    }

    started = now_iso()
    session = requests.Session()
    results = {}
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {
            pool.submit(grade_span, session, api_key, system_prompt, i, span, sent_by_idx): i
            for i, span in enumerate(spans)
        }
        done = 0
        for fut in as_completed(futures):
            rec = fut.result()
            results[rec["span_id"]] = rec
            done += 1
            if rec["status"] == "ok":
                j = rec["judgment"]
                flag = f"ok role={j['role']} signals={len(j['slot_signals'])}"
            else:
                flag = f"INVALID ({rec.get('error')})"
            print(f"[span] {done}/{len(spans)} span {rec['span_id']} "
                  f"s{rec['sent_idx_start']}-s{rec['sent_idx_end']}: {flag}")

    manifest["finished_at"] = now_iso()
    manifest["started_at"] = started
    manifest["ok"] = sum(1 for r in results.values() if r["status"] == "ok")
    manifest["invalid"] = sum(1 for r in results.values() if r["status"] != "ok")
    tok = lambda k: sum((r.get("usage") or {}).get(k) or 0 for r in results.values())
    manifest["tokens"] = {
        "prompt": tok("prompt_tokens"),
        "completion": tok("completion_tokens"),
        "total": tok("total_tokens"),
        "cache_hit": tok("prompt_cache_hit_tokens"),
        "cache_miss": tok("prompt_cache_miss_tokens"),
    }
    for k in ("exact", "normalized", "corrected", "dropped"):
        manifest[f"quotes_{k}"] = sum((r.get("quote_counts") or {}).get(k, 0)
                                      for r in results.values())

    out_path = OUT_DIR / f"{paper_path.stem}.spans.json"
    payload = {
        "paper": str(paper_path),
        "paper_name": paper_path.stem,
        "stage": "me_span_judge_v1",
        "manifest": manifest,
        "spans": [results[i] for i in sorted(results)],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"[span] ok={manifest['ok']} invalid={manifest['invalid']} "
          f"quotes: {manifest['quotes_exact']} exact / {manifest['quotes_normalized']} normalized / "
          f"{manifest['quotes_corrected']} corrected / {manifest['quotes_dropped']} dropped "
          f"-> {out_path}")


if __name__ == "__main__":
    main()
