# 63_PAPER_AUDIT

One paper (or a folder of them) through the whole audit, one station after another, all results in one OUTBOX.

| Step | Station | What it adds | API |
|---|---|---|---|
| 1 | 43_PAPER_GRADER | paper_grader 0.2.0, July paper-proof-grader, advanced metrics (causal claims, hedges, idea density, drift, coherence, contradictions) | no |
| 2 | 65_PAPER_INTELLIGENCE | Paper Intelligence Suite: text analytics, academic standard, chi / W-K / fruits / Master Equation variables, NLP, Truth Engine, emotion, linguistic depth, knowledge graph | no |
| 3 | 57_API_DEEP | Fruits, Axioms, Atoms, Lean, Stories, Master Equation, Coherence (one chain per paper) | yes |
| 4 | 58_ARGUMENT_GRADE | strength and originality 0-8 per argument, from quoted checks | yes |
| 5 | 59_CHI_EVALUATOR | each claim on the Master Equation's ten channels, then four statements | yes |
| 6 | 42_STATISTICS_WALL | every metric in Python, with corpus and series percentiles | no |
| 7 | 46_REPORT_COMBINE | every station's JSON in order: report.html and report.xlsx | no |
| 8 | 64_SITE_PACKAGE | files it all into the series house: a page per part (Markdown + HTML), the series title page rebuilt | no |

The steps are the `chain` list in `station.json`: edit that list to add, drop or reorder a step.
40_ANALYTICAL_ARMS is not in the chain: 57 already runs Fruits, the Master Equation, axiom nodes and coherence.

- `1 RUN HERE`: the papers in this `INBOX` (`00_PRIORITY` first, then `01_SERIES\<series>`, then `02_GENERAL\<group>`).
- `2 RUN ON FOLDER`: asks for the folder, which papers, and where the output goes.
- No questions: `python BACKSIDE\63_paper_audit.py <papers or folder> --outbox <folder> --workers 8`.
- From the menu: `ONE_MENU.bat G --item <paper>` runs the same stations as routine G.
