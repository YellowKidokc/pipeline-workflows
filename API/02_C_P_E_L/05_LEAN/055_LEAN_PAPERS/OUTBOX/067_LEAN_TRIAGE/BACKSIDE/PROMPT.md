Triage one Lean 4 file for David Lowe's Theophysics vault. Be brief; this pass runs over the whole corpus.

Return one JSON object:
{"file_kind": "proof | spec | scratch | test | docs_extract | duplicate",
 "one_line_purpose": "one line: what this file is for",
 "quality": "floor_candidate | solid | draft | noise",
 "duplicate_of_hint": "the file this duplicates, if you can tell from declarations/names, else \"\"",
 "action": "nominate_floor | keep | archive | delete_candidate"}

Vocabulary:
- proof: proved results live here.  spec: definitions/axioms as a specification.  scratch: working notes.
  test: exercises other code.  docs_extract: documentation or quoted material.  duplicate: another file's twin.
- floor_candidate: clean enough to nominate for the verified floor (a nomination — the build decides).
  solid: real work, not floor-ready.  draft: unfinished.  noise: no lasting value.
- nominate_floor only travels with floor_candidate. delete_candidate only for true noise or duplicates;
  it is a label for a human, never a deletion.
- If PARTIAL: yes, you saw the head of the file plus its declaration list; judge from that and say less.
