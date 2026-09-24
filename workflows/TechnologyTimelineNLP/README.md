# Technology Timeline NLP

Evidence-preserving workflow for turning scraped timelines, transcripts,
articles, tables, and notes into one coherent technology dependency history.

## Purpose

This workflow does not merely sort inventions by date. It extracts atomic
events, separates development stages, reconciles duplicate names, preserves
priority disputes, and asks how each development enabled later technologies.

```text
raw sources
-> atomic event records
-> normalized event clusters
-> date and priority audit
-> dependency graph
-> readable chronology
```

## Safe operating boundary

- Sources are read and preserved.
- Conflicting dates and contributor claims remain visible.
- Similar events are clustered but never silently merged.
- Missing evidence remains `UNKNOWN`.
- NLP confidence is a triage signal, not historical authority.
- Every final event must retain source-file and source-span lineage.

## Input

Place HTML, Markdown, text, CSV, JSON, transcript, or converted source files in
`INPUT`. Media should be transcribed before this workflow unless the upstream
station already supplies a transcript.

## Main prompt

`PROMPTS/MASTER_TIMELINE_REFINERY.md`

## Expected outputs

1. `01_SOURCE_INVENTORY.md`
2. `02_EVENT_LEDGER.jsonl`
3. `03_EVENT_CLUSTERS.md`
4. `04_DISPUTES_AND_UNCERTAINTIES.md`
5. `05_DEPENDENCY_EDGES.csv`
6. `06_CHRONOLOGICAL_TIMELINE.md`
7. `07_DEPENDENCY_NARRATIVE.md`
8. `08_RESEARCH_GAPS.md`
9. `09_RUN_RECEIPT.md`

All outputs remain `CANDIDATE` until reviewed.

## X-drive routing

The ready job-card template is `CONFIG/X_JOB_TEMPLATE.yaml.disabled`. Copy it to
`X:\00_INBOX`, change the extension to `.yaml`, point `inputs` at the scraped
files, and run `X:\00_INBOX\SEND.bat`.
