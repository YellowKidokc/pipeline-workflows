# Structure Reorg Packet

This packet records the non-destructive structure reorg doctrine for Codex work.

## Current sequence

1. Make `models/` the obvious model-slot knowledge source.
2. Make `contracts/` the obvious interface-promise home while preserving
   `schemas/` compatibility paths.
3. Audit station source mirrors only for obvious junk, without changing live NAS
   station paths in `stations/STATION_REGISTRY.json`.

## Non-destructive rules

- Keep GitHub as the governor/spec layer and NAS as the runtime/body layer.
- Do not upload model weights, generated outputs, secrets, vector indexes,
  databases, or station runtime bodies.
- Add compatibility pointers/shims before moving paths consumed by tests or code.
- Nothing destructive happens without an approval packet.


## Station source mirror status

`stations/source/` is a sanitized mirror location for online prompting, not the
live runtime. Keep source snapshots repo-safe, preserve `stations/STATION_REGISTRY.json`
paths, and document uncertainty instead of deleting files.
