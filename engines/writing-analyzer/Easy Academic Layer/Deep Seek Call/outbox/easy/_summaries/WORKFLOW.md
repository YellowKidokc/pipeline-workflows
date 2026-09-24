```yaml
---
claims:
  - "A structured workflow with nine stages is required to convert HTML to clean Markdown while maintaining accountability through a control ledger."
  - "Layer 0 (the Workflow Control Ledger) must capture workflow name, run ID, stage timestamps, file counts, and error logs for every run."
  - "The first pass must process one source file at a time, emitting one summary set and one set of candidate terms per file, without merging across series."
  - "Output artifacts must be organized into eight specific folders including workflow-runs, clean-markdown, by-source, index, definitions, qa, vectors, and _prompts."
  - "Later consolidation of repeated terms across series is explicitly deferred to a separate workflow, not part of the first pass."
domains:
  Workflow Management: 60
  File Organization: 25
  Data Processing: 15
---
```

# Summary Workflow

This folder is where we do the first pass of turning HTML files into clean Markdown files.

## Current Stage Model

Here are the nine stages in order:

0. `workflow-control-ledger` — the record-keeping stage
1. `conversion-layer` — turning HTML into Markdown
2. `clean-markdown-layer` — cleaning up the Markdown
3. `source-inventory` — listing what files we have
4. `series-vectorization` — turning text into searchable data
5. `summary-drafts` — writing first versions of summaries
6. `definition-and-claim-drafts` — writing first versions of definitions and claims
7. `summaries-done` — marking summaries as finished
8. `ollama-checker` — checking quality with an AI tool
9. `canonical-publish` — publishing the final version

## Layer 0: Workflow Control Ledger

Before we do any content work, every run must create a control record. That ledger (record book) should capture:

- workflow name and version
- run ID (a unique number for each run)
- which series or folder we're working on
- the list of stages
- where input files come from and where output files go
- start time and finish time for each stage
- how many files went in and how many came out for each stage
- file hashes (digital fingerprints) where practical
- errors, warnings, skipped files, and notes about retries

Layer 0 is the accountability layer (the part that keeps everyone honest). It answers:

- What workflow ran?
- What files went in?
- What came out?
- When did each stage start and finish?
- Which stage failed, skipped, or produced warnings?
- Where are the logs, manifests, and index rows?

## Pass 1: One-to-One

- Convert one source file at a time.
- Emit (output) one summary set for that source file.
- Emit candidate terms (possible important words) for that same source only.
- Emit series-specific definition pages for important terms.
- Do not merge definitions across different source series in this pass.

## Folder Layout

Here's how the folders are organized:

- `workflow-runs/` = run manifests (record sheets), stage ledger CSVs (spreadsheet files), event JSONL logs (detailed event records)
- `clean-markdown/` = cleaned Markdown files used for searching and summaries
- `by-source/` = summaries and term extraction output grouped by source file
- `index/` = CSV or index files that point to the things we've created
- `definitions/` = official definition pages, grouped by source series
- `qa/` = quality check output and review status
- `vectors/` = search indexes grouped by series
- `_prompts/` = reusable instructions used by the station

## Output Rule

Keep the first pass local to the source file (don't mix files together). Later consolidation can merge repeated terms across series, but that is a separate workflow — not part of this first pass.

## Export Targets

- Source summary tree (a map of all summaries organized by source)
- Definition pages
- Index rows
- Optional later bundle export to a Pacific folder or other destination folder