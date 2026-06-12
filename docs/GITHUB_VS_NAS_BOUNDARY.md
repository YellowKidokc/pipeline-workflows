# GitHub vs NAS Boundary

GitHub is the governor/spec layer. NAS is the body/runtime layer.

## GitHub Gets

- station, model, and workflow registries
- schema contracts
- repo-safe configs
- prompt templates
- queue and export folder contracts
- adapter code
- tests
- documentation

## NAS Keeps

- model weights
- learned artifacts
- vector indexes
- secrets
- private vault data
- runtime logs
- generated workflow outputs
- bulky export artifacts unless intentionally packaged

## Rule

If GitHub needs to reason about it, commit a map or contract. If the system needs to execute or store it, keep the artifact on NAS/local storage and reference it.
