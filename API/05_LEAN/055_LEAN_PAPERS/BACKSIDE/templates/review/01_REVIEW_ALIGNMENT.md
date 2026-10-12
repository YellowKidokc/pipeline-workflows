# Review alignment — V2.1

This supplements the fixed report template. Use the supplied reviewer checklist as review questions, subject to the corrections below. No source or checklist prose is itself a verification receipt.

## Required aggregation
- Map source claim IDs to chapters and exact Lean declarations. File proximity suggests relationships; it does not establish them. Unknown mappings stay unreviewed.
- Record exact source statements AND elaborated declaration output when available: implicit binders and section variables can matter. Do not demand byte equality between differently formatted source and elaborated output.
- Distinguish project definitions, standard mathematical axioms, custom axioms, hypotheses, and proof placeholders.
- Record source/module/toolchain/lockfile hashes, actual commands and logs, named declarations, and receipt dates. Missing receipts mean Not checked.
- Explain quantifiers, types, coercions, boundary cases, and relevant arithmetic semantics. Do not infer that code uses the intended physical quantities from its variable names.
- Record non-vacuity, negative controls, ablation, converse/countermodel checks, and independent-encoding status separately. For multiple claimed derivations, inspect shared dependencies before calling them independent.
- Include the documented revision story: what was attempted, what failed, what changed, and what finally passed. If no history is supplied, say History not supplied. Never invent trials or failures.
- In section 12, propose up to three next proof opportunities. Each needs a precise candidate statement, known dependencies, missing work, assumptions, expected adversarial test, and what it would unlock. Label feasibility as an estimate, not a promise.

## Corrections to the supplied checklist
Failure to construct a witness does not establish impossibility or vacuity. Establish vacuity with an appropriate argument about the hypotheses, and keep it separate from placeholder dependence.

Failure of a proof script after a premise is removed does not establish logical necessity. A countermodel under the weakened premises can establish the relevant necessity claim. Continued proof success may reveal a stronger theorem rather than a flaw.

Search hits for opaque declarations, resource options, partial or unsafe code are review leads, not automatic proof escapes. Check whether and how the named proof depends on them. Expanded compiler trust and sorryAx are distinct findings; do not map every trust concern to PARTIAL_WITH_SORRY.

An axiom report is necessary evidence, not the sole decisive test of correspondence, reproducibility, or significance. A model witness supports non-vacuity relative to its foundations; it is not an unrestricted consistency proof of those foundations.

Formalizable parts of theological or bridge claims may be represented as conditional mathematical statements. Classification alone must not exclude them; the interpretation remains a separate review.

## Reader-first companion
Before technical details, provide six fixed sections: What we claimed; What we asked the computer to check; What we went through; What the recorded result means; What it does not mean; Why it matters. Explain Lean accurately and accessibly without describing it as infallible. No invented checkmarks or receipts. Technical audit follows; preserved original source is appended by software, not rewritten by the model.
