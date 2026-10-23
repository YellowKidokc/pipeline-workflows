# Call: MAP

Runs first. Its JSON is passed to every later call as PRIOR RESULTS.
(Copied verbatim from the current runner: vendor/ckg/workbench/ckg.py, _build_prompt, stage "map".)

---
Map this document as JSON. Return ONLY a single JSON object matching the schema below.
CRITICAL RULE: every non-empty 'quote' must be copied EXACTLY from the SOURCE text.
If you cannot find an exact verbatim substring, leave 'quote' empty.
Never invent, paraphrase, or approximate a quotation.

SCHEMA:
{
  "title": "document title",
  "domain": "primary knowledge domain",
  "project": "collection or project name",
  "purpose": "paper | note | draft | objection | evidence | synthesis",
  "summary": "one-paragraph summary",
  "keywords": ["keyword"],
  "objects": [
    {
      "key": "C1",
      "type": "CLAIM | DEFINITION | AXIOM | EVIDENCE | OBJECTION",
      "register": "e.g. FORMAL_MATHEMATICAL, THEOLOGICAL, EMPIRICAL",
      "quote": "exact substring from the source, or empty",
      "statement": "paraphrased or formal statement",
      "reason": "why the object is classified this way"
    }
  ],
  "unmapped": ["important content not captured above"]
}

SOURCE:
{{source}}
