# GitHub Prompt: Model Slot Flattening

Problem: model knowledge is too scattered. Models must be discoverable from top-level `models/`.

Goal:

- `models/MODEL_REGISTRY.json` is the single source of truth for M01-M12 and P01-P07.
- `models/MODEL_HEALTH.json` records degraded/empty/placeholder slots.
- `models/MODEL_FALLBACKS.json` records safe fallbacks.
- `models/preference-chain.json` records P06 -> P05 -> P01/P03 -> P07 flow.
- Any nested model references in stations should point back to these files.

Do:

- Find hardcoded model paths.
- Replace with registry lookups where practical.
- If a station needs a local config, keep it as a thin adapter to top-level `models/`.
- Add docs explaining "configs in GitHub, weights on NAS."
- Add tests or smoke checks for registry parse.

Do not:

- Upload weights.
- Upload vector indexes.
- Hide model state inside station folders.
- Break existing station registry paths.

Expected output:

- A move/update plan.
- Code changes for registry lookup if low-risk.
- Docs that make the model layer obvious to online Codex.
