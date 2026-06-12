# Exports

Transitional build lane for work that is becoming finished but is not finished yet.

Use this for partial series, HTML assembly, spreadsheet-derived stats, build metadata, assets, and review-ready drops.

```text
exports/active/SERIES_OR_PROJECT/
  SOURCE_MAP.json
  BUILD_NOTES.md
  INPUTS/
  HTML_PARTS/
  DATA/
  METADATA/
  ASSETS/
  REVIEW/
  READY/
  CLEANUP_CANDIDATES/
```

Deletion rule: move generated junk to `CLEANUP_CANDIDATES/`, record it in `_manifest/cleanup-ledger.jsonl`, and delete only after approval.
