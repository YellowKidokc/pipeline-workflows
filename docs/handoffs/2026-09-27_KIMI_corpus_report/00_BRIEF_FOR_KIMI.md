# Brief: one analysis standard and one report page for the whole corpus

From David Lowe (Faith Through Physics / Theophysics), 2026-09-27. Prepared with Claude Code.

## The goal

Everything David analyses goes through one base analysis, the **CKG**: his own papers, YouTube transcripts, and
anything else later. Domain passes are added on top (theology, physics, math). The CKG output is what will make it
possible later to classify, aggregate and pull out arguments across the whole corpus.

What David is asking you to design:

1. **The unifying parameters.** Which fields from the CKG analysis should be the fixed, consistent parameters for every
   source in the corpus? These are the fields that stay comparable from one of his papers to a YouTube interview to
   anything else. Each field needs a definition, a type, a scale, and whether it is computed or AI-judged.
2. **The per-source report page.** One HTML page per source (for example, one per YouTube video, sitting in that
   video's folder), built from those parameters, in the visual language of file 04.

Expect several rounds of refinement. This is version 1 of about 10.

## What is in this folder

| File | What it is |
|---|---|
| `01_CKG_TEMPLATE_MASTER_PAPER_COMPANION.md` | The CKG template, MASTER PAPER COMPANION v0.4.1. A YAML scoring header, a scorecard, S01-S11 (claim, argument and 4-dimension defense, evidence, objections, boundaries, formal/math, bridges, falsifiability, audit), Q0-Q14, hidden premises, truth predicates. |
| `02_EXAMPLE_Habermas_2026-09-12_full_note.md` | A finished example: one Gary Habermas YouTube video with every analysis on the note. In order: scorecard; summary; full CKG; argument grades; Fruits of Love and Truth; YouTube argument catalogue; transcript. |
| `03_EXAMPLE_API_DEEP_report.html` | The current per-source HTML for that video: Love × Truth plot, fruit lollipops, sentence heat strip, axioms, atoms, Lean targets, stories, master-equation slots, coherence, searchable sentences. Opens offline. |
| `04_Paper_Information_Matrix_circles.html` | **The approved design language** (David: "a masterpiece"). A 12-number headline strip; one band per statistic family, one circle per statistic; colour = needs work -> strong; size = distance from the norm; inner glyph = computed / AI-judged / runs disagree; a corpus vs academic toggle; a family map; 15 specialized charts; a searchable wall. Demo data. |
| `05_EVD_RUBRIC_v2.0.0.json` | The evidence rubric: 11 epistemic modes, 10 dimensions × 18 probes, 8 global gates. |
| `06_CLASSIFICATION_MASTER.md` | The corpus classification record. Every source is named `<Author code> <Date> · <Title> · <Keyword>, <Keyword> · <Move>`, and every keyword and move used so far is listed with counts. |
| `07_ARGUMENT_LEDGER.html` | Per-argument Strength × Originality (each 0-8, computed from quoted yes/partly/no checks, two independent gradings). Machine ceiling 8; human review +1; Lean receipt +1. |
| `08_CHARACTER_PROFILES.md` | The Fruits of Love and Truth character types (Love × Truth quadrants, 10 fruit shapes). |

## Lessons already learned (please keep them)

- **Scores the model gives directly are not trustworthy.** Asked for a 0-10 score, the model drifts to about 8: S01
  was 8 on all ten Habermas chapters. Scores must be **computed** from checks the model answers with quotes (see file 07).
- **Sections that do not apply** (for example, formal/math for a history interview) should be NOT_APPLICABLE and left
  out of totals, not scored low.
- **One source = one page.** All analysis sits on the original note, never in scattered side files.
- **Generic tags are useless.** "Theology" and "Apologetics" are a given for this corpus. Classifications must be
  specific (Resurrection, Early Creed, Minimal Facts Approach).
- The corpus mixes David's papers, which argue from an openly admitted root axiom ("God Is"), with other people's
  videos. The parameters must work for both, and must never apply David's axiom preamble to someone else's work.

## What would help most back from you

1. A **data contract**: a list of parameters, each with name, definition, type/scale, computed or AI-judged, and which
   CKG section or field it comes from.
2. A **page layout** for the per-source HTML: which parameters go in the headline strip, which become circle bands,
   and which charts.
3. What in the current CKG should be **dropped, merged or added** to serve that contract.
