# Summary Workflow Order

This workflow starts with a series or folder of files. It treats station conversion (turning source files into Markdown) as optional — you can skip it if you don't need it.

## Order Of Operations

0. `workflow-control-ledger`
   - Find the workflow and its version.
   - Create the run ID (a unique label for this run).
   - Pick one series folder or all series.
   - Write down the stage list (the steps you'll follow).
   - Record where files come from, where they go, how many there are, timestamps, errors, warnings, skipped files, hashes (checksums) when possible, and output indexes.
   - This is the accountability layer (the record-keeping system) for every step after this.

1. `conversion-layer`
   - Optional: convert source files (like HTML) into Markdown format.
   - Only run this when new HTML or source files need converting.
   - You can skip this step if Markdown files already exist.

2. `clean-markdown-layer`
   - Take the converted Markdown and remove junk left over from conversion.
   - Remove YAML/front matter (metadata blocks), breadcrumb junk (navigation trails), encoding artifacts (garbled characters), leftover script/style code, and obvious export noise.
   - Keep it as Markdown, not plain text.
   - Keep headings, lists, equations, tables when possible, and the original folder structure.

3. `source-inventory`
   - Find all clean Markdown files.
   - Keep the original folder structure.
   - Write the source index (a list of what you found).

4. `series-vectorization`
   - Build or refresh a search/vector index for each series.
   - Use clean Markdown as the input for vectorization (turning text into searchable data).
   - This comes before heavy canonical summaries and definitions (the official versions).

5. `summary-drafts`
   - Write a draft summary for each file.
   - Include: one-line summary, short summary, executive summary, outline, key claims, and terms detected.

6. `definition-and-claim-drafts`
   - Write draft glossary/definition candidates.
   - Write draft claim-control notes (notes about what claims are made).
   - Keep definitions organized by series.

7. `summaries-done`
   - All summary drafts are written, organized, and indexed.
   - This is the current first-pass target stage (the goal for now).

8. `ollama-checker`
   - Optional: run a local quality check.
   - Checks for: grounding (does it match the source?), risky language, missing sources, and the difference between standard ideas and Theophysics ideas.

9. `canonical-publish`
   - Human-reviewed final canonical summaries and definitions (the official, approved versions).

## Output Roots

These are the folders where files get saved:

- Workflow runs: `X:\conversion_station\HTML to Markdown\outbox\_summaries\workflow-runs`
- Clean Markdown: `X:\conversion_station\HTML to Markdown\outbox\_summaries\clean-markdown`
- Summaries: `X:\conversion_station\HTML to Markdown\outbox\_summaries\by-source`
- Definitions: `X:\conversion_station\HTML to Markdown\outbox\_summaries\definitions`
- Indexes: `X:\conversion_station\HTML to Markdown\outbox\_summaries\index`
- QA: `X:\conversion_station\HTML to Markdown\outbox\_summaries\qa`
- Vectors: `X:\conversion_station\HTML to Markdown\outbox\_summaries\vectors`

## Runner

Python module (a piece of code you can run):

```powershell
python -m theophysics_conversion.summary_workflow --dry-run
```

This runs a test without actually changing anything.

Process one series through stage 7:

```powershell
$env:PYTHONPATH="X:\conversion_station\backside\engine\src"
python -m theophysics_conversion.summary_workflow --series genesis-to-quantum --to-stage 7 --dry-run
```

This processes one series called "genesis-to-quantum" up to stage 7, in test mode.

Skip station conversion by default. Add `--run-station` later only when you want the station to run first.