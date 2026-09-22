# APIs — portable research workbench

Copy this entire folder to a writable location on another Windows computer.
The source scripts, prompts, templates, and empty working folders travel together.
Python 3.11 or newer must be installed as `python`. Setup and API processing need internet access.

## Start here

1. Run **0_SETUP.bat** once on each computer. It creates a local Python environment and installs the requirements using their full path.
2. Run **1_ADD_API_KEY.bat** to enter your DeepSeek key privately, or set `DEEPSEEK_API_KEY` in your environment.
3. Run **5_CHECK_SETUP.bat** to check dependencies, the key's presence, and input counts. This does not contact the API or verify the key's balance.
4. Drop papers or folders into **EVIDENCE/INBOX**, and Lean files or whole Lean projects into **LEAN4/INBOX**.
5. Run **START_HERE.bat** to choose a job, or **4_WATCH_INBOXES.bat** to keep both inboxes running automatically.

The watcher makes paid API requests. Keep its window open and the computer awake.
It waits for the input file listing and sizes to settle (15 seconds by default).
For large network copies, finish copying outside INBOX and then place the completed folder inside it.
Ctrl+C stops the watcher. Inspect session receipts after an interrupted run before restarting.
This package does not install a Windows startup service.

## Familiar folders

| Folder | Job |
|---|---|
| **SCRIPTS** | Start menu, setup, watcher, export, and shared orchestration |
| **EVIDENCE** | Existing article review engine, templates, indexes, and original-preserving stacked output |
| **LEAN4** | Existing source reader, one paper per unique Lean source, growing reading library, and separate compiler checks |
| **CANONIZATION** | Original candidate material, review decisions, prepared output, and human-admitted material |
| **CONFIG** | Example settings and private local API configuration |
| **LOGS** | Watcher run output |

The package starts with empty working folders; `.gitkeep` only keeps their structure in Git.
The NAS production folders are not moved or changed by this package.

## Launchers

| Launcher | What it does |
|---|---|
| 2_RUN_EVIDENCE | Processes supported papers with 12 workers and DeepSeek |
| 3_RUN_LEAN_READER | Counts available Lean sources, asks only how many, and processes with 12 workers |
| 4_WATCH_INBOXES | Watches both input folders and processes available work without a count prompt |
| 6_CHECK_LEAN_PROOFS | Runs the existing Lean compiler-check path; requires Lean/Lake and a valid project |
| 7_INVENTORY_LEAN | Local source inventory, no API requests |
| 8_EXPORT_PORTABLE | Builds a clean source-only ZIP outside the package |

Workers are per lane: running both lanes at once can use 24 workers. To change this, copy
`CONFIG/settings.example.json` to `CONFIG/settings.local.json` and edit `workers` (1–30).
Use `watch_lanes` to select one lane if desired. Provider limits still apply.
The DeepSeek model is configurable; the inherited Lean workflow uses `deepseek-flash`.
This packaging pass did not make a live API request or verify current model availability.
The standard Evidence launcher uses DeepSeek only, with no paid fallback to another provider.

## Inputs and results

Evidence accepts `.md`, `.txt`, `.html`, `.htm`, and `.tex`, including nested folders.
It retains the existing priority and series conventions: `INBOX/_PRIORITY` and `INBOX/SERIES/<name>`.
Successfully processed inputs move into `PROCESSED_ORIGINALS`; failures go to `FAILED`.
Keep your master originals outside the input queue and drop copies for processing.
Outputs include `OUTBOX/FOR_SUBSTACK`, `OUTBOX/MASTER_INDEX`, and per-session `OUTBOX/RUNS/.../PAPERS.csv`.
The generated layer is above an original-byte/hash boundary. Broken existing stack hashes stop processing.

Lean reader mode accepts `.lean`. It preserves source files and writes the reading library to
`LEAN4/OUTBOX/READING_LIBRARY`, including the growing `MASTER_LIST.csv`.
Session folders remain under `LEAN4/OUTBOX/RUNS`. `_PRIORITY` takes precedence while it contains sources;
remove or relocate completed priority inputs when you want the regular inbox processed.
The reader's existing hash/checkpoint logic avoids repeating completed source reviews.

Copy complete Lean projects with their `lean-toolchain`, Lake configuration, and imports for compiler checks.
Loose files may be readable but blocked from compilation. Compiler setup and dependencies are separate from Python setup.
Generated reader papers are explanations, not compiler receipts or automatic canon decisions.

`EVIDENCE/OUTBOX/FRUITS` is an empty output destination. The separate Fruits grading application
is not included in this four-folder package. It can be connected in the next iteration.

## Other existing tools

The supporting Evidence Python tools are retained under `EVIDENCE/SCRIPTS`: synthesis, argument building,
series evaluation, sidecars, database synchronization, and proof-companion preparation.
Their machine-bound default paths now point inside this package. Consult each tool's arguments before running it;
they are not automatically chained by the watcher. The older shared Lane 4 breakdown tool is also retained.
The legacy proof bridge generates formal scaffolding; its outputs must not be interpreted as independent
proof of the paper's substantive claims. Use the separate source-aware reader and compiler receipts.

## Secrets and updates

`CONFIG/keys.local.json` contains your API key in local plaintext. It is excluded from Git and the clean export.
Do not copy that file to a public location. Existing environment variables also work.
The export is the recommended way to transfer an empty installation; copying a used folder also copies its papers and local keys.
Do not copy `.venv` between computers; rerun setup. No model weights, private corpus, cached outputs, executable watcher binary,
API credentials, or production databases are bundled.

`SOURCE_MANIFEST.json` records the original source hashes and their relative source locations.
`PACKAGE_FILES.json` is the explicit export allowlist. Files added later must be deliberately added to it.
Runtime data is ignored by Git; this package does not push or publish the repository.

## Canonization

Put candidate material in `CANONIZATION/INBOX`, review records in `REVIEW`, and prepared presentations in `OUTBOX`.
`ADMITTED` is reserved for decisions you endorse. No AI run moves a claim there automatically.
The claim register and admission workflow can be connected after your next design discussion.
