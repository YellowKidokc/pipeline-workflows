# PROMPT FOR CLAUDE CODE — Rust launcher for the API Workspace (one installable program, no Python server)
*Prepared for David Lowe, POF 2828 · Oct 17, 2026*

## Goal
Replace the Python web server from PR #28 (`workspace.py`) with **one small Rust program** that:
1. serves the existing workspace page (`API PIPELINE\index.html` / the live page from PR #28) from inside the binary,
2. reads the stations, and
3. starts station runs by calling the EXISTING Python station code (`button.py` in its "plan" mode),
so David installs one program, double-clicks it, and the workspace opens. No Python web server.

## Scope — read carefully
- **DO NOT rewrite the 53 stations in Rust.** The station logic stays Python. Rust replaces only the server + launcher.
- **DO reuse what exists:**
  - PR #28 on `YellowKidokc/pipeline-workflows` (branch `claude/bold-keller-zq3hjn`): `workspace.py` (612 lines) and the
    live `index.html` (715 lines). Port `workspace.py`'s HTTP endpoints to Rust one for one; keep the page's API the same
    so `index.html` works unchanged.
  - The Rust wrapper pattern in `D:\GitHub\deep-research-hub\hub\` — it spawns apps from an allow-list (`launch.json`),
    keeps state in `data/`, serves a built front end, listens on 127.0.0.1 only. Follow that pattern.
- Model calls keep going through the engine's relay (`_system\engine\gateway.py`) exactly as they do now. Do not add a
  second way of calling DeepSeek.

## Requirements
1. **Single binary** `pipeline-workspace.exe`, built with `cargo build --release`. Front-end files embedded
   (e.g. `include_str!` / `rust-embed`). Opens the default browser on start.
2. **127.0.0.1 only.** Never listen on other interfaces. Port from config, default free port.
3. **No raw command lines over HTTP.** The page can only ask for actions on an allow-list: list groups/stations,
   read/write PROMPT.md and FOCUS.md inside a station's BACKSIDE, plan/run/stop a station, list OUTBOX results,
   piece-by-piece send/accept/assemble. Every path is checked to stay inside the API folder.
4. **Paths** come from `API\_system\config\paths.json` (the one central config). Nothing hard-coded.
5. **Runs** spawn `python <API>\_system\engine\...button.py` in plan mode with the same answers workspace.py passes;
   stream stdout/stderr to the page as the live log; Stop kills the process tree (Windows: job object or taskkill /T).
6. **Python discovery:** find Python (py launcher, then PATH, then a path in config); clear error on the page if missing.
7. **Mock mode** passes through exactly as now.
8. **Concurrency:** one shared limit across all runs started from the page (same as PR #28).
9. **Logs:** every run writes its log file under `_data\logs\workspace\`; the page shows it live.

## Install / package
- `cargo build --release` -> `pipeline-workspace.exe`.
- Add `ONE_MENU.bat workspace` support so it launches the exe if present, else falls back to `workspace.py`.
- Optional (only if simple): a zip "portable" build with the exe + README. No installer framework needed for v1.

## Tests (required before saying done)
- `cargo test`: allow-list refuses anything outside it; path traversal (`..\`) refused; paths.json read correctly.
- Run the repo's existing 27 Python tests — all must still pass.
- End-to-end in **mock mode**: run `041_STORIES` alone, then the sequence 041 -> 044_TAGGER (this caught a rename bug
  once — confirm renamed notes are still found by step 2).
- Manual check on Windows: Stop actually kills the run; the drive list in Browse works.

## Known issues to leave alone (report, don't fix unless trivial)
- `story_bank.py` usage error at the end of every button run (pre-existing; listed in PR #28).
- Station folders may be RENUMBERED by another agent (Kimi) soon. Read station folders and labels from `station.json`
  at runtime — never hard-code a station folder name.

## Deliverables
1. A PR (or branch) with the Rust crate, e.g. `API\_system\workspace-rs\`.
2. README: build, run, where logs go, how to switch mock on/off.
3. A short report: what was ported, anything that behaves differently from workspace.py, what is untested.
   Say problems plainly.
