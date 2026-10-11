# Fruits station

The Fruits station evaluates observable actor-to-target conduct sentence by sentence, then builds a relational report. It does not infer salvation, hidden motives, or spiritual status, and it does not reduce the paper to one morality score.

Set `DEEPSEEK_API_KEY`, place or select an HTML source, and run the portable launcher in `API/API/FRUITS/SCRIPTS`. Paths are resolved from the launcher location, so the repository can be moved without editing its internal paths. The pilot launcher points to BGL-01; copy it and change only the source path for another paper.

Each successful paper folder contains the extracted sentence packet, validated Fruits JSON, page-writing JSON, Excel workbook, Markdown analysis, HTML preview, and a run receipt with source and template SHA-256 hashes.

Existing JSON checkpoints are reused on rerun. This prevents duplicate paid calls when only Excel, Markdown, or HTML generation needs repair.

## Article-page preview

`SCRIPTS/inject_fruits_html.py` inserts a scoped, front-page Fruits dashboard into a copy of the analyzed article. It refuses to run when the article SHA-256 no longer matches the run receipt, leaves the source untouched, and replaces its own marked block on rerun instead of duplicating it.

For the current pilot, run `API/API/FRUITS/SCRIPTS/BUILD_BGL01_FRUITS_PAGE.bat`. The resulting `*.fruits-integrated.html` is written beside the paper's other OUTBOX artifacts. The dashboard shows the main relational finding, sentence-level fruit/anti-fruit balance, strength, danger, counterfeit patterns, the paper's self-mirror, recommended repair, and expandable quoted evidence.
