# 091_CHAT — Desk Chat

A conversational desk tool that routes every message through Forge.

## Files

- `station.json` — station metadata for the workbench.
- `91_chat.py` — batch runner: reads INBOX notes, sends them to Forge as chat messages, writes replies to OUTBOX.
- `desk_chat.html` — interactive panel: type messages, stream replies, keep follow-up context. Open this from nerve's launcher.
- `templates/chat_system.txt` — default system message for batch runs.

## Usage

- **Batch:** drop notes into `INBOX` and run `1 RUN HERE.bat`. Each note becomes a user message; the assistant reply is written to `OUTBOX`.
- **Interactive:** open `desk_chat.html` in a panel. Type messages and press Send (or Ctrl+Enter). Streaming and follow-up context are preserved.

## Rules

- All AI calls go to Forge at `FORGE_URL` (default `http://127.0.0.1:8790`), endpoint `/v1/chat/completions`.
- No provider URL, key, or model selector lives in this HTML.
- If Forge is down, the panel says so and does not fall back to a provider.
