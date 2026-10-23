# 23B_HTML_ASSEMBLY

Atom JSON/YAML -> one standalone HTML page per atom. No API calls.

Sits right after 23_CPEL. Takes atom files that follow the atom contract
(`Faith-through-physics-atoms\_template\schemas\atom-api-contract.md`) and
builds the black atom card for each one. Every output page is self-contained:
CSS, renderer, lens grammar and atom data are all baked into the single `.html`
file, so it opens by double-click, works offline, and can be published as-is.

Run:
- `1 RUN HERE.bat` — every `.json` / `.yaml` atom in `INBOX\` becomes a page in `OUTBOX\`.
- `2 RUN ON FOLDER.bat` — drag a folder or a single atom file onto it (or paste the path).

Output:
- `<atom>.html` — the finished standalone page.
- `<atom>.receipt.json` — what it was built from (source hash, shell version, warnings).
- `index.html` — a list of every page built, with type, ID and warning count.

The template is read from `SHELL_DIR` in `settings.txt` (default: the live
`Faith-through-physics-atoms\_template\html`). If that folder is missing, the
snapshot in `BACKSIDE\shell` is used instead.
