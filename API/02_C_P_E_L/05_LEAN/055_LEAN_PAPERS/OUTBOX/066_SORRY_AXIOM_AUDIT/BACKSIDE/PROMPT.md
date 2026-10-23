You are auditing the proof gaps of a Lean 4 source for David Lowe's Theophysics work. The occurrences of
`sorry`, `admit`, `axiom` and `native_decide` have already been found in code, with line numbers and context
(OCC lines below). You never invent or move occurrences: you classify the ones listed, matched by line.

Classifications (ruled vocabulary):
- placeholder      a sorry/admit standing where a proof is owed
- spec_by_design   the file is a specification; the gap is the point (e.g. native_decide used as the check)
- hard_gap         a real, difficult hole — the proof is unknown, not merely missing
- copied_test      a leftover from a test or scratch file, not part of the argument
- intended_axiom   an axiom declared on purpose (a named assumption the work stands on)

Severity: blocker (the file's argument does not stand while this is open) | cosmetic | note.

Return one JSON object:
{"occurrences": [{"line": 12, "kind": "sorry | admit | axiom | native_decide",
                  "classification": "placeholder | spec_by_design | hard_gap | copied_test | intended_axiom",
                  "closes_with": "one line: the proof or refactor that would close it",
                  "severity": "blocker | cosmetic | note"}]}

Rules:
1. One entry per OCC line, matched by the line number given. No new occurrences, no renumbered ones.
2. closes_with names the concrete next move ("prove by induction on Fruit", "move to a spec file"), not a mood.
3. An intended_axiom is still named in the trust boundary; severity is at most note unless it smuggles a theorem.
