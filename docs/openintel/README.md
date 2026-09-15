# OpenIntel reconciliation

This repository implements the evidence ledger as the system of record. Obsidian files are projections; generated sections must remain bounded by markers and hand-written content beneath `<!-- manual -->` must survive regeneration.

## Bootstrap

```bash
python scripts/openintel_init.py openintel.sqlite
python scripts/openintel_migrate_xlsx.py --workbook "Open Intel.xlsx" --ledger openintel.sqlite
python scripts/openintel_install_templates.py "/path/to/OPENINTEL STATER"
```

The SQLite schema follows `Open Intel.xlsx` **DB Schema v2.0** and adds first-class `hunches`, `statements`, `sources`, and typed `links`. It uses the canonical ID families, retains `legacy_ids`, gives claims/evidence tier values (including `UNRATED`), keeps hunches untiered, and enforces the `CANDIDATE → REVIEW → ACCEPTED/REJECTED` lifecycle. Rejected records require reasons. Dropped hunches require reasons and remain stored.

`openintel_install_templates.py` restores both `00_SCHEMA_TEMPLATES/HUNCH.md` and `CASE_TEMPLATE/HUNCH.md`. It intentionally does not guess the UNC mount point; supply the locally mounted vault root.

## ID audit (report only)

```bash
python scripts/openintel_id_mapper.py "/path/to/OPENINTEL STATER" --output openintel-reports
```

This writes `id_map.csv` and `broken_links.csv`. It never edits the vault. Generic collection code `GEN` and entity type `UNK` mean that a reviewer must select a more specific canonical value before applying a map.

## YouTube refinery

```bash
python workflows/YouTubeChannelRefinery/SCRIPTS/run_pipeline.py \
  --input export.md --profile conspiracy --ledger openintel.sqlite --collection COW
```

Transcript sentences are immutable source statements, not claims. Extraction creates only candidates. Accusatory person-naming text is conservatively sensitive and excluded from the public views. Conflicting-year observations become machine hunches.

## Hunch re-check

```bash
python scripts/openintel_recheck_hunches.py openintel.sqlite --threshold 0.18
```

The offline job uses reproducible token Jaccard matching against newly accepted statements, claims, and evidence. A match creates a candidate `SIG` record and a `PROMOTED_FROM` link; it does not promote the hunch or claim automatically. The `hunch_matches` key makes repeated runs idempotent. An embedding/NLI worker can later write matches through the same table and lifecycle.

## Epistemic rules

- A hunch needs no evidence, has no tier, and is never a finding.
- Untested claims and evidence are `UNRATED`; `T5` means tested and unsupported.
- Tier applies to individual claims/evidence. `case_tier_distribution` supports a `Mixed` case projection.
- Every machine-created record awaits human review.
- Sensitive accusations never appear in public projection views without review and an explicit projection decision.
