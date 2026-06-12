# GitHub Prompt: Queue and Exports Workflow

Goal: make David-facing input/output lanes simple.

Queue:

```text
queue/01_PROMPTS/
queue/02_FILES/
queue/03_WORKFLOW_IDEAS/
queue/04_CORRECTIONS/
queue/05_REVIEW_DECISIONS/
```

Exports:

```text
exports/active/
exports/ready/
exports/published/
exports/archived/
```

Tasks:

1. Ensure `workflows/prompt-evolution.json` uses queue prompts safely.
2. Add or refine export manifest handling.
3. Define cleanup ledger rules for `exports/active/*/CLEANUP_CANDIDATES`.
4. Keep bulky export artifacts out of GitHub unless intentionally packaged.
5. Add docs showing where partial series builds go.

Expected output:

- Clear queue/export docs.
- Optional script for export manifest validation.
- No deletion without approval ledger.
