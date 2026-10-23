Merge these claims about "{{topic}}". Each line is one claim with the paper codes it came from. Many lines say the same thing in different words.

Merge every group of lines that say the same thing into ONE claim. Return AT MOST {{max}} claims. Fewer is fine. Load-bearing claims (the ones the argument stands on) first.

Each line ends with the review's group: (STRONGEST), (MUST_DEFEND) or (PROBABLY_WRONG). Keep the balance the lines have: claims that held must be as well represented as claims that broke. Carry the group forward in a "group" field (if merged lines differ, use the most common).

Every paper code that appears in the lines must appear in at least one of your claims; do not drop a paper.

Each claim under 25 words, stated as the papers state it (not softened). Keep every paper code from the lines you merged.

Return ONLY a JSON object:
{"claims": [{"claim": "...", "papers": ["P01", "P07"], "group": "STRONGEST", "load_bearing": true}]}

THE LINES:
{{lines}}
