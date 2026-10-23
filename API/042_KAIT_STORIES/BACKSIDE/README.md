# 042_KAIT_STORIES

Map a paper to Kait Willett moves: three alternative spines with loop IDs for OpenWriter.

- Script: `42_kait_stories.py` (run it through `ONE_MENU.bat 69`)
- Works on: papers
- Menu options it accepts: limit, workers, provider, model, focus, redo, outbox
- Standing focus: `FOCUS.md` (2-4 lines; appended to every prompt this station sends)

## What it does

For each input paper, the station reads the source text and the Kait Willett moves library, then asks the model to build **three alternative spines**. Every spine is a sequence of Kait moves (with IDs like `K01`, `K05`, `K33`) mapped to the paper's own canonical points.

The output is both human-readable and importable into OpenWriter:
- `<note> · 042_KAIT_STORIES.md` — the three spines with explanations
- `<note> · 042_KAIT_STORIES.json` — structured data including an `openwriter_outline`

## Outputs

Per item, in a dated folder that is never overwritten: `02_RUNS/042_KAIT_STORIES/<date>/` with `.json`, `.xlsx`, `.html`, `.run.json` (receipt: source hash, model, prompt version, focus text + hash, tokens, time, errors), `.md` where the station writes prose, `calls/<goal id>-<n>.json` (every reply), and `steps.log` (every step it took).
