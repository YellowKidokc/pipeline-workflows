# Preference Engine

The preference engine is a stack, not one library.

The preference layer observes and calibrates. It should not silently perform destructive actions or bypass packet approval.

```text
P06_river       hot loop      live event learning
P05_ppk         identity      portable preference kernel
P01_implicit    pattern loop  station/workflow co-occurrence
P03_lightfm     hybrid loop   behavior + metadata recommendation
P07_markovify   voice loop    text/style prediction
```

Slot folders live at `X:\Backside\_models\_Models\P01-P07`. Resolve paths through `models/MODEL_REGISTRY.json`, not hardcoded folder names.

## Feedback Spine

```text
human decision
  -> approve.py / correction_logger.py
  -> preference event
  -> BIL / P06 River
  -> P05 PPK
  -> P01 Implicit / P03 LightFM
  -> workflow recommendation
  -> review
  -> correction event
```

## Loops

- hot loop: immediate River updates from actions and corrections
- identity loop: River distills into PPK
- pattern loop: implicit/LightFM learn workflow choices
- voice loop: Markovify learns accepted phrasing
- audit loop: monthly or 6-month review freezes what worked and retires bad defaults

## Engines

| Engine | Slot | Role | Source |
|---|---|---|---|
| River | P06 | online learning from immediate events and corrections | https://github.com/online-ml/river |
| PPK | P05 | portable JSON preference identity | custom |
| Implicit | P01 | collaborative pattern learning from behavior | https://github.com/benfred/implicit |
| LightFM | P03 | hybrid behavior + metadata recommendation | https://github.com/lyst/lightfm |
| Markovify | P07 | lightweight accepted-text prediction | https://github.com/jsvine/markovify |

## BIL Endpoints

- `http://localhost:8420` — BIL server / River hot loop.
- `POST /bil/correction` — correction events from `scripts/correction_logger.py`.

If BIL is offline, local JSONL remains the source of truth and can be replayed later.

## Signal Weights

Human correction is the strongest signal because it is an explicit override. Passive behavior is useful but weaker.

| Signal | Weight |
|---|---:|
| manual_approval | 1.0 |
| manual_rejection | 1.0 |
| human_correction | 1.0 |
| file_reused | 0.9 |
| copied_text | 0.8 |
| bookmark_save | 0.7 |
| long_dwell_scroll | 0.5 |
| opened_tab | 0.2 |
| accidental_visit | 0.0 |

Canonical weights live in `preferences/signal-weights.json`.

## Correction Data

`scripts/correction_logger.py` writes structured JSONL to `logs/corrections/corrections.jsonl` by default and pushes each event to BIL when available.

The correction log is training data. Without it, the system does not improve.

## Portable Identity

PPK's real weights stay in the P05 model slot. GitHub may contain `weights.example.json`, but not David's real learned preference artifact.
