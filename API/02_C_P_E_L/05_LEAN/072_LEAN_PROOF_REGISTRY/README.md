# 72 — Lean Proof Registry

## CODEX ONLINE: START HERE

Your assignment is to build the governed Lean 4 verification-and-explanation
station in this folder. Work only inside this station unless a test proves that
one small registry integration change is necessary. Preserve all unrelated
repository work.

The result David wants is simple:

> Drop a Lean job into `INBOX`, run the station, and receive a trustworthy JSON
> receipt plus a Markdown report in `OUTBOX` that explains the exact theorem to
> an average reader without confusing interpretation with proof.

Do not merely design it. Implement it, test it, run negative controls before
positive checks, and provide a bounded demonstration. Do not claim verification
unless the actual pinned Lean toolchain ran successfully.

## Required report

Every declaration report must contain:

1. exact source path and SHA-256;
2. exact Lean and Lake versions and pinned toolchain;
3. negative-control results;
4. project, file, and declaration outcomes as separate statuses;
5. exact `#check` output;
6. exact `#print` output;
7. exact `#print axioms` output;
8. all explicit and relevant implicit assumptions;
9. precise mathematical meaning preserving quantifiers and logical direction;
10. a genuinely plain-language explanation;
11. limitations and converses not established;
12. separately labeled philosophical interpretation;
13. separately labeled theological interpretation;
14. interpretation confidence independent of Lean status;
15. human review and canon status;
16. commands, exit codes, timestamps, artifacts, and a reproducible receipt.

## Non-negotiable status boundaries

- `NEGATIVE_CONTROL_PASS` means Lean rejected an intentionally invalid case for
  the expected reason.
- `PROJECT_BUILD_PASS` means Lake returned success and actual work was observed.
- `PROJECT_BUILD_PASS_CACHED_NO_JOBS` means Lake returned success with zero jobs;
  it is not a fresh-compilation claim.
- `DECLARATION_INSPECTION_PASS` means the actual `#check`, `#print`, and
  `#print axioms` inspection commands succeeded.
- `PROVED_KERNEL` may be assigned only when its documented gates actually pass.
- LLM prose can never upgrade formal verification status.

## Required pipeline shape

```text
INBOX request
    -> validate and hash
    -> toolchain receipt
    -> negative controls
    -> actual Lean project/declaration inspection
    -> structured formal evidence
    -> explanation pass
    -> schema validation
    -> JSON + Markdown OUTBOX
```

Canonical Lean sources are always read-only. Create inspection files and
assumption-removal experiments only in temporary work directories. Hash sources
before and after every job and fail visibly if anything changed.

## Explanation rules

The explanation layer must receive formal evidence, not replace it. It must keep
these fields separate:

- `mathematical_meaning`
- `plain_language`
- `limitations`
- `philosophical_interpretation_nonformal`
- `theological_interpretation_nonformal`
- `interpretation_confidence`
- `human_review`

If no model is configured, formal inspection must still work. Mark explanation
`NOT_RUN`; never fabricate one. Any model response must be schema-validated and
stored with provider/model identity and prompt hash. Prefer the repository's
existing gateway rather than adding another provider client.

## Negative controls required before the first positive sample

- false proposition;
- missing hypothesis;
- unknown declaration;
- invalid project root;
- source path escaping the approved root;
- malformed request;
- unavailable toolchain;
- cached zero-job build classification;
- failed or malformed explanation response;
- source-hash change detection.

## Governance

- The system may inspect, verify, explain, and recommend.
- It may not edit canonical Lean sources, delete originals, canonize an
  interpretation, hide disagreement, or compute what a person must believe.
- A meaningful yes requires a permitted no: objections and failed checks remain
  visible.
- Apply the Garden Test: use the fewest transparent controls necessary and
  provide a review and repair path.
- David retains final authority over canon and consequential file actions.

## Local prototype evidence to preserve conceptually

A separate local prototype already demonstrated one declaration:

```text
declaration: T1Kernel.reference_not_error
formal status: DECLARATION_INSPECTION_PASS
negative controls: PASS
source unchanged: true
#print axioms: 'T1Kernel.reference_not_error' does not depend on any axioms
canon status: HUMAN_REVIEW_REQUIRED
```

Do not treat that statement as a substitute for running your own fixtures in
the cloud. The real canonical corpus is machine-local and may not be available
to Codex online. Build portable fixture projects so CI proves the classification
logic; document that local-corpus acceptance must run on David's machine.

## Completion gate

Do not mark the assignment complete until the branch contains:

- implemented FastAPI endpoints and folder runner;
- documented configuration with no machine-specific secrets;
- JSON Schema and Markdown template;
- portable known-good and intentionally broken Lean fixtures;
- automated tests for the status boundaries and negative controls;
- a sample JSON and Markdown report produced from the fixtures;
- commands to run locally on Windows;
- an explicit list of what still requires David's local Lean corpus;
- no generated caches, credentials, large receipts, or canonical Lean sources.

## Intended endpoints

```text
GET  /health
GET  /governance
POST /jobs/inventory
POST /jobs/verify
POST /jobs/explain
POST /jobs/run-all
GET  /jobs/{run_id}
```

The folder runner and HTTP API must call the same core functions. Do not create
two verification implementations.

