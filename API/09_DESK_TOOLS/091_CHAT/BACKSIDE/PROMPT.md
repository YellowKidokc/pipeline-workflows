# Desk Chat

Interactive AI chat routed through Forge.

Drop a `.md` file into INBOX to seed the conversation with its contents, or run the desk panel and type messages directly. Every assistant reply is a Forge `/v1/chat/completions` call. Provider selection, keys, and model routing live in Forge only — this station never calls a provider itself.
