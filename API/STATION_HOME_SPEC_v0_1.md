# STATION HOME SPEC v0.1 — for the Rust build
*David Lowe · POF 2828 · Oct 17, 2026 · builds on api-workspace.html (mockup) — keep its layout, add what is below*

The mockup already has: group home (preset/model, format, folder structure, skip/rerun, in/out folders), Run tab
(start/pause/stop, live log, current work, receipt), Backside (template parts, prompt + output layout, preview),
Workflows (ordered steps, auto-added HTML assembly), HTML Assemblies, Python workspace, Settings.
The Rust app is that mockup made real. This spec lists only the additions and fixes.

## 1. Run mode across stations (missing — the main addition)
On the Workflows page, one setting:

| Mode | Meaning |
|---|---|
| BREADTH | every selected paper through station 1, then all through station 2, ... |
| DEPTH_BY_SERIES | one whole series through every station, then the next series |
| DEPTH_BY_PAPER | one paper through every station, then the next paper |

The existing `order` setting stays, but it only controls order INSIDE one station (note-first vs call-first vs parallel).

## 2. Series awareness
- Selection can be: folder, list of papers, or a series from `SERIES_REGISTRY` / `SERIES_HEADER.json` (000 station).
- Every call is prefixed with the 000 sidecar header (paper_uuid, version_uuid, series code like MIM-07 of 20, siblings, NABLA address).
- Outputs land in `API_PIPELINE\SERIES\<CODE>_<Name>\<CODE-NN>_<paper>\<station>\` (STANDALONE\ for papers with no series).

## 3. Fixes
- `concurrency` is a NUMBER (calls at once), not a copy of the order options.
- Paths come from the one central file `API\_system\config\paths.json` (`api_pipeline_out`, `originals_root`). No path is typed in two places.
- Provider keys come from the same gateway the engine uses (`_system\config\settings.json`), never pasted into the page.

## 4. Backside: template x questions
- A station template = fixed parts (frame, output layout) + a list of questions.
- Expansion: N questions x 1 template = N calls per paper. Two modes: SWAP_QUESTION (same template, each question) and SWAP_TEMPLATE (same question, each template).
- The plan count shown before Run = papers x questions x templates, with the estimated token cost.
- Extra calls beyond the main one go to the station OUTBOX; the station folder name carries the count prefix (open item from Oct 16).

## 5. Run log (live) — what each line records
timestamp · station · paper code · call n of N · status (QUEUED / RUNNING / OK / RETRY / FAILED / SKIPPED) · seconds · tokens.
A call that has not answered in 3x its median time is flagged STUCK in the log. Network drops retry 3 times, then FAILED (not silent).
The run receipt at the end: counts by status, failures listed, cost, and the output folders written.

## 6. Honesty rules carried from the 000 station
- AI proposes, code validates: a model's output that fails its schema is marked INVALID and shown, never "fixed" silently.
- Re-running a paper is a new run, not an overwrite of history; the registry keeps versions.
- Classification stability: NABLA runs 3x per paper, majority vote per variable, flipped variables flagged.

## 7. Open
- Compare view for two series (Φ panel) — design later.
- Whether HTML assembly runs right after each station (02 -> 02B) or once at the end; the mockup assumes per station.
