# Complete Grading Bundle: Codex Prompt Sequence

Use these prompts in order. Each prompt is a separate, reviewable change. Do not
start the next prompt until the current prompt's acceptance criteria pass.

## Invariants for every prompt

Repeat these boundaries in the implementation notes and enforce them in tests:

1. Old engine code is reference material, not authority.
2. JSON is canonical; Markdown, HTML, and Excel are projections.
3. Metrics describe text; they do not establish truth.
4. A completed grade requires six valid station results: Atoms, Axiom Nodes,
   Master Equation, Fruits of the Spirit, Coherence, and Coherence Score.

Never commit credentials, paper contents, generated private reports, or files
from the read-only legacy engine. Use environment variables for secrets and
redacted fixtures for tests.

## Prompt 1 — Inventory and architecture

```text
Work only on architecture and inventory. Do not implement or migrate runtime
code yet.

Inspect this repository and the mounted Z: engine read-only. Record the exact
paths inspected and identify unavailable paths explicitly. Produce a component
map with one classification per item:

- Keep
- Adapt
- Replace
- Archive/reference only
- Unsafe because of credentials
- Unverified
- Duplicate

For every item record its path, purpose, classification, rationale,
dependencies, credential risk, and proposed destination. Treat old engine code
as reference material, not authority. Do not copy secrets or private source
documents. Identify duplicated station names and competing schemas.

Document the proposed dependency DAG and lifecycle folders. The intended flow
is PAPER_METRICS -> ATOMS -> six-station completion barrier -> PAPER_GRADER /
SYNTHESIS, with Axiom Nodes, Master Equation, Fruits, Coherence, and Coherence
Score parallelized after Atoms unless an evidenced dependency requires a
different edge. Declare every edge; do not rely on execution order.

Deliverables:
1. A machine-readable inventory (JSON or CSV).
2. An architecture decision document.
3. A credential-risk report containing paths and remediation, never values.
4. A proposed migration sequence with explicit unknowns.

Acceptance criteria:
- No production implementation is changed.
- The Z: engine was only read, or is marked unavailable/unverified.
- Every discovered component has exactly one classification.
- Duplicate and credential-risk findings are actionable.
- The DAG names inputs, outputs, and completion conditions.
```

## Prompt 2 — Shared runtime and schemas

```text
Build the shared foundation used by every grading station. Do not implement
station-specific analysis.

Define paper_id, run_id, and a source hash derived from immutable source bytes.
Implement a provider interface and a DeepSeek client whose credentials come
only from environment variables. Ensure logs and exceptions cannot expose
credentials. Add versioned JSON Schemas, lifecycle folders, atomic claiming,
parallel-safe workers, bounded retry/backoff, append-only state history, a
canonical JSON merger, and a six-result completion barrier.

Make dependencies explicit in a machine-readable DAG. Claims must use an
atomic filesystem primitive and must prevent two workers from owning the same
paper/station attempt. A retry must preserve attempt history and reuse valid
completed station results. The merger must reject identity/hash mismatches and
must not mark a bundle complete unless all six station documents validate.

JSON is canonical; other formats are projections. Metrics do not establish
truth. Old engine code is reference material, not authority.

Tests must cover stable IDs, hash changes, schema rejection, crash recovery,
claim contention, independent retry, idempotent rerun, redacted provider
errors, merge conflicts, and an incomplete five-of-six bundle.

Acceptance criteria:
- Every station can use one runtime contract without local alternatives.
- No API key appears in repository files, logs, receipts, or exceptions.
- Atomic-claim contention has a deterministic automated test.
- State transitions and retry attempts are auditable.
- Completion is impossible with fewer than six valid results.
```

## Prompt 3 — Paper Metrics

```text
Implement PAPER_METRICS as a deterministic, local-only preflight. It must make
zero API calls and must use only the shared runtime and schemas.

From useful backend references, adapt structural counts, readability,
vocabulary, and argument-language measurements. Version every metric definition
and document its formula, tokenizer assumptions, limitations, and null/error
behavior. Produce canonical metrics JSON plus projections: an Excel comparison
matrix and HTML graphs. Do not interpret any metric as proof that a claim is
true, false, coherent, or valuable.

The JSON must include paper_id, run_id, source hash, schema version, metric
definition version, tool version, measurements, warnings, and evidence locators.
Projections must be regenerated exclusively from validated canonical JSON.

Tests must use small redacted fixtures and golden JSON. Prove determinism,
offline operation, source immutability, empty/malformed input handling, version
reporting, and agreement among JSON, Excel, and HTML.

Acceptance criteria:
- A network-denied test run passes.
- Repeated runs produce equivalent canonical measurements.
- Every value identifies its versioned definition.
- Projections contain no facts absent from canonical JSON.
- Documentation states that metrics do not establish truth.
```

## Prompt 4 — Atoms

```text
Implement only the Atoms station on the shared runtime. Its permitted inputs
are the immutable source, validated PAPER_METRICS, and documented shared
contracts. Old engine output may be used as test/reference material, not as
authority.

Before coding, add a station specification containing: permitted references,
required analytical questions, exact versioned JSON Schema, evidence
requirements, prohibited inferences, tests, a complete example output, and
acceptance criteria. Each extracted atom must have a stable local ID, a type,
the minimally sufficient source excerpt or redacted test equivalent, and an
exact locator. Distinguish explicit statements from station inference and give
inferences a confidence and rationale. Do not infer author intent, truth, or
logical validity from wording or metrics.

Use the provider interface; do not call DeepSeek directly. Validate provider
output before publishing it. Failed validation must enter retry/review state,
not OUTBOX.

Acceptance criteria:
- Schema, prompt, example, implementation, and tests agree.
- Every atom resolves to exact evidence.
- Unsupported and prohibited inferences are rejected or flagged.
- Rerunning does not duplicate a valid result.
- JSON is the canonical station result.
```

## Prompt 5 — Axiom Nodes

```text
Implement only the Axiom Nodes station on the shared runtime. Require validated
Atoms and the immutable source; declare any additional dependency in the DAG.

First write the station specification: permitted references, required
questions, exact JSON Schema, evidence rules, prohibited inferences, tests,
example output, and acceptance criteria. Identify candidate axioms/premises and
their relationships without asserting that they are true, universal, or
endorsed by the author. Each node and edge must cite atom IDs and exact source
evidence. Separate explicit premises, reconstructed premises, definitions, and
assumptions. Record ambiguity and competing reconstructions.

Use only the provider interface. Validate output before completion and preserve
raw provider receipts according to the shared redaction policy.

Acceptance criteria:
- No orphan node or edge exists.
- Explicit and reconstructed content cannot be confused in JSON.
- Every conclusion has a traceable evidence path.
- Invalid output retries independently without invalidating other stations.
- Metrics are never used as evidence of truth.
```

## Prompt 6 — Master Equation and covariance

```text
Implement only the Master Equation station, including covariance analysis, on
the shared runtime. Consume validated Atoms and any explicitly declared station
dependencies; do not silently read another station's files.

Write the complete station specification before implementation. Model the
paper's proposed variables, relationships, constraints, and covariance claims.
Distinguish equations quoted from the source, normalized equations, and station
reconstructions. Preserve symbols and define every normalization. For each
covariance claim state the variables, direction, scope, evidence locator,
whether it is textual or computed, and the method/assumptions. Never manufacture
numeric covariance from prose or use correlation as causation.

Provide an exact JSON Schema, evidence rules, prohibited inferences, tests, and
an example containing both an equation and an explicitly unavailable covariance
result. Use the provider abstraction and canonical merger contract.

Acceptance criteria:
- Every symbol and relationship traces to evidence or is labeled reconstruction.
- Missing data yields null/not-computable, never invented numbers.
- Dimensional/structural checks produce warnings rather than truth claims.
- JSON validates and retries independently.
```

## Prompt 7 — Fruits of the Spirit

```text
Implement or adapt only the Fruits of the Spirit station to the shared runtime.
Audit the existing Fruits implementation first; retain behavior only where it
matches the new contracts. Old engine code is reference material, not authority.

Write the station specification with permitted scriptural/framework references,
required questions, exact JSON Schema, evidence requirements, prohibited
inferences, tests, example output, and acceptance criteria. Declare the rubric
version. Keep textual evidence from the paper distinct from rubric references
and station judgment. Do not infer an author's character, faith, motive, or
spiritual state. Score only the defined textual dimensions and expose uncertainty.

Use the shared provider, IDs, hashing, lifecycle, validation, retry, receipts,
and state history. Remove or isolate station-local substitutes.

Acceptance criteria:
- Rubric and schema versions are recorded.
- Every assessment cites exact paper evidence and the applicable rubric item.
- Prohibited personal/spiritual inferences are absent.
- Existing behavior has regression tests where intentionally retained.
- No result is complete merely because this station succeeds.
```

## Prompt 8 — Coherence and Coherence Score

```text
Implement Coherence and Coherence Score as two separately validated station
results. They may share code but may not share completion status. Declare
whether Coherence Score depends on Coherence; encode that edge in the DAG.

Create a full specification for each result: permitted references, required
questions, exact schema, evidence rules, prohibited inferences, tests, example,
and acceptance criteria. Coherence identifies supported/unsupported transitions,
contradictions, unresolved terms, and structural continuity. Coherence Score
applies a versioned rubric to those findings. It must not use readability,
vocabulary, style, agreement with the evaluator, or factual truth as a proxy for
coherence. Every score component must trace to findings and evidence.

Use shared provider and lifecycle contracts. A valid Coherence result must be
reusable when Coherence Score alone fails and retries.

Acceptance criteria:
- The two JSON documents validate independently.
- Score arithmetic is deterministic and tested at boundaries.
- Findings point to exact evidence; scores point to finding IDs.
- One station can retry without duplicating or erasing the other.
- The bundle barrier counts both results separately.
```

## Prompt 9 — Integration, projections, and end-to-end verification

```text
Integrate the completed stations and prove the workflow with one paper, BGL-01,
before enabling batch execution. Do not weaken individual station validation.

Execute PAPER_METRICS, then ATOMS, then the explicitly declared parallel DAG,
then the six-result completion barrier, then PAPER_GRADER/SYNTHESIS. Build
canonical.json first. Generate Markdown, HTML, and Excel only from that validated
canonical JSON. Disclose DeepSeek/model usage, provider/model identifiers,
attempts, timestamps, and non-provider/local stages without exposing secrets.

For the BGL-01 pilot, automatically prove:
- original bytes and source hash are unchanged;
- metrics JSON and all six station JSON files validate;
- five-of-six or any invalid result cannot complete the bundle;
- canonical JSON, Markdown, HTML, and Excel agree;
- every conclusion resolves to exact evidence;
- DeepSeek usage is disclosed;
- rerunning creates no duplicate work;
- a failed station retries independently.

Only after that pilot passes, enable four or five configurable workers. Discover
inputs recursively in strict lane order: Priority, Series, General. Never process
Hold. Prove no duplicate claiming under contention, resume from valid station
results, and apply shared rate limiting and bounded retry.

Acceptance criteria:
- The pilot produces a verification report for every assertion above.
- Failed/incomplete bundles never appear in PROCESSED or as completed output.
- Batch mode cannot be enabled unless the pilot gate passes.
- Worker count, rate limits, and retry policy are configuration, not constants.
- JSON remains canonical; projections are reproducible and consistent.
```

## Review gates

At the end of each prompt, require Codex to report:

- files changed and why;
- schemas added or changed;
- tests run with exact commands and results;
- unresolved risks and assumptions;
- whether any legacy code or external drive was unavailable;
- a statement confirming each of the four invariants.

Stop rather than guessing when required source material, rubric definitions, or
the BGL-01 fixture is unavailable. Mark it `Unverified` and identify the smallest
specific input needed to proceed.
