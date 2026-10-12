# Station Source Mirror Audit — 2026-06-12

## Result

`stations/source/` exists only as a repo-safe mirror location. It currently has
no station snapshots. All 52 entries from `stations/STATION_REGISTRY.json` are
therefore marked as missing from the mirror in `AUDIT.json`.

## Important distinction

A missing source snapshot does **not** mean the station is missing from the NAS
runtime. The live station body remains whatever path is listed in
`stations/STATION_REGISTRY.json`.

## Junk cleanup

No generated junk was removed because no station snapshot folders were present.
A local `.gitignore` was added to keep obvious runtime artifacts out of future
snapshots.

## Risky deletes avoided

- No NAS station bodies were moved or deleted.
- No live station paths were changed.
- No uncertain files were deleted.
