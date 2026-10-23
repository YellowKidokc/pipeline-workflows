# Call: PROOF_GLANCE · Proof review at a glance — when applicable

DRAFT prompt. Today's runner sends one generic prompt for every section with the whole
template attached; this is that same prompt narrowed to one section, so the template
on the right (output.md) is the only shape the model sees.

---
Fill in this one section of the CKG record: Proof review at a glance — when applicable.
Return ONLY a single JSON object matching this schema:
{
  "status": "AI_PROPOSED",
  "reason": "concise rationale for the section content",
  "markdown": "the section content in GitHub-Flavored Markdown, following OUTPUT TEMPLATE exactly",
  "object_keys": ["C1"]
}

OUTPUT TEMPLATE:
{{output_template}}

PRIOR RESULTS:
{{prior_results}}

SOURCE:
{{source}}
