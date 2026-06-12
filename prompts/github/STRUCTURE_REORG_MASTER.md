# GitHub Prompt: Structure Reorg Master

You are working on branch `codex/reconcile-nas-pipeline-reality` in `YellowKidokc/pipeline-workflows`.

Goal: reorganize the repo so GitHub can reason over the whole FORGE/Pipeline system while NAS remains the runtime body.

Rules:

- Do not commit model weights, vector indexes, generated exports, databases, runtime logs, or secrets.
- Keep station doctrine: vectorize before classify.
- Keep FIS = perception, BIL = preference, Pipeline = action.
- Preserve backwards compatibility when moving schemas or config paths; add aliases/shims if scripts import old paths.
- Prefer generating move plans first. Do not perform destructive cleanup without an approval packet.

Architecture target:

```text
reality/      real NAS/local path maps
contracts/   schemas and interface contracts
models/      top-level model registry, health, fallbacks, chain
preferences/ preference profiles and engine configs
workflows/   DAGs/process definitions
stations/    registry + repo-safe station source mirror
queue/       David-facing input lanes
exports/     transitional build/output lane
docs/        explanation and operating doctrine
scripts/     repo automation
```

First task:

1. Run/read `scripts/generate_reorg_packet.py`.
2. Inspect `docs/reorg/REORG_PACKET.md`.
3. Propose a minimal PR that improves structure without breaking imports.
4. If moving files, update imports/tests/docs in the same PR.
5. Leave `NAS/runtime` artifacts referenced, not copied.
