# MeaningIntake

Turns conversations, articles, and research notes into reviewable two-layer knowledge records
without discarding the source. The readable top layer presents the strongest defensible case; the
lossless bottom layer preserves the complete original.

## Flow

```text
INPUT
  -> hash and preserve exact source
  -> infer document type and tags
  -> create a semantic-analysis prompt
  -> create a structured CANDIDATE_DRAFT record
  -> append the complete source
  -> REVIEW when purpose is ambiguous
```

The deterministic runner never claims that placeholder analysis is an AI conclusion and never
admits material to canon. `ARCHIVE` contains source copies, while files in `INPUT` remain in place.

## Run

Drop `.md`, `.txt`, or `.html` files into `INPUT`, then run `RUN_PIPELINE.bat`.

Outputs:

- `OUTPUT/<name>.knowledge.md` - structured record plus complete source
- `OUTPUT/<name>.intake.json` - machine-readable receipt
- `REVIEW/<name>.analysis-prompt.md` - full prompt for an AI semantic pass
- `REVIEW/<name>.question.md` - created only when routing is ambiguous
- `ARCHIVE/<run-id>/sources/` - exact preserved source copies
- `LOGS/<run-id>.json` - run receipt

The next integration step is to let an approved model return the semantic sections described in
`PROMPTS/knowledge_record.md`; the runner will remain responsible for appending the untouched source.
