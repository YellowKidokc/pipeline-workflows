# Behavioral Intelligence Layer (BIL)

This directory holds the repo-safe source shape for the Behavioral Intelligence
Layer preference engine. BIL is the **preference** layer: it observes browser,
folder, and manual signals, converts them into `preference_event` contracts, and
feeds the P06 River hot loop before preference state is compacted toward P05 PPK.

## Placement

- `source/bil/` mirrors the Python adapter/server shape from the BIL package.
- `source/browser/` mirrors the browser extension signal collector shape.
- `requirements.txt` records optional runtime dependencies for the NAS/body layer.
- `EVENT_MAP.json` is the machine-readable bridge from BIL observations to the preference-event contract.
- GitHub keeps this as source/spec only; live services, data, logs, JSONL event
  streams, databases, and learned model state remain runtime/NAS-side.

## Preference loop fit

```text
browser/folder/manual signal
  -> BIL adapter or runtime endpoint
  -> contracts/schemas/preference-event.schema.json
  -> P06_river hot online learning
  -> P05_ppk portable preference kernel
```

If BIL is offline, local JSONL remains the replayable source of truth for later
learning. This snapshot does not activate live wiring by itself.

## Event mapping

| BIL input | `source` | `signal` | Default weight |
| --- | --- | --- | --- |
| Human approval | `approval_gate` | `manual_approval` | `1.0` |
| Human correction | `correction_logger` | `manual_correction` | `1.0` |
| File reused/opened again | `folder_observer` | `file_reused` | `0.9` |
| Clipboard copy | `browser_extension` | `copied_text` | `0.8` |
| Bookmark/save action | `browser_extension` | `bookmark_save` | `0.7` |
| Long dwell/scroll | `browser_extension` | `long_dwell_scroll` | `0.5` |
| Tab opened | `browser_extension` | `opened_tab` | `0.2` |
| Accidental/short visit | `browser_extension` | `accidental_visit` | `0.0` |

Browser extension signals are passive preference inputs. Folder observations are passive unless promoted by a human review. Manual approvals and corrections are active signals. All should calibrate future routing and ranking, never block the active pipeline.

`EVENT_MAP.json` mirrors this table for tests and future adapters.

## Not included

Do not add zip archives, credentials, runtime logs, event JSONL, databases,
vector indexes, generated exports, or learned model artifacts here.
