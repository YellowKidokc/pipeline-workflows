# Portable API workbench

This is the repository's modular, copyable API workbench. It does not replace or import the existing pipeline engine, and it does not move unrelated content. Each copied station contains its Python runtime (standard library only), configuration, prompts, launchers, queues, and durable local records.

## Folder map (inventory before implementation)

| Home | Purpose / actual status |
|---|---|
| `APIs/templates/MY_STATION` | Clean portable station template. |
| `APIs/workbench` | Shared source for provider, queue, event, export, and coordinator building blocks. Copied into each station at creation time. |
| `APIs/nlp/{cleanup,extraction,classification,chunking,indexing}` | Capability homes. The dependency-free implementations currently live in `workbench/nlp.py`; these directories reserve clear extension points. |
| `APIs/components/evidence` | Compatibility pointer only: the working Evidence implementation remains at `workflows/EvidenceChainIntake`; it was not reorganized. |
| `APIs/components/lean` | No Lean compiler workflow was found in this checkout. This home does not pretend one exists. |
| `APIs/components/canonization`, `APIs/components/ckg` | Reserved integration homes. Existing repository station declarations and the Evidence CKG prompt are inventory items, not claimed implementations. |
| `APIs/stations/Stories` | Working example station. |
| `APIs/coordinator` | Generated structured inventory. |
| `APIs/activity` | Generated aggregate activity CSV. |

Old-to-new compatibility: there are no old `APIs/` paths in this checkout. Existing `SYSTEM.bat`, `scripts/station_runner.py`, `engines/pipeline`, station manifests, and Evidence launchers remain unchanged. The new workbench is additive.

## Quick start

Create a blank station only when requested (the destination must not exist):

```console
python APIs/create_blank_station.py "C:\My Work\Research Station"
```

Creation copies only runtime programs, prompts, config, launchers, and empty runtime folders, then assigns a UUID. It excludes secrets, inputs, outputs, logs, caches, environments, and state. Stations never replicate themselves. Moving/renaming preserves `STATE/identity.json`; creating again assigns a new identity. Coordinator discovery flags duplicate identities.

On Windows, run `SETUP.bat`, edit `CONFIG\station.json`, put UTF-8 `.txt` or `.md` files in `INBOX`, and run `RUN_ONCE.bat`. Launchers pass quoted absolute paths derived from `%~dp0` and never change directory, call `pushd`, invoke `net use`, or create a drive mapping; this supports paths with spaces and UNC shares. On other systems:

```console
python SCRIPTS/workbench_cli.py setup --root .
python SCRIPTS/workbench_cli.py run-once --root .
```

## Configuration and safety

Supported adapters are OpenAI Responses, Anthropic Messages, DeepSeek Chat Completions, and OpenRouter Chat Completions. The implementation was checked against the official API reference locations on 2026-09-22: [OpenAI Responses](https://platform.openai.com/docs/api-reference/responses/create), [Anthropic Messages](https://docs.anthropic.com/en/api/messages), [DeepSeek chat completion](https://api-docs.deepseek.com/api/create-chat-completion), and [OpenRouter chat completion](https://openrouter.ai/docs/api-reference/chat-completion). Network access to those pages returned HTTP 403 in the build environment, so live conformance was not claimed; adapters are covered with wire-format mocks and live tests require explicit user action.

Provider and model are explicit. There is no silent fallback. Credentials are read from the provider environment variable or ignored `CONFIG/private.local.json`. Errors expose at most a bounded provider message, never request headers. Retry applies only to network failures, 408/409/425/429, and 5xx; `Retry-After` is honored. Stable call IDs aid investigation, but since not all providers guarantee idempotency, an interrupted ambiguous HTTP submission is not automatically claimed successful.

Steps are declared in JSON and restricted to built-in safe types (`preserve`, allowlisted local `nlp`, `api`, `validate`). API/document output is never evaluated as code. Chunk boundaries and full source coverage appear in receipts; input is never silently truncated. Handoffs are disabled by default and, when explicitly enabled, copy a provenance packet only to the configured destination.

### Queue and reprocessing policy

The watcher continuously rescans only while explicitly running. Atomic locks reject a second instance. Priority uses a 3:1 weighted merge so ordinary files cannot starve. Files must remain size/mtime-stable. Twelve workers is the per-station default; aggregate concurrency is the sum of simultaneously running stations. Completion keys combine source SHA-256 with step configuration and prompt bytes. Same content/workflow resumes without repeating completed calls; source or workflow changes make a new job. Use `retry` for failed jobs and `reprocess` only for an intentional full replay. Originals are immutable hash-addressed copies.

Each run has one session CSV. Local JSONL is append-only and contains IDs, hashes, versions/settings, status, and output metadata—not bodies or keys. Provider-reported usage/cost is preserved in receipts; absent values remain `null`, never zero or a fabricated estimate. Central aggregation is a best-effort read and cannot stop a station.

## Coordinator

Discovery is manifest-driven and bounded to roots the user passes—there is no hard-coded station list or whole-computer scan:

```console
python APIs/coordinator_cli.py APIs/stations "C:\My Work\Stations"
```

Inventory reports purpose, folders, prompts/steps, redacted provider settings, NLP capabilities, dependencies/handoffs, activity, stale roots, invalid manifests, and duplicate identities. To assess a proposed workflow, compare its required provider, local handlers, input types, and destination against these factual fields; missing items require an explicit config/prompt/handler change. No AI is enabled by default, no corpus is uploaded, and the coordinator never rewrites prompts, executes generated code, moves research, or admits canon claims.

## Clean export allowlist

`workbench.export.ALLOW` is the executable allowlist (run `python APIs/clean_export.py SOURCE DESTINATION`): five `.bat` launchers, `README.md`, public `CONFIG/station.json`, `PROMPTS`, and `SCRIPTS`. Export then creates empty runtime folders and a new identity. Everything else—including private config, keys, inputs, originals, output, logs, state, caches, and virtual environments—is excluded.

## Honest limitations

Only UTF-8 text is currently read; PDF/DOCX extraction requires a deliberately configured future handler. Token boundaries are approximated by a conservative character limit because the portable runtime has no tokenizer dependency. Costs are recorded only when a provider reports one; no price estimate is invented. Locks do not auto-break after a crash (remove a demonstrably stale `STATE/station.lock` manually). The included NLP is lightweight deterministic text handling, not a claim that the repository's aspirational NLP/CKG station declarations are implemented. AI explanations are model outputs; they are not Lean compilation receipts, and no Lean compiler integration exists here.
