# Axiom Nodes governed reference package

This package combines two complementary sources without conflating their authority.

## Controlling source

`AXIOM_CHAIN_MASTER_v2.3_CANONICAL_SEALED.md` is the controlling axiom-chain source. It governs canonical node IDs, names, modes, dependency claims, epistemic grades, and chain-impact analysis. Its contents were copied byte-for-byte from the supplied attachment and must not be silently edited by the API.

Declared version: **2.3**, sealed **2026-08-22**. It explicitly supersedes v2.2, v1, and the document previously called v3.

## Supplemental source

`MASTER_CLASSIFICATION_API_DYNAMIC_INDEX.md` is a dynamic classification and retrieval index. It contains 279 categorized domains and 2,485 registered domain nodes. It may supply search terms, document candidates, domain routing, and supporting references, but it may not create canonical axiom IDs or override the sealed chain.

Its opening summary cites `FULL AXIOM API.md`, but that underlying file was not included in the supplied pair. Consequently, the summary is supplemental context rather than a verified replacement for the sealed v2.3 chain.

## Precedence rules

1. The sealed v2.3 chain controls axiom identity and graph relationships.
2. The dynamic index assists retrieval only.
3. A paper may map only to an ID present in the controlling source.
4. Similar wording in the dynamic index is not enough to establish an axiom relationship.
5. Every mapping must preserve an exact quotation from the evaluated paper and identify the relationship as `supports`, `extends`, `depends_on`, `tests`, `threatens`, or `illustrates`.
6. Conflicts or missing IDs route to review; the model must not repair the canon itself.

## Preserved discrepancy

The sealed document's frontmatter reports 197 formal graph claims: 4 CORE, 0 DERIVED, 43 SCAFFOLD, 114 EXTENDED, and 35 EVIDENCE. Its body reports 198 entries: 4 CORE, 0 DERIVED, 43 SCAFFOLD, 115 EXTENDED, 35 EVIDENCE, and 1 DROP_DUPLICATE. It also retains an older v2.1 historical paragraph reporting 195 entries.

These statements are preserved exactly. For API work, use the body inventory of 198 rows as the catalog count, treat the single `DROP_DUPLICATE` row as non-evaluable, and treat 197 as the active graph-claim count pending comparison with the cited Lean commit `6638f13c`.

See `reference_manifest.json` for hashes and machine-readable authority rules.
