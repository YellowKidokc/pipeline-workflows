# New pipeline station template

This template reuses the existing engine, limiter, cache, focus, receipts and output writer.
It does not replace multi-pass stations such as Stories.

1. Choose an unused menu number and label. Copy `station.py.template` to a new
   `API/<family>/<folder>/BACKSIDE/<script>.py`; replace `__LABEL__` and `__NAME__`.
2. Copy `PROMPT.md` beside it. Add `FOCUS.md` with the station focus.
3. Copy `station.json.example`, replace the placeholders and save as `station.json`.
4. Add one row to `API/_system/config/stations.json`: number, name, label, folder
   relative to `API/_system`, script, rank, retired=false. Do not renumber existing rows.
5. Add INBOX and OUTBOX beside BACKSIDE. Use the existing `ONE_MENU.bat <number>` launcher.
6. Run `python -m unittest discover -s API/_system/tests -p test_station_feed.py`.
7. Refresh the Rust page's Pipeline stations panel. The card appears automatically.
8. Review with `ONE_MENU.bat <number> --dry-run` before authorizing paid calls.

For a multi-pass workflow, preserve its sequencing and gates in its Python runner;
do not flatten it into a generic Forge job template.
