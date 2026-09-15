# YouTubeChannelRefinery

A lossless workflow packet for combined YouTube channel/playlist Markdown exports. It splits in source order, cleans transcripts, enriches notes through the configured NAS NLP service, validates review-worthy failures, and routes Obsidian notes beneath `vault_root/YouTube/<Channel>`.

## Run

1. Edit `CONFIG/config.json` (especially `vault_root`).
2. Put a channel or playlist `.md` in `INPUT`.
3. Double-click `RUN_PIPELINE.bat`, or run `python SCRIPTS/run_pipeline.py --input INPUT/file.md --profile christian`.

Use `--dry-run` to print the destination and chapter count without creating, moving, or changing anything. Generated content is bounded by markers; content after `<!-- manual -->` is retained on reruns. A failed NAS request creates a reason file under `REVIEW` and does not stop the remaining chapters.

The packet intentionally has no required Python packages. PyYAML/jsonschema/dateparser can be installed for downstream integrations, but core splitting, cleaning, regex extraction, and HTTP use the standard library.
