# GitHub Prompt: Station Source Reorg

`stations/source/` is a repo-safe mirror of station bodies from `X:\Backside\stations`.

Goal: make stations understandable online without pretending GitHub is the live runtime.

Rules:

- Live station paths remain in `stations/STATION_REGISTRY.json`.
- `stations/source/` is for prompting/refactoring context.
- Remove generated junk from `stations/source/` if found.
- Redact secrets.
- Keep source, configs, manifests, docs, and tests.

Tasks:

1. Compare `stations/STATION_REGISTRY.json` against `stations/source/`.
2. Identify missing high-value station source snapshots.
3. Identify mirrored files that are generated/runtime artifacts.
4. Propose a clean station taxonomy:
   - `intelligence`
   - `transform`
   - `validate`
   - `route`
   - `media`
   - `framework`
   - `graph`
5. Do not move live station bodies. Only reorganize repo-safe references/mirrors.

Output:

- Station source cleanup plan.
- Registry corrections.
- Any safe docs/tests updates.
