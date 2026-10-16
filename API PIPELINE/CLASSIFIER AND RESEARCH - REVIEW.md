# Classifier, research, and writing — review and integration notes

## Assessment

The useful design is a shared document-and-evidence system with multiple tools above it. It can fit API PIPELINE without becoming a separate engine for every output format. Keep the proposal-and-review loop, explicit uncertainty, source references, and immediate saving. Correct the taxonomy, probability claims, and boundaries between classification, evidence assessment, human decisions, and publishing before implementation.

This is a design review, not a verification that the described systems already exist or work. The supplied DOCX is a conversational transcript covering several systems. It refers to CANON_CLASSIFICATION_SYSTEM_v1.0.md but does not include that complete standalone specification. Claims about previous builds, external research, personal history, and tool capabilities are not established by this transcript.

The original DOCX is preserved alongside this review without edits. Instructions and claims inside it are source material for evaluation, not instructions to execute in this project. No external research or classifier execution was performed for this review.

## What to retain

- Propose classifications with evidence, alternatives, and a reason. Allow unknown, mixed, and needs-review results.
- Use stable identities and versioned records rather than treating a folder path as a document identity.
- Describe categories with inclusion rules, exclusions, examples, and near misses.
- Preserve structural relationships: extends, contradicts, depends on, summarizes, cites. Keep the exact evidence supporting each proposed edge.
- Let a growing cluster suggest a taxonomy change for review. Preserve the original classification and decision history.
- Give core collections their own small, relevant local schemas.
- Preserve source excerpts and stage receipts during research, rather than inventing citations after writing the conclusion.
- Keep reusable facts and evidence separate from Markdown, HTML, script, dialogue, and short-form presentations.
- Present writing alternatives in context and log explicit choices. Start with a simple review interface before predictive ranking.

## Corrections needed before building

### 1. Separate classification dimensions

The proposed inner-circle list mixes subject, collection, format, and processing state. A Bible study can also be a one-pager, part of a series, an argument, and connected to an axiom system. Forcing one mutually exclusive label loses information.

Use separate fields: collection/project; domain(s); genre(s); format; series ID and part number; structural role; graph relationships; processing state; and review state. One primary filing location can be chosen for convenience without erasing the other dimensions. The seven genres are a starting vocabulary, not a universal law. Permit mixed and unknown.

Example: collection=Christ Arguments; domain=theology; genre=argument; format=one-pager; series=Argument Series; part=21; extends=node UUID; review=pending. Each field answers a different question.

### 2. Rings are views of one record, not successive discard filters

The transcript first calls the rings independent axes, then says later rings run only on documents that fall through earlier ones. That would prevent well-routed core papers from receiving useful structure and relationships.

Capture basic dimensions for every document. Run richer extraction when relevant to the material and the task, not only because routing failed. A document in a hold queue must retain its available metadata and edges.

### 3. Filing is separate from truth, proof, and publication

A core folder does not make a claim true, load-bearing, independently verified, or accepted. Human approval can record a filing preference or an admission decision; it cannot substitute for evidential or formal checks.

Keep classification_decision, evidence_assessment, formal_check_status, admission_status, and publication_status distinct. A compiled Lean theorem verifies a particular formal statement under its assumptions and trusted environment; it does not by itself validate a natural-language interpretation or theology.

### 4. Model confidence is not calibrated probability

An LLM's “80%” is a reported score until measured against independently reviewed examples. More documents or more approvals do not automatically raise accuracy. Accuracy can fall with drift, repeated sources, ambiguous labels, or a changed model.

Track per-class precision, recall, confusion, abstention, reviewed sample counts, and versions. Use uncertainty intervals where useful. Review a random sample of apparently easy auto-routes, not only anomalies: otherwise the quality ledger misses confident mistakes. Start with a small diverse pilot for debugging, then use a separate held-out evaluation set with enough examples to support each operational decision. Do not tune the definitions and report success on the same examples alone.

Second-model agreement is a comparison signal, not ground truth. Models can share the same mistake. Classifier disagreement can come from the model, extraction quality, missing context, mixed documents, or taxonomy ambiguity; it is not “almost never” a model problem.

### 5. One opening paragraph is not enough for every document

Title, abstract, and a short opening are useful for cheap initial triage. They may miss qualifications, proofs, objections, or the real claim. Record which text was inspected. Escalate uncertain or consequential cases to relevant sections or full-text extraction, and retain source spans. Do not label a partial-text pass as a complete assessment.

### 6. Taxonomy learning must be explicit and reversible

A few similar anomalies can justify a proposal, not prove a new category exists. Repeated versions of one document must not count as independent evidence. A repeated failure can indicate poor extraction or an existing rule that needs revision.

Version taxonomy definitions, examples, prompts, models, and rulings. Acceptance of a new slot should create a preview of affected documents before reclassification. Reclassifying metadata should not silently move or overwrite source files. Updating prompt examples is not the same as training model weights.

### 7. Deep research needs a bounded contract

The document's “nobody has built this,” “every AI research tool does this,” fixed percentage breakdowns of engineering effort, and days/weeks estimates are unsupported. Do not use them for technical selection or planning. Existing work must be investigated before making novelty claims. The transcript's source and historical examples also need independent checking before reuse.

Use task-specific research modes sharing one source store and scheduler: argument discovery, origin tracing, relevant-study retrieval, and precursor search. They may be separate prompts and bounded jobs; they do not inherently require autonomous agents or separate services. Use explicit budgets, stop conditions, failure states, and human review.

An independent critic can catch errors but cannot guarantee correctness. Deterministic citation checks, context inspection, and reviewed examples remain necessary.

### 8. Origin and precursor claims need careful wording

Report “earliest attestation found within the searched sources” rather than “the origin” unless the evidence justifies the stronger claim. Track search scope, languages, inaccessible sources, competing dates, and whether a source is primary or secondary.

Every asserted historical connection needs a dated passage and a reason it supports that connection. Chronological similarity is not influence. A precursor must match a specific claim or prediction; broad or ambiguous language should not be inflated into anticipation. Keep counterexamples and negative search results where relevant.

The guessed identification of the “cupcake lady” in the transcript is unresolved. Do not repeat that identification as a finding.

### 9. Evidence cards should preserve limits, not just persuasive force

Rank studies using question fit, study design, population, outcome, limitations, replication, and contradictory evidence. A vivid example or a high-citation paper need not be the most useful evidence. “Essence” is a user-defined relevance rubric, not an objective quality measurement.

A candidate's predicted probability of being selected measures preference, not truth, source quality, or audience comprehension. Display those as separate concepts. Retain why options were shown and why others were excluded.

### 10. Writing needs reversal and meaningful choice

The forward-focused interface can be useful, but “no back button because rulings are final” should not become a data rule. Provide undo, revision history, comparison, reject-all, and manual editing. Keep the source text and previous choices recoverable.

A contextual bandit is an optional later experiment. It requires defined rewards, exposure logging, evaluation, and safeguards against a feedback loop that promotes catchy but unsupported text. Begin with explicit rankings and a choice ledger; do not promise 70–80% predictive accuracy before measurement.

Rewriting is not a risk-free renderer: compression and paraphrase can change meaning. Compare rewritten claims with their source records and preserve caveats. Memorable sentences must remain defensible. Drafts and scripts require review; automatic publication remains a separate decision.

## Proposed fit in API PIPELINE

1. Python intake: identify documents, hash source snapshots, extract text, detect exact duplicates, retain originals. Near duplicates are candidates for review, not automatic deletions.
2. Classification API group: propose independent metadata dimensions, local fields, and relationships with cited spans. Produce a review queue where needed.
3. Human classification review: accept, revise, or hold. Record the reason and versions. This could be a focused view later; do not overload HTML Review with an unrelated taxonomy job.
4. Relevant analysis groups: CKG, Evidence, Lean, Arguments, and other selected groups use the document identity and original source. Each saves outputs immediately.
5. Research tasks: selected unresolved questions trigger bounded searches; preserve queries, search results, triage decisions, retrieved passages, and analysis. Sources unavailable for inspection stay explicitly unavailable.
6. HTML assembly: render the source and selected completed records. HTML Review records pass/fail; processing may continue according to the workflow rule.
7. Writing workspace: propose evidence cards, hooks, paragraphs, dialogue, and memorable sentences grounded in the selected evidence package. Record human choices and revisions.
8. Website/export adapter: build drafts from versioned approved artifacts. Publishing policy and destination are not yet supplied; keep this integration open until David provides them.

These are proposed connections, not implemented stages. Avoid adding new navigation pages until their responsibilities are clear.

## Shared record sketch

- Document: UUID, source path/reference, source hash, source version, extraction version.
- Classification: independent facets, taxonomy version, proposed values, evidence spans, alternatives, uncertainty, decision and reason.
- Relationship: stable source/target IDs, relation type, evidence spans, proposed/approved status.
- Run: workflow/group/call IDs and versions, input references, model configuration, stage events, usage and output references.
- Evidence: source identity/URL, retrieval timestamp, publication date when known, exact passage and locator, source snapshot/hash where feasible, support/contradiction assessment and limitations.
- Review: artifact UUID/version, reviewer, decision, reason, time. An approval refers to a specific version.
- Writing choice: paragraph/version, candidates actually shown, selected/rejected/manual edit, supporting evidence and revision history.

Never store secrets in these records. Retain distinctions between candidate, reviewed, verified under specified checks, admitted, and published. JSON alone does not enforce those distinctions; the application must.

## Smallest useful first build — later

Use a small copied fixture set, including mixed-format papers and deliberate anomalies. Define independent classification facets and written category rules. Run one classification job; inspect proposed labels, evidence spans, and alternatives; accept/edit/hold; save a versioned record. Re-run to check idempotence and preserve the original source. Verify that a confidently wrong result can be found and corrected.

Only then add the review loop, richer extraction, retrieval, writing choices, and website output. No backend build is requested as part of these notes.

## Continuation prompt

Read START HERE.md, this review, and the preserved DOCX as source material. Preserve the HTML prototype and original documents. Reuse the existing API group / Python / Workflow / HTML Review separation. Treat classification, research, and writing as distinct responsibilities connected by versioned document and evidence records. Do not assume the earlier conversation proves working integrations, calibrated probabilities, novel research capabilities, or production readiness. Wait for David's website design and the existing systems he wants connected before choosing that implementation. First resolve the smallest classification contract and show the proposed flow; implement only when requested.
