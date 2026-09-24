# Review corrections — 2026-09-20

- Paper grading, axiom mapping, wiki model jobs, and classification receive complete input text. The shared queue no longer crops input at 8,000 characters.
- The shared hub defaults to this repository's prompts. Explicit prompt-directory overrides remain supported.
- Local generation requests a context budget sized conservatively from the full UTF-8 prompt plus output allowance. Provider-reported output exhaustion is a failed review, not completion. Actual model/server capacity remains finite; no live capacity claim is made here.
- Paper grading surfaces failed jobs for review, rejects invalid scores, and invalidates previous source-less or changed-source grading state.
- God Is is the single admitted root axiom. Supporting nodes are not additional axioms. Mapping confidence no longer depends on covering 22 axioms. Warranted uncertainty is preserved in voice assessment.
- CorpusTriage's main entrypoint uses the content-based processor, supports invocation outside the repository, and does not write classification sidecars into the source corpus. Its ranking is explicitly heuristic relevance, not evidence strength.
- Epistemic intake's adversarial pass receives the complete original, extraction, and evaluation. Prior synthesis checkpoints without this source version are not reused as current synthesis.
- PaperGrading and KnowledgeRefineryBackplane packet entrypoints remain unconnected. They now fail explicitly with NOT CONFIGURED and exit 2. This correction does not implement the entire planned backplane.

Validation uses temporary fixtures and mocked model dispatch; no production corpus or paid API calls are required.
