# Classification master record

Every classification the corpus uses, rebuilt each time a source is titled (tools/standard_title.py; data: API_ALL/API_HOME/tools/taxonomy.json). The tagger is told to reuse these terms, so over time this becomes the fixed vocabulary the whole corpus works within.

## Rules

- File name: `<Author code> <YYYY-MM-DD> · <Title> · <Keyword>, <Keyword> · <Move>`; all keywords are in the note's YAML.
- Keywords: specific search topics, broadest first, Title Case, 1-3 words. Never generic fields: apologetics, bible, christian apologetics, christianity, faith, philosophy, religion, theology.
- Move: what the source mainly does. One of: Evidence, Argument, Objection-reply, Scholarly-survey, Method, Application, Testimony, Debate.
- Author code: first initial + surname for a person; overrides in tools/author_codes.json.

## Keywords (9)

| Keyword | Sources | Examples |
|---|---:|---|
| Resurrection | 10 | [[GHabermas 2026-09-12 · The Resurrection Connection to Christian Theology · Resurrection, Theological Implications · Scholarly-survey\|GHabermas 2026-09-12]] · [[GHabermas 2026-09-05 · Powerful Historical Reasons to Believe Jesus Resurrected · Resurrection, Historical Jesus Criteria · Evidence\|GHabermas 2026-09-05]] · [[GHabermas 2026-08-29 · Remarkably Early Historical Information for the Resurrection of Jesus · Resurrection, Early Creed · Argument\|GHabermas 2026-08-29]] … |
| Pauline Epistles | 5 | [[GHabermas 2026-09-05 · Powerful Historical Reasons to Believe Jesus Resurrected · Resurrection, Historical Jesus Criteria · Evidence\|GHabermas 2026-09-05]] · [[GHabermas 2026-08-29 · Remarkably Early Historical Information for the Resurrection of Jesus · Resurrection, Early Creed · Argument\|GHabermas 2026-08-29]] · [[GHabermas 2026-08-22 · The Resurrection Connection to All of Life · Resurrection, Theological Implications · Application\|GHabermas 2026-08-22]] … |
| Minimal Facts Approach | 4 | [[GHabermas 2026-08-01 · Which Scholars Accept the Facts for the Resurrection · Resurrection, Minimal Facts Approach · Argument\|GHabermas 2026-08-01]] · [[GHabermas 2026-07-25 · The Evidential THRESHOLD for Resurrection Belief · Minimal Facts Approach, Historical Jesus Criteria · Method\|GHabermas 2026-07-25]] · [[GHabermas 2026-07-18 · Resurrection Views Across the Theological Spectrum (Pt.… · Resurrection, Minimal Facts Approach · Scholarly-survey\|GHabermas 2026-07-18]] … |
| Historical Jesus Criteria | 3 | [[GHabermas 2026-09-05 · Powerful Historical Reasons to Believe Jesus Resurrected · Resurrection, Historical Jesus Criteria · Evidence\|GHabermas 2026-09-05]] · [[GHabermas 2026-08-01 · Which Scholars Accept the Facts for the Resurrection · Resurrection, Minimal Facts Approach · Argument\|GHabermas 2026-08-01]] · [[GHabermas 2026-07-25 · The Evidential THRESHOLD for Resurrection Belief · Minimal Facts Approach, Historical Jesus Criteria · Method\|GHabermas 2026-07-25]] |
| Early Creed | 2 | [[GHabermas 2026-08-29 · Remarkably Early Historical Information for the Resurrection of Jesus · Resurrection, Early Creed · Argument\|GHabermas 2026-08-29]] · [[GHabermas 2026-08-15 · A Number of Critical Scholars Often Date These Biblical Creeds to the 30s… · Resurrection, Early Creed · Argument\|GHabermas 2026-08-15]] |
| Scholarly Perspectives | 2 | [[GHabermas 2026-07-18 · Resurrection Views Across the Theological Spectrum (Pt.… · Resurrection, Minimal Facts Approach · Scholarly-survey\|GHabermas 2026-07-18]] · [[GHabermas 2026-07-11 · What Scholars Believe About Jesus' Resurrection (Pt. 1) · Resurrection, Scholarly Perspectives · Scholarly-survey\|GHabermas 2026-07-11]] |
| Theological Implications | 2 | [[GHabermas 2026-09-12 · The Resurrection Connection to Christian Theology · Resurrection, Theological Implications · Scholarly-survey\|GHabermas 2026-09-12]] · [[GHabermas 2026-08-22 · The Resurrection Connection to All of Life · Resurrection, Theological Implications · Application\|GHabermas 2026-08-22]] |
| Bodily Resurrection | 1 | [[GHabermas 2026-08-08 · What Critical Scholars Say About Jesus' Bodily Resurrection · Resurrection, Pauline Epistles · Scholarly-survey\|GHabermas 2026-08-08]] |
| Suffering | 1 | [[GHabermas 2026-09-12 · The Resurrection Connection to Christian Theology · Resurrection, Theological Implications · Scholarly-survey\|GHabermas 2026-09-12]] |

## Moves (5 of 8 in use)

| Move | Sources |
|---|---:|
| Evidence | 1 |
| Argument | 3 |
| Objection-reply | 0 |
| Scholarly-survey | 4 |
| Method | 1 |
| Application | 1 |
| Testimony | 0 |
| Debate | 0 |

## Author codes

| Code | Author / channel |
|---|---|
| GHabermas | Gary Habermas |
