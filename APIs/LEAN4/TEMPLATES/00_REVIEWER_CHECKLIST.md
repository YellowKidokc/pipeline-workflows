# Lean 4 Reviewer Checklist — V2

Companion to `00_TEMPLATE_CONTRACT.md`. Sits under it; does not replace it.

## What this is for

A Lean-literate stranger opens the formal packet cold. They never talk to us. If the packet holds everything below, they rebuild the result and land on the same verification label we printed. If it doesn't, they land somewhere else, and the gap is ours.

Assume throughout that the theorem is true and the encoding is right. None of that is the reviewer's starting position. Their starting position is: *show me.*

The checklist runs in the order a reviewer actually works: find it, read it, rebuild it, try to break it, decide what it says, decide what it doesn't.

---

## Stage 1 — Find it (packet §01, §06)

| # | The reviewer needs | Where it lives | PASS when | Missing means |
|---|---|---|---|---|
| 1.1 | Permalink: repo, commit hash, file path, fully qualified declaration name | §01 source paths + SHA-256; §06 hashes | The named declaration exists at that commit at that path | DECLARED — NOT VERIFIED HERE. Nothing else can start. |
| 1.2 | Toolchain pin: `lean-toolchain` content and hash | §03 toolchain file content and hash | Reviewer's Lean version matches the pin exactly | CHECK BLOCKED — reason: toolchain unpinned or mismatched |
| 1.3 | Dependency lock: `lake-manifest.json` with Mathlib commit, and its hash | §03 dependency lock and hash | `lake update` is not needed; manifest resolves as recorded | CHECK BLOCKED — reason: dependency drift |
| 1.4 | Selection disposition: why this file and not its siblings | §01 selection disposition | SELECTED with reason; duplicates and supersedes named | Reviewer cannot tell if a stronger or weaker version exists elsewhere |

A template that prints a Lean version is not a pin. The pin is whatever the project actually has; the contract says so and the reviewer will check the file, not the packet prose.

---

## Stage 2 — Read it (packet §02)

| # | The reviewer needs | Where it lives | PASS when | Missing means |
|---|---|---|---|---|
| 2.1 | The `theorem` signature verbatim — every binder, every hypothesis, every section-level `variable` in scope | §02 fully qualified declaration + quoted statement | Signature in packet is byte-identical to source at the pinned commit | Reviewer reads the paper's sentence instead and grades that. Verdict diverges. |
| 2.2 | The exact proposed statement in prose, scoped to what the Lean says | §02 exact proposed statement | Prose quantifiers match Lean quantifiers (∀ vs one instance; ∃ vs ∃!) | Scope inflation. The most common way a true theorem becomes an overstated claim. |
| 2.3 | Symbol table: paper symbol → Lean identifier → Mathlib type → source correspondence | §02 symbol table | Every identifier in the signature has a row; every row points to a real Mathlib type or a defined structure | Reviewer assumes the gap hides a custom real or an axiomatized predicate (see 4.4) |
| 2.4 | Which definitions are ours and which are Mathlib's | §02 symbol table, formal definition column | Custom `def`/`structure` marked as such | Reviewer cannot run 4.3 (triviality) without knowing what is load-bearing |

---

## Stage 3 — Rebuild it (packet §04 rows 1–4)

| # | Control row | Command | PASS when | Result label consequence |
|---|---|---|---|---|
| 3.1 | Selected module compilation | `lake build <module>` from a clean clone | Exit 0, log saved, module named explicitly (ordinary `lake build` may skip it) | FAIL → CHECK FAILED. NOT_RUN → DECLARED — NOT VERIFIED HERE. |
| 3.2 | Declaration and premise inspection | `#check`, `#print <name>` | Output matches §02 signature | Mismatch → packet is describing a different declaration |
| 3.3 | Axiom dependency inspection | `#print axioms <name>` | Output is a subset of `propext`, `Classical.choice`, `Quot.sound` | `sorryAx` present → PLACEHOLDER-DEPENDENT. Any custom `axiom` → disclosed as custom dependency; label stays VERIFIED CONDITIONAL only if the axiom is listed in §03 as a stated premise. |
| 3.4 | Proof escape audit | grep for `sorry`, `admit`, `native_decide`, `unsafe`, `partial`, `implemented_by`, `opaque`, `set_option maxRecDepth`/`maxHeartbeats` spikes | None present in the dependency closure, or each occurrence explained | `native_decide` is compiler-trusted, not kernel-checked; a strict reviewer downgrades. Record it, don't hide it. |

3.3 is the single decisive check. Everything before it is finding the thing; everything after it is asking what the thing means.

---

## Stage 4 — Try to break it (packet §04 rows 5–9)

These are the checks most formalizers skip and the ones a good reviewer runs first. A passed build is not a completed audit.

| # | Control row | What the reviewer does | Predeclared expected outcome | PASS when |
|---|---|---|---|---|
| 4.1 | Non-vacuity witness | Constructs `example : <Structure> := ...` satisfying all hypotheses | The instance exists and type-checks | Hypotheses are jointly satisfiable. FAIL → theorem is vacuously true; label cannot exceed PLACEHOLDER-DEPENDENT in spirit even if `#print axioms` is clean. |
| 4.2 | Negative control | Swaps in an absurd definition — `chi := fun _ => 0`, or drops the key hypothesis — and rebuilds | Build **fails** | Build fails as predicted. If the theorem still compiles, it is not constraining what we think it constrains. PASS is the predicted failure, not a clean exit. |
| 4.3 | Definitional triviality | Reads each custom definition against the conclusion | Conclusion is not a restatement of a definition or a hypothesis | Reviewer can name at least one step of real deduction between premises and conclusion |
| 4.4 | Lean semantics traps | Checks for `ℕ` truncated subtraction, `x / 0 = 0` on `ℝ`, `Real.sqrt` of negatives = 0, `Finset` vs `Set` cardinality, coercion ambiguities | None of these carry the result | Each trap either absent or explicitly shown not to be load-bearing |
| 4.5 | Converse / countermodel | Attempts the converse; searches for a model of the premises where the conclusion fails | Converse fails or is separately proved; no countermodel found | Recorded with reason if NOT_APPLICABLE |
| 4.6 | Ablation / role permutation | Removes one premise at a time; permutes roles of symmetric terms | Proof fails without each load-bearing premise; permutation changes the result where the claim says it should | Every premise listed in §03 is shown to be used |
| 4.7 | Independent encoding | A second formalization from the prose alone, by a different hand or model, not reading the first | Same theorem provable; or divergence recorded | NOT_RUN is acceptable and must say so |
| 4.8 | Independence of derivation routes *(added for multi-route claims such as A042/L9/C1)* | Traces both proofs' lemma dependency trees | The two routes share no lemma that already contains the conclusion | Two theorem names calling one `conservation_lemma` is one derivation, not two |

---

## Stage 5 — Decide what it says (packet §05)

| # | Field | Rule |
|---|---|---|
| 5.1 | Verification status | Derived from Stages 3–4, never typed by hand: see the derivation table below |
| 5.2 | What is established under the premises | One sentence. Names the premises. Stops. |
| 5.3 | What remains open | Every NOT_RUN and NOT_APPLICABLE control, with reason. Every interpretive step the Lean does not touch. |
| 5.4 | Encoding-fidelity review | Does the Lean statement say what the paper sentence says? This is a human judgment, recorded as such, separate from 5.1. |

### Label derivation

| Compilation | `#print axioms` | Escape audit | Non-vacuity | Label |
|---|---|---|---|---|
| NOT_RUN | — | — | — | DECLARED — NOT VERIFIED HERE |
| attempted, could not complete (toolchain, deps, environment) | — | — | — | CHECK BLOCKED — reason |
| FAIL | — | — | — | CHECK FAILED |
| PASS | contains `sorryAx` | — | — | PLACEHOLDER-DEPENDENT |
| PASS | clean | FAIL | — | PLACEHOLDER-DEPENDENT (trust boundary named) |
| PASS | clean | PASS | FAIL | CHECK FAILED — vacuous (state it as such; the theorem may be true and still say nothing) |
| PASS | clean | PASS | PASS or NOT_RUN | VERIFIED CONDITIONAL — with negative control and ablation status appended |

VERIFIED CONDITIONAL with negative control NOT_RUN is an honest state. It is not the same state as VERIFIED CONDITIONAL with negative control PASS, and the packet must show which one it is.

### Cross-walk to the atom canon receipt classes

The claim-atom canon uses a different ladder. Both are in use; map, don't merge.

| Lean Floor V2 label | Atom canon receipt class |
|---|---|
| DECLARED — NOT VERIFIED HERE | SPECIFICATION_ONLY |
| CHECK BLOCKED | (no class — record as blocked) |
| CHECK FAILED | (no class — record as failed; not a refutation) |
| PLACEHOLDER-DEPENDENT | PARTIAL_WITH_SORRY |
| VERIFIED CONDITIONAL | BUILT_ZERO_SORRY |
| not in packet | NOT_ATTEMPTED |

A claim atom marked `verificationStatus: machine-verified, kernelChecked: true` is asserting VERIFIED CONDITIONAL. The reviewer will ask for the §06 receipt that backs it. If the receipt is not there, the atom's status is a claim, not a record.

---

## Stage 6 — Decide what it doesn't say (packet §05, companion §07 and §09)

The reviewer reaches our verdict only if our verdict stops where the proof stops.

| Lean establishes | Lean does not establish |
|---|---|
| The conclusion follows from the encoded premises in the pinned toolchain | That the premises hold in the world |
| The encoded structure is consistent enough to inhabit (4.1) | That the encoded structure is the physical or moral system named in the paper |
| The definitions are non-trivial with respect to the conclusion (4.3) | That the definitions are the right ones |
| Two routes are independent (4.8) | That either route describes reality |
| — | Any bridge grade. A bridge is graded in the bridge lane, never inherited from a proof receipt. |
| — | Any theological identification. Identification is warranted by Scripture, doctrine, argument — the companion §07 says which — never by `lake build`. |

If the paper's verdict line claims anything in the right column on the strength of the Lean, the reviewer's verdict and ours diverge at that line, and they are right.

---

## Stage 7 — Receipt (packet §06)

| # | Field | Must contain |
|---|---|---|
| 7.1 | Run ID and timestamp | Stable ID; ISO timestamp |
| 7.2 | Hashes | Source file, module, harness, toolchain file, manifest — all SHA-256 |
| 7.3 | Commands | Exact, with working directory, in the order run |
| 7.4 | Exit codes and logs | Every command; log paths that exist |
| 7.5 | Declarations actually checked | By name. Build success on the project is not a check on the declaration. |
| 7.6 | Prior receipt | Link and diff. Never overwrite. |
| 7.7 | Technical reviewer | Name or Pending. Model/provider if AI-assisted, and what it did. |

---

## The one-line test

Hand the packet to someone who has never heard of the framework and knows Lean. If they can, from the packet alone and without asking a question, (a) find the declaration, (b) rebuild it, (c) run the negative control, and (d) write the same label we wrote — the packet is complete. Anything they'd have to ask us is a hole.

---

## Fill-in stub (copy into a new packet)

```
STAGE 1  find      1.1 [ ]  1.2 [ ]  1.3 [ ]  1.4 [ ]
STAGE 2  read      2.1 [ ]  2.2 [ ]  2.3 [ ]  2.4 [ ]
STAGE 3  rebuild   3.1 ____  3.2 ____  3.3 ____  3.4 ____      (PASS/FAIL/NOT_RUN/NOT_APPLICABLE + reason)
STAGE 4  break     4.1 ____  4.2 ____  4.3 ____  4.4 ____  4.5 ____  4.6 ____  4.7 ____  4.8 ____
STAGE 5  label     derived: ______________________  encoding fidelity: ______________
STAGE 6  boundary  claimed on the strength of Lean: ______________  not claimed: ______________
STAGE 7  receipt   run ID ______  reviewer ______  prior ______
STAGE 8  QEC map   8.1 ____  8.2 ____  8.3 ____  8.4 ____      (PASS/NOT_APPLICABLE/NOT_CHECKED + step ID)
```

---

## Stage 8 — QEC Protocol Mapping (packet §07)

The master isomorphism maps the seven steps of fault-tolerant quantum error correction onto the biblical redemption arc. Each reviewed source may touch one or more of these steps. This stage asks whether the source's claims land on a specific protocol step and whether the mapping preserves structural relationships.

| QEC Step | Protocol operation | Redemption counterpart | Structural requirement |
|---|---|---|---|
| 1. Encoding | Distribute logical qubit across entangled ensemble | Image of God encoded relationally across creation (Four Debts: existence, distinction, relation, orientation) | Information stored in correlations, not single nodes |
| 2. Error basis | Errors decompose into finite elementary types (bit-flip, phase-flip) | The Fall decomposes into classifiable structural corruptions; every downstream sin is a combination of elementary error types | Error space has a finite basis |
| 3. Syndrome measurement | Measure the error without collapsing the encoded data | The Law diagnoses sin without destroying the image of God; identifies error type and location without constituting the cure | Diagnosis without data destruction |
| 4. Recovery operation | Apply targeted correction matched to each diagnosed error type | The Cross: seven specific counter-moves matched to seven specific corruptions at the same structural level | Wrong correction on wrong error makes things worse; correction must match |
| 5. Clean ancilla | Uncorrupted auxiliary system coupled to corrupted data but not sharing its error channel | Christ: fully human (coupled), without sin (uncorrupted); absorbs error information so data qubits can be restored | Corrupted ancilla propagates errors instead of correcting them (Knill-Laflamme 1997) |
| 6. Fault tolerance | Continuous correction cycle; correction rate must exceed error rate (threshold theorem) | Pentecost: Spirit as persistent internal error-correction code; surrender parameter determines whether correction exceeds error rate | Below threshold = coherence increases; above threshold = collapse |
| 7. Logical qubit survival | Logical information survives physical qubit destruction | Resurrection: information (image of God) survives bodily death; re-encoded in incorruptible carriers | Physical carriers fail; logical content preserved through the protocol |

### Reviewer questions for each source

| # | Question | PASS when | Missing means |
|---|---|---|---|
| 8.1 | Does this source's central claim map onto a specific QEC step? | Step identified with justification; or NOT_APPLICABLE with reason | Mapping not attempted for this source |
| 8.2 | Does the mapping preserve the structural relationships required by the protocol? | The protocol constraint for that step is satisfied by the theological counterpart | Structural correspondence claimed but not demonstrated |
| 8.3 | Does the source's claim require anything the protocol does not predict, or omit anything the protocol requires? | No unexplained additions or omissions; or divergence explicitly noted | Gap between protocol prediction and theological claim not examined |
| 8.4 | Is the source's claim consistent with the claims mapped to adjacent protocol steps in other sources? | No contradiction with adjacent-step sources reviewed in the same batch | Cross-source consistency not checked (acceptable for single-source review) |

### Kill condition for the master isomorphism

The isomorphism fails if any step in the QEC protocol has no corresponding step in the redemption arc, or if any step in the redemption arc has no corresponding step in the protocol. A single broken mapping downgrades the claim from structural isomorphism to partial analogy.

### What this stage does NOT establish

This stage tests structural correspondence. It does not establish that the theological identifications (G = grace, O = openness, S = entropy, ancilla = Christ) are the correct interpretations of the formal variables. Those identifications are tested by empirical predictions (Cochrane 2020, PEAR Lab, decoherence curve fit) and by theological argument, not by the structural mapping alone.

*POF 2828 · Lean Floor V2 · a passed build is not a completed audit · a failed check is not a refutation*
