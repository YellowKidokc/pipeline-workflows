# LEAN 4 — READ THIS FIRST

**Status:** Governing location policy  
**Established:** November 6, 2026

## The three authorized Lean locations

1. **Master archive, intake, history, and human review**

   `H:\Desktop 2\LEAN 4`

   This is where discovered or recovered Lean material is preserved first. It holds originals, historical copies, intake manifests, hashes, comparison receipts, and human-review records. A filename containing words such as “canonical” or “final” does not by itself make a file authoritative.

2. **Canonical execution root**

   `D:\.lean4_canonical_backup`

   This is the only place from which governed Lean proof jobs should run. Approved source copies, the pinned Lean toolchain, negative controls, build results, declaration extraction, and axiom inspection belong in this workflow.

3. **Versioned API and pipeline implementation**

   `D:\GitHub\pipeline-workflows\API\02_C_P_E_L\05_LEAN`

   This contains the code, schemas, templates, tests, and documentation that operate the Lean registry. It is not the historical source archive.

## Normal flow

```text
New or rediscovered Lean material
        ↓
H:\Desktop 2\LEAN 4  (preserve, hash, inventory, review)
        ↓
Human approval and recorded source identity
        ↓
COPY into D:\.lean4_canonical_backup
        ↓
Run negative controls before positive verification
        ↓
Compile with the actual pinned Lean toolchain
        ↓
Extract declarations, #check, #print, and #print axioms
        ↓
Write JSON and Markdown receipts back to the H: archive
```

The API and runner code used for this flow is maintained in `pipeline-workflows`.

## Non-negotiable rules

- Preserve original files. Discovery does not authorize moving, renaming, replacing, deleting, or canonizing them.
- Negative controls run before positive proof jobs.
- “Passed” means the actual pinned Lean toolchain compiled the scoped target. Inventory, parsing, HTTP success, or an LLM explanation is not proof verification.
- A project-level pass, file-level pass, theorem inspection, and axiom inspection are separate statuses and must be reported separately.
- Each verified declaration should retain its source path, source hash, toolchain identity, command, output, assumptions, and receipt.
- Run `#check`, `#print`, and `#print axioms` where applicable. A compiled theorem remains limited to its stated assumptions.
- LLM explanations must separately label:
  - precise mathematical meaning;
  - explicit and implicit assumptions;
  - limitations and what was not proved;
  - plain-language explanation;
  - philosophical interpretation;
  - theological interpretation.
- Philosophical and theological interpretations are interpretations, not Lean verification results.
- Obsidian may reference a Lean source, hash, and receipt, but it is not an additional canonical execution location.
- The prototype at `A:\_workspaces\codex\Lean-4` is transitional. Do not begin new canonical work there. Do not delete it until its useful code and outputs have been migrated and compared.
- Any Lean material found elsewhere is an `UNCLASSIFIED_MIGRATION_CANDIDATE`. Do not run, move, or delete it merely because it was discovered.

## Required migration record

Before any candidate is copied into the canonical execution root, record:

- original absolute path;
- discovery date;
- file count and project structure;
- SHA-256 hashes;
- Lean version or `lean-toolchain`, if present;
- whether it matches an existing source;
- proposed destination;
- review status;
- David’s approval.

## The plain rule

**Archive and review on H:. Execute only from the D: canonical root. Maintain the API in pipeline-workflows. Preserve everything until migration is verified.**

