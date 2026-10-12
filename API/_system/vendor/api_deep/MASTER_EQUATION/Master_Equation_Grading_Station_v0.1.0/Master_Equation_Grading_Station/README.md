# Master Equation Grading Station

This station grades papers against the Master Equation frame: the ten factor
slots (G, M, E, S_eff, T, K, R, Q, F, C), the product test (multiplicative vs
additive), fit language (direct | analogous | stretched | absent),
canon-status vocabulary, and drift markers (protected markers and context
cues from the canon drift rules).

It is cloned from the Fruits of the Spirit Grading Station v0.3.0. All seven
passes now run end to end: **Stage 1** is the local, no-API half (lexicon
build, lexicon pass, statistics engine, Excel workbook); **Stage 2** adapts
the span judge and adds the canon ledger — the point of the station;
**Stage 3** adapts the report page (ME heartbeat, slot chart, span ledger,
canon docket, generated Reading). Only `relational_pass.py` and
`fruits_grade.py` are still copied unchanged and speak "fruits" internally —
they are not part of the run chain.

## Files

- `run_me_validate_only.bat` — local validation: builds the lexicon workbook,
  then runs lexicon pass + stats engine + stats workbook on the W3 Master
  Equation canonical paper. No API calls.
- `run_me_pilot.bat` — the full 7-pass chain with the two LLM passes capped
  (`span_judge --limit 12`, `canon_ledger --limit 12`), so a smoke test costs
  a handful of API calls. Paper is `%1`, else the resolved W3 pilot paper.
- `run_me_full.bat` — the full 7-pass chain on one paper
  (`run_me_full.bat "path\to\paper.md"`). Each pass prints a timestamped
  `[N/7] <name>` line; on failure the bat names the pass that died.
- `install_me_requirements.bat` — installs the Python requirements
  (`openpyxl` for the workbooks; `python-docx`/`pypdf` for the fruits-grade
  runner's DOCX/PDF inputs later).
- `config.json` — run settings for the (still fruits-flavoured) API runner.
  `input_dir` is the placeholder `@paths:gold_canon_source`; the launchers
  resolve the real folder from `_system\config\paths.json` through
  `scripts\station_paths.py`. Contains environment-variable **names**, never
  API keys.
- `scripts\me_lexicon_build.py` — Stage 0. Builds `ME_LEXICON_V1.xlsx` (one
  level above the versioned station folder, in `MASTER_EQUATION\`) from:
  - the ME pill atoms (paths.json key `me_pills`),
  - the drift rules (paths.json key `me_drift_rules`),
  - the generic epistemic lists (claim strength, hedges, absolutes,
    grounding, contradiction, jargon, propaganda), carried over from the
    sibling FRUITS station workbooks when present, with baked-in fallbacks.
- `scripts\lexicon_pass.py` — Stage 1. Sentence splitter + regex lexicon
  matching against `ME_LEXICON_V1.xlsx`; writes
  `grading_out\<paper>.lexicon.json` (stage string `me_lexicon_pass_v1`).
- `scripts\stats_engine.py` — Stage 2. ~200 stats over the lexicon JSON,
  driven by `scripts\weights.json`; writes `grading_out\<paper>.stats.json`
  (stage string `me_stats_engine_v1`). The ME_SCORE formula (the TRUTH
  analogue) is documented in `weights.json` under `_me_formula_note`.
- `scripts\stats_workbook.py` — renders `grading_out\<paper>.stats.xlsx`
  (Summary, All_Statistics, Per_Sentence, Slot_Profile, Spikes, Spans; the
  Spans sheet appears once a spans file exists).
- `scripts\station_paths.py` — prints a path from `_system\config\paths.json`
  (found by walking up). Used by the launchers so machine paths stay out of
  code.
- `scripts\span_judge.py` — Stage 3 (DeepSeek). Judges ~3-sentence spans
  against `scripts\rubric\me_rubric_v0.1.0.json`; roles SLOT_CLAIM |
  PRODUCT_TEST | FIT_CLAIM | DEFINITION | KILL_CONDITION | EVIDENCE |
  MECHANISM | RHETORIC; per-span `slot_signals` with verified quotes
  (exact/normalized/corrected/dropped — dropped quotes are never presented as
  data); canon-condition gate flags; verbatim kill conditions. Writes
  `grading_out\<paper>.spans.json` (stage `me_span_judge_v1`) and
  regenerates `scripts\prompts\me_system_v0.1.0.txt` from the rubric.
- `scripts\canon_ledger_pass.py` — Stage 4, the canon ledger. Collects claims
  from the spans, normalizes them to atoms (DeepSeek, memoized to
  `grading_out\<paper>.canoncache.json`; degrades gracefully with no API
  key), then checks the five canon conditions **in code**: address (M###),
  grade vocabulary, recorded Lean receipts (via the `lean_vault` paths.json
  key), ruling-citation authority, and slot/protected-marker conflict.
  Verdicts CANON-READY / HOLD / NEEDS-RULING. Writes
  `grading_out\<paper>.canon.json` + `grading_out\<paper>.canon.md` (the
  review docket, ending in RETIREMENT WATCH). Stage `me_canon_ledger_v1`.
- `scripts\report_page.py` — Stage 5. Renders the single self-contained
  `grading_out\<paper>.report.html`: stats ribbon, ME heartbeat chart (SMA-9
  over the weighted ME signal, with hover inspector), slot coverage chart
  (absent slots show a red dashed ABSENT box, never a silent zero bar),
  product-test span section, clickable span ledger (dropped quotes collected
  in a collapsed "dropped, never data" block), the canon docket table (per
  claim: five ✓/✗ checks with tooltip detail, verdict badge, filter buttons,
  retirement watch), and The Reading — a five-section narrative generated from
  `scripts\prompts\me_narrative_v1.0.txt`, cached in
  `grading_out\<paper>.narrative.json` (keyed by the data brief + prompt
  hashes; a cache hit costs 0 API calls). Stage `me_report_page_v1`. Skips the
  narrative gracefully without a DeepSeek key.
- `scripts\charts_svg.py` — inline-SVG chart builders (heartbeat, donut,
  slot profile) used by the report page. ME-adapted in Stage 3.
- `scripts\tests\test_me_pipeline.py` — unit tests for the span validator,
  quote verification, and the five-condition logic (`py -3 -m unittest
  discover -s scripts\tests -p "test_me_*.py"`). No API calls.

## Required paths.json keys

Set in `API\_system\config\paths.json` (machine-specific, never committed):

- `me_pills` — folder of ME pill JSON-LD atoms
  (e.g. `...\Faith-through-physics-atoms\master-equation\01_canonical`)
- `me_drift_rules` — `master-equation.rules.json`
- `gold_canon_source` — folder holding the canonical papers
  (e.g. `...\Faith-through-physics-atoms\_runtime\canon-source`); the pilot
  paper `W3-master-equation.canonical.md` is read from here.
- `lean_vault` — the Lean 4 Files vault folder (the one holding
  `THEOPHYSICS_LIBRARY`); the canon ledger reads the gauntlet receipt
  (`_gauntlet\corpus_package\RECEIPT_18OF18_2026-10-11.md`), the floor module
  list (`00_FLOOR\*.lean`), and `_design\LATEST_ATOM_DRAFT.json` when present.

## Pass order

1. `me_lexicon_build.py` — build/rebuild `ME_LEXICON_V1.xlsx` (rerun after
   editing pills, drift rules, or curated terms).
2. `lexicon_pass.py --paper <paper.md>` — per-sentence lexicon JSON.
3. `stats_engine.py --paper <paper.md>` — stats JSON (+ console table of the
   in-report stats).
4. `stats_workbook.py --paper <paper.md>` — Excel workbook.
5. `span_judge.py --paper <paper.md> [--limit N]` — span judgments
   (DeepSeek; requires `DEEPSEEK_API_KEY`).
6. `canon_ledger_pass.py --paper <paper.md> [--limit N]` — the canon ledger
   (DeepSeek for normalization; runs degraded without a key).
7. `report_page.py --paper <paper.md>` — the HTML report page (DeepSeek for
   The Reading; skips the narrative gracefully without a key).

`run_me_full.bat` and `run_me_pilot.bat` run exactly this order.

## Artifact family

Everything lands in `grading_out\`, one set per paper (`<stem>` is the paper
filename without extension):

- `<stem>.lexicon.json` — per-sentence lexicon hits
- `<stem>.stats.json` — the ~200 stats + series
- `<stem>.stats.xlsx` — the Excel workbook
- `<stem>.spans.json` — span judgments (stage 5 input)
- `<stem>.canon.json` + `<stem>.canon.md` — the canon ledger and docket
- `<stem>.canoncache.json` — memoized claim normalization (API saver)
- `<stem>.narrative.json` — cached narrative for The Reading
- `<stem>.report.html` — the single self-contained report page
- `diagnostics\` — per-pass failure diagnostics when something goes wrong

## Safe operating sequence

1. Run `install_me_requirements.bat` once.
2. Run `run_me_validate_only.bat` — all local, no API key needed.
3. Run the unit tests: `py -3 -m unittest discover -s scripts\tests -p "test_me_*.py"`.
4. With `DEEPSEEK_API_KEY` set, run `run_me_pilot.bat` (LLM passes capped at
   12 spans / claims) and review `grading_out\<paper>.canon.md` and
   `<paper>.report.html` before any wider run.
5. Run `run_me_full.bat "path\to\paper.md"` for the full grading. The canon
   ledger memoizes normalization (`canoncache.json`) and the report caches
   the narrative, so reruns only pay for what changed.

## Known measurement notes

- Single-letter slot symbols (G, M, E, T, K, R, Q, F, C) are lexicon terms;
  matching is case-insensitive with word boundaries, so they catch the
  equation lines (genuine slot usage) with a small false-positive risk in
  prose. `S_eff` is multi-character and unambiguous.
- `canon_status` and `fit_language` contain ordinary English words ("draft",
  "review", "direct", "absent"); treat their counts as vocabulary-density
  signals, not adjudications.
- The old `ME_VARS` sheet in the fruits `LEXICON_V2.xlsx` uses a superseded
  ten-variable scheme (G=gravity/belonging, …) and is **not** used; the slot
  definitions come from the canonical pills ME-01-020..029.

## Scope boundary

The station measures observable vocabulary in the text: slot coverage,
product-test language, fit vocabulary, canon-status terms, drift markers, and
generic epistemic signals. It does not judge whether the paper's claims are
true, and it never calls an API in Stage 1.
