# 102_FIS_EXACT_COPIES

Groups files of 101's scan by size, hashes only same-size candidates, and lists every copy group with every location (CSV + report, with a root-by-root summary). Nothing is chosen, moved or deleted: which copy is best is decided later, from this inventory. Collections are left out.

## Buttons

- `1 RUN HERE.bat`: the roots listed in `INBOX` (`.txt` files, one folder path per line; `00_PRIORITY` first), or, with
  no lists, the FIS roots registered in David-OSv3's `config/folder_registry.yaml` (entries with a `fis:` field).
- `2 RUN ON FOLDER.bat`: asks for one folder (drag it in).

Both show the plan first (dry run) and ask before running for real. Nothing is copied into INBOX: it only holds lists.

## Rules

- Thin wrapper: the FIS logic is David-OSv3's `engine/understand.py`, loaded from the folder in `paths.json`
  (`david_osv3`). No FIS logic is copied here.
- R1: nothing is moved, renamed or deleted. Every scanned root is read-only (`engine/path_write_policy.py`); output goes
  to the FIS database (`David-OSv3/.data/fis_understand.sqlite`) and this OUTBOX only.
- Unreadable files are findings (listed with the reason), never silent skips.
- Inferences are shadow (R7). Nothing here is a decision or an authorization (R3).

## Command line

```
python 102_fis_exact_copies.py            plan only
python 102_fis_exact_copies.py --apply    run
```
