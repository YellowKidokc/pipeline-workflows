You are judging the merged claims of "{{topic}}". Below are (1) a numbered list of merged claims and (2) compact records of CKG V4 reviews of every paper, which hold what each review concluded about each claim.

For EACH numbered claim, give a verdict based on what the reviews say:
- HOLDS: defensible as written.
- MUST_DEFEND: true or defensible, but draws the hardest attacks.
- OVERSTATED: claims more than it shows. Give the defensible version in David's voice.
- WRONG: false as stated. Say what can be kept.
If reviews disagree about the same claim, say so in "conflict".

RULES:
- Judge by TRUE or FALSE only. Never "a critic would say".
- What holds gets the same weight as what breaks.
- Never invent a citation, name, or date.
- Blast radius: STRUCTURAL only if that paper's central conclusion falls when this claim falls. LOCAL if fixing the wording repairs it. INERT if nothing rests on it. Expect most rows to be LOCAL.
- Never leave a placeholder such as [cite source]. If a source is missing, say "source needed".

Keep every field short: defensible_version under 35 words, conflict under 20 words.

Return ONLY a JSON object:
{"rows": [{"n": 1, "verdict": "HOLDS | MUST_DEFEND | OVERSTATED | WRONG", "defensible_version": "", "blast_radius": "LOCAL", "conflict": ""}],
 "notes": "two or three sentences: the shape of the ledger and which rulings David should make first"}

(1) THE MERGED CLAIMS:
{{claims}}

(2) THE RECORDS:
{{records}}
