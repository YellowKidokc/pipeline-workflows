# Portable blank station

This folder is independent: rename or move it (including to a UNC path) and its identity/history remain in `STATE`. Run `SETUP.bat`, edit `CONFIG/station.json` and prompts, place UTF-8 text/Markdown in `INBOX`, then run `RUN_ONCE.bat`. `WATCH_INBOX.bat` runs only in its visible terminal.

The default provider is credit-free `mock`. For a live provider, explicitly set `provider.name`, `provider.model`, and its documented environment variable (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, or `OPENROUTER_API_KEY`). Alternatively put `api_key` in ignored `CONFIG/private.local.json`. Never share that file.

Priority receives three jobs for each ordinary job while both queues are populated. Series files are recursively found and lexically ordered by relative path; the default policy processes each independently. Default concurrency is 12 **per running station**, so three stations can attempt 36 calls. Configure lower values around account rate limits.

Completed work is keyed by source and workflow/prompt hashes. A move resumes history; changed source/workflow is a new job. `retry` preserves successful steps; `reprocess` deliberately clears job state. Outputs are data only and are never executed. Originals are preserved by SHA-256.
