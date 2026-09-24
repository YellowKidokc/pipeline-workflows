# Codex brief — build the `YouTubeIntel` workflow packet

Build a new workflow packet in `D:\GitHub\pipeline-workflows` that watches a folder,
and when a new YouTube channel or video arrives, identifies it, pulls transcripts,
extracts entities, and routes the result.

**Read before writing code.** This repo already defines every contract you need.
Do not invent a parallel one, do not create a new engine, do not restructure folders.

- `README.md` — packet contract, stages, preference layer
- `engines/pipeline/station_base.py` — `StationBase`, `StationVerdict`, `Signal`, `Manifest`
- `engines/pipeline/pipeline_engine.py` — watcher, registry, routing
- `engines/pipeline/llm_hub.py` — queued LLM checkpoints
- `engines/pipeline/stations/classifier.py` — **the reference station; imitate its shape**
- `schemas/signal.schema.json`, `schemas/preferences.schema.json`
- `preferences/defaults.json`

Create the packet with the existing script, not by hand:

```bat
scripts\create_workflow_packet.bat YouTubeIntel
```

---

## Hard constraints

1. **Every station subclasses `StationBase`** and implements
   `process(file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]`
   and `accepts_file(file_path: Path) -> bool`. Nothing else is a station.
2. **Signals go through `emit_signal(SignalType, message, payload)`** and must validate
   against `schemas/signal.schema.json`: type is one of `GAP|DUPLICATE|QUALITY|READY|UPSTREAM`,
   severity one of `info|review|warning|fail|hold`.
3. **`preferences/defaults.json` has `run_behavior.dry_run: true` and
   `preserve_originals: true`.** Honor both. Default behavior is to report what it
   would do, not to do it. Never delete a source file.
4. **LLM calls go through `LLMHub.submit()`**, never a direct `requests.post` to a
   model. The hub is the queue, and the queue is how work reaches other machines.
5. **Secrets come from the environment only.** This is a git repo. `DEEPSEEK_API_KEY`,
   `WEBSHARE_USER`, `WEBSHARE_PASS` are read from `os.environ` and never written to a
   file, logged, or committed.
6. **Reuse the existing tools. Do not reimplement them.**

---

## Reuse these — they already work

| Need | Use | Location |
|---|---|---|
| Channel/video resolution + transcript pull | `ytgrab.py` | `D:\GitHub\Research-Acquisition\yt-bulk-subtitles-downloader` |
| Any file -> markdown | `to_markdown.py` | `D:\GitHub\prior-art-sweep\SCRIPTS` |
| schema.org entity front-matter | `extract_yaml.py` + `PROMPTS/extract_entities.md` | same |
| Prior-art link sweep | the whole `prior-art-sweep` packet | `D:\GitHub\prior-art-sweep` |

Notes that will save you a day:

- `ytgrab.py` writes **one markdown file per video with `[MM:SS]` timestamps per
  segment**. That is the format this packet wants. Do not use the `ytbsd.py` wizard's
  markdown modes — they flatten segments into prose and discard all timing.
- `ytbsd.py` now has `CHANNEL_INFO_TIMEOUT = 300` for channel/playlist enumeration
  and `VIDEO_INFO_TIMEOUT = 15` for single videos. A 2,426-video channel takes ~57s
  to enumerate. Do not reintroduce a short timeout.
- Webshare rotating residential is wired into both the yt-dlp path
  (`ytbsd.webshare_proxy_url()`) and the transcript path (`WebshareProxyConfig`).
  The stored username has **no** `-rotate` suffix; each path adds what it needs.
- **YouTube transcripts carry no speaker labels.** Segments are `{text, start, duration}`.
  Multi-speaker sources (interviews, debates, panels) produce text where host and guest
  are indistinguishable. See the QUALITY signal requirement below.

---

## Stations

### 1. Intake — `youtube_intake.py`

Accepts a `.txt`/`.json`/`.url` file dropped in `INPUT/` containing one or more YouTube
channel or video URLs, or a bare handle like `@gracetoyou`.

- Normalize to canonical URLs. Resolve with `ytgrab`'s helpers.
- Compute `Manifest.compute_hash` and check against the known-channels registry
  (`CONFIG/known_channels.json`). Already present -> `DUPLICATE` signal, severity
  `info`, and stop.
- **LLM checkpoint (DeepSeek, `strong` lane) via `LLMHub.submit()`.** Prompt lives in
  `PROMPTS/identify_channel.md`. Given channel title, description, and 20 sampled video
  titles, return strict JSON:

```json
{
  "channel_name": "",
  "owner": "",
  "domain": ["theology", "physics", "history", "philosophy", "other"],
  "stance": "supports | challenges | neutral | unknown",
  "scholarly_level": "popular | semi-technical | academic",
  "primary_speaker": "",
  "is_interview_format": true,
  "relates_to_known_channels": [{"channel": "", "relation": "same-topic | cites | rebuts | competitor", "confidence": 0.0}],
  "worth_processing": true,
  "reason": ""
}
```

- `worth_processing: false` -> `QUALITY` signal, severity `review`, route to `REVIEW/`.
  A human decides. Do not silently drop.
- On success append to `CONFIG/known_channels.json` and emit `READY`.

**`relates_to_known_channels` is the point of this packet.** It is what turns a pile of
channels into a map. Ground it in the registry — the model may only cite channels that
already exist there, never invented ones.

### 2. Transform — `youtube_transform.py`

- Call `ytgrab.py` as a subprocess with the resolved URL. Capture its exit code and
  output paths. Do not import its internals.
- Per-video markdown lands in `OUTPUT/<channel>/`.
- Run `extract_yaml.py` per file for entity front-matter.
- **Chunk budget:** `extract_yaml.py` uses `CHUNK_CHARS = 6000`. Log chunks attempted
  vs. chunks that returned data.

### 3. Validate — `youtube_validate.py`

Gate before anything is routed:

- **Coverage:** videos with a transcript / videos found. Below 0.5 -> `QUALITY`, `review`.
- **Extraction integrity:** if any chunk timed out or returned nothing, emit `QUALITY`
  severity `warning` naming the file and chunk count. **This is a real bug in the current
  pipeline** — `extract_yaml.py` prints `done` after a failed chunk and writes
  front-matter as if it succeeded, producing empty-but-plausible output. Fix that print,
  and never let a partially-extracted file pass as complete.
- **Speaker ambiguity:** if intake said `is_interview_format: true`, stamp every output
  file's front-matter with `x-speaker-attribution: unreliable` and emit `QUALITY`,
  severity `info`. Claims from interview transcripts must not be confidently attributed
  to the channel owner.

### 4. Route — `youtube_route.py`

Honor `preferences.routing.allowed_destinations`. Default destination is `REVIEW`.
NAS archive, vault drop, and Postgres warehouse are opt-in per packet prefs.

---

## Distributed processing

David wants heavy NLP off the NAS and onto a laptop, with more machines added later.

**Use `LLMHub`'s queue as the seam. Do not build a new job system.** It already writes
jobs to `D:\FAP\_queue` and has `process_queue(backend_filter=...)`.

Scope for this build:

- Stations `submit()` jobs and return; they never block on inference.
- A worker entry point, `SCRIPTS/run_worker.bat`, calls `process_queue()` in a loop so
  any machine that can see the queue directory can drain it.
- Jobs carry a `backend_filter` so a GPU laptop takes the `strong` lane and the NAS
  takes `fast`.

Explicitly **out of scope** — do not build: leader election, job stealing, retry
backoff across hosts, or a scheduler. A shared queue directory plus per-host backend
filters is enough for two or three machines and is reversible. Say so in the README
rather than designing for a fleet that does not exist yet.

---

## Deliverables

```
workflows/YouTubeIntel/
  INPUT/ OUTPUT/ REVIEW/ ARCHIVE/ ERROR/ LOGS/
  CONFIG/settings.json          # paths to ytgrab, prior-art-sweep, queue dir
  CONFIG/known_channels.json    # the registry; starts as []
  PREFS/preferences.json        # overrides only, inherits defaults.json
  PROMPTS/identify_channel.md
  PROMPTS/relate_channels.md
  SCRIPTS/youtube_intake.py
  SCRIPTS/youtube_transform.py
  SCRIPTS/youtube_validate.py
  SCRIPTS/youtube_route.py
  SCRIPTS/run_worker.bat
  RUN_PIPELINE.bat RUN_THIS_STAGE.bat TROUBLESHOOT.bat
  README.md
```

Plus `tests/` fixtures: one channel URL, one video URL, one already-known channel
(to prove the DUPLICATE path), and one transcript-less video (to prove the coverage gate).

## Definition of done

- `RUN_PIPELINE.bat` runs end to end on the fixtures in dry-run mode and changes nothing.
- Every emitted signal validates against `schemas/signal.schema.json`.
- No secret appears in any file under the repo.
- A failed extraction chunk produces a `QUALITY` signal, never a silent pass.
- `README.md` states plainly what was built, what was deliberately left out, and the
  speaker-attribution limitation.

Report anything in the existing engine that had to change. Prefer asking over guessing
if a contract is ambiguous.

---

# Addendum 1 — existing watcher, reuse it

`D:\GitHub\Research-Acquisition\youtube-transcript-ytdlp\watch_downloader\` is a
Chrome extension plus a local server on `:8765` with a SQLite log, a dashboard,
and batch download. It already shells out to ytbsd. Built, not yet used
(`watch_log.db` does not exist).

It is a **different trigger** from this packet: it fires when David watches a
video in Chrome, not when a file lands in a folder. Complementary, not duplicate.

- Do not build a second dashboard or a second SQLite log. If this packet needs a
  browser trigger, extend that server to drop a file into `INPUT/`.
- Its `config.json` has `"ytbsd_args": ["--free-proxies"]`, which forces the free
  proxy swarm. Webshare rotating residential is now live and wired. Drop that flag.

# Addendum 2 — AI notes are mandatory

Read `docs/AI_NOTES_STANDARD.md` before writing any station. Every LLM call in
this packet emits a `station_note` under the `NSE-1.0` envelope.

Locations, no exceptions:

```
workflows/YouTubeIntel/NOTES/<station>/<object_id>.note.yaml
<artifact_path>.note.yaml
```

A station that produces no note has not finished. Wire note emission into
`LLMHub` dispatch so it is structural, not per-station discipline — any station
added later inherits it for free.

Use `prompts/write_ai_note.md` verbatim as the note-writing prompt.

Also generate `schemas/ai_note.schema.json` from the standard and validate every
note against it on write. Rules R1–R8 in the standard are the requirements;
`could_not_determine`, `negative_results` and at least one `drift_gates` entry
are required fields, and a note whose `source_hash` no longer matches its input
must be treated as absent rather than trusted.
