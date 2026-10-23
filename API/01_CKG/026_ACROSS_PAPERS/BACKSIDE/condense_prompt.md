You are extracting a compact record from one CKG V4 review of the paper "{{paper}}". This is extraction, not new judgment: copy what the review says, shortened. Do not add claims or verdicts the review does not make.

Return ONLY a JSON object:
{
  "finding": "the paper's central finding, one sentence",
  "claims": [
    {"claim": "the claim, quoted or near-quoted, under 40 words",
      "group": "STRONGEST | MUST_DEFEND | PROBABLY_WRONG",
      "why": "the review's reason, one sentence",
      "attack": "for MUST_DEFEND: the attack, one sentence; else empty",
      "answer": "for MUST_DEFEND: the best answer, one sentence; else empty",
      "defensible_version": "for PROBABLY_WRONG: the defensible version; else empty",
      "blast_radius": "INERT | LOCAL | STRUCTURAL | empty"}
  ],
  "legs": [{"name": "short name", "holders": "who holds it, as the review says", "status": "used | answered | ignored"}],
  "strongest_against": "the leg the review says presses hardest, and why, one sentence",
  "still_to_answer": ["legs the review says the paper must still answer"],
  "whats_new": "what the review says is original here, one or two sentences",
  "defeat_condition": "what would break the paper, one sentence",
  "build_next": ["up to three items"]
}
At most 12 claims. Keep every field short.

THE REVIEW:
{{review}}
