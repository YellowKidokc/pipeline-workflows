# CLAUDE CODE PROMPT: finish the quick call / 00_PREP gate (v0.1)
**Date:** 2026-10-23 | **Author:** Claude (Sonnet) with David | **Status:** ready for a builder, read receipt first

## Read receipt (first message back, before any edit)
Restate in your own words: (1) why UUIDs are minted in exactly one place (`identity.py`) and never re-minted,
(2) why a Master Equation id and the graph tags are AI-PROPOSED and never canon, (3) why every AI call goes
through Forge, (4) why the namer may only choose from a closed list. If any restatement is wrong, stop and ask.

## 1. David's ruling (2026-10-23)
The UUID, the Master Equation namer, and the knowledge-graph tags belong in the quick call. They run first, on
every item, before any other station. Design: hub repo (on `origin/main`)
`docs/superpowers/specs/2026-10-20-api-prep-gate-design.md` and `docs/superpowers/plans/2026-10-20-api-prep-gate-plan.md`.
**Read both first.** This prompt covers their stages 3, 4 and 5 and packaging.

## 2. What exists (checked 2026-10-23, `pipeline-workflows` branch `wip/api-restructure-2026-10-23`)
- `API/000_QUICK_CALL/identity.py`: the UUID registry. `paper_uuid` (uuid4, permanent), `version_uuid`
  (uuid5 of the sha256 under the CKG namespace). **Built. Reuse it, do not touch its formula.**
- `API/000_QUICK_CALL/nabla.py`: the NABLA classifier. **Built.**
- `API/000_QUICK_CALL/quick_call.py` + `series_run.py`: write the header sidecar. Identity is filled. But
  `master_equation_id` only accepts a hand-typed `--me-id` (nothing proposes one), and `knowledge_graph` is all
  null slots. `BACKSIDE/00_quick_call.py` is the older ad-hoc prompt.
- No `00_prep.py`. No `debate_map` key in `API/_system/config/paths.json`.

## 3. What to build
**a. Master Equation namer (spec stage 3).** Keep an id passed with `--me-id` or already in the sidecar.
Otherwise propose one through Forge from the NABLA result plus a one-sentence decode, **choosing ONLY from the
closed list in `API/_system/config/me_vocab.json`**: `ME-LAW<nn>` for the primary law (01-10), optional
secondaries joined with `+` (max 2), or `ME-CORE`, `ME-NONE`, `ME-UNSURE` (which must carry a reason).
Why closed: the spec as written lets the model invent a free-text id, and that is already happening. One vault
holds 17 different `ME-` spellings (`ME-0001`, `ME-01-001-trilemma-impossibility`, `ME-AXIOM-001`, `ME-COR-001`,
`ME-CHI-0001`...), and pipeline outputs hold model-made ones like `ME-PHYS-TD-THEO`. Reject any model answer
outside the list and retry once, then fall back to `ME-UNSURE`.
Apply `retired_numbering` from the same file: an item citing the OLD law numbers (Law 8 = Fermi, Law 9 =
Einstein) must map to the CURRENT ones (Law 9 = Weak/moral conservation, Law 8 = Relativity/Covenant).
`me_vocab.json` is a **draft working vocabulary, not canon** (see its `open_conflicts_for_david`). Never edit
its laws yourself. Mark every result `status: PROPOSED`; only David confirms.
**b. Knowledge-graph tags (stage 4).** Fill `node_type`, `q7_dimension`, `edge_types`, `canonical_claims`
from closed vocabularies. API plus keyword fallback. If unsure, leave null WITH a reason. Never guess.
Axiom ids (`AX-001`..`AX-188`) are the one consistent id system David already uses everywhere; link to them
as edges only from the axiom registry, never invent one.
**c. Debate-map match (stage 5).** Index every `Q-*` folder under `paths.json` key `debate_map`, keyword
shortlist, then model confirmation through Forge returning 0-5 `{question_id, score, reason}`. Add a placeholder
`debate_map` to `paths.example.json`; David sets the real value locally
(`C:\Users\David\Documents\faiththruphysics.com\Canon\DEBATE_MAP`). You cannot see that folder: test against a
small fixture tree of 4-5 fake question folders. Real format: `DEBATE_MAP.md` lines like ``- `Q-ID` question text``
and folders `P00..P10/NN_Q-ID`; 20 of 112 questions have no text, so use id tokens for those.
Learn from the prototype `scripts/argument_match_dryrun.py` and the "Dry-run findings" in
`docs/ARGUMENT_AGENT_BUILD_PROMPT_v0.1.md` (hub branch `wip/hub-docs-and-loops-2026-10-23`). Known traps:
David's framework words (e.g. "coherence") poison keyword matching; multi-topic list files must be matched line
by line; generic filenames add nothing; one-word questions saturate scores.
**Record matches only. Do NOT write stubs into debate-map folders** (that is the Argument Agent's job).
**d. Package** as the engine-native `00_prep.py` with `station.json` per the spec. Folder stays
`000_QUICK_CALL`, label `00_PREP`; the old ad-hoc prompt stays reachable as `--call QUICK_CALL`.
**Read `API/KIMI_PROMPT_STATION_000_AND_RENUMBER.md` first; do not renumber anything.**
Outputs per spec: `00_PREP.yaml` sidecar, engine bundle, receipt, reuse `UUID_REGISTRY.json`.

## 4. Rules
- Every AI call: `POST {FORGE_URL}/v1/chat/completions` (default `http://127.0.0.1:8790`). No provider URLs or
  keys. Check whether `nabla.py` or `quick_call.py` call a provider directly today; if so route them through
  Forge and report it as a separate diff.
- Never write inside the source file's folder except the sidecar. Never mint a UUID outside `identity.py`.
- `--no-ai` still works and writes the header with null slots. Re-runs reuse existing blocks unless `--redo`.
- **Back-dating:** `2 RUN ON FOLDER` must work over an existing folder without changing any source file. Add a
  `--dry-run` that prints item count and estimated calls (about 3 per item) before any spend.

## 5. Tests and acceptance
Tests with a fake Forge: identity is stable across re-runs and renames; a given `--me-id` is kept; an answer
outside `me_vocab.json` is rejected and falls back to `ME-UNSURE`; an item citing old law numbering maps to the
current number; unknown graph tags stay null with a reason; debate match returns at most 5; source files are
byte-identical after a run. Acceptance is PENDING on David's machine: run on 5 real papers and show the
`00_PREP.yaml` files. Say "acceptance pending on target machine" in the PR description.

## 6. Branches
`pipeline-workflows`: branch from `wip/api-restructure-2026-10-23`, draft PR, never push to main or master.

## 7. Out of scope
Writing stubs into the debate map, the FIS stations, the workbench page, Rust, editing the laws in `me_vocab.json`.
