# 65_PAPER_INTELLIGENCE

The Theophysics Paper Intelligence Suite v2.0 on each paper. Local, no API.
Source: `X:\THEOPHYSICS_PAPER_INTELLIGENCE`, vendored as `_system\vendor\paper_intelligence` (code unchanged apart from drive
letters; the model cache, the 320 MB `04_ANALYTICS` dashboards and three one-off batch scripts were left out).

| Layer | What it measures |
|---|---|
| L1 Text analytics | readability (Flesch, Fog, SMOG, Coleman-Liau, Dale-Chall...), vocabulary, keywords, n-grams |
| L2 Academic standard | citations, external theories, structure (abstract, method, results...), academic grade |
| L3 Theophysics metrics | chi, wisdom/knowledge ratio, fruits composite, the ten Master Equation variables, cross-domain bridges, CKG tier |
| L5 NLP deep | named entities, topics, key sentences |
| L6 Truth Engine | fruits and chi anchors in embedding space, tier (near-canonical / strong / provisional / weak) |
| L7 Knowledge graph | every paper of the run as a node, linked by shared variables, topics and similarity |
| L8 Emotion profile, L9 Linguistic depth, L10 Idea density | as named |

L4 (OpenAI 7Q) is off: it is an API call, and Academia is the local side; API work lives in `08_API_DEEP`.

**Output** (flat, in the folder chosen at the button; default this OUTBOX):
- `<note> · 65_PAPER_INTEL.md`: every measure of the paper, one table per layer; `_json\<note> · 65_PAPER_INTEL.json`
- `PAPER_INTELLIGENCE\<stamp>\`: the suite's workbook (one row per paper), JSON, and the knowledge graph (`.html`, `.graphml`)

All papers of one run go through together, so the graph links them. Step 2 of `063_PAPER_AUDIT`.
No questions: `python BACKSIDE\65_paper_intelligence.py <papers or folder> --outbox <folder>`.
