# SENTENCE MARKER SPEC v0.1 — glyphs in the text
*David Lowe · POF 2828 · Oct 17, 2026 · companion to HTML_ASSEMBLY_SPEC_v0_1.md*

## The idea
A marker at the start and end of a tagged sentence travels WITH the words. Copy the paragraph, move it, run it
through a station — the tag goes along, and anything tagged can always be pulled back out of any document.

## The rule
One bracket pair for everything; the type is written inside. Plain text in the source, icons only in the HTML.

    ⟦TYPE id⟧ the sentence or sentences ⟦/⟧

    ⟦CLM C004⟧ Grace is a source term, not a force. ⟦/⟧
    ⟦KILL⟧ If the ledger closes with no remainder, this fails. ⟦/⟧
    ⟦PERS⟧ The Bart story. ⟦/⟧
    ⟦EVD E012 src=Habermas-2004⟧ Twelve facts are granted by most critical scholars. ⟦/⟧

- `id` is optional; when present it is the node's claim_key (links to node_id in the node record).
- Extra fields `key=value` are allowed after the id (src, q=Q-ID, law=05, status=...).
- Markers may sit inside one another only fully nested (⟦A⟧ … ⟦B⟧ … ⟦/⟧ … ⟦/⟧); never crossing.
- ⟦ and ⟧ are U+27E6 / U+27E7. If a tool cannot type them, `[[TYPE id]]` and `[[/]]` are accepted and normalised.

## Types (mapped to the 56 glyphs in theophysics_glyphs\svg\)
| Marker | Glyph | Layer |
|---|---|---|
| DEF | definition.svg | L1 |
| AX | axiom.svg | L1 |
| BND | boundary.svg | L1 |
| LAW | law.svg | L1 |
| CLM | claim.svg | L2 |
| PRED | prediction.svg | L2 |
| EQ | equation.svg | L2 |
| ISO | isomorphism.svg | L4 (bridge; add ladder=analogy..isomorphism) |
| EVD | evidence.svg | L3 |
| PRF | proof.svg | L3 |
| WIT | witness.svg | L3 (historical witness: Augustine, Aquinas...) |
| KILL | kill-condition.svg | L3 |
| PERS | personal-claim.svg | owner=PERSONAL — shown, never graded as framework evidence |
| INV | invariant.svg | L4 |

Status glyphs are NOT markers in the text; they are computed and drawn by the HTML from the node record:
lean4.svg, python-verified.svg, wolfram.svg, ai-validated.svg, canonical.svg, draft.svg.
Domain and term glyphs (physics, theology, grace, sin, logos...) are tags (`law=`, `term=`), drawn as small badges.

## The guard (required)
AIs rewriting a paragraph tend to drop unusual brackets. Every station runs a marker count before and after:
same markers, same ids, same nesting -> pass; anything missing -> the change is flagged MARKER_LOSS and not accepted.

## HTML
`⟦CLM C004⟧` renders as the claim icon at the sentence start; `⟦/⟧` as a small end mark.
Hover = preview of the node; click = Node drawer. The sentence span carries data-node-id for the graph.
