You are writing a note to the next model that opens this file.

That model is not you. It has no memory of this call, no access to your
reasoning, and no way to ask you a question. Everything it will know about what
happened here is what you write now. It will act on this note. If the note is
wrong, it will be wrong confidently.

You are not writing for a human. Nobody is going to read this for pleasure or
for reassurance. Optimize for a machine reconstructing your operating state, not
for a person feeling informed.

## What the receiving model actually needs

Not what you concluded. It needs what it would otherwise have to re-derive, plus
what would make it go wrong:

1. What you actually saw — and whether the input was truncated or incomplete.
2. What you decided, and **what you rejected and why.** The rejected branch is
   what stops the next model repeating your dead end.
3. What you could not determine. This is not an admission, it is the map edge.
4. What you tried that failed, and whether it is worth retrying.
5. Which of your statements are in the source, which you inferred, and which you
   assumed. Kept separate. A later model that cannot tell your inference from
   the source text will build on it as fact.
6. How the next model will misread this — stated as the wrong reading, the right
   reading, and what breaks if the wrong one is taken.
7. What would make this note stale.

## Forbidden

- Teaching prose, narration, or transitions
- Restating the task back
- Hedging, apology, or praise of the input
- Any sentence whose removal loses no information
- Prose where a field will do

Compression is the job. Hard cap: 1,200 tokens of payload. If it does not fit,
you are summarizing instead of handing off. Summary discards what was hard to
learn and keeps what was easy to say. Do the opposite.

## Required

`could_not_determine` and `negative_results` may not be omitted. An empty list is
an explicit claim that there was nothing unclear and nothing failed, and will be
read as one.

`drift_gates` must name at least one wrong reading. There is always one. If you
cannot find it, you have not understood the object well enough to hand it over.

## Output

Return ONLY a YAML `payload:` block conforming to the `station_note` profile in
`docs/AI_NOTES_STANDARD.md`. No fences, no commentary, no preamble.

---

TASK GIVEN: {task}
STATION: {station}
INPUTS: {inputs}
WHAT YOU PRODUCED: {result}
UPSTREAM NOTE: {upstream_note}
