# CLAUDE CODE PROMPT: put every station in the workbench page (v0.1)
**Date:** 2026-10-23 | **Author:** Claude (Sonnet) with David | **Status:** ready for a builder, read receipt first

## Read receipt (first message back, before any edit)
Restate in your own words: (1) why the page must read stations from ONE source and not a typed-in list,
(2) why you must not renumber or retire any station, (3) which of the two page copies you may edit.
If any restatement is wrong, stop and ask.

## 1. What is true today (checked 2026-10-23)
- The live page is `Rust_AI_API/ui/api-workspace.html` (served by Forge). It is **static**: no `fetch`, no
  folder access, a typed-in list of 8 groups, header text "no APIs connected". Nothing feeds it stations.
- `pipeline-workflows/API/api-workspace.html` (136 KB) is a second, bigger copy. `Rust_AI_API/api-workspace_1.html`
  is the older mockup (7 groups, no Desk Tools). **Edit only `Rust_AI_API/ui/api-workspace.html`.**
  Report how the other two differ; do not edit them and do not delete them.
- The real station feed exists: `pipeline-workflows/API/_system/engine/console.py list` prints every station as
  JSON (number, label, family, buttons, inbox/outbox counts). It currently feeds Nerve's Station Console only.
  It lists 63 stations, 0 errors.
- 64 stations exist on disk. Three are missing from `_system/config/stations.json` (so missing from the feed):
  `02_C_P_E_L/023B_HTML_ASSEMBLY`, `09_DESK_TOOLS/091_CHAT`, `09_DESK_TOOLS/092_RECONCILIATION`.
- The page has no group for 8 stations: `000_QUICK_CALL` (UUID + NABLA quick-call), `041_STORIES` (2),
  `042_KAIT_STORIES`, `047_NEW_PAPER`, `048_TOPIC_SYNTHESIS`, `049_GAP_MAP`, `060_OPENAI_STATIONS`.

## 2. What to build
1. Register the three missing stations in `API/_system/config/stations.json`. **Read
   `API/KIMI_PROMPT_STATION_000_AND_RENUMBER.md` first.** Do not renumber, retire or move anything. Add rows only.
2. Give the page ONE source: Forge serves `GET /api/stations` (same JSON shape as `console.py list`, produced by
   importing or running it; do not copy its logic) and the page `fetch`es it at load. If Forge cannot reach the
   pipeline folder, return a clear error the page shows; never fall back to a typed-in list silently.
3. Group stations by `family`. Stations with no family (the 000, 041, 042, 047, 048, 049 ones) get a visible
   group called "Front stations" so nothing is hidden. Keep the existing 8 group names and order.
   **David's ruling (2026-10-23): everything is shown EXCEPT the OpenAI stations (`060_OPENAI_STATIONS`).**
   Keep that exclusion in ONE list (`EXCLUDED_FROM_PAGE`) that both the page and the test read. The station
   stays registered and in the feed; the page just does not show it.
4. One station card shows: number, name, kind, `uses_api`, buttons, inbox and outbox counts, last run.
5. Forge's address comes from `FORGE_URL` (default `http://127.0.0.1:8790`). No provider URLs or keys in the page.
6. A completeness test that FAILS when any `station.json` on disk is not in the feed, or any feed station has no
   visible group, with the one exception of what is listed in `EXCLUDED_FROM_PAGE`. Put it where the pipeline's
   other tests live and say how to run it.

## 3. Safety
Read-only on station folders. Do not run any station. Do not edit the other two page copies. Branch from
`wip/api-restructure-2026-10-23` (pipeline-workflows) and from `feat/desk-tools-group` (Rust_AI_API). Draft PRs.
Never push to main or master.

## 4. Acceptance (pending, on David's machine)
Start Forge, open the page: expect 65 stations visible (63 in the feed today, which includes 2 under `_system`,
plus the 3 newly registered, minus the 1 excluded OpenAI station), 7 front stations under "Front stations",
and `000_QUICK_CALL` among them. Say "acceptance pending on target machine" in the PR description.

## 5. Out of scope
The FIS group (`10_FIS`, separate prompt), running stations from the page, restyling, Rust beyond the one endpoint.
