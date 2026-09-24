# AI Notes Standard — NSE profile `station_note`

Every LLM call in this pipeline leaves a note for the next model that opens the
file. Not a log. Not a summary. An **operating handoff**.

Governing question, borrowed from the project-state profile:

> If this model vanished mid-task, could a different model pick up the file and
> continue correctly — without re-deriving what was already settled, and without
> inheriting a mistake as fact?

## Where notes live — the ubiquitous rule

Two places, always, no exceptions:

```
workflows/<PACKET>/NOTES/<station>/<object_id>.note.yaml   # station-scoped
<artifact_path>.note.yaml                                   # sidecar, beside the artifact
```

A station that produces no note has not finished. `LLMHub` writes the sidecar on
every dispatch; the station writes the station-scoped note on verdict.

## Envelope

Reuse `NSE-1.0`. The note is a payload profile, not a new format.

```yaml
semantic_enclosure:
  format: NSE-1.0
  object_id:
  object_type: station_note
  source_hash:            # SHA-256 of what this note was derived from
  source_authority: original_bytes
  created_at:
  provenance:
    workflow:
    station:
    model:
    prompt_version:
    upstream_note:        # object_id of the note this one builds on, or null
  reconstruction_contract:
    original_preserved: true
    semantic_layer_is_interpretive: true
    unsupported_inferences_forbidden: true
  payload_profile: station_note
  payload: {}
```

## Payload

```yaml
payload:
  task:                   # what this call was asked to do, one line
  verdict:                # PASS | FAIL | HOLD | PARTIAL
  confidence: 0.0

  saw:                    # what was actually in front of it
    inputs: []            # paths + hashes
    truncated: false      # was input cut for context budget
    missing: []           # expected and absent

  did:                    # decisions, in order
    - decision:
      because:
      rejected: []        # alternatives considered and dropped, with reason

  could_not_determine: [] # the gaps. Required. Empty list is a claim.

  negative_results:       # tried and failed. Highest-value field.
    - tried:
      failed_because:
      do_not_retry: true

  epistemic:
    observed: []          # in the source, quotable
    inferred:             # derived, with basis
      - claim:
        basis:
        confidence: 0.0
    assumed: []           # taken on faith, unverified

  drift_gates:            # how the next model will get this wrong
    - forbidden:          # the wrong reading
      allowed:            # the right one
      kill_condition:     # what breaks if the wrong reading is taken

  invalidates_if: []      # conditions that make this note stale

  next:
    should: []
    should_not: []
    blocked_on: []
```

## Rules

**R1 — Notes are invalidatable.** `source_hash` is the hash of the exact input.
If the source changes, the note is stale and any consumer must treat it as
absent. A note that cannot tell you it is out of date is worse than no note.

**R2 — Epistemic status is mandatory, not optional.** `observed` / `inferred` /
`assumed` must be separated. The failure this prevents is a successor treating
an inference as a fact and building on it. We have already seen the shape of
that failure locally: a station that writes plausible-looking output after its
work silently failed.

**R3 — Negative results are required.** "I tried X, it failed because Y, do not
retry" saves the successor more time than any positive finding. Models do not
volunteer this. The prompt demands it and the schema enforces it.

**R4 — `could_not_determine` may not be omitted.** An empty list is an explicit
claim that nothing was unclear, and is treated as one.

**R5 — Drift gates carry kill conditions.** Say the wrong reading out loud, say
the right one, say what breaks. Stating only the correct reading does not stop
the incorrect one.

**R6 — Compression is the point.** Hard cap 1,200 tokens of payload. If it does
not fit, the note is doing summary instead of handoff. Compression that loses
recoverability has failed; compression that loses politeness has succeeded.

**R7 — The note never modifies the artifact.** Source bytes stay canonical. A
note is a derived layer and may be regenerated at any time.

**R8 — Registers that are forbidden.** No teaching prose, no restating the task
back, no hedging, no apology, no praise of the input, no transitions. Machine
reads only. Human readability is not a requirement and must not be paid for.

## Chaining

`upstream_note` links a note to the one before it, so a reader can walk the
chain back through the stations without reading any artifact. A corpus-level
reader can reconstruct the whole run from notes alone — that is the test of
whether the standard is working.
