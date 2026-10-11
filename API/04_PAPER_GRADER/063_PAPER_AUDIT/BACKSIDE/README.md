# 63_PAPER_AUDIT

One paper (or a folder of them) through the whole audit, one station after another, all results in one OUTBOX.

| Step | Station | What it adds | API |
|---|---|---|---|
| 1 | 43_PAPER_GRADER | July paper-proof-grader + paper_grader 0.2.0: structure, claims, math, evidence, falsifiability, readiness | no |
| 2 | 57_API_DEEP | Fruits, Axioms, Atoms, Lean, Stories, Master Equation, Coherence (one chain per paper) | yes |
| 3 | 58_ARGUMENT_GRADE | strength and originality 0-8 per argument, from quoted checks | yes |
| 4 | 59_CHI_EVALUATOR | each claim on the Master Equation's ten channels, then four statements | yes |
| 5 | 42_STATISTICS_WALL | every metric in Python, with corpus and series percentiles | no |
| 6 | 46_REPORT_COMBINE | every station's JSON in order: report.html and report.xlsx | no |

The steps are the `chain` list in `station.json`: edit that list to add, drop or reorder a step.
40_ANALYTICAL_ARMS is not in the chain: 57 already runs Fruits, the Master Equation, axiom nodes and coherence.

- `1 RUN HERE`: the papers in this `INBOX` (`00_PRIORITY` first, then `01_SERIES\<series>`, then `02_GENERAL\<group>`).
- `2 RUN ON FOLDER`: asks for the folder, which papers, and where the output goes.
- No questions: `python BACKSIDE\63_paper_audit.py <papers or folder> --outbox <folder> --workers 8`.
- From the menu: `ONE_MENU.bat G --item <paper>` runs the same stations as routine G.
