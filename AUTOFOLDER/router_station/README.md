# Portable File Router

Drop `route.py`, `FolderWatcher.py`, and `route.yaml` into any folder to turn it into a routing station.

## What it does

- Watches one or more source folders (configured in `route.yaml`).
- Routes incoming files through ordered rules.
- Supports `copy`, `move`, and shell `command` actions.
- Keeps state in `.route_state.json` so files are not re-routed.
- Logs every action to `route.log`.

## Usage

```bash
python route.py                 # watch forever
python route.py --backfill      # route existing files once, then watch
python route.py --backfill --once  # route existing files once, then exit
python route.py --dry-run       # log what would be done without doing it
```

## Configuration

Edit `route.yaml`:

```yaml
log: route.log
state: .route_state.json

watch:
  - "../../obsidian_transcripts/*"

routes:
  - name: "Markdown transcripts to CKG inbox"
    match: "*.md"
    action: copy
    destinations:
      - "//192.168.2.50/h_hp/Desktop/APIs/APIs/CKG/INBOX"

  - name: "Run custom processor on videos"
    match: "*.mp4"
    action: move
    destinations:
      - "_outbox/videos"
    command: "python process_video.py {path}"
```

### Placeholders for commands

- `{path}` — full path to the file
- `{name}` — filename with extension
- `{stem}` — filename without extension
- `{ext}` — file extension
- `{parent}` — parent directory

## Portability

The router resolves paths relative to the folder containing `route.py`. You can copy the three files to any folder and update `route.yaml` without changing the script.
