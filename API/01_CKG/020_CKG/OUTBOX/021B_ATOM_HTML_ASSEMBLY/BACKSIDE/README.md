# 21B Atom HTML Assembly

Drop the JSON/YAML results from the separate claim, evidence, proof, and Lean calls into an INBOX lane, then run 1 RUN HERE.bat. Use 2 RUN ON FOLDER.bat for another folder.

The station writes combined JSON, YAML, Markdown, HTML, a SHA-256 receipt, index.html, and _last_run.txt to OUTBOX. Replaced files move to OUTBOX/_older/<timestamp>/.

Shell order: --shell, ATOM_SHELL_HTML, a path found in API/_system/config/paths.json, then the bundled fallback shell. Adjacent shell assets are copied to OUTBOX/_assets. No API key is needed, and only explicit source relationships become graph edges.
