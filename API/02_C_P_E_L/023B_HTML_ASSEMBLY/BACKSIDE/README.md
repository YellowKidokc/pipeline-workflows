# 23B HTML Assembly

Sits right after 23_CPEL. Takes atom files (claim, evidence, proof, lean, bridge, definition) and builds the black atom card for each one as a **standalone HTML page**. No API calls; it costs nothing and gives the same page every time.

Same layout as every station: **BACKSIDE** (code, settings, shell snapshot), **INBOX** (00_PRIORITY, 01_SERIES, 02_GENERAL), **OUTBOX**, two buttons.

## Buttons

- **1 RUN HERE**: every `.json` / `.yaml` atom in INBOX becomes a page in OUTBOX.
- **2 RUN ON FOLDER**: drag a folder or a single atom file onto it (or paste the path).

## What goes in

Atom files that follow the atom contract: `D:\GitHub\Faith-through-physics-atoms\_template\schemas\atom-api-contract.md`. Examples are in `D:\GitHub\Faith-through-physics-atoms\_template\schemas\examples\` (claim, evidence, proof, lean, each as YAML and JSON) and in `D:\GitHub\Faith-through-physics-atoms\_template\html\sample-*.json`. Missing fields don't stop a page: the card shows **TODO** in red, and the run prints a warning.

## What comes out (OUTBOX)

- `<atom>.html`: the finished page. Everything is inside the one file (style, renderer, lens grammar, the atom's data), so it opens by double-click, works offline, and can be published as-is.
- `<atom>.receipt.json`: what it was built from (source hash, shell version, warnings).
- `index.html`: a list of every page built, with type, ID and warning count.

Rerunning skips atoms whose file and template haven't changed. Change the template and every page rebuilds on the next run.

## The template

Uses the live template in `Faith-through-physics-atoms\_template\html` (change `SHELL_DIR` in `BACKSIDE\settings.txt`). If that folder isn't there, it uses the snapshot in `BACKSIDE\shell`. Edit the look in the live template, not in the pages.

## What it doesn't do yet

23_CPEL still writes Markdown. For CPEL's output to flow straight into this station, CPEL's four calls need to return atoms in the contract's JSON shape and save them. Until then, atoms come from the examples or from any call that returns contract JSON.
