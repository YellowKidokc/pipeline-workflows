# Portable Conversion Station

This folder is self-contained and can be copied, renamed, or moved. Every launcher resolves paths from its own location. After moving to another computer or drive, run `SETUP.bat` (or `REPAIR_AFTER_MOVE.bat`) to rebuild the local virtual environment.

## First run

1. Run `SETUP.bat` while connected to the internet.
2. Use `IMPORT_TO_DROP.bat` to copy a file or folder into `Workspace\DROP` without changing the source.
3. Run `PROCESS_ONCE.bat`, or leave `START.bat` open to watch continuously.
4. Read converted notes in `Workspace\OBSIDIAN_READY` and direct conversions in `Workspace\CONVERTED`.

## Included capabilities

- Preserved, SHA-256-indexed originals for Markdown, text, SRT, and VTT intake.
- Local transcript formatting and Obsidian-ready output.
- Direct readable-prose transcript conversion with five-minute timestamp headings, long paragraphs, conservative speaker-turn markers, channel preservation, and incremental reruns.
- Document, PDF, HTML, spreadsheet, image, audio/video, and URL conversion through the bundled conversion engine and MarkItDown dependencies.
- TubeScribe command-line installation for YouTube audio/transcript acquisition.
- Portable Subtitles MD and Media Transcript Obsidian plugin bundles.
- Relative paths throughout the active package.

Run `INSTALL_OBSIDIAN_PLUGINS.bat` and enter a vault path to install both bundled plugins. The installer leaves any existing plugin folder unchanged; enable newly installed plugins in Obsidian's Community plugins settings.

## Moving the station

Stop the watcher with `STOP.bat`, copy this entire folder, then run `SETUP.bat` at the new location. Do not copy `.venv` between computers; it is machine-specific and is ignored by Git. `Workspace` may be copied when you want its originals, receipts, and output to travel with the station.

No API key is stored here. DeepSeek routing is optional and reads `DEEPSEEK_API_KEY` from the environment when configured.

## Readable-prose transcript conversion

Run:

```bat
CONVERT_TRANSCRIPTS_TO_READABLE_PROSE.bat "D:\path\to\subtitles" "D:\path\to\output"
```

This goes directly from raw transcript Markdown/SRT/VTT to the approved readable format; the older timestamp-per-paragraph layer is not required. See `ReadableProseConverter\README.md` for the complete behavior and advanced options.
