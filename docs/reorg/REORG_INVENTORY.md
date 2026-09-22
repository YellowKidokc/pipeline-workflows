# Reorganization Inventory

Phase 0 inventory only. No repository content has been moved. The inventory describes the checked-in tree; transient ignored test output is excluded.

## Directory tree (directories only, two levels)

```text
APIs/
  CANONIZATION/
  CONFIG/
  EVIDENCE/
  LEAN4/
  LOGS/
  Reusable_Tools_From_Theophysics/
  SCRIPTS/
  STATE/
  TESTS/
  components/
  nlp/
  stations/
  templates/
  tests/
  workbench/
contracts/
  schemas/
docs/
  imported/
  openintel/
  reorg/
drop_pipeline/
engines/
  embeddings/
  pipeline/
  truth/
models/
  nlp/
  preference/
openintel/
  templates/
preferences/
  engines/
  profiles/
prompts/
  fap/
  personas/
schemas/
scripts/
signals/
  duplicate/
  gap/
  quality/
  ready/
  upstream/
stations/
  analysis/
  framework/
  graph/
  intake/
  intelligence/
  media/
  processing/
  route/
  source/
  transform/
  validate/
templates/
  sandbox_test/
  workflow_packet/
tests/
  fixtures/
tools/
  drop_watcher/
  prompt_box/
workflows/
  BrainHandoff/
  ClipSyncExport/
  CorpusTriage/
  CrawlIngest/
  EvidenceChainIntake/
  GTQArticlePublicRefinery/
  KnowledgeRefineryBackplane/
  MasterHTMLComponentPipeline/
  PaperGrading/
  SubstackPublish/
  TTSRender/
  TikTokPrep/
  VaultCompiler/
  VaultPageCompiler/
  YouTubeChannelRefinery/
```

## Top-level directory classification

“K1,” “K2,” and “K3” mean the three currently visible kernels: `engines/pipeline`, `drop_pipeline`, and `APIs`. “Shared” identifies governor/spec or support material rather than another runtime kernel.

| Current directory | What it holds | Kernel | Proposed destination |
|---|---|---:|---|
| `APIs/` | Standalone API workbench, external-service launchers, evidence/Lean/canonization tooling, embedded NLP, station/template copies, and runtime placeholders | K3 | Rename to `adapters/`; extract NLP to `nlp/`, runtime state to `runtime/`, and overlaps to `legacy/adapters_overflow/` as explicitly ruled |
| `contracts/` | Canonical interface contracts and contract schemas | Shared / K1 governor | Keep `contracts/` |
| `docs/` | Architecture, operating, boundary, and imported reference documentation | Shared | Keep `docs/` |
| `drop_pipeline/` | Older parallel drop-zone classifier/router/indexer implementation | K2 | `legacy/drop_pipeline/`, only after the required import check |
| `engines/` | Main pipeline runtime, station runtime implementations, truth engine, and embeddings | K1 | Keep `engines/`; move only `engines/embeddings/` to `nlp/embeddings/` |
| `models/` | Model registry/health/fallback configuration plus preference and NLP configuration | Shared / K1 governor | Keep `models/`; move `models/nlp/nlp-pipeline.json` to `nlp/pipeline.json` |
| `openintel/` | Open Intel ledger/XLSX code and small Markdown schema templates | Shared utility used by K1 workflows | Keep `openintel/`; root workbooks go to `data/openintel/` |
| `preferences/` | Preference defaults/profiles and the checked-in BIL source snapshot | Shared / K1 governor | Keep `preferences/` pending the NAS-duplication decision below |
| `prompts/` | Reusable FAP and persona prompts | Shared / K1 governor | Keep `prompts/`; receive the two root prompt documents |
| `schemas/` | Compatibility schemas for existing consumers | Shared / K1 governor | Keep `schemas/` (known duplication with `contracts/schemas/` is intentional per the boundary doc) |
| `scripts/` | Repository launchers, migration helpers, orchestrators, and CLI utilities | Primarily K1 | Keep `scripts/`; park its non-canonical `station_runner.py` after approval |
| `signals/` | Signal-channel contracts/documentation represented as folder READMEs | Shared / K1 | Keep `signals/` |
| `stations/` | Station registry, declarative station definitions/manifests, and sanitized source pointer/snapshot area | Shared / K1 governor | Keep registry/index in `stations/`; park NAS-duplicated detail and add a pointer once the exact NAS-owned subset/path is approved |
| `templates/` | Workflow-packet and sandbox templates | Shared / K1 | NAS-owned according to the hard boundary: park duplicated detail and leave a NAS pointer, but exact NAS path is needed |
| `tests/` | Canonical repository test suite and fixtures | Shared; mostly K1, with K2 coverage | Keep `tests/` |
| `tools/` | Drop watcher and prompt-box utilities | Shared / K1 support | Keep `tools/` |
| `workflows/` | Canonical workflow registry, loose workflow configs, and runtime packet skeletons | Shared / K1 | Keep `workflows/`; move only the ten ruled loose configs to `workflows/_config/` |

## Root-file disposition

All checked-in root files are classified: the three workbooks go to `data/openintel/`; the two build/integration prompts go to `prompts/`; `.gitignore`, `README.md`, `SYSTEM.bat`, `pipeline.config.example.json`, and `watch-folders.example.json` remain at root.

## Files not classifiable under the ruled plan

These checked-in items have no unambiguous destination in the phase instructions. They must not be moved until David rules:

- The entire `APIs/Reusable_Tools_From_Theophysics/` subtree (256 checked-in files): it is a bulk imported library containing API station references, conversion/data tools, templates/prompts, metadata conventions, an inventory, and an omissions manifest. It looks like NAS/archive material, but Phase 3 also explicitly says which adapter subfolders remain and does not name this one.
- `APIs/TESTS/test_portable.py`: Phase 3 names overlapping `tests/` (lowercase), but not the distinct uppercase portable test suite.
- `preferences/engines/bil/source/`: a source snapshot that may be repo-governed code or a duplicate of a NAS-owned engine body; the boundary document does not make this specific ownership clear.
- `stations/source/AUDIT.md`, `stations/source/AUDIT.json`, and `stations/source/.gitignore`: the boundary explicitly permits sanitized station source snapshots, while the reorg request says station “detail files” are suspected NAS duplicates. The folder contains only audit/control files, so whether it should remain needs confirmation.
- `openintel/templates/`: executable code clearly belongs in the repo, but the two content templates may fall under the NAS-owned template-library rule. No NAS path is recorded for them.

No other checked-in file was unclassifiable at the level needed for the ruled moves.

## Suspected duplicates

The comparison used basename grouping followed by byte hashes/diffs. Repeated packet scaffolding (`README.md`, `.gitkeep`, `RUN_PIPELINE.bat`, `RUN_THIS_STAGE.bat`, `TROUBLESHOOT.bat`, prompt-stage names, `preferences.json`, and `config.example.json`) is expected templating rather than an accidental collision and is not a canonicalization candidate.

### Canonicalization candidates

| Files | Comparison | Judgment (inventory only) |
|---|---|---|
| `engines/pipeline/station_runner.py`; `scripts/station_runner.py` | Different implementations (60 vs. 199 lines). Engine version runs `StationBase` objects and is imported/tested by `tests/test_station_runner.py`; script version is a standalone NAS/registry launcher. Git history dates the script to 2026-06-10 and the engine version to 2026-05-12. | `engines/pipeline/station_runner.py` is canonical by location, active test coverage, and the ruled `external_adapter` architecture. The script is newer chronologically but non-canonical; park `scripts/station_runner.py` in `legacy/` in Phase 4. |
| `schemas/{approval,correction,export-manifest,manifest,model,preference-event,station,workflow}.schema.json`; corresponding `contracts/schemas/*` | Each corresponding pair is byte-identical. | `contracts/schemas/` is canonical; `schemas/` remains a compatibility mirror because `docs/GITHUB_VS_NAS_BOUNDARY.md` explicitly says existing consumers still use it. Do not park without a separate ruling. |
| `APIs/workbench/{cli,config,coordinator,events,export,nlp,providers,station}.py`; copies under both `APIs/stations/Stories/SCRIPTS/workbench/` and `APIs/templates/MY_STATION/SCRIPTS/workbench/` | All copies are byte-identical. | `APIs/workbench/` is canonical adapter code. The station/template copies are overflow candidates for `legacy/adapters_overflow/`, subject to the NAS pointer decision. |
| `APIs/stations/Stories/SCRIPTS/workbench_cli.py`; `APIs/templates/MY_STATION/SCRIPTS/workbench_cli.py` | Byte-identical. | Template/station duplication; no canonical repo counterpart. Park with the respective adapter station/template overflow rather than selecting one file ad hoc. |
| `APIs/stations/Stories/{CHECK_SETUP,RUN_ONCE,SETUP,WATCH_INBOX}.bat`; matching files in `APIs/templates/MY_STATION/` | Byte-identical. (`START_HERE.bat` is also identical between these two but differs from `APIs/START_HERE.bat`.) | Generated/template overlap; park both detail trees as adapter overflow if NAS owns them, retaining the adapter-level launcher. |
| `APIs/EVIDENCE/SCRIPTS/SCHEMAS/EPISTEMIC_INTAKE_V2_RUBRIC.json`; `workflows/EvidenceChainIntake/SCRIPTS/SYSTEM_FILES/SCHEMAS/EPISTEMIC_INTAKE_V2_RUBRIC.json` | Byte-identical. | The workflow packet is the canonical in-repo job copy; the API/Evidence copy belongs with adapter functionality unless NAS ownership says otherwise. Do not merge/delete either. |
| `APIs/EVIDENCE/SCRIPTS/SCHEMAS/intake-receipt.schema.json`; `workflows/EvidenceChainIntake/SCRIPTS/SYSTEM_FILES/SCHEMAS/intake-receipt.schema.json` | Byte-identical. | Same judgment as the rubric above. |
| `APIs/Reusable_Tools_From_Theophysics/.../CALL/call_openai.py`; `.../YAML-COPILOT/call_openai.py` | Byte-identical. | Imported-library duplication. Destination is part of the unresolved imported-library decision. |
| `APIs/Reusable_Tools_From_Theophysics/.../MIRROR_POLICY_TEMPLATE.yaml` (two locations) | Byte-identical. | Imported-library duplication; unresolved with its parent subtree. |
| `APIs/Reusable_Tools_From_Theophysics/.../Tagged-Links-Footer.md` (two locations) | Byte-identical. | Imported template-library duplication; likely NAS-owned, but NAS path is unknown. |
| `APIs/Reusable_Tools_From_Theophysics/.../note.tmpl.md` (two locations) | Byte-identical. | Imported template-library duplication; likely NAS-owned, but NAS path is unknown. |
| `openintel/templates/HUNCH.md`; `openintel/templates/00_SCHEMA_TEMPLATES/HUNCH.md` | Same basename but different content. | Related variants, not safe duplicates. Keep both pending the template/NAS ruling. |
| `workflows/mda-publication.json`; `stations/processing/mda-publication.json` | Same basename but different schemas and purposes (job config vs. station definition). | Not duplicates; both canonical in their respective registries/homes. |
| `drop_pipeline/{connections,runner}.py`; same basenames deep in the imported API data-command-center tree | Content differs and belongs to unrelated implementations. | Not duplicates. K2 is parked as ruled; imported-library destination remains unresolved. |
| `templates/workflow_packet/SCRIPTS/run_packet.py`; packet-local `workflows/*/SCRIPTS/run_packet.py` | Some packet copies match the template byte-for-byte; others are workflow-specific variants. | Intentional instantiated-template copies, not safe deduplication targets. |
| `templates/workflow_packet/SCRIPTS/troubleshoot.py`; packet-local copies | Most are identical; YouTube’s differs. | Intentional packet scaffolding, not safe deduplication targets. |

### Other repeated basenames reviewed

Repeated `__init__.py`, manifests, requirements files, launchers (`RUN.bat`, `HEALTHCHECK.bat`, `ACTIVATE.bat`), configs, prompts, and packet README names were compared by hash. They are conventional names in separate packages/jobs and either differ by role or are intentional scaffolding. They are not candidates for consolidation based only on filename.

## NAS-boundary findings requiring approval

The repo identifies NAS roots in station/model configuration, but it does not state a single authoritative NAS path for the templates library, imported Theophysics bundle, station detail archive, or BIL snapshot. Pointer documents cannot accurately name “where it lives on the NAS and who owns it” until those paths/owners are supplied or confirmed.

## Baseline test result

`python -m pytest -q` completed with **13 failed, 90 passed, 1 skipped**. The failures predate any move in this phase and fall into three groups:

- missing platform/dependencies: Windows-only `msvcrt`, `requests`, and `sklearn`;
- nine `drop_pipeline` failures caused by absent `sklearn` (part of the legacy K2 kernel);
- two YouTube refinery failures because the temporary Open Intel database lacks a `videos` table.

Because Phase 0 changed only this inventory document, these failures are recorded as the baseline rather than a reorganization regression. Per the prime directive, no code was changed to repair them.

## Decision needed before Phase 1

1. Confirm the proposed classifications and the `station_runner.py` canonical judgment.
2. Rule on `APIs/Reusable_Tools_From_Theophysics/` and `APIs/TESTS/`, which are not assigned by the phase plan.
3. Supply/confirm NAS paths and owners for the templates library, station detail, imported Theophysics archive, and (if NAS-owned) BIL source snapshot and Open Intel templates.
4. Confirm whether `stations/source/` audit/control files remain as part of the permitted sanitized snapshot area.
5. Acknowledge the failing baseline test suite so later phases can be checked for *new* failures against this baseline.

**STOP:** Phase 1 must not begin until David approves these decisions.
