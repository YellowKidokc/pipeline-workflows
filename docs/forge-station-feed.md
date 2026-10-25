# Forge station feed

`API/_system/engine/console.py list` remains the single station discovery source.
The Rust workspace invokes it read-only through `GET /api/stations`.

`API/_system/config/workspace.json` owns the ordered group names and the single
`EXCLUDED_FROM_PAGE` list. The OpenAI station remains registered and in the feed;
the page hides it. Unmapped families appear under Front stations.

The feed includes station goals, SHA-256 hashes for declared prompt files, and
quick-call preset names with prompt hashes. It reads the current files on refresh;
there is no copied prompt catalog in Rust. It never runs a station, makes a model
call, repairs paths, or changes a prompt. A stale script path is an explicit error.

Registered the existing `23B_HTML_ASSEMBLY`, `091_CHAT`, and
`092_RECONCILIATION` folders without renumbering or moving them.

Run from the repository root:

```
python -m unittest discover -s API/_system/tests -p test_station_feed.py
```

New station starter files and registration steps:
`docs/templates/FORGE_STATION/README.md`.

The root HTML mockup and pipeline HTML prototype are preserved. The integrated
page is `Rust_AI_API/ui/api-workspace.html`, served at Forge's root URL. The
Python station launchers remain the execution interface; Forge Quick Run continues
to execute Forge job templates rather than Python station IDs.
