# API 2 / API 3: where the model-calling code went (2026-10-01)

`API 2` and `API 3` are gathered copies. This is every file in them that calls a model, and where that job lives now. Nothing was deleted from `API 2` / `API 3`.

| Found in | Calls a model for | Now |
|---|---|---|
| `API 2/01_chi-evaluator` (run_evaluator, synthesize_statements, chi_engine) | scores each claim on the ten Master Equation channels, then four statements | **new station `059_CHI_EVALUATOR`**, code in `_system/vendor/chi_evaluator` (2 calls per claim, DeepSeek) |
| `API 2/chi-evaluator` | older copy of the same | superseded by 059 |
| `API 2/pipeline/llm_hub.py` | provider hub | superseded by `_system/engine/llm.py` + relay |
| `API 2/writing-analyzer` (call_openai, process_*, run_*) | the 23 OpenAI prompts | already `060_OPENAI_STATIONS` |
| `API 3/03_EVIDENCE` (turbo, three_dials, argument_builder, series_*) | evidence | `030_EVIDENCE` bundle; argument_builder (033), series_* (034/035) still stations, see PROMPT_OUT_BUNDLES.md |
| `API 3/05_API_DEEP_STATIONS` (ATOMS, AXIOM_NODES, FRUITS) | atoms, axioms, fruits | `045_ATOMS` bundle; `057_API_DEEP` |
| `API 3/01_YOUTUBE/deepseek-home` (index_video, lens_pass, watch_pipeline, home) | YouTube CKG index, lenses, watch | stations 03 / 04 / 06, now also `_ACTIONS` `yt_*` |
| `API 3/02_CKG` (workbench, providers) | CKG | `020_CKG` |
| `API 3/06_LEAN/LEAN_ATOM_EXTRACTOR` (briefs, axiom_registry) | Lean atoms | station 52 (not folded yet) |
| `API 3/07_PIPELINE_WORKFLOWS_API/EvidenceChainIntake` (epistemic_intake_v2, semantic_analysis, daily_api_preflight) | evidence chain | station 39 (not folded yet) |

Not model-calling, left alone: `API 2/P01..P07` preference engines, `embeddings`, `truth`, `vectorization`.

## YouTube

The eleven `02_YOUTUBE` stations are also actions in `_ACTIONS` (`yt_grab`, `yt_clean`, `yt_index`, `yt_lenses`, `yt_catalog`, `yt_watch`, `yt_convert`, `yt_summary`, `yt_deep`, `yt_tidy`,
`yt_channel_summary`; workflows `youtube_channel`, `youtube_index`). Each runs its station through ONE_MENU. The station folders were not moved.
