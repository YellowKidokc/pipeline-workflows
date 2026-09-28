# Readable Prose Transcript Converter

This is the portable ConversionStation copy of the approved YouTube transcript formatter.

It converts a transcript library directly into Obsidian-readable Markdown. The timestamp-heavy intermediate format is not required.

## Output format

- Ordinary multi-sentence paragraphs, normally 900-1,400 characters.
- One linked timestamp heading every five minutes.
- YouTube `>>` speaker changes become an em dash at the start of the new turn.
- Explicit speaker names are retained only when the source supplies a `Name:` label.
- YAML front matter records source, channel, video ID, URL, conversion date, interval, and word count.
- Channel folders are preserved.
- Originals are never changed, moved, or deleted.

## Supported source library

The source root may contain:

```text
subtitles/
  Channel Name/
    Video title.md
    Video title.srt
    Video title.vtt
  playlist_or_channel_dump.md
```

Single-video Markdown, SRT, VTT, and combined channel/playlist Markdown are supported. Failed-download placeholders and empty transcript sections are reported and skipped. Duplicate videos in combined dumps are suppressed when a separate source file already supplies the same video ID.

## Run it

From the ConversionStation root:

```bat
CONVERT_TRANSCRIPTS_TO_READABLE_PROSE.bat "D:\path\to\subtitles" "D:\path\to\output"
```

If the output argument is omitted, output goes to:

```text
Workspace\READABLE_PROSE
```

Run `SETUP.bat` first on a new or moved copy of ConversionStation. Setup installs the local punctuation package. The punctuation model runs locally through ONNX; the first use may download the model files from Hugging Face if they are not already cached. Transcript text is not sent to an analysis API.

## Advanced Python options

```bat
.venv\Scripts\python.exe ReadableProseConverter\readable_prose_converter.py ^
  --src "D:\path\to\subtitles" ^
  --out "D:\path\to\output" ^
  --punctuate
```

Useful options:

- `--timestamp-minutes 5` changes timestamp-section spacing.
- `--target-chars 900 --max-chars 1400` changes paragraph size.
- `--channel "Channel Name"` processes one channel.
- `--source "Channel Name/video.srt"` processes one exact source-relative path.
- `--dry-run` inventories the conversion without writing notes.
- `--force` rebuilds selected sources instead of using incremental state.

The output root contains `.readable_prose_state.json`. It records source size, modification time, generated notes, and video IDs so ordinary reruns process only new or changed sources.

## Bundled implementation

- `readable_prose_converter.py` — library traversal, duplicate control, paragraphs, sparse timestamps, speaker turns, output rendering, and state.
- `Python Clean Library/clean_library.py` — source discovery, metadata parsing, local text cleanup, and punctuation support.
- `Python Clean Library/transcript_polish.py` — loss-preserving SRT/VTT/Markdown parsing, including numeric dialogue after timestamps.
