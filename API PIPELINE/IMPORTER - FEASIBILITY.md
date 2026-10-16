# Importer feasibility — inspected, not implemented

## Conclusion

A read-only Python importer for the catalog is a good fit. Automatically converting every existing script into a fully editable and executable template is a separate, harder task. Import metadata first, then verify individual execution adapters. Do not import Python modules or run batch files merely to discover their contents.

## Evidence from the available checkout

Inspected /workspace/pipeline-workflows/API. Found 54 station.json files outside _system and the separate Open-AI-CALL-OBS-Plugin-Final-Claude tree. This is a file count, not a count of distinct API calls. Declared kinds: 24 native, 23 legacy, 3 bundle, 1 chain, 3 unspecified. Some stations are local processing steps rather than API calls.

All 54 include number, name, label, options, and description. Most include uses_api and goals. Prompts and focus files commonly sit next to station.json in BACKSIDE. Some stations sit inside another station's OUTBOX, so discovery must recurse and identify station metadata rather than excluding every OUTBOX.

Examples:
- YouTube Summary: PROMPT.md and QUESTIONS.md; the prompt also contains the JSON output requirements.
- Lean Papers: four declared prompt files and four goal records; formatting templates, output assembly, checks, and dependencies also appear in Python and _system/templates/lean.
- OpenAI Stations: 23 prompt stations may be bundled into fewer requests; bundles.json and the Python planner control grouping and ordering.
- CKG Run: a legacy station points to a vendored script. The visible station folder does not itself establish the actual call breakdown.
- API Deep / Analytical Arms: several logical goals, repeated runs, and per-sentence work; goal count is not request count.

02_C_P_E_L was supplied by David but is absent from this cloud checkout. Report unavailable source groups rather than inventing contents. Check the intended Windows checkout when implementing.

## Easy automatic import

Produce a catalog JSON, separate from source code, with:
- group identity and actual relative path;
- station identity, name, description, kind, uses_api, and declared options;
- discovered prompt, question, focus, template, and configuration file references;
- declared goals and bundle/chain metadata;
- provenance for each imported value and explicit unresolved fields.

Read source files only; do not execute scripts, load keys, move files, or rewrite original stations. Scan for BACKSIDE/station.json and preserve folder nesting. Treat descriptions and prompts as data. Keep credentials and user note contents out of the export. Preserve custom UI names, ordering, and edits on re-import using stable identities and a separate override layer. Flag duplicate identities and changed/missing sources for review.

## Requires station-specific review

A PROMPT.md is not proof it is the complete prompt actually sent. Questions, system messages, source wrappers, schemas, and context may be added in Python. Output requirements may be embedded in a prompt, a Markdown template, or rendering and validation code. Do not pretend an importer has separated these perfectly.

A generic UI cannot safely override every model, destination, call order, or table format until its adapter supports that setting. Preserve existing validation and trust rules. An output format change may require updating a renderer, not an API prompt.

Represent task dependencies and bundle behavior explicitly. Reordering independent steps is straightforward; reordering a dependent step must warn or be refused. An existing station may stay opaque and run through its supported entry point until its internals have been mapped.

## Recommended sequence

1. Read-only scan -> catalog JSON + import warnings.
2. Feed the catalog into the static UI's groups and Backside lists. Mark unsupported settings and unresolved output contracts.
3. Verify one simple station end-to-end using a mock provider and temporary inputs, checking the actual prompt, completed outputs, logs, immediate saves, and restart behavior.
4. Add adapters for more complex stations only as needed. Reuse the existing station engine rather than building a second executor by default.

The HTML currently embeds example data; a Python scan alone does not populate it. A small explicit catalog-loading step must be added. Local HTML can load JSON through a file picker without a server; background execution and automatic writes to fixed Windows folders need a local service or desktop integration.

No importer or execution wiring was built during this assessment. No API requests were sent and repository source files were left unchanged.
