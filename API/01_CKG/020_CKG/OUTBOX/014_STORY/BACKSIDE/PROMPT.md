Apply Story Material System v1.0 (below) to ONE SECTION of a transcript. Build compact records for original writing using
the six record kinds: fast_fact, human_moment, connection, memorable_line, story_device, story_spine. Do not rewrite or
summarize the whole story.

Extract every distinct item in THIS SECTION with a defensible future writing use; impose no quota and invent nothing to fill
categories. An empty category is valid. Preserve important counterexamples and complications. Classify with the test
questions, allowing several devices on one record.

Distinguish historical claims, fictional events, the speaker's interpretation, your interpretation, and directly observed
wording or structure. Reading the transcript does not verify its claims: leave verification "unchecked" unless the record
is only about the wording or structure of this source (then "source_checked"). Never mark anything externally_checked:
nothing outside the transcript is being consulted. Keep exact quotations separate from paraphrases; transcript_wording must
be copied character for character from the section (it will be checked in code). Attribute fictional speech to its
character.

LOCATORS: the transcript is broken by timestamp headings like "### [05:00](...)" every few minutes. Give each source span a
start (the timestamp heading the passage sits under, as "HH:MM:SS") and an end (the next heading, or null). These are
approximate; never invent finer times. If the section has no timestamps, use null and describe the place in "where".

Story spines: only where a narrative exists in THIS SECTION (embedded_story or underlying_work). Do NOT write a
presentation spine for the whole video; that is done separately after all sections are read.

Return ONLY a JSON object:
{
  "items": [
    {
      "kind": "fast_fact | human_moment | connection | memorable_line | story_device | story_spine",
      "subtype": "one of the kind's subtypes, or null",
      "gist": "one sentence",
      "value": "one sentence: what this could help a writer show",
      "topics": ["short normalized subjects; keep specific people and works"],
      "uses": ["from: opening, explanation, illustration, evidence_lead, transition, humor, emotional_turn, ending"],
      "appeal": ["from: surprising, vivid, human_stakes, tension, humorous, memorable_wording, revealing_connection"],
      "devices": ["only from the device table"],
      "basis": "reported_fact | fictional_event | speaker_interpretation | extractor_interpretation | observed_wording | observed_structure | hypothetical",
      "verification": "unchecked | source_checked | disputed | unresolvable",
      "reuse": "fact_after_check | attributed_quote | attributed_example | pattern | research_lead",
      "sources": [{"start": "HH:MM:SS or null", "end": "HH:MM:SS or null", "where": "a few words locating it"}],
      "details": {"only the kind-specific fields that apply"},
      "checks": ["what must be verified before factual reuse, or nothing"]
    }
  ],
  "notes": ["vocabulary candidates, missing context, anything a reviewer should know"]
}
