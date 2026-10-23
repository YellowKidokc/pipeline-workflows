You are building the theorem-to-claim reverse ledger of a Lean 4 source for David Lowe's Theophysics work.
The source is below, whole, with line numbers (L1, L2, ...). Its assumptions (ids A1 ...) and its claims
(ids C1 ...) have already been listed (CLAIMS AND ASSUMPTIONS).

Every theorem, lemma, def, instance, structure and inductive in the source gets one ledger entry. The ledger
answers, for each declaration: what does it say, what does it not prove, and which canon/vault claim does it
receipt.

Return one JSON object:
{"ledger": [{"name": "the declaration name as written in the source",
             "line": 12,
             "kind": "theorem | lemma | def | instance | structure | inductive",
             "plain_statement": "one sentence: what the declaration says, in plain words",
             "does_not_prove": "one sentence: the nearest thing it does NOT establish",
             "receipts_claim": "the claim this declaration receipts (a C-id from the claims list or a canon/vault address), or \"none\"",
             "grade_suggestion": "FLOOR | VERIFIED | DRAFT | PROSE",
             "grade_evidence": "for FLOOR or VERIFIED only: the source line that records the build receipt (e.g. \"L88: #print axioms ... shows no sorryAx\"), else \"\""}]}

Rules:
1. Grades are ruled vocabulary. FLOOR = on the verified floor with a recorded build; VERIFIED = builds clean
   with a recorded receipt; DRAFT = written but no recorded build; PROSE = not meant for the compiler.
2. You have not compiled anything. FLOOR or VERIFIED without a cited receipt line in grade_evidence is thrown
   out in code and becomes DRAFT; only the build receipt (the compiler's record, e.g. VERIFICATION.md) certifies.
3. "line" is the L-number of the declaration's own line. A line that does not exist in the source is thrown
   out in code.
4. does_not_prove is mandatory: name the closest overclaim (the physics, history or theology the proof does
   NOT touch).
5. receipts_claim is "none" unless the declaration genuinely receipts a listed or canonized claim; do not
   invent addresses.
6. Every declaration of the six kinds appears exactly once; nothing is skipped, nothing invented.
