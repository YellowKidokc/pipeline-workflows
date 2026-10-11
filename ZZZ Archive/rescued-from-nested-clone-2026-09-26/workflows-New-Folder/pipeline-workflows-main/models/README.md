# Model Slot Registry

`models/` is the GitHub-side source of truth for model slot knowledge. It is a
spec/governor layer only: model weights, generated outputs, vector indexes,
databases, and secrets stay on the NAS runtime/body layer.

## Canonical files

| File | Purpose |
| --- | --- |
| `MODEL_REGISTRY.json` | Canonical identity, NAS path, category, status, and wiring for all 19 slots. |
| `MODEL_HEALTH.json` | Human-auditable overlay for degraded, placeholder, and empty slots. |
| `MODEL_FALLBACKS.json` | Safe fallback map for degraded slots; references NAS paths only. |
| `preference-chain.json` | BIL preference chain extracted from the registry for quick review. |
| `nlp/nlp-pipeline.json` | Nested mirror for M01-M12; points back to `MODEL_REGISTRY.json`. |
| `preference/*.json` | Nested mirrors for P01-P07; each points back to `MODEL_REGISTRY.json`. |

## Slot map

| Slot | Key | Role | Status | Visibility note |
| --- | --- | --- | --- | --- |
| M01 | `M01_summarizer` | Summarizer | active | NAS weights only. |
| M02 | `M02_embedder` | Sentence embedder | installed / degraded | Use `sbert_minilm` fallback until repaired. |
| M03 | `M03_contradiction` | Contradiction detector | installed / degraded | Use `deberta_nli` fallback until repaired. |
| M04 | `M04_imager` | Image-text CLIP | active | NAS weights only. |
| M05 | `M05_transcriber` | Whisper transcriber | active | NAS weights only. |
| M06 | `M06_llm` | Local LLM slot | active | Runtime inference is local/NAS-side. |
| M07 | `M07_fact_verify` | Fact verification | installed | Contains fact-verification submodels on NAS. |
| M08 | `M08_contradiction_deep` | Deep NLI | installed | NAS weights only. |
| M09 | `M09_claim_extract` | Claim extraction | installed | NAS weights only. |
| M10 | `M10_timeline` | Timeline reasoning | installed | NAS weights only. |
| M11 | `M11_math_verify` | Math verification | empty | Folder exists; no weights assigned. |
| M12 | `M12_paper_review` | Paper review | empty | Folder exists; no weights assigned. |
| P01 | `P01_implicit` | Implicit collaborative filtering | installed | Installed, needs wiring into preference flow. |
| P02 | `P02_recbole` | RecBole recommendation | placeholder | Reserved; do not route live decisions yet. |
| P03 | `P03_lightfm` | LightFM hybrid recommendation | placeholder | Reserved; do not route live decisions yet. |
| P04 | `P04_paper_recommender` | Paper recommender | empty | Use the station implementation until slot weights exist. |
| P05 | `P05_ppk` | Portable Preference Kernel | active | JSON weights only; no personal data in GitHub. |
| P06 | `P06_river` | River streaming ML | active | BIL online learning service. |
| P07 | `P07_markovify` | Markovify text prediction | installed | Installed; needs training corpus. |

## Doctrine reminders

- GitHub is the governor/spec layer; NAS is the runtime/body layer.
- FIS = perception, BIL = preference, Pipeline = action.
- Vectorize before classify.
- Nothing destructive happens without an approval packet.
- Nested model configs are discoverability mirrors; update
  `MODEL_REGISTRY.json` first and keep mirrors pointing back to it.
