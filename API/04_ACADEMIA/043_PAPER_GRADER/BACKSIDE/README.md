# 43_PAPER_GRADER

Three local passes on each paper, no API. Every number measures structure, coverage and connection; none is a truth ruling.

| Pass | Code (vendored, unchanged) | What it measures |
|---|---|---|
| 1 | `vendor/grader_v2/paper_grader.py` (paper_grader 0.2.0, NAS `APIs/MAIN/PYTHON/SCRIPTS`) | structure, terms, math, evidence, argument, bridges, falsifiability, voice, readiness |
| 2 | `vendor/grader/pipeline.py` (July paper-proof-grader) | metrics, sections, equations, claim candidates with maturity labels |
| 3 | `vendor/grader_metrics/` (OPERATOR_2 modules + Paper Metrics Engine, NAS `Academic Paper Grading`) | causal claims and warrants, hedges vs boosters, idea density, concept drift, paragraph topic coherence, self-contradiction (NLI), 76-field metrics engine |

Pass 3 uses `all-MiniLM-L6-v2` (drift, coherence) and DeBERTa-v3 NLI (contradictions, downloaded once on first use).
A metric that cannot run is reported in the file, never fatal. About a minute per paper on the first run, less after.
`vendor/grader_metrics/novelty_rank.py` is kept but not run here: corpus novelty is in 42_STATISTICS_WALL.

Output: `<note> · 43_PAPER_GRADER.md` (all three passes) and `.html` in the folder chosen at the button; JSON and xlsx in the item's run folder.
Menu options: limit, workers, redo, outbox.
