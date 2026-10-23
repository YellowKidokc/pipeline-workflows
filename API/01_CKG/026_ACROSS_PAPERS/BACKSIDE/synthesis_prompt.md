You are writing the synthesis for "{{topic}}" from compact records of CKG V4 reviews of every paper on it. Write to David, in plain paragraphs, readable. This is the document he uses to close the argument and write ONE final paper.

RULES:
- Judge by TRUE or FALSE only. Never "a critic would say".
- What holds gets the same weight as what breaks.
- Historical thinkers are WITNESSES who reached an idea independently, never sources David borrowed from.
- Never invent a citation, name, or date. Keep UNVERIFIED marks the reviews made.
- Blast radius on every flag: INERT, LOCAL or STRUCTURAL. Most are LOCAL.

Sections, in order (Markdown, ## headings):
1. **Where the whole body of work stands**: three or four paragraphs. What the papers together actually establish, what they only claim, and the single sentence the final paper should stand on.
2. **Every leg across the corpus**: merge the legs from all reviews into one list (no duplicates). For each: one line, who holds it, and whether the corpus as a whole answers it, uses it, or ignores it. End with the legs still unanswered and the one pressing hardest.
3. **Where the papers disagree with each other**: real contradictions or drifts between papers (definitions, numbers, claims), each with which paper should win and why. Say plainly if there are none.
4. **What is original**: what no witness reached before, gathered across the papers.
5. **The spine of the final paper**: the argument in six to ten steps, each marked HOLDS / MUST_DEFEND, and which source papers supply each step. Then a short outline for both registers: the declaration piece (public, unhedged, inviting) and the canon version (graded).
6. **What is missing before it can close**: at most five items, most important first, each with what "done" looks like.

Papers are given as short codes (P01, P02, ...); refer to them by code. Keep the whole synthesis under 3,500 words.

Return ONLY a JSON object: {"markdown": "the whole synthesis"}

THE RECORDS:
{{records}}
