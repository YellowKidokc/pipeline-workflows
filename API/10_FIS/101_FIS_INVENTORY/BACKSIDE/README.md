# 101_FIS_INVENTORY

Walks every root to register in ONE scan (so 102 can match copies across roots) and records files, folders, markers and every unreadable file or folder with its reason. Collections (D:\CHI PARTS) are inventoried and recorded as one collection. Roots marked skip are not walked. Stage 2 (identify + extract) is not in the engine yet.

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
python 101_fis_inventory.py            plan only
python 101_fis_inventory.py --apply    run
```
