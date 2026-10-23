# Desk Reconciliation

Classification reconciliation (Stage 5) routed through Forge.

Drop an atom JSON file into INBOX and run to receive AI-proposed classifications. The proposal is editable and must be staged through the existing **Stage Candidate** flow — the AI step never stages.

Canon engine communication (load target, blast radius, stage candidate) stays at `http://127.0.0.1:8765` and is untouched. Only the AI-propose step moves to Forge's local route.
