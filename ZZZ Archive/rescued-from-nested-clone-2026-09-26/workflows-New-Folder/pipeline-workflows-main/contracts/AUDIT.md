# Contracts Audit — 2026-06-12

## What exists now

- `schemas/` contains the compatibility JSON Schema files already referenced by
  docs and tests.
- `contracts/` is now the interface-promise home for priority contracts.
- `contracts/schemas/` mirrors priority schemas while keeping the old `schemas/`
  paths intact.

## Promotion decisions

| Schema | Decision | Reason |
| --- | --- | --- |
| `workflow.schema.json` | Mirror into `contracts/schemas/` and keep `schemas/` | Workflow DAGs are interface promises, but tests/docs already use `schemas/`. |
| `station.schema.json` | Mirror into `contracts/schemas/` and keep `schemas/` | Station configs define station I/O boundaries; live station bodies remain NAS-side. |
| `model.schema.json` | Mirror into `contracts/schemas/` and keep `schemas/` | Model slot configs are GitHub-side contracts; weights remain NAS-side. |
| `preference-event.schema.json` | Add to both paths | BIL preference events needed an explicit interface shape. |
| `correction.schema.json` | Mirror into `contracts/schemas/` and keep `schemas/` | Corrections are BIL training events and must remain compatible. |
| `approval.schema.json` | Add to both paths | Human approval gates needed an explicit `CONFIG/approval.json` contract. |
| `export-manifest.schema.json` | Add to both paths | Export manifests needed a no-payload interface contract. |
| `manifest.schema.json` | Mirror into `contracts/schemas/` and keep `schemas/` | Packet/global manifests are runtime-adjacent interfaces. |

## Deliberately not moved

- Runtime configs.
- Generated workflow outputs.
- Station runtime bodies.
- Model weights.
- NAS artifacts, vector indexes, databases, logs, and secrets.

## Compatibility path rule

`schemas/*.schema.json` remains valid until a later approval-backed migration
updates all consumers. New documentation should point readers to `contracts/`
first, then mention the preserved `schemas/` compatibility paths.

## Follow-up: station source cleanup

Next PR should audit `stations/source/` or any station mirror folders only for
obvious junk. It should not change live paths in `stations/STATION_REGISTRY.json`
and should not delete runtime station bodies without an approval packet.
