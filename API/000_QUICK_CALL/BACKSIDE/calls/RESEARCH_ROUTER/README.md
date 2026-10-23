# RESEARCH_ROUTER quick call

Drop files into `input/` and ask one question. The call scans every file and returns:
- a direct answer,
- the strongest quote,
- all relevant findings sorted by relevance,
- and gaps in the corpus.

## Run

```bash
cd D:\GitHub\pipeline-workflows\API\000_QUICK_CALL\BACKSIDE
python 00_quick_call.py --call RESEARCH_ROUTER --focus "Why was the crucifixion so documented that no one can argue with the resurrection?"
```

You can pass multiple focus lines:

```bash
python 00_quick_call.py --call RESEARCH_ROUTER --focus "Question one" --focus "Also look for..."
```

## Input

Put any `.md`, `.txt`, `.csv`, `.json`, `.html`, `.srt`, `.vtt`, or other text files into `calls/RESEARCH_ROUTER/input/`.
YouTube transcripts work best if they still contain timestamps.

## Output

Answers land in `000_QUICK_CALL/OUTBOX/RESEARCH_ROUTER/`.

## Making another one

Copy this whole `RESEARCH_ROUTER` folder under `BACKSIDE/calls/`, rename it, and edit `prompt.txt`.
That is the whole pattern.
