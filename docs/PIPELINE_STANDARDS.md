# Pipeline Standards

The rules David and Claude agreed on (2026-09-24 → 2026-09-27) while building ONE_MENU, the YouTube chain and the analytical stations.
When a new station, script or report is built, it follows these. When an older one is touched, bring it up to these.

Related docs in this folder:
- `station-contract.md`: status values and never mutating inputs
- `review-corrections.md`: full input text, no cropping
- `AI_NOTES_STANDARD.md`: the handoff note each LLM call leaves
- `repo-packaging.md`: what goes in Git

The live build is `D:\GitHub\Research-Acquisition\API_ALL` (GitHub `YellowKidokc/API_ALL`, **public**). Its build plan is
`CODEX_MASTER_PROMPT.md`, and its map of existing code is `SYNTHESIS_STATIONS_AND_PAPER_INTELLIGENCE.md`.

---

## 1. One front door

- **One batch file, `ONE_MENU.bat`, identical everywhere it is copied.** Every variant (turbo or not, provider, worker count, how many items)
  is an *option* or a *routine*, never a new .bat file. Adding a station = one folder + one entry in `config\stations.json`.
- **Every run asks the same four questions:**
  1. What to run: one number, several (`22 23 24`), or a routine letter.
  2. Options: turbo, how many, provider, redo.
  3. Extra focus?: 0 = none, a saved focus number, or free text.
  4. Confirm: show the exact plan and the token estimate, then run.
- Everything also runs without questions (`ONE_MENU.bat 22 23 --turbo --limit 5 --focus "..."`).
- The menu shows the **top 20 stations by rank**; `M` shows all of them. David's manual rank always wins over usage statistics.
- Only ask for options a station actually accepts. Never fake a flag.

## 2. Names and numbers

- **Every station is a folder `NN_NAME`, and its main script is `NN_name.py`: same number, same name.** The menu number is the folder number.
  Logs, receipts and outputs use the same `NN_NAME` label.
- Numbers are grouped by family and permanent:
  - 01-07 YouTube
  - 20s CKG
  - 30s Evidence
  - 40s grading and analysis
  - 50s Lean / axioms
  - 60s OpenAI stations
  - 90s utilities

  Leave gaps for growth. A retired station keeps its number (`retired` in stations.json), and its number is never reused.
- Every station folder holds: `NN_name.py`, `PROMPT.md` (if it calls a model), `FOCUS.md`, `station.json`, `README.md`, and `templates\section.html` (its piece of the report).

## 3. FOCUS.md: the extra request, written next to the call

- Every station folder has a plain-text `FOCUS.md`. David writes 2-4 things he wants that station to hone in on.
- Focus stacks in three layers, all appended to the prompt under `## EXTRA FOCUS FROM DAVID`:
  1. **Standing:** `stations\NN_NAME\FOCUS.md`
  2. **Per paper / per channel:** the paper folder's `01_NOTES\FOCUS.md`, or `focus\<Channel>.json` for YouTube
  3. **Per run:** menu question 3
- Focus **adds attention and never removes** the station's normal job. The station still returns its full output, plus a `## Focus findings` section.
- The run receipt records the exact focus text and its hash.
- Why a text file and not Python: David can change it without touching code, and it sits in the folder of the call it affects.

## 4. Portability

- **No script contains an absolute path.** Paths inside the home folder resolve relative to `engine\paths.py`. Everything outside it
  (NAS, vault, subtitles, Lean root, Excel lexicons, papers root) comes from `config\paths.json` by key.
- `config\paths.json` is git-ignored. Ship `paths.example.json`.
- Don't guess a path. Leave the key blank until David confirms it.
- **`RELOCATE.bat`** runs after the folder is moved or copied. It detects its own location, walks `paths.json`, and asks only for entries it can't find.
  Then it health-checks every station.

## 5. API calls

- **Every model call goes through one function** (`engine\llm.py`). No station talks to a provider directly.
- **Providers:**
  - DeepSeek is primary (`deepseek-chat`, env `DEEPSEEK_API_KEY`).
  - The free option is the automatic fallback (OpenRouter free models, env `OPENROUTER_API_KEY`).
  - Every provider is listed in `config\providers.json` with base URL, default model, key env var and cost tier, even the ones not in use.
  - Log every fallback in the receipt.
- **One item = one whole, independent call.** Send the whole document so the model has full context. Never crop input (see `review-corrections.md`).
  Never pack several items into one call. No call continues from another.
- **The only split is on output size.** If a reply would exceed the output cap (deepseek-chat ≈ 8k tokens), send the **whole document in every call**
  and split *which part each call answers for* (sentences S001-S080, S081-S160 …). Split the input itself only when a document is bigger than the context window, and log it.
- **A reply cut off by the length limit is a failure, not a result.** Treat `finish_reason = length` as an error.
- **Parallel by default: 30 calls at once.** The cost is the same as running one at a time; only the wall-clock time changes.
  - One **global limiter** shared by every level: papers × output ranges × stations never multiply past it.
  - Retry 429/5xx/timeout with exponential backoff + jitter (3 tries). If errors pass ~10% over a minute, halve concurrency and creep back up.
  - One failed item never stops the batch. Save each finished item immediately, and a rerun skips finished items (keyed by source hash + prompt version + model + focus hash).
- **Group calls; never 1,000 calls per paper.** One call per paper per station. A station that makes one call per *sentence* doesn't scale;
  claim-extraction timed out doing exactly that.
- **Keys only ever come from environment variables.** Never write a key into code, config examples, prompts, git or chat.

## 6. Python first: the same data every time

- Every statistic an API produces gets a **deterministic Python route** wherever one is possible. The Python number is the reference;
  the API adds judgment on top and never replaces it. Mark each metric `method: python | api | both`.
- **Where both exist, report their agreement**, using the pattern the Atlas Method Comparison already uses: freeze one source, run the same
  contract through the local lane and the API lane, and score agreement (structural 0.25 / field 0.35 / content 0.40; high ≥ 0.80).
- **Transcript cleaning is always local Python** (rules + local punctuation model), never an API.
- Before building something new, **check what already exists**: the Paper Intelligence suite (356-field registry), the 04_STATIONS library and
  `_DORMANT` (62 retired stations). Wrap and fix before rewriting.

## 7. Outputs and reports

- **Every station run on an item writes four files:**
  - `NN_station.json`: canonical; everything else reads this
  - `NN_station.xlsx`: its own rows, e.g. per sentence
  - `NN_station.html`: its public section
  - `NN_station.run.json`: receipt with source hash, model, prompt version, focus text + hash, tokens, time, errors
- **One working folder per paper**, created from the template and always the same shape:
  ```
  <PAPER_ID>_<slug>\  paper.json · 00_SOURCE · 01_NOTES · 02_RUNS\NN_STATION\<date> · 03_REPORT · 04_MEDIA · 05_WEB
  ```
  - Stations write only inside the paper's folder.
  - Reruns go into dated subfolders and never overwrite.
  - The source copy is read-only, with its sha256 recorded.
- **Reports are JSON → HTML.** Each station keeps its own `templates\section.html`. The combine step fills every template from the JSON into
  `03_REPORT\report.html` + `report.xlsx`. Templates hold no logic, so any paper can be re-rendered without new API calls.
- **The house visual language is the approved Paper Information Matrix.** The prototype is at
  `API_ALL\08_NEW_STATION_SPECS\STATISTICS_MATRIX_PROTOTYPE.html`, and David wants it used "for visual everything":
  - one circle per item
  - colour = needs work → typical → strong on a diverging red / grey / blue scale
  - size = distance from the norm
  - inner glyph = computed (dot) / AI-judged (diamond) / runs disagree (ring)
  - dashed = no benchmark
  - a corpus vs academic toggle
  - a two-axis family map
  - specialised charts: few pies, few line charts
  - the full searchable wall of numbers under it

## 8. Standard runs

| Routine | Applies to | Runs |
|---|---|---|
| **B Baseline** | every paper, transcript or document | SUMMARY + CKG |
| **P Published paper** | everything David publishes | Baseline + the four analytical arms together (axiom nodes, master equation, coherence, Fruits) + statistics wall + report combine |
| **D API Deep** | when wanted | the full API-deep chain (station 48) |

Everything else is picked from the menu when wanted. The four analytical arms never run alone.

## 9. YouTube

- **The chain is automatic:**
  1. download
  2. keep the original + converted `.md`
  3. clean (local)
  4. index (CKG argument-first)
  5. channel focus (lenses)
  6. tagger
  7. catalog
- **Per-channel folder:** raw transcripts at the top level, then `Clean MD\`, `Channel Summary\` and `Prompts\`. A download session auto-cleans the channels it touched.
- **Focus is numbered and saved per channel:**
  - Lenses 1-17 are `lenses\*.md`, with the number in the front matter.
  - Layers are letters for bundles of numbers in `layers.json` (A Arguments, C Christianity, S Science/Theophysics, W One-world/conspiracy, K Clips).
  - David types a mix like `C 7 16`.
  - It is saved to `focus\<Channel>.json`, and the watcher applies it to every new video from that channel.
- Adding a lens = one `.md` with the next id. Adding a layer = one entry in `layers.json`.

## 10. Git and secrets

- API_ALL is a **public** repo:
  - Code, prompts, templates, specs and config *examples* go in.
  - Run data (inbox/outbox/results), private papers, model weights and databases stay out.
- **Scan for keys before every push.** Known plaintext secrets on the NAS that must never be copied:
  - `API 2\writing-analyzer\config.txt` (DeepSeek + OpenAI keys)
  - `A_AI-RESEARCH-AGENTS\gpt-researcher\.env`
  - `A_BIL\docker-compose.yml` (MySQL password, web secret)
  - the NLP_FIS `settings.ini` / `settings.example.ini` (Postgres password)
- Commit only the paths you mean to. Never sweep up unrelated pending changes in a repo.
- Back up a script (`.bak-YYYYMMDD`) before editing it in place.

## 11. How changes are verified

- **Verify with a real run at a small limit** (`--limit 1`). API cost for tests is fine. Report what ran, where the outputs landed, the tokens used, and anything that failed.
- **A run is only "done" when the output exists and is complete.** Exit codes aren't enough: several legacy runners exit 0 while printing FAIL or with layers in error.

## 12. Decisions still open (David's to make)

1. **Master equation:** is C a tenth factor, or a wrapper around nine? The code disagrees with itself.
2. **The canonical axiom registry:** AXIOMS_PART1 (A1.1…), the AX-### pills, or the single root axiom "God Is"?
3. **One claim-type vocabulary.** Three exist today.
4. **One tag registry.** Two exist today.
5. **The canonical YouTube download root:** `subtitles\` or `E:\YouTube\channels`?
6. **The 12 headline statistics**, to be chosen from real numbers.
7. **The Fruits sentence scale:** -2..+2 (proposed) or 0-4.
