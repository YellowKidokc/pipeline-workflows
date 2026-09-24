# OpenIntel Reconciliation — one scheme for Codex

Reference material in `docs/openintel/reference/`:
- `Open Intel.xlsx` — master workbook (DROPDOWNS vocabulary, DB Schema v2.0, case template, MKUltra case + YAML export, case_links_master, Field Interview Protocol, intake engine).
- `openintel_top100_conspiracy_sites.xlsx` — competitor list + gap analysis.
- `RECOVERED_trash_Claims_README.md` — the original "claims are not your hunch" guidance, found in the vault's `.trash`.
- (`openintel_1000_conspiracy_keywords.xlsx` was not copied: its sheets duplicate `Open Intel.xlsx`.)

Vault this maps to: `\\192.168.2.50\zobsidian\00_OPEN_INTEL\OPENINTEL STATER`.

---

## 1. The rule that governs everything: suspicion comes before proof

Almost nothing starts as a claim. It starts as **"something doesn't add up."**
A system so rigorous that it only accepts sourced claims will record nothing, and it will
lose the exact instinct that finds cases in the first place.

So the pipeline has a **pre-claim layer**, and writing it down is a *required discipline*, not optional:

```text
HUNCH  ->  ANOMALY / SIGNAL  ->  CLAIM (testable)  ->  EVIDENCE  ->  tiered, reviewed record
  ^ "something's off"   ^ "here's the specific thing"   ^ "here's a sentence that can be wrong"
```

### HUNCH record (`HNCH-<COLL>-NNNN`)

| field | notes |
|---|---|
| `hunch_id` | stable ID |
| `case_id` | optional — a hunch can exist before any case |
| `written_by` | David / contributor / `system extraction` |
| `written_at` | timestamp — **never edited**, so we can see what was suspected *before* the evidence |
| `gut_statement` | free text, messy is fine: "the timeline feels rehearsed" |
| `what_triggered_it` | the moment/span/quote that set it off (link if possible, not required) |
| `what_would_make_it_real` | first thing to check |
| `what_would_kill_it` | what would make you drop it |
| `status` | `OPEN / PROMOTED / PARKED / DROPPED` |
| `promoted_to` | ANOM-/SIG-/CLM- IDs when it grows up |
| `drop_reason` | required when DROPPED — dropped hunches are **kept**, never deleted |

Rules:
1. **No evidence required to write a hunch.** Missing facts is the normal state, not a defect.
2. A hunch is **never shown as a finding**, never tiered, never counted in OCS. It lives in its own view.
3. Hunches are **never deleted**. Dropped ones stay visible — being wrong on the record is part of the rigor,
   and a parked hunch sometimes becomes real when new material arrives.
4. The system periodically **re-checks OPEN/PARKED hunches** against new ledger records
   (embedding/NLI match) and raises a `SIGNAL` when new material touches one.
5. Hit rate is tracked: how many hunches became supported claims. That is a measure of investigator instinct.

> Note: the vault used to have `HUNCH.md` in the starter kit. The 2026-08-16 cleanup removed blank copies as
> boilerplate, and the current `00_SCHEMA_TEMPLATES` has no hunch record. Restore it as a first-class template.

### Machine hunches
The YouTube/NLP pipeline may also create hunches (`written_by: system extraction`) for things like:
a date mentioned two different ways, a speaker contradicting an earlier video, a name that appears with
no introduction, a claim with no source given. These stay hunches until a person promotes them.

---

## 2. One ID scheme (replaces all six current formats)

| Record | Format | Replaces |
|---|---|---|
| Case | `CASE-<COLL>-NNNN` | `CT001`, `OI-CT-0001`, `OI-CT-0002`, `CASE-0011`, `CASE-004-C317`, `CASE-YYYY-NNN` |
| Hunch | `HNCH-<COLL>-NNNN` | (new) |
| Source | `SRC-<COLL>-NNNN` | `SRC-YYYY-NNN`, `SRC-004-C317-001` |
| Statement | `STMT-<COLL>-<SRC#>-NNNN` | `STMT-C317-001`, `STMT-YYYY-NNN` |
| Claim | `CLM-<COLL>-NNNN` | `CLM-YYYY-NNN` |
| Evidence | `EVID-<COLL>-NNNN` | `EV-CT001-001`, `evidence-CT001-001`, `EVID-YYYY-NNN` |
| Entity | `ENT-<TYPE>-NNNNN` (global, not per collection) | `ENTITY-sidney-gottlieb`, `ENT-TYPE-NNN` |
| Event | `EVT-<COLL>-NNNN` | `EVT-YYYY-NNN` |
| Anomaly / Signal / Contradiction / Financial | `ANOM- / SIG- / CONTRA- / FIN-<COLL>-NNNN` | template forms |

`<COLL>` = short collection code (`MKU`, `EPS`, `COW` Candace Owens, `HAB` Gary Habermas).
Keep a `legacy_ids` field on every record so old links still resolve.

## 3. Tiers — use the DROPDOWNS sheet, applied per claim/evidence

From `Open Intel.xlsx › DROPDOWNS`: `T1 PROVEN`, `T1-T2`, `T2 STRONG`, `T2-T3`, `T3 CREDIBLE`, `T3-T4`,
`T4 WEAK`, `T4-T5`, `T5 SPECULATIVE`, `Mixed`.

- Tiers go on **claims and evidence**. A **case** shows its distribution and is `Mixed` whenever claims differ
  (MKUltra: program existence T1; Olson homicide not T1 → case = `Mixed`, not `T1`).
- **Hunches have no tier.** Untested claims are `UNRATED`, not T5 (T5 means *tested and unsupported*).
- Evidence types: the 38-type / 6-tier `evidence_types` lookup in DB Schema v2.0 (tier `NEGATIVE` = evidence of absence/destruction).

## 4. Storage: one ledger, notes are views

- Master schema = `Open Intel.xlsx › DB Schema v2.0` (Postgres `192.168.1.97`), **plus** tables it lacks:
  `hunches`, `statements` (columns from vault `STATEMENT_LEDGER_SCHEMA.md`), `sources` (fields from
  `SOURCE_FAMILY_RULES.md`), `links` (types from `LINK_TYPES.md`, plus `PROMOTED_FROM`).
- Local/offline fallback: SQLite with the same tables; sync later.
- Obsidian notes, dossiers, timelines, contradiction indexes = **generated projections**. Hand-written text goes
  below `<!-- manual -->` and is preserved on regeneration.

## 5. Record lifecycle (every machine-created record)

`CANDIDATE` → `REVIEW` → `ACCEPTED` / `REJECTED`
Machine output never skips review. Rejected records are kept with a reason (same rule as dropped hunches).

## 6. Sensitive-person gate

Any statement or hunch that names a living private person with an accusation
(e.g. "X is more suspicious") is flagged `sensitive: true`, excluded from public projections, and requires
human review before publication. Public figures are still flagged when the accusation is criminal.

## 7. Tasks for Codex (in order)

1. Add `hunch` to vault `00_SCHEMA_TEMPLATES/` and to the ledger; restore `HUNCH.md` in the case template.
2. Create SQLite ledger from DB Schema v2.0 + section 4 additions; migration script from the xlsx sheets.
3. ID mapper: scan the vault, emit `id_map.csv` (legacy → new) and a broken-link report. **Report only, no edits.**
4. Point YouTube refinery extraction at the ledger (see `workflows/YouTubeChannelRefinery/CODEX_BUILD_SPEC_ADDENDUM.md` §G).
5. Hunch re-check job (section 1 rule 4).
