# Drop Pipeline

Drop a UTF-8 Markdown, text, SRT or VTT file (or a folder containing those files) into `Workspace/DROP`. The watcher waits for the copy to settle, sends the complete text to DeepSeek in chunks, and copies it into the selected YouTube, document, prompt or review workflow. Local NLP then prepares the Obsidian note. Source files stay unchanged.

## Start on Windows

1. Install Python 3.11 or newer (64-bit) with its command available as `python`.
2. Extract this folder anywhere writable and run `SETUP.bat` once. Internet is needed to install dependencies.
3. Set `DEEPSEEK_API_KEY` in the environment of the account running the watcher. It requires a funded DeepSeek API account. No key is included or stored by this package.
4. Run `START.bat`. Leave its window open while processing. Put files into `Workspace/DROP`.
5. Open `Workspace/OBSIDIAN_READY` as an Obsidian vault, or copy its generated notes into your vault. Open `Library Index.md` to browse.

`STATUS.bat` displays job receipts. `STOP.bat` requests a graceful stop after the current job. Starting again skips completed content. Installation does not register a startup service. The computer must stay awake and the watcher must be running.

## Linux and macOS

Use `sh setup.sh`, then set the API key in your environment and run `sh start.sh`. Python 3.11+, pip and venv are prerequisites; your operating system may package venv separately. The same source package is used on all platforms. Rebuild `.venv` on each computer; virtual environments are not portable.

## Folder and workflow layout

- `Workspace/DROP`: watched intake, including subfolders.
- `Workspace/WORKFLOWS/<route>/INPUT`: source packets, routing receipts and jobs. Each route has `workflow.json` and an `OUTPUT` folder.
- `Workspace/OBSIDIAN_READY`: Markdown, YAML properties, topic tags, readable text, highlights, research signals, link notes and a library index.
- `Workspace/ORIGINALS`: byte-identical source copies, indexed by SHA-256.
- `Workspace/STATE`: persistent jobs and local document index.

A single watcher supervises both intake and all route queues. Each route chooses its own stage sequence. This avoids requiring a separate always-running process per route. The review route waits for an explicit decision.

You may rename or relocate the outer package and choose any workspace location. Internal folders are created automatically. To use another location, run from this package directory:

    python -m drop_pipeline.runner watch --workspace "YOUR CHOSEN LOCATION"

With the bundled virtual environment, use `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on Linux/macOS instead of `python`. The existing repository interface also accepts `SYSTEM.bat drop watch --workspace "YOUR CHOSEN LOCATION"`.

## Local NLP and Obsidian

The default stages are normalization, local TF-IDF analysis, multiple topic views, reading highlights, research signals and Obsidian output. Prompts also receive a section/placeholder inventory; they are never executed. You can enable or disable optional registered stages in each route's `workflow.json`. Add topic patterns to the workspace `pipeline.json` `categories` object, using a lowercase identifier and a regular expression.

Extractive summaries quote source sentences. Highlights decorate copies of those sentences. Categories can overlap on the same paper. Scripture and year detection use lexical patterns, not a complete entity model. Cross-document links are local vocabulary-similarity suggestions with a supporting passage, not verified agreement, contradiction or proof. Drop your own papers into the same workspace to include them in these suggestions.

There is no fixed source-character cutoff. DeepSeek receives every chunk; conflicting chunk decisions go to review. Full transcripts remain in the generated notes. Summary excerpts are intentionally selective. Timed cues are retained when supplied; speaker identities are not guessed. Audio transcription/diarization, PDF/DOCX conversion, external archive delivery and deep relationship reasoning are outside this initial text pipeline.

## Recovery and adding layers

Rebuild local output after changing a workflow, without another routing call:

    python -m drop_pipeline.runner reprocess --workspace "YOUR LOCATION"
    python -m drop_pipeline.runner once --workspace "YOUR LOCATION"

If the watcher is running it will consume the queued work itself. Optionally select `--job "relative/path.md"` or `--route document` for reprocessing. Resolve an uncertain route with:

    python -m drop_pipeline.runner resolve --workspace "YOUR LOCATION" --job "relative/path.md" --route document

Supported choices are youtube, document and prompt. The original review receipt remains preserved. Inspect a failed/interrupted job before explicitly retrying:

    python -m drop_pipeline.runner retry --workspace "YOUR LOCATION" --job "relative/path.md"

A routing retry can repeat API costs; failed routing is not automatically retried. Local processing retries reuse the source packet. `relink` rebuilds the local connection index. Unsupported extensions are left untouched and are not processed. This release accepts UTF-8 text only.

## Portability and distribution

Distribute the small source ZIP, not `.venv`, caches, credentials or your corpus. To move an existing library, stop the watcher and copy `Workspace` along with the package, then rerun setup on the destination. Receipts use relative paths and read older Windows path separators. Dependency setup and API routing need network access; subsequent NLP runs locally on CPU. Processing speed and memory use depend on file and library size. Arbitrarily large libraries have not been load-tested.
