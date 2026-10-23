## A16 · Shared-record, blind-review and compatibility contract

### One authoritative structured record, multiple presentations
The versioned JSON package is the authoritative structured assessment record. A-records are its detailed Markdown projections; the Atom Map, Audit, inventory and S-sections render those same records by UUID/version. Neither presentation is a second independently filled form. The preserved source remains authoritative for what the author actually wrote; JSON does not overwrite author meaning or confer canon admission.

Render the Audit/S10 from shared assessment records; S02/A1 from claim discovery records; S04/A2 from evidence records; S07/A3/A10 from mathematical and proof records; S08/A12 from mapping records; S03 hidden premises/A1 stage 3 from dependency records. Paper-level synthesis may add prose, but must cite the same underlying versions and introduce no unsupported verdicts. Human edits to any rendered section become revision proposals to reconcile into the structured record, followed by re-rendering.

### Blind comparison packet
{{Required when the versioned IC assessment rule calls for blinded comparison; otherwise explicit NOT_APPLICABLE with reason.}}

| Field | Value |
|---|---|
| Packet UUID/version and artifact reference | {{ }} |
| Packet SHA-256 and creation receipt | {{ }} |
| Neutral tokens / anonymization procedure | {{ }} |
| Included candidate and rival pairings | {{ }} |
| Selection rule and pre-result registration | {{rule version, hash, timestamp}} |
| Separate deblinding-key artifact and hash | {{restricted reference; do not expose key in blinded packet}} |
| Evaluator, available information and blind exposure | {{ }} |
| Execution state, results and receipt | {{NOT_RUN or result}} |
| Deblinding event and subsequent interpretation | {{ }} |
| Grade proposal versus validated grade | {{distinct fields}} |

An IC grade remains a proposal until its required checks have receipts or an explicit recorded ruling addresses exceptions. Missing blinded work blocks only the grade promotion that requires it, not unrelated processing. Do not claim anonymity just because a packet field exists.

### Required reasons, falsification and termini
Before any paid review, detect routing questionnaires, missing-document references and empty sources. Preserve them as intake records with INSUFFICIENT_SOURCE; do not publish them as reviews of the referenced paper. A routing decision never substitutes for fetching the actual document. A no-object mapping stops downstream review and records the reason. Legitimate procedures and short substantive claims must not be rejected solely for length.

When the same blocking unknown affects three or more sections, assign one stable unresolved-item ID, explain it once in the overview and A9, and render dependent sections as “blocked: <ID>” plus only section-specific findings. Retain section markers without repeated empty tables. Always retain the optional scorecard skeleton with NOT_ASSESSED rows when grading is disabled.

Every NOT_APPLICABLE, NOT_RUN, DEFERRED, UNKNOWN or OPEN section carries a reason and applicability/completion state. Empty required reasons fail structural validation. The report separately displays coverage, actual checks completed and deferred work; placeholder completeness is not assessment completeness.

Every `falsifies` edge names its target claim/version, exact defeat condition/version, observed result and receipt. Link preregistration when present; retrospective application requires an explicit ruling and rationale. Preserve unruled retrospective findings as proposals; absence of preregistration does not erase a genuine counterexample.

No terminus may close merely by renaming the desired conclusion. Record the reviewer, premises and non-circularity rationale. Python checks that the record exists and flags missing/cyclic references; substantive circularity is a reasoning review, not something a field-presence check can prove absent.

### Independent convergence and historical witnesses
Add the provenance category **Author-original; independently convergent with historical witness**. Preserve the author's independent-origin assertion, dated source when available, witness citation, structural correspondence and verification status. Do not infer borrowing merely because older related work exists, or infer independent discovery merely from resemblance. Historical witness is not automatically independent empirical confirmation. Retain adaptation/prior-work categories where actual borrowing is documented.

### Dashboard migration contract
Inspection of EVIDENCE/SCRIPTS/TEMPLATES/EVIDENCE_DASHBOARD_v0.3.md confirms queries read flat `evd_*` fields and many require `type = "evidence-sheet"`. Nested fields alone will not satisfy those queries. For migration, Python may emit read-only flat compatibility projections from the same structured record, never a second AI-authored set: evd_state, evd_support, evd_counter, evd_balance, evd_families, evd_coverage, evd_gated, evd_stable, evd_weakest_claim, evd_unassessed and evd_assessors; applicable s##_pos/neg/net fields likewise derive from recorded rubric assessments.

Unassessed numbers remain null, not zero; flat evd_state maps NOT_ASSESSED/NOT_RUN to UNSCORED with the original state retained. Gate and stability values remain unknown unless checked. Before rollout, update dashboard filters to accept the new record_version as well as legacy evidence-sheet records, handle nulls as unknown, and avoid treating missing stability as a failed robustness test. Keep document purpose distinct from legacy dashboard type. Test a not-run record and an assessed record. This template change does not itself modify deployed dashboards.

Legacy scores remain UUID/version-addressable for comparison, with origin and date, but never become current assessment by default. Stage numbering in this template is 0–11 (twelve stages), with governance at 11; the earlier request template uses stages 0–10 followed by governance. Preserve an explicit mapping rather than describing the two as literally identical.

