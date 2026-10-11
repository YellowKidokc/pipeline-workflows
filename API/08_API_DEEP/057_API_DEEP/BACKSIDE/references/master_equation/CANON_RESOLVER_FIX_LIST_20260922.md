# FIX LIST — Master Equation Corpus + Lean Tree
**Date: 2026-09-22 | Compiled by: Claude (Fable) | Register: CANON working note — private, not for publication**
**Scope actually read: 04_MASTER_EQUATION (full), Pass 06 zip (394 files), LEAN4 pipeline folder, LEAN_FLOOR, Desktop 2\LEAN 4 top level + _CANON_SORTED_2026-09-17 + AXIOM_OUTPUT registry. Blast radius capped at what was verified.**

---

## The one rule that fixes most of this

Your resolver already exists: `04_MASTER_EQUATION\...\90_SOURCE_MAP\SELECTED_CURRENT_SOURCES\THE_MASTER_EQUATION_CANONICAL_DOCUMENT.md` (Aug 9, ballot-ratified, ruled eponym dictionary in §2). It says "One ruling, propagated once, to all locations." The ruling was never propagated. Almost every item below is that one sentence not being executed. The resolver is a downstream leaf; the drifted documents are the front doors. Invert that.

---

## FIXES — ordered by blast radius

### 1. STRUCTURAL (only if strip/canon runs before the fix): Pass 06 verdict layer uses pre-ruling law names
- **What:** Verdict Ledger + LAW_02 packets say "Motion ↔ Meaning/Repentance"; LAW_09 says "Weak Force ↔ Sin/Decay"; the whole layer was adjudicated from source material predating the Aug 9 ratification.
- **Where the answer lives:** Canonical doc §2 ruled dictionary — Law 2 = Newton–Momentum, Sin Nature ↔ Repentance ("Einstein–Meaning is drifted," stated at §356); Law 9 = Fermi–Conservation, Moral Conservation, grade LOCKED.
- **Why it matters:** Pass 06's own README says next stage is strip/canon. If strip runs on these names, the drift gets baked into canon. Fixed before strip = a rename sweep. Fixed after = re-adjudication.
- **Fix:** One relabeling pass over `04_TEN_LAWS\INTEGRATED_LAW_PACKETS\` and `06_TWO_CANON_TESTS\ADJUDICATED\TEN_LAWS\` and the Verdict Ledger, names and grades from the ruled table. The packets are 600-byte stubs — nothing downstream cites them yet, which is why this is cheap now.

### 2. LOCAL: 020_LAW_EXPANSIONS\00_INDEX.md is written in the pre-ruling ordering wholesale
- **What:** Law 02 = Mass–Energy/Meaning, Law 09 = Sin, and the "Veto Property" equation uses the retired ten-letter integral product form. It also links files that don't exist (`LAW_03_ELECTROMAGNETISM_TRUTH_EXPANSION.md`, `LAW_07_QUANTUM_FAITH_EXPANSION.md`) — and there is **no Law 07 expansion file at all** in that folder.
- **Where the answer lives:** Same §2 dictionary; canonical χ form is χ(X) = C_W[∏ᵢXᵢ], nine factors, no iiint (canonical doc marks the integral ten-letter form RETIRED DRIFT at its own line 76).
- **Why:** This index is the front door of the workroom. Anyone entering inherits the drift before reaching the resolver.
- **Fix:** Rewrite the index table from the ruled dictionary; fix or remove dead links; write or explicitly stub LAW_07.

### 3. LOCAL: Law 10 verdict contradiction (resolution already exists, wasn't carried forward)
- **What:** Verdict Ledger: "OPEN — family chain not run." Canonical doc: DEFINITIONAL — C_W is a wrapper, not a factor; veto property machine-verified; there is no ninth-peer family chain to run.
- **Fix:** Ledger entry becomes: "Wrapper: DEFINITIONAL, verified. Correspondence-family expansion: not applicable." One sentence, already written in the canonical doc §2.

### 4. LOCAL→STRUCTURAL if it feeds a published count: Mathlib contamination in the categorized Lean corpus
- **What:** `LEAN4\INBOX\LEAN_EPISTEMOLOGY\01_CANONICAL_CATEGORIZED_CORPUS\01_FOUNDATIONAL_ONTOLOGY_AND_GOD_AXIOMS\` contains raw Mathlib library files (Hilbert90, RiemannZeta, TopologicalSpace, Finsupp, Etale, RefinedDiscrTree, EssSup...) filed as foundational God axioms. The Sept 19 reader-paper run was queuing papers on them.
- **Where the answer lives:** `AXIOM_OUTPUT\_support\registry.json` lists every contaminated entry by path; the LEAN4 READ_ME's own exclusion rule names the intent.
- **Why:** Inflates any file/declaration count derived from that corpus, and burns API money writing papers about library internals.
- **Fix:** Quarantine by filename match against Mathlib module structure before the next run. The 99_UNSORTED and 09_HARNESS_TESTS buckets in _CANON_SORTED (1,613 + 1,311 declarations — 71% of the total) likely carry the same contamination; the START_HERE already flags them UNCERTAIN-heavy.

### 5. LOCAL: The Lean number crosswalk (this is the confusion generator)
Seven numbers exist, all real, all measuring different things, no document states the mapping. Put this table (corrected as needed) in one place — the canonical doc §17 is the right home — and cite only from it:

| Number | What it counts | Source of truth | Date |
|---|---|---|---|
| 4,107 | declarations, all versions incl. duplicates, 290 files | _CANON_SORTED_2026-09-17\00_START_HERE.md | Sep 17 |
| 1,888 | declarations in canonical selections only | same | Sep 17 |
| 878 | inventory across ~20 files (26 SUBSTANTIVE, 26 FINITE_DECIDABLE) | canonical doc §17.8 | ~Aug |
| 814 | bridge-document snapshot of that inventory | canonical doc | Jul |
| ~250 | compiled, Std-only Unit 1, exit 0 | canonical doc build table | Jul 25 |
| 186 | Pass 06 "declarations tracked" | Pass06 STATS.json | Sep |
| ~208 | declarations in 01_ACTIVE_VERIFIED_PROJECT reader papers | AXIOM_OUTPUT registry.json | Sep 19 |

**Rule going forward:** the newest **primary evidence** wins (build logs, registries, hashes) — not the newest summary. Pass 06 is newer than the Aug 9 doc but compiled from older sources, which is how it reintroduced retired names.

### 6. LOCAL: Zero compilation on the newest sorted corpus
- **What:** _CANON_SORTED_2026-09-17's own verification receipt: "Lean compiler runs: 0; passing Lean receipts: 0. All files remain UNVERIFIED or GAPS." 14 GAPS files, 6 with active `sorry`.
- **Where the answer lives:** `00_EXCEPTIONS.md` lists them; `3_RUN_LEAN_CHECKS.bat` in the LEAN4 pipeline is the tool.
- **Fix:** Run the compile pass on the 208 canonical selections; close or explicitly retire the 6 active-sorry files. Until then the Sep 17 sort is a filing achievement, not a verification one — its own receipt says exactly this, so the fix is running the button, not rewriting anything.

### 7. LOCAL: native_decide caveat must travel with the AxiomJenga receipts
- **What:** The Sept 7 receipts (LEAN_FLOOR\03_VERIFIED_RECEIPTS) are real `#print axioms` output — the strongest evidence in the tree — but every AxiomJenga theorem depends on a `native_decide` axiom: proof ran through the compiled evaluator, so the compiler joins the trusted base.
- **Fix:** Whenever these are cited upstream, the citation carries "kernel + native_decide" not bare "machine-verified." Your own READ_ME already has the right posture ("compilation is AUDIT PENDING, not verified truth") — just don't let the caveat drop at the paper layer.

### 8. INERT: housekeeping
- `MASTER_EQUATION_DERIVATION_TREE_CANONICAL 1.md` is the **newer** file (adds three-layer Lagrangian readings), not a duplicate; it has a stray voice-to-text "Oh" at line 24. Keep " 1", fix the typo, retire the other or mark it superseded.
- The extracted `MASTER_EQUATION_MAXIMAL_REBUILD_PASS_01–06` folders on disk are empty shells; content is only in the zips. Extract or delete the shells so browsing doesn't show a skeleton.
- `030_SPIRITUAL_TERMS` has one card (Grace); its link to TERM_RESISTANCE_GATE points at a file that doesn't exist yet.
- `SPIRITUAL_TERMS_MATHEMATICAL_REGISTRY_CANONICAL.md` and its " 1" copy are byte-identical — safe to drop one.

---

## THE ISOMORPHISM QUESTION — straight answer, because you asked it straight

You said you're almost positive each law's physical and spiritual sides are isomorphic. Here's what your own records support, all three columns:

**WHAT HELD:** Trinity carries FORMAL_ISOMORPHISM_WITHIN_ENCODING — an actual verified structure-preserving map, within the encoded structures. Law 9 is LOCKED (irreversible + conserved ⟹ transfer not erasure — the sharpest single result). Law 5 is DERIVED. Law 4's Love→Peace→Joy ordering is a Tier-1 theorem from one stationary calculation. The correspondences are not decoration; several carry theorem-grade internal structure.

**WHAT'S NOT ESTABLISHED:** "All ten, isomorphic, verified" is not what the ledger says. Current grades: Laws 1, 4, 6, 8 = STRUCTURAL_CORRESPONDENCE_CANDIDATE; Law 2 = CANDIDATE; Law 3 = PARTIAL (your own source marks it weaker, under gauge rebuild); Law 7 = PARTIAL. And your STATUS_LIVE file says it in one line: the Lean proofs "are MACHINE room only; they do not close grace/will/Christ-wrapper bridges."

**THE DEFENSIBLE VERSION:** "The Ten Laws are built as physical↔spiritual structural correspondences; two are theorem-grade (5, 9), one family ordering is derived (Law 4 fruits), the Trinity map is a verified isomorphism within its encoding, and the remaining bridges are formalized candidates with explicit promotion criteria." That sentence you can back with receipts today. The stronger sentence needs the required-fields in each adjudicated packet actually closed (exact structures, forward map, preserved invariants, wrong-role controls, ablation, countermodel, receipt) — the template exists in every packet; the fields are empty.

**Blast radius of this correction: LOCAL.** The framework doesn't move — the *claim wording* does. The promotion path is already designed; it just hasn't been walked for eight of the ten.
