# HTML ASSEMBLY SPEC v0.1 — the lossless handoff
*David Lowe · POF 2828 · Oct 16–17, 2026 · merges the Kimi design session (3 days) with the 000_QUICK_CALL pipeline*

This is the whole design in one place, so any AI or developer can build it without the conversation.
The rule underneath everything: **stations emit JSON; HTML assembly only renders JSON. Nothing is typed into HTML by hand.**

---

## 1. The four layers (the most basic breakdown of every paper)

Every node is tagged **before** it is graded. Grading is type-matched — a definition is never "supported," a prediction is never "needs evidence."

| Layer | Name | Speech acts that live here | How it closes | Border color |
|---|---|---|---|---|
| L1 | Primitives | DEFINITION, AXIOM, BOUNDARY, SCOPE_NOTE (disclaimers live here) | DISCRIMINATING_CLOSED / UNDERDETERMINED (beats its rivals) | gold |
| L2 | Claims | ASSERTION, DERIVATION, PREDICTION, BRIDGE_ASSERTION | assertion: SUPPORTED / NEEDS_EVIDENCE · prediction: FALSIFIABLE / UNTESTED (needs a counterworld, not evidence) | blue |
| L3 | Warrant | EVIDENCE_REPORT, STAT, DATA, PROOF, KILL_CONDITION | ATTESTED / INDEPENDENT / CONTESTED (provenance + independence) | teal |
| L4 | Closure | CONVERGENCE_VERDICT, BRIDGE (with ladder level), REALITY_MIRROR | WHY_CLOSED / WHY_UNFINISHED | purple |

**Truth register** (second tag on every node): FORMAL · EMPIRICAL · HISTORICAL · EXPERIENTIAL · THEOLOGICAL · CROSS_DOMAIN.

**Bridge ladder** (bridges name their level instead of being called "overstated"): metaphor → analogy → homology → invariant → grammar → functorial → isomorphism.

**Ownership** (David's C066 rule, Oct 16): every node carries `owner: FRAMEWORK | PERSONAL`. PERSONAL = testimony that is true and load-bearing for David but does not prop up the framework (e.g., the Bart story). PERSONAL nodes are shown, never graded as framework evidence, never required to carry rigor.

**Counterworld**: every ASSERTION carries its exact negation and at least one rival mechanism (BFP-DG §13). Empty counterworld = review flag, not a pass.

---

## 2. Identity and addresses (two different things — never merge them)

| What | Permanence | Source |
|---|---|---|
| `paper_uuid` | permanent, survives every edit | 000_QUICK_CALL / identity.py registry |
| `version_uuid` | one per exact byte-version | uuid5(CKG_NAMESPACE, "paper-version:" + sha256) |
| `node_id` | permanent per node | uuid5(CKG_NAMESPACE, "node:" + paper_uuid + ":" + claim_key) |
| `address` | **readable location, changes with edits** | `SERIES.PAPER.PAGE.PARA.SENT.CLAIM` e.g. `GTQ.01.03.12.2.C004` |

Links always point at `node_id`. The address is for reading and citing a position inside one version. When a new version arrives, nodes are carried forward by `node_id`; addresses are recomputed.

---

## 3. The node record (what every station emits — one JSON object per node)

```json
{
  "node_id": "uuid", "paper_uuid": "uuid", "version_uuid": "uuid",
  "address": "GTQ.01.03.12.2.C004", "claim_key": "C004",
  "layer": "L2", "speech_act": "ASSERTION", "register": "THEOLOGICAL",
  "owner": "FRAMEWORK",
  "text": "exact sentence(s)", "source_span": {"start": 0, "end": 0, "sha256": "..."},
  "status": "UNRESOLVED | PARTIAL | CONVERGED | LOCKED",
  "grade": "type-matched value from section 1",
  "depends_on": ["node_id"], "supports": ["node_id"], "evidence": ["node_id"],
  "kill_conditions": ["text"], "counterworld": {"negation": "", "rival": ""},
  "bridge": {"to_domain": null, "ladder_level": null, "receipt": null},
  "operators": ["source", "boundary", "repair"],
  "station": "01_CKG", "proposed_by": "model name", "validated_by": "script name"
}
```

`status` rules (computed, never AI-written):
- UNRESOLVED — no evidence and no derivation attached
- PARTIAL — some layers closed
- CONVERGED — claim + evidence + proof all present and none contested
- LOCKED — CONVERGED **and** a Lean receipt or independent confirmation exists

---

## 4. One shell, four modes (AtomBLACK outside, Truth Node inside)

```
IDENTITY BAND   paper_uuid · code · label · state · version     <- 000 sidecar
NABLA BAND      D/N/V/A/U/R :: GMESTKRQFC :: hash               <- 000 sidecar
PERIODIC-15     01..11 from records · 12..15 COMPUTED ONLY      <- blank/pending until computed
CONTROLS        [Local][Series][Global] · mode [Read][Node][Graph][Compare]
LEFT RAIL       graph stats · receipts · dependency spine
CENTER          L1 / L2 / L3 / L4 rows, each with a big title bar
RIGHT RAIL      alerts · open items · kill conditions · actions
```

- All four layer rows are always in the HTML. Focusing one layer collapses the others to a thin bar showing title + block count.
- **Read** = flowing prose with inline node icons (superscript) and margin dots. Hover = preview, click = Node.
- **Node** = Truth Node drawer: v1.1 master-template markings on top, the atom-interior prototype in the middle, larger and plain-language ("this is this; this is what it does").
- **Graph** = force-directed network of the current scope, filter by layer / type / status; click an edge = its bridge receipt.
- **Compare** = two scopes side by side; shared nodes green, unique blue/red; Φ adjudication panel underneath. (Design open — David: "figure that out later.")

Node icons: L1 primitive ● gold · L2 claim ◆ blue · L3 evidence ■ teal · L3 kill ✕ red · L4 closure ⬡ purple · L4 bridge → green.
Convergence look: gray (unresolved) → blue pulsing (partial) → gold bar (converged) → gold + lock ring (locked). A paragraph where claim, evidence and proof all close gets the gold left border and a sealed-envelope badge in the margin.

Navigation: Series (only converged/locked nodes, paper buttons + All Papers) → Paper (page buttons + Full Paper) → Page → Node → Graph.

---

## 5. Pipeline wiring (how the API fills the HTML automatically)

```
file -> 000_QUICK_CALL  (UUIDs, NABLA, series slot, ME id, original copied)  -> sidecar YAML = header of every call
     -> 01_CKG          emits node records (L1/L2 tagging, dependencies)      -> JSON_CKG/      -> HTML_ASSEMBLY/
     -> 02_C_P_E_L      claims/proofs/evidence/links (L2/L3)                   -> JSON_CPEL/     -> HTML_ASSEMBLY/
     -> 04_ACADEMIA     L3 warrant, citations                                  -> JSON_ACADEMIA/ -> HTML_ASSEMBLY/
     -> 06_ATOMS        atom records                                           -> JSON_ATOMS/    -> HTML_ASSEMBLY/
     -> 07_ARGUMENTS    L4 + counterworlds; copies into matching argument folders
     -> 08_API_DEEP     L4 convergence, bridges                                -> JSON_API_DEEP/ -> HTML_ASSEMBLY/
     -> 041_STORIES / 047_NEW_PAPER                                            -> each with HTML_ASSEMBLY/
     -> FINAL           all JSON into one continuous stream; compute status + Periodic 12-15; prune unused station folders
```

HTML assembly per station = merge that station's node records into the paper's single `nodes.json`, then re-render the one shell. The shell never changes per paper; only the data does.

Markdown authoring (Kimi's compiler) stays as the input format: `<!-- BLOCK:type label="..." --> ... <!-- ENDBLOCK -->`. The block type sets speech act and layer; the compiler assigns addresses; the stations fill everything else.

---

## 6. Rules that keep it honest

1. AI proposes; code validates and computes. Status, grade bands, Periodic 12–15 and convergence glow are computed, never written by a model.
2. Tag speech act and register before any grade.
3. PERSONAL nodes are displayed, not graded as framework evidence.
4. Link by `node_id`, cite by `address`.
5. Ten-factor diagrams must not be labeled the Master Equation. Canon form is χ(W) = C_W[∭ nine factors]. (Kimi's compiler sample still shows the old ten-factor line — update the sample.)
6. If a layer has no nodes, the row still renders, collapsed, saying "none yet" — absence is information.

## 7. Open items
- Compare-mode design (Φ panel)
- Outbox call-count prefix on station folders
- DeepSeek key wiring for 000 (find the .env the other stations use)
- Build order: compiler addresses → reader shell → node drawer → graph → compare
