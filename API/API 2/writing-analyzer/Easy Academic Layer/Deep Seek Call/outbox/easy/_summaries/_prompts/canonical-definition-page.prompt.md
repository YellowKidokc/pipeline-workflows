# Canonical Definition Page Prompt

## Mission

For each candidate term, produce a canonical definition page for a serious nontechnical reader, roughly 8th grade and above. Write clearly, but do not dumb down the concept. Keep standard academic meaning separate from David Lowe's Theophysics framework.

Use only the provided source text and any explicitly provided retrieved context. Do not invent citations, names, dates, papers, or equations. If support is missing, write `source needed`.

This is a one-to-one workflow in the first pass:

- one source file in
- one summary set out
- one definition page per important term out

Do not merge across files during the first pass. Keep series-specific definition pages separate until a later consolidation step.

## Inputs

- Term: `<TERM>`
- Source file: `<SOURCE_PATH>`
- Source series: `<SOURCE_SERIES>`
- Source text: `<SOURCE_TEXT>`
- Optional retrieved context: `<RETRIEVED_CONTEXT>`

## Output Routing

Write each definition page into the definitions output tree, grouped by the source series or folder it came from.

Base output folder:

`X:\conversion_station\HTML to Markdown\outbox\_summaries\definitions`

Use this path pattern:

`X:\conversion_station\HTML to Markdown\outbox\_summaries\definitions\<SOURCE_SERIES>\<term-slug>.definition.md`

Recommended companion tree for the first pass:

- `outbox\_summaries\by-source\<SOURCE_SERIES>\`
- `outbox\_summaries\index\`
- `outbox\_summaries\definitions\<SOURCE_SERIES>\`
- `outbox\_summaries\_prompts\`

Examples:

- `definitions\genesis-to-quantum\entropy.definition.md`
- `definitions\mda\coherence.definition.md`
- `definitions\moral-decline\constraint.definition.md`
- `definitions\master-equation\grace-as-external-work.definition.md`

If a term appears in more than one series, do not overwrite the series-specific pages. Create one definition page per series first. A later canonical merge pass may combine them into a cross-series glossary entry.

Also update or create an index row for each generated page:

`X:\conversion_station\HTML to Markdown\outbox\_summaries\index\definition-index.csv`

Recommended index columns:

`term,term_slug,source_series,source_path,definition_path,status,needs_sources,claim_risk`

## Output Format

# <TERM NAME>

## 1. Plain Definition

A clear definition for a serious nontechnical reader.

## 2. Standard Academic Definition

Define the term as it is normally understood in physics, philosophy, theology, information theory, sociology, psychology, consciousness studies, or the relevant field.

Do not use Theophysics claims in this section unless clearly labeled as a nonstandard interpretation.

## 3. Historical Context

Give a short historical note: who introduced it if known, where it became important, and why the term matters.

If the source text does not support the historical note and no retrieved context is provided, write `source needed`.

## 4. Mathematical / Formal Form

Include equations only if they are standard, present in the source file, or present in the retrieved context.

Separate these categories:

- Standard equation:
- Theophysics equation:
- Speculative / proposed equation:

If no equation is available, write `No formal equation identified in the supplied material.`

## 5. Theophysics Definition

Explain how David Lowe's Theophysics framework uses the term. Preserve the framework's insight, but label the usage correctly as one or more of:

- formalized structural analogy
- speculative bridge
- theological interpretation
- poetic/narrative use
- internal technical term

## 6. Seven-Domain Mapping

Create a table:

| Domain | Meaning | Standard or Theophysics? | Confidence |
|---|---|---|---|
| Physics |  |  |  |
| Information |  |  |  |
| Consciousness |  |  |  |
| Psychology |  |  |  |
| Sociology |  |  |  |
| Theology |  |  |  |
| Theophysics |  |  |  |

Use confidence values: High, Medium, Low, or Source needed.

## 7. Relationships

List:

- Parent terms:
- Child terms:
- Prerequisites:
- Contrasts:
- Closely related terms:
- Common false equivalences:

## 8. Failure Modes

Name where the definition breaks, becomes misleading, or becomes dangerous. Consider:

- Treating analogy as identity
- Treating interpretation as established science
- Treating metaphor as proof
- Confusing observer with conscious observer
- Ignoring domain boundaries
- Overclaiming mathematical rigor
- Collapsing theology, physics, and psychology into one meaning

## 9. Claim-Control Notes

Flag risky language from the original file.

For each risky claim, provide:

- Original: "..."
- Problem: Why this could be challenged.
- Safer replacement: "..."

If there are no risky claims in the supplied material, write `No risky claims identified from the supplied material.`

## 10. Source Candidates

List suggested source categories. Do not invent exact citations unless they are present in the supplied context.

- Wikipedia page:
- Stanford Encyclopedia of Philosophy page:
- Internet Encyclopedia of Philosophy page:
- arXiv / review paper:
- Textbook / standard reference:
- Internal Theophysics file:

If unsure, write `source needed`.

## 11. Final Canonical Sentence

Give one polished sentence that can serve as the canonical glossary definition.

## 12. Agent Verdict

Give a short verdict:

- Ready for glossary: Yes / Needs review / Not yet
- Main risk:
- Best next source to verify:

## Style Rules

- Serious, clear, 8th grade and above.
- Explain technical terms when they first appear.
- Do not flatten hard ideas into slogans.
- Keep standard academic definitions separate from Theophysics claims.
- Use "Theophysics proposes..." for framework claims.
- Use "standard usage..." for established academic meanings.
- Avoid saying "proves" unless the supplied source gives a formal proof and the claim is actually proven.