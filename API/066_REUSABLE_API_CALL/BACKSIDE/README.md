# 66 Reusable API Call

This is the copy-and-configure station for repeatable API work.

## The three switches

1. PROMPT.md controls the analyst's role and permanent rules.
2. questions.yaml controls the individual questions. Set enabled true or false, add questions, or reorder them.
3. ACTIVE.yaml selects the prompt, question file, execution mode, and output profile. outputs.yaml defines the available output contracts.

The Python engine should normally remain unchanged. Copy the whole station when a job becomes permanent, give the copy a new number and label, then specialize only the BACKSIDE configuration.

## Front-side use

- Drop one urgent paper into INBOX/00_PRIORITY and double-click 1 RUN HERE.bat.
- Or double-click 2 RUN ON FOLDER.bat and drag a folder into the window.
- Select how many documents and concurrent calls.
- Add up to five one-time focus questions if needed.
- Confirm. Results and receipts go to OUTBOX and the standard dated run folders.

## Changing the job

- Different analysis: edit PROMPT.md or select another prompt in ACTIVE.yaml.
- Different questions: change enabled in questions.yaml.
- Different result shape: change active_output_profile.
- One call per question: execution.mode separate.
- One combined call: execution.mode bundle.

Do not put API keys in this folder. Providers, keys, retry policy, fallback, caching, model names, and concurrency remain owned by _system.
