# CONVERSATION MINER — station spec v0.1
*David Lowe · POF 2828 · 2026-10-20 · for Kimi / Claude Code to build as a station under the AGENTS.md rules*

## Why
Long working conversations (Claude, Kimi, GPT, Gemini) produce theses, corrections, papers-that-should-exist, and promises,
then move on. Tonight's session produced ~10 papers only because they were written by hand. This station reads a
conversation (or a single doctrinal note) and returns the same structure every time, so nothing good is lost.

## Input
- A chat export (Markdown/JSON/TXT) or a single note.
- Chats are split by CODE into THREADS before any API call: a thread is a run of turns about one subject. Split on
  topic shifts (embedding distance between consecutive turns above a threshold) and on explicit markers ("new topic",
  "let's go back to", a new file path). Each thread keeps its turn range so every finding cites turns.
- A single doctrinal note is one thread.

## One call per thread. DeepSeek returns ONLY this JSON:
```json
{
  "thread_title": "short, specific",
  "turns": [start, end],
  "thesis": "one sentence: what is being claimed or built",
  "who_claimed": "user | assistant | other-AI (name) | joint",
  "structure": {
    "steps": ["the argument in order, one line each"],
    "weakest_step": "which step and why",
    "broke_in_thread": [{"what": "...", "turn": n, "fixed": true, "fix": "..."}],
    "unresolved_breaks": ["..."]
  },
  "best_version": "the strongest defensible statement of the thesis after the thread's own corrections (2-4 sentences)",
  "overstated": [{"claim": "...", "turn": n, "defensible_version": "..."}],
  "named_prior_art": [{"name": "person/work/doctrine", "relation": "supports | anticipates | refutes"}],
  "witnesses": ["Scripture refs and historical thinkers cited in the thread, with turn"],
  "tests": ["what observation or proof would kill or confirm it"],
  "lean_target": "a statement that could be formalized, or null",
  "already_written": ["file paths the thread says were created"],
  "paper": {"exists": false, "should_write": true, "register": "declaration | canon", "working_title": "..."},
  "reminders": [{"what": "promise / to-do / open ruling", "owner": "David | Claude | Kimi | GPT | Gemini", "turn": n}],
  "standing_rules": ["any rule the user set for future work, verbatim-ish, with turn"],
  "contradicts_canon": ["anything that conflicts with a canon file named in the thread"]
}
```

## Rules for the model (put in PROMPT.md)
1. Every item cites a turn number. No turn, no item.
2. Quote the user's own words for theses and rules; do not upgrade a passing mention into a position.
3. "best_version" must include the thread's own corrections; never restore a retracted claim.
4. Do not grade. No scores. The station computes priority in code (below).
5. If the thread is small talk or logistics, return thesis = null and only `reminders`.
6. Say "none" rather than inventing prior art; prior art must be a real, checkable name.

## Computed in code, not by the model (house rule: scores from code)
- **paper_priority** = (should_write AND NOT exists) × (2 if unresolved_breaks is empty else 1)
  × (1 + count(tests)) × (1 + count(named_prior_art)).
- **at_risk** = should_write AND NOT exists AND the thread is older than 3 days.
- **verified_witnesses**: Scripture refs checked against the KJV text in 23_BIBLE; non-matches flagged.

## Outputs (one run = one folder, AGENTS.md style)
- `<conversation> · MINED.md`: one section per thread, rendered from the JSON, newest first.
- `PAPERS_TO_WRITE.md`: every thread with should_write and no existing paper, sorted by paper_priority, at_risk on top.
- `REMINDERS.md`: every promise and open ruling, grouped by owner.
- `STANDING_RULES.md`: every rule the user set, deduplicated, with source turn — for review before it enters preferences.
- Each thread's JSON stamped with the conversation's `uid` and `version_uuid` (identity module, BUILD_PROMPT_IDENTITY_LINEAGE_v0_1).

## First test
Run it on the Oct 19–20 Claude session. Pass condition: it finds the ten papers listed in
`C:\theophysics\PAPERS_INDEX_2026-10-20.md`, marks the creed test as retracted (not restored), lists the open rulings
(E10 dictionary, PRED14/18, BC4, R6 rephrase, ledger row 004), and surfaces at least one thread we did NOT write up.
