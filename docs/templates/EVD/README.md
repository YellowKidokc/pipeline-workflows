# EVD: Epistemic Intake Rubric v2.0.0

`EVD_RUBRIC_v2.0.0.json` is the evidence rubric (EVD). This is a copy made on 2026-09-27. The runner reads
`API\_system\vendor\evidence_chain\SCRIPTS\SYSTEM_FILES\SCHEMAS\EPISTEMIC_INTAKE_V2_RUBRIC.json`.
The same file is also in `vendor\evidence\SCRIPTS\SCHEMAS\`. It is used by the Evidence Chain intake engine
(`epistemic_intake_v2.py`, station 39). Its results are the `evd_*` fields in a companion's YAML header:
`evd_support`, `evd_counter`, `evd_balance`, `evd_coverage`, `evd_weakest_claim` and so on.

**Governing rule:** understand before classifying; reconstruct before criticizing; test before concluding; never claim
more or less than the evidence warrants.

## What it contains

- **11 epistemic modes.** Every claim is labeled as one of: definition, logical, mathematical, formal-verified,
  empirical, historical, philosophical, theological, bridge, analogy, conjecture.
- **10 dimensions × 18 probes = 180 checks:**

| Dimension | What it asks |
|---|---|
| Logical Validity | Does the conclusion follow? No equivocation, circularity or suppressed premises. |
| Internal Coherence | Do the paper's own claims, definitions, equations and tables agree with each other? |
| Definition Precision | Is every load-bearing term defined, non-circular, and kept in its own domain? |
| Evidence Adequacy | Does each claim have relevant, retrievable, proportionate support? |
| Explanatory Compression | Does it explain more with less, counting primitives, parameters and exceptions? |
| Rival Discrimination | Are rivals stated fairly, and does the evidence favour this view over them? |
| Testability and Falsifiability | Defeat conditions, specific predictions, and what would change the verdict |
| Cross-Domain Integrity | Is each bridge mapped term by term, without promoting analogy to identity? |
| Adversarial Robustness | Does a real core survive premise denial, ablation and countermodels? |
| Epistemic Calibration | Is every claim stated at exactly the strength its evidence warrants? |

- **Each probe** is marked PASS, PARTIAL, FAIL, NOT_APPLICABLE or UNKNOWN, with a reason and the IDs of the
  source objects it rests on. Each dimension score is capped at 10, and it reports coverage and confidence separately.
- **8 global gates.** Any one of these blocks a clean verdict: unknown source, critical hidden premise, failed formal
  receipt, untested central empirical claim, unresolved category error, fatal counterexample, source mismatch,
  unresolved contradiction.

## How it relates to the other scores

- The **CKG companion** (EVIDENCE engine, `02_MASTER_PAPER_RENDERED_FORMAT.md`) reviews a paper section by section.
  EVD is the rigorous per-paper audit behind the `evd_*` numbers.
- **Station 49 (argument grade)** is the lighter per-argument version: 8 strength checks and 4 originality checks.
  EVD's probes are the natural way to deepen 49's strength checks. For example, "Logical Validity" could replace the
  single "inference" check.
- Two notes on station 39 as it stands (observed 2026-09-27, not yet changed):
  - It also asks the model for each dimension's numeric `score`. It would be more reliable to compute the score from
    the probe results (PASS 1, PARTIAL 0.5) in code, as station 49 does.
  - 180 probe results with reasons is a long reply. Check it for the 8k output cap, the same cut-off that affected the
    CKG companions.
