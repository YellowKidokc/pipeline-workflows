# CKG companion: how it prints (2026-09-27)

The runner fills `CKG_ATOM_MASTER_TEMPLATE.md` stage by stage (map, S01-S10, audit) and writes one companion per
paper to `OUTBOX\<paper_uuid>.md`. It then copies it under a readable name to the OUTBOX root and to
`02_BY_DOMAIN\`, `03_BY_TAG\` and `04_BY_SERIES\`. The page reads top to bottom:

```
---  paper_uuid · source_path · source_hash · model · provider · grade   (front matter)
# CKG Companion — <title from the map>
`<paper_uuid>`

## Map
Domain · Project · Purpose
<one-paragraph summary>
Keywords: ...
| Key | Type | Register | Statement | Quote |      one row per object (C1, D1, A1 ...), quotes verbatim
Not captured above: ...

## S01 — Core Finding and One-Sentence Claim
## S02 — Axiom/Definition Spine
## S03 — Argument Chain
## S04 — Evidence and Sources
## S05 — Objections and Counterarguments
## S06 — Theological/Philosophical Translation
## S07 — Formal and Mathematical Layer
## S08 — Bridge Integrity and Cross-Domain Checks
## S09 — Open Questions and Falsification Boundaries
## S10 — Consilience Summary and Next Steps
## Audit Report        quotation check, status labels, unsupported claims, placeholders, verdict

## Source              the full original text, last
```

Every section carries `Status: AI_PROPOSED`. Each claim in the map is also written as its own atom under
`OUTBOX\CLAIMS_PROOFS_EVIDENCE\claims\`, one file per claim.

Changes made on 2026-09-27 in `API\_system\vendor\ckg\workbench\` (`ckg.py`, `extract_cpe.py`):
- The map is rendered as a table. It used to be raw JSON.
- Each section heading appears once. It used to be doubled ("S01", then "S01 — ...").
- The title comes first and the source goes last. A transcript's own YAML block no longer breaks the page header.
- The claim extractor reads each paper once, although the OUTBOX root holds two copies of it. It used to write every claim twice.

Example: Gary Habermas Chapter 001 in `API\020_CKG\OUTBOX\`.

The same video run through the YouTube CKG (station 03) produces a different shape: a catalogue of arguments
filed under the debate questions. See `..\YOUTUBE_CKG\`.
