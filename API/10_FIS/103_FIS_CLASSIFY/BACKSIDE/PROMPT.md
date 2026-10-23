# Classify

Reports the engine's rule-based folder classification of 101's scan (kind + domain, with evidence and denominators). The folders the rules leave unresolved (open questions) go to Forge, POST {FORGE_URL}/v1/chat/completions, with folder name, file names and extension mix only. Answers are shadow inferences. Per-document classification is not in the engine yet.

The only model call is the engine's Forge request in understand.escalate_forge: a JSON-only folder classification (kind, domain, purpose, confidence) from folder name, file names and extension mix. No file contents, no provider URL or key in this station.
