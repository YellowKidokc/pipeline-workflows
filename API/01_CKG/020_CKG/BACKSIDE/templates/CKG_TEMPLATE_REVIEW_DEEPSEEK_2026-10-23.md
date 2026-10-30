# DeepSeek review of the CKG template (V3.2) and V4 pipeline, Oct 23 2026

## A. Honest verdict on the V3.2 template

**Strong.** V3.2 gets the authority boundary right in principle: Python supplies IDs, hashes, timestamps, counts, and validation; AI proposes content and classifications; a human rules on admission. That is the correct spine. It also preserves source text and hashes, insists on source spans, versions objects, records typed relationships, distinguishes evidence direction from evidence count, separates proof build status from substantive truth, and makes unknowns explicit rather than filling them with fake zeros. The correction ledger, proof receipts, defeat conditions, and “what held / what broke / what is overstated” audit are all good. The template is trying to be auditable rather than persuasive. That is the right instinct.

**Bloated and redundant.** It is too many things at once: paper record, atom record, review report, extraction schema, run log, dashboard compatibility layer, scoring system, admission workflow, and library maintenance manual. The YAML front matter is enormous and includes fields an atom record should not carry per paper: `stations`, `grading`, `call_routes`, `usage_tokens`, `provider`, `model`, `review_status`, `lifecycle_state`, `admission`, `integrity` details, and many refs. Those belong in an orchestration sidecar or database, not repeated in every Markdown record.

The bigger problem is duplication. The same object is rendered in the Atom Map, S02, A1, A11, A12, A3, A10, S04/A2/A4, and S07/S08. Audit findings appear in the overview, S10, and A8. Classification appears in YAML, S01, A6, A14. That is not just verbose; it creates drift. An AI or human will update one copy and leave another stale. The template says “one authoritative structured record, multiple presentations,” but the physical template still invites multiple independently filled presentations. That is a design smell.

**Missing.** It lacks a clear minimal core versus optional modules. Every paper seems to get the full cathedral even when half the sections are `NOT_APPLICABLE`. It needs stronger per-field extraction provenance: not just object-level spans, but “is this source-stated, inferred, analyst-proposed, verified, or absent?” It needs controlled enums for predicates and statuses, not prose. It needs deduplication and canonical identity rules across papers: when are two claims the same claim, a refinement, a contradiction, or a version? It needs an explicit human review queue and priority rule. It needs a hard rule: an extractor may not fill external-knowledge fields unless a search receipt or explicit `UNVERIFIED`/`ANALYST_PROPOSED` marker is attached. It also needs a cleaner separation between “what the paper says” and “what the reviewer thinks about what the paper says.” Right now those are mixed in the same template.

**Fields an extractor model will fill badly or invent.** The dangerous fields are not the obvious metadata fields; those can be left null. The dangerous ones are the ones that look like analysis but require external knowledge or judgment:

- `unique power / proposed contribution`, `strongest rival comparison`, `WHY closure`, `IC grade`, bridge grades, and `preservation/loss` without formal definitions. These will be guessed.
- `historical witnesses and prior-work relationships`, originality categories, “independently convergent” claims, and “no borrowing inferred.” These require literature work. An LLM will hallucinate witnesses or overstate convergence.
- `hidden premises`, `strongest objection`, `countermodels`, `rival explanations`, `defeat conditions`, and `what would break the paper`. Some of these can be proposed, but only as analyst proposals. An extractor will present them as if the paper itself supplied them.
- `best evidence`, `what survives`, `coherence assessment`, `implications by register`, `six-door lens`, `self-assessment and blind spots`. These are synthesis and evaluation. Fine for a human review, bad as auto-filled structured fields.
- `admission`, `human_ruling`, `review_status`, `lifecycle_state`, `grading`, `integrity` booleans. These must be Python/human only. An LLM should never set them.
- `source span` fields if the model is not given a pre-segmented source. It will approximate spans, merge passages, or invent line references.
- `evidence independence family`, `common cause`, `discrimination`, and `falsifies` edges. These are exactly where models overclaim. `falsifies` should require an explicit defeat condition plus receipt.
- Any numeric count, percentage, token count, date, score, or “coverage” figure. Compute it or leave it null.
- `defensible wording` and “overstated → correction.” An LLM can draft this, but it must be marked as a proposal, not a verdict.

The core rule should be: **the extractor extracts source-bound objects; the reviewer proposes judgments; Python computes facts; a human rules.** V3.2 says this in comments, but the field list still tempts the model to do everything.

## B. Is V4’s step-by-step design an improvement?

Yes, as a **review-writing sequence**. It is a real improvement over one giant prompt because each step has a distinct cognitive job: faithful synopsis, question ladder, argument landscape, paper’s own argument, claim discipline, evidence review, paragraph walk, audit. The “earlier sections” feedforward, the plain-language house rules, the blast-radius vocabulary, and the insistence on citing historical thinkers as witnesses rather than sources are all good for producing a readable, honest review. It reduces the “one giant pass” failure mode where the model summarizes, evaluates, and invents metadata all at once.

But V4 is **not** a replacement for the structured record. It is a prose review generator. It does not produce stable IDs, typed edges, source spans, versioned objects, evidence ledgers, proof receipts, schema validation, or a human-ruling queue. If you treat V4 as the CKG pipeline, you will get good essays and bad canonization data.

Also, the set you pasted has **eight** prompts, not seven: synopsis, ladder, legs, arguments, claims, evidence, walk, audit. Minor, but worth fixing in the docs.

**Where V4 overlaps.** `SYNOPSIS` and `WALK` both walk the paper section by section. Keep synopsis as the faithful account; move walk to an optional editorial-QA layer or merge it into audit. `LADDER` and `ARGUMENTS` both ask about the paper’s questions and premises. `LEGS` and `ARGUMENTS` both map argumentative territory, one external and one paper-specific; that distinction is real but will drift into repetition. `CLAIMS`, `EVIDENCE`, and `AUDIT` overlap on overstatement, missing support, and defeat conditions. The “do not repeat earlier sections” instruction helps prose, but it is unreliable because the model only sees prose, not structured object IDs. Dedupe should be done by Python/object identity, not by a prompt instruction.

**Where V4 leaves gaps.** It has no source segmentation step, no definition/math extraction, no proof/build record, no bridge record, no typed relationship table, no classification sidecar, no extraction confidence, no validation, no cross-paper linking, no admission workflow, and no exhaustive claim inventory. `CLAIMS` deliberately picks three to five per group, which is right for a review and wrong for CKG canonization. `LEGS` asks for every serious position on the question, which is exactly where an LLM will invent names, dates, and “modern proponents.” The `UNVERIFIED` rule is good, but it does not stop the model from inventing a plausible-sounding witness and marking it `UNVERIFIED`; the safer rule is “no witness without a checkable source, otherwise omit.”

So: **V4 is an improvement for the readable review lane. It is a regression if it replaces the structured extraction lane.** Keep both, but separate them.

## C. Recommended design: leaner record template and step order

I would split the system into two artifacts:

1. **A JSON/JSONL atom store** as the authoritative structured record, with one object per claim, evidence item, argument, definition, math object, proof, bridge, test, etc.
2. **A lean Markdown paper record** that renders the source map, object index, audit, and human-readable review from that store. Do not duplicate every object’s full anatomy in five sections.

### Lean Markdown record template

```markdown
---
record_version: CKG_PAPER_V5_LEAN
paper_id: P000123
paper_uuid: 00000000-0000-0000-0000-000000000000
source_file: path/to/source.md
source_sha256: null
source_version_uuid: null
extraction_run_id: null
extractor_model: null
prompt_set: CKG_V5_EXTRACT
review_status: EXTRACTED | AI_REVIEWED | HUMAN_REVIEWED | RULED
human_ruling: pending | admitted | rejected | deferred
---

# {{Title}}

## 0. Source and coverage

- **Source:** {{file, hash, version, length}}
- **Governing question:** {{source-stated or ABSENT with reason}}
- **One-sentence finding:** {{source quote + span, or ABSENT}}
- **Classification:** {{project / domain / content_type; source-stated vs proposed; confidence}}
- **Global limits:** {{what this record does not cover}}

| Section ID | Heading | Span | Processed? | Unprocessed reason |
|---|---|---|---|---|
| S001 | ... | ... | yes/no | ... |

## 1. Definitions, symbols, and math objects

| ID | Term / expression | Exact source span | Plain meaning | Formal meaning | Scope / context | Status | Conflicts |
|---|---|---|---|---|---|---|---|
| DEF001 | ... | ... | ... | ... | ... | source-defined / used-undefined / imported / proposed | ... |

## 2. Claims

| ID | Exact claim text | Span | Plain rendering | Mode | Scope / quantifiers | Depends on | Load-bearing? | Assessment |
|---|---|---|---|---|---|---|---|---|
| CLM001 | "..." | ... | ... | asserted / used / quoted / modeled | ... | ... | yes/no/unknown | unassessed / supported / opposed / disputed / overstated / false / true-as-scoped |

Use `ABSENT` when the paper does not supply a field. Do not infer a claim from a heading alone.

## 3. Arguments

| Argument ID | Conclusion claim ID | Premises / steps | Inference license | Hidden premise | Source span | Status |
|---|---|---|---|---|---|---|
| ARG001 | CLM001 | ... | ... | PROPOSED: ... | ... | source-stated / reconstructed / proposed |

## 4. Evidence

| Evidence ID | Source / finding | Target claim | Direction | Lane | Independence family | Inspected? | Limitations | Status |
|---|---|---|---|---|---|---|---|---|
| EVD001 | ... | CLM001 | supports / contradicts / tests / unassessed | native / bridge / identification | ... | yes/no/citation-only | ... | ... |

Do not use `falsifies` unless a defeat condition and receipt are linked.

## 5. Formal / proof records

| Proof ID | Exact proposition | Premises | Toolchain | Build result | Receipt | Trust status | Correspondence |
|---|---|---|---|---|---|---|---|
| PRF001 | ... | ... | ... | NOT_RUN / PASSED / FAILED / TIMEOUT | ... | CLEAN / SORRY / ADMIT / CUSTOM_AXIOMS / ... | EXACT / PARTIAL / MODEL_ONLY / PROPOSED |

## 6. Bridges and mappings

| Bridge ID | Source structure | Target structure | Mapping | Preserved | Lost | Reverse map | Countermodels | Status |
|---|---|---|---|---|---|---|---|---|
| BRG001 | ... | ... | ... | ... | ... | ... | ... | proposed / checked / rejected |

## 7. Defeat conditions and tests

| ID | Target claim | Exact negation / defeat condition | Test | Result / status | Receipt | Impact |
|---|---|---|---|---|---|---|
| DEF-T001 | CLM001 | ... | ... | NOT_RUN / PASSED / FAILED | ... | INERT / LOCAL / STRUCTURAL |

## 8. Relationships

| Edge ID | Source | Predicate | Target | Load-bearing? | Reason | Status |
|---|---|---|---|---|---|---|
| EDG001 | CLM001 | dependsOn / supports / contradicts / tests / defines / bridgesTo / derivedFrom / corrects | DEF001 | yes/no | ... | proposed / verified / ruled |

## 9. Audit

### What held

{{Bounded findings, with object IDs and source spans.}}

### What broke

{{Exact defect, affected object, blast radius, receipt or reason.}}

### What is overstated → defensible wording

| Object | Original quote and span | Problem | Defensible wording | Blast radius | Status |
|---|---|---|---|---|---|
| CLM001 | "..." | TRUE/FALSE reason | ... | INERT / LOCAL / STRUCTURAL | proposed / ruled |

### What remains untested or disputed

{{Open items, missing sources, unresolved rivals.}}

### Completeness checks

- Every claim has an exact span or `MISSING_SPAN` reason.
- Every evidence edge names a target claim/version.
- Every proof names its conclusion and receipt or absence.
- Every object ID is unique; relationships resolve.
- Coverage is reported: mapped units / unmapped units / reasons.
- Human ruling queue is explicit.

## 10. Provenance, confidence, and corrections

- Run ID: ...
- Model/provider: ...
- Prompt set version: ...
- Input hash / output hash: ...
- Extraction confidence notes: ...
- Corrections ledger: ...

| Correction ID | Target | Defect class | Previous | Proposed successor | Reason | Applied? | Human ruling |
|---|---|---|---|---|---|---|---|
| COR001 | ... | LOCAL_FIX / SUBSTANTIVE / WITHDRAWAL / RECLASSIFICATION | ... | ... | ... | yes/no | pending |

## Atom index

| Atom ID | Type | Short statement | Span | Status | Key links |
|---|---|---|---|---|---|
| CLM001 | CLAIM | ... | ... | unassessed | supports: EVD001 |
```

Keep the Atom index as an index, not a second full record. The detailed object anatomy should live in the JSONL store. The Markdown should be readable and auditable without becoming five parallel databases.

### Recommended step order

0. **Intake and source validation — Python only.** Hash the source, split into sections, assign section IDs, verify no truncation. No AI judgment yet.
1. **Coverage map and faithful synopsis.** Map the paper section by section. Write the synopsis only from source text. No evaluation.
2. **Question ladder — optional but useful.** State the paper’s governing question and the next few questions a careful reader would ask. Mark answers as source-stated or `ABSENT`.
3. **Definitions, symbols, and math objects.** Extract terms, equations, units, scopes, and conflicts. Do not formalize beyond what the paper gives; mark proposed formalizations separately.
4. **Claim extraction.** Exhaustive for load-bearing claims, not every sentence. Include exact text, span, mode, quantifiers, and dependencies. No evaluation in this step.
5. **Argument reconstruction.** Build premises, steps, inference licenses, conclusions, and hidden premises as `PROPOSED` where not stated. Link to claim IDs.
6. **Evidence extraction.** Only evidence the paper actually offers. Direction, target claim, lane, inspected status, limitations. Independence family only if the paper or reviewer can justify it; otherwise `UNKNOWN`.
7. **Conditional formal/proof and bridge extraction.** Run only when applicable. Proofs need exact proposition, premises, toolchain, build result, receipt, trust status. Bridges need mapping, preservation/loss, reverse map, countermodels.
8. **Defeat conditions, tests, and predictions.** Propose where the paper does not state them; mark `ANALYST_PROPOSED`. Never mark `falsifies` without a defeat condition and receipt.
9. **External landscape / legs / historical witnesses / prior art.** This is the V4 `LEGS` and part of `ARGUMENTS` moved into a **review layer**, not the canonical record. No witness without a checkable citation. Omit rather than hallucinate.
10. **Claim discipline and evidence critique.** V4 `CLAIMS` and `EVIDENCE` belong here. Give blast radius, exact problem, defensible wording. Do not let this step overwrite the extracted claim record.
11. **Audit and build next.** What held, what broke, what is overstated, exact defeat condition, three next actions.
12. **Paragraph walk — editorial QA.** Keep it last and optional. It is about readability, not truth or canonization.
13. **Reconciliation and human ruling.** Python validates schema, counts, spans, duplicate IDs, unresolved references. Human rules on admission, corrections, and load-bearing judgments.

The important change from V4: **do not let the external-argument “legs” step come before paper-bound extraction.** For canonization, the order must be source first, objects second, evaluation third, human ruling last. V4’s order is good for an essay; the order above is better for an auditable pipeline.

## D. What this system is actually good for, and what it should not be trusted to do

This system is good for producing a disciplined, readable review draft of a paper and for turning that paper into a source-bound, versioned map of claims, arguments, definitions, evidence, proofs, bridges, and open questions that humans can audit and cross-link. It is good at forcing explicit boundaries, recording what was not checked, separating AI proposals from human rulings, and preventing the usual review failure where everything is summarized and nothing is traceable. It should **not** be trusted to establish truth, canonize claims, decide admission, verify citations or empirical claims without external receipts, perform novelty searches, resolve historical priority, grade coherence, or replace human judgment. Its proper role is a citation-backed, uncertainty-marked assistant and workflow engine, not an authority.
