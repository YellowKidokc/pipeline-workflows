# CKG_SPLIT_DRAFT: CKG cut into one folder per call

A **copy**, made 2026-10-15. Nothing in `API\` was changed, and nothing runs from here yet.
It's the data the CKG backside page will show: the calls in order on the left, each call's
output template on the right.

## What's here

```
ckg.json            the list: every call, on/off, run order, page order, model, workers, output settings
calls\000_MAP\      prompt.md   (copied verbatim from today's runner)
calls\009_S01\      prompt.md   (draft: today's generic prompt narrowed to this one section)
                    output.md   (this section's slice of CKG_ATOM_RECORD_V3.2, verbatim)
...                 39 folders in template order
```

- **Run order** (`run_order` in ckg.json): MAP → S01–S10 → A1–A16 → the summaries that read
  everything (title block, proof glance, audit, atom map, at a glance, build next) → YAML last.
  GRADER is listed but switched off.
- **Not called:** ORIGINAL (the source gets pasted in), two divider headings, and LEGACY.
- **Check:** joining every `output.md` in page order gives back `CKG_ATOM_RECORD_V3.2_TEMPLATE.md`
  byte for byte. `source_sha256` in ckg.json records which version was split.

## Two things found while splitting

1. **The runner doesn't use this template.** `vendor\ckg\workbench\ckg.py` sends the 3 KB
   `CKG_ATOM_MASTER_TEMPLATE.md`, which gives S01–S10 different meanings (S01 "core finding",
   S02 "axiom spine", …). The 47 KB V3.2 here (S01 "Classification & Routing", S02 "Claim
   Definition", …) sits in `020_CKG\BACKSIDE\templates` but CKG never reads it.
   **Decided 2026-10-15 (David): V3.2 is the real CKG.** The live runner still uses the 3 KB
   template until it is switched over to read this folder.
2. **Today there's one prompt for all sections.** Every section call gets the same "Execute CKG
   section {stage}" text plus the whole template plus every earlier result. The per-call
   `prompt.md` files here are drafts that narrow it to one section. They haven't been tested
   against a model.

## Variants (math, YouTube, …)

One variant is one folder like this, with its own `ckg.json` (`"variant": "math"`) and its own
calls. Copy the folder, then edit or switch off calls.
