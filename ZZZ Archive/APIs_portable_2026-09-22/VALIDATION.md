# Portable package validation â€” 2026-09-22

- Python environment created successfully from the included requirements.
- Nine tests passed: relocation/path handling, nested inputs, original bytes including BOM/CRLF, invalid-stack rejection, durable session CSVs, duplicate-launch locking, private-file export exclusion, mocked Evidence success/failure processing, mocked Lean reader processing, and watcher settling/no-repeat behavior (some tests cover multiple checks).
- Evidence processing was exercised from a temporary folder with spaces in its name; both successful and failed files appeared in the session CSV. The preserved original matched byte-for-byte.
- Lean reader test wrote its own session CSV and retained the input source.
- All packaged Python files parsed. Executable absolute workstation/NAS defaults were replaced with package-relative destinations.
- Git ignore checks confirmed that local keys, private inputs/outputs, and the Python environment are excluded.
- The clean ZIP uses an explicit file allowlist, with SHA-256 hashes inside the archive. All exported hashes were verified.
- A clean extraction in a different folder passed setup diagnostics, Lean inventory, and Evidence CLI startup from a different working directory.

No live API requests, model-availability check, Lean compilation, or real second-computer deployment was performed. Supporting legacy tools were packaged and syntax-checked; they were not all exercised end-to-end. Canonization is a prepared folder handoff, not automated admission. Fruits grading is a reserved output destination, not a bundled grading application.

Run the tests with `.venv\Scripts\python.exe -m unittest discover -s TESTS -v` from this folder.
