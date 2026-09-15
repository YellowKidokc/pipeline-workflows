# YouTubeChannelRefinery

A lossless workflow packet for combined YouTube channel/playlist Markdown exports. It splits in source order, cleans transcripts, enriches notes through the configured NAS NLP service, validates review-worthy failures, and routes Obsidian notes beneath `vault_root/YouTube/<Channel>`.

## Run

1. Edit `CONFIG/config.json` (especially `vault_root`).
2. Put a channel or playlist `.md` in `INPUT`.
3. Double-click `RUN_PIPELINE.bat`, or run `python SCRIPTS/run_pipeline.py --input INPUT/file.md --profile christian`.

Use `--dry-run` to print the destination and chapter count without creating, moving, or changing anything. Generated content is bounded by markers; content after `<!-- manual -->` is retained on reruns. A failed NAS request creates a reason file under `REVIEW` and does not stop the remaining chapters.

Pass `--ledger /path/to/openintel.sqlite --collection MKU --station-chain` to write the source and transcript to the ledger first, then run the S0–S10 chain. Every extracted record starts at `CANDIDATE`; the workflow never promotes machine output. Accusatory statements naming a person are conservatively marked sensitive and cannot enter public projections. Sentences containing multiple, potentially conflicting years create machine hunches for human review rather than claims.

## Independent stations

Each pass is a separate file under `SCRIPTS/stations/`, records completion in both the ledger and `STATE/<video>/`, and can be resumed without duplicating records:

```text
S0 intake → S1 chunks → S2 entity mentions → S3 resolution → S4 dates/events
→ S5 statements/claims → S6 themes → S7 citations → S8 check-backs
→ S9 validation → S10 Obsidian projections
```

Run one pass with `python SCRIPTS/breakdown.py station s6_themes --video VID-HAB-abc --ledger openintel.sqlite`; use `--force` only to deliberately rebuild that station. `S7` is disabled outside the Christian profile. Conspiracy claims include claimed-evidence and counterclaim placeholders for review. S10 always writes all five CKG sections, uses `none found` for empty results, adds the Christian lens only for that profile, and updates a channel-level CKG card.

## Watcher and scheduler

Run `START.bat` to start the stable-file watcher and scheduler in separate minimized processes. The watcher launches an always-on-top Tk prompt without blocking detection. Its five-minute timeout uses `default_trigger` (`idle` by default), and every choice is persisted to `STATE/queue.json`.

Idle scheduling requires the configured input-idle interval, CPU below the configured ceiling, and no full-screen foreground application. A channel job runs one video atomically and pauses before the next video when the user returns. `LAUNCH.bat` provides a dependency-free queue/progress and run/open-output menu in environments without `pystray`. Completion writes `_RUN_COMPLETE.json`, a READY marker, and a Windows toast.

The packet intentionally has no required Python packages. PyYAML/jsonschema/dateparser can be installed for downstream integrations, but core splitting, cleaning, regex extraction, and HTTP use the standard library.
