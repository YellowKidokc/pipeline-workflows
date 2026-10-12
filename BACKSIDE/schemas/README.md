# Schemas Compatibility Directory

`schemas/` remains the current compatibility location for JSON Schema files used
by tests, scripts, docs, and runtime-adjacent code.

New readers should treat `contracts/` as the interface-promise home:

- `contracts/README.md` explains the contract boundary.
- `contracts/schemas/*.schema.json` mirrors the priority schemas here.
- Existing `schemas/*.schema.json` paths are preserved so imports and docs do not
  break during the reorg.

Do not delete or move files from `schemas/` without an approval packet and a
consumer migration plan.
