# BUILD PROMPT — Identity, Sentence Lineage, Lasers, and Vectors (v0.1)
*David Lowe · POF 2828 · 2026-10-20 · for Claude Code or Kimi · repo: D:\GitHub\pipeline-workflows\API*

Read `AGENTS.md` first. All its rules apply: wrap don't rewrite, nothing hard-coded, finish each item before the next,
small real tests, `work` branch only. This is ONE system in four parts, built in order. Each part propagates to every
station because it lives in `_system\engine\`, not in any station.

## Goal
Every paper and every sentence has a permanent ID. Every sentence that draws on an earlier one says which one and how.
Sources we cannot write in (other people's papers, transcripts, Augustine) are pinned by anchors instead. Every paper and
every station output is vectorized as it is made, so DeepSeek is handed the right 20 sentences, not the whole corpus.

## Part 1 — Identity (do first; everything hangs off it)
- **Move** `000_QUICK_CALL\identity.py` to `_system\engine\identity.py`. It already mints `paper_uuid` (uuid4, permanent),
  `version_uuid` (uuid5 of the sha256), and a `chain_hash` per version. Keep its logic; registry path from `paths.json`.
- **Wire** it into `engine\items.py` `create_paper` (line ~117 currently uses `digest[:12]` as the ID; replace with the
  registry's paper_uuid; keep the 12-char digest only as a short display code) and into the first touch of any note
  (YouTube notes included): write `uid:` into the note's YAML once; never change it.
- **Stamp** `source_uid` and `version_uuid` in ONE place each: the receipt in `engine\gateway.py`, and the YAML that
  `tools\publish_analysis.py` writes. No station is edited.
- `previous_names` stays (it is harmless), but lookups now go by `uid` first.

## Part 2 — Sentence IDs and lineage (extends SENTENCE_MARKER_SPEC_v0_1.md; do not replace it)
- A sentence's own ID: `S-` + uuid4, minted the first time the sentence is tagged, then carried by its marker forever:
  `⟦CLM S-7f3a… from=S-21bc…,S-90de… rel=builds⟧ text ⟦/⟧`
- New fields: `from=` (comma list of sentence IDs or anchor IDs) and `rel=` (one of `quote`, `paraphrase`, `builds`,
  `answers`, `contradicts`).
- The existing MARKER_LOSS guard must also check that `from=` and `rel=` survive a rewrite unchanged.
- Registry table `sentences(sentence_uid, paper_uuid, version_uuid, text, sha256)` and `lineage(child, parent, rel, by, at)`
  in `_data\catalog.sqlite` (it already exists).

## Part 3 — Lasers (anchors) for text we cannot mark
Follow the W3C Web Annotation selector model. An anchor stores, together:
- `position`: character offset from the start of the source
- `exact`: the quoted words
- `prefix` / `suffix`: ~32 characters before and after (the two lasers)
- `source_uid` + `version_uuid` of the source
**Re-anchoring after a revision (David's rule):** start at the old position; search backward and forward at the same
time, widening the window, using fuzzy match on `prefix + exact + suffix`, scored partly by distance from the old position
(diff-match-patch's `match_main` does this; use it). Expect a hit within ~15 sentences; widen to the whole document only
if not found. If two candidates tie, the prefix/suffix decide. Record each re-anchor as a new anchor version; never edit
the old one. Store anchors in `anchors(anchor_id, source_uid, version_uuid, position, exact, prefix, suffix, status)`.

Optional storage (the "compression day"): store each unique sentence once by sha256 and keep a paper version as an ordered
list of sentence hashes (content-addressed, like Git). Rebuild any version from the list. Do this only if Parts 1–3 are done.

## Part 4 — Vectors on everything, at birth
- Every new paper and every station output is embedded **as it is published**, at sentence level, keyed by `sentence_uid`
  (or `anchor_id` for unmarked sources). Use the existing plan in
  `D:\GitHub\deep-research-hub\docs\engine-integration\VECTORIZATION_SPEC_v0.1.md`; do not start a second vector store.
- **Lineage finder** (forward, while writing; and backward, once, over the existing corpus):
  1. code pulls the 10 most similar older sentences (with their IDs) for each new sentence — no API call;
  2. DeepSeek, through the gateway, gets the new sentence + those 10 and returns which it drew on and the `rel`;
  3. code REJECTS any ID not in the 10 it was given. The model chooses among real sources; it cannot invent one.
- **Negation check:** embeddings can place "X is Y" next to "X is not Y". The judging step reads the text; never mark
  `paraphrase`/`builds` on similarity alone.
- **Retrieval for every station:** a station may ask the engine for "the 20 most relevant sentences in the corpus" for a
  question and receive them with IDs — so DeepSeek works from the right pieces instead of the whole corpus.

## Rust
`D:\GitHub\Rust_AI_API` (semtag, forge) must read the same registry and call models only through the gateway relay, and
read `settings.json` / `GLOBAL_FOCUS.md` — not its own copies. One source of truth.

## Tests before "done"
- A paper edited by one comma keeps its `paper_uuid` and gets a new `version_uuid`; its old results are still found.
- A marked sentence moved to another paper keeps its `S-` ID; a rewrite that drops `from=` is flagged MARKER_LOSS.
- An anchor into a source survives inserting 10 sentences above it (found by the windowed search, not a full scan).
- The lineage finder, on 2 real papers, returns only IDs from its candidate list.
- The existing tests still pass. Mock mode end-to-end on 041_STORIES.

## Report
What was built, what behaves differently, what is untested. Say problems plainly.
