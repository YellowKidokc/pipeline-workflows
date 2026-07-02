# Knowledge Refinery Backplane

This repo should hold the control plane for the automated production line, not
the heavy runtime vault.

## Two Workflow Classes

### David-facing front doors

These folders should stay simple, visible, and safe to use repeatedly:

- session handoff drop
- link pull drop
- paper grading drop
- manual review queues

They are not the backplane. They are intake counters.

### Automated backplane

The backplane is the machine room. It routes content through a sequence:

```text
paper/source in
-> classify
-> normalize
-> grade
-> claim extract
-> math verify
-> fact verify
-> contradiction detect
-> timeline verify
-> paper review
-> axiom map
-> lossless summary
-> executive summary
-> plain English layer
-> academic summary
-> Obsidian export
-> AI portal package
-> archive
```

`KnowledgeRefineryBackplane` is the repo-side packet that describes and controls
that process.

## Source Systems

Do not move these source systems into the repo by default. Register them first,
then let the backplane call into them.

| Source | Role | Default Local Path |
|---|---|---|
| Brain NLP | legacy NLP stations, claims, DeBERTa, SBERT | `D:\brain` |
| C4C wiki | compiled wiki layer | `D:\C4C-wiki` |
| C4C | upstream C4C source/system folder | `D:\C4C` |
| FAP | formal automation pipeline runtime | `D:\FAP` |
| X models | local model rack and Ollama-facing stations | `X:\models` |
| X refinery | live knowledge-refinery runtime | `X:\knowledge-refinery` |

## Rule

The repo keeps contracts, prompts, scripts, manifests, and health checks. Live
model weights, vector stores, private vault dumps, and runtime databases stay
outside the repo.
